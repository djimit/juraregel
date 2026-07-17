"""Tests for Gate module — covenant, receipt, engine."""

import os
import tempfile
import pytest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.gate.covenant import Covenant, load_covenant
from shared.gate.receipt import Receipt, ReceiptStore
from shared.gate.engine import Gate


@pytest.fixture
def covenant():
    return Covenant(
        agent="test-agent",
        version="1.0",
        rules=[
            {"permit": "read"},
            {"permit": "calculate"},
            {"require_approval": "calculate", "when": "amount > 100000"},
            {"forbid": "delete_records"},
            {"forbid": "modify_ruleset"},
        ],
    )


@pytest.fixture
def gate(covenant, tmp_path):
    return Gate(covenant=covenant, store_dir=str(tmp_path / "receipts"))


class TestCovenant:
    def test_permit_action(self, covenant):
        result = covenant.evaluate("read")
        assert result["decision"] == "permit"

    def test_forbid_action(self, covenant):
        result = covenant.evaluate("delete_records")
        assert result["decision"] == "forbid"

    def test_require_approval_with_condition(self, covenant):
        result = covenant.evaluate("calculate", {"amount": 150000})
        assert result["decision"] == "require_approval"

    def test_permit_when_condition_not_met(self, covenant):
        result = covenant.evaluate("calculate", {"amount": 50000})
        assert result["decision"] == "permit"

    def test_default_deny(self, covenant):
        result = covenant.evaluate("unknown_action")
        assert result["decision"] == "forbid"

    def test_wildcard_match(self):
        c = Covenant(agent="test", version="1.0", rules=[{"permit": "read_*"}])
        assert c.evaluate("read_file")["decision"] == "permit"
        assert c.evaluate("write_file")["decision"] == "forbid"

    def test_covenant_hash(self, covenant):
        h = covenant.hash
        assert len(h) == 16
        assert covenant.hash == h  # deterministic

    def test_load_from_yaml(self, tmp_path):
        yaml_content = """
agent: yaml-agent
version: "2.0"
rules:
  - permit: read
  - forbid: delete
"""
        yaml_path = tmp_path / "covenant.yaml"
        yaml_path.write_text(yaml_content)
        c = load_covenant(str(yaml_path))
        assert c.agent == "yaml-agent"
        assert c.evaluate("read")["decision"] == "permit"
        assert c.evaluate("delete")["decision"] == "forbid"


class TestReceipt:
    def test_create_receipt(self):
        r = Receipt(
            agent_id="test", action_name="read", decision="permit", authorized=True
        )
        assert r.receipt_id is not None
        assert r.status == "pending"

    def test_serialization(self):
        r = Receipt(
            agent_id="test", action_name="read", decision="permit", authorized=True
        )
        data = r.to_dict()
        r2 = Receipt.from_dict(data)
        assert r2.receipt_id == r.receipt_id
        assert r2.decision == "permit"


class TestReceiptStore:
    def test_save_and_load(self, tmp_path):
        store = ReceiptStore(str(tmp_path / "receipts"))
        r = Receipt(
            agent_id="agent1", action_name="read", decision="permit", authorized=True
        )
        store.save(r)
        loaded = store.load("agent1")
        assert len(loaded) == 1
        assert loaded[0].receipt_id == r.receipt_id

    def test_get_by_id(self, tmp_path):
        store = ReceiptStore(str(tmp_path / "receipts"))
        r = Receipt(
            agent_id="agent1", action_name="read", decision="permit", authorized=True
        )
        store.save(r)
        found = store.get(r.receipt_id)
        assert found is not None
        assert found.agent_id == "agent1"

    def test_chain_verification(self, tmp_path):
        store = ReceiptStore(str(tmp_path / "receipts"))
        r1 = Receipt(
            agent_id="agent1",
            action_name="read",
            decision="permit",
            authorized=True,
            status="sealed",
            seal_sig="sig1",
        )
        r2 = Receipt(
            agent_id="agent1",
            action_name="write",
            decision="permit",
            authorized=True,
            status="sealed",
            seal_sig="sig2",
        )
        store.save(r1)
        store.save(r2)
        result = store.verify_chain("agent1")
        assert result["valid"] is True
        assert result["receipts"] == 2


class TestGate:
    def test_authorize_permitted(self, gate):
        receipt = gate.authorize("test-agent", "read", {"file": "test.txt"})
        assert receipt.authorized is True
        assert receipt.decision == "permit"
        assert len(receipt.authorization_sig) > 0

    def test_authorize_forbidden(self, gate):
        receipt = gate.authorize("test-agent", "delete_records", {})
        assert receipt.authorized is False
        assert receipt.decision == "forbid"

    def test_authorize_requires_approval(self, gate):
        receipt = gate.authorize(
            "test-agent", "calculate", {"amount": 150000}, {"amount": 150000}
        )
        assert receipt.decision == "require_approval"

    def test_seal_receipt(self, gate):
        receipt = gate.authorize("test-agent", "read", {"file": "test.txt"})
        sealed = gate.seal(receipt, {"result": "success"}, "success")
        assert sealed.status == "sealed"
        assert len(sealed.seal_sig) > 0
        assert sealed.result_hash is not None

    def test_verify_valid_receipt(self, gate):
        receipt = gate.authorize("test-agent", "read", {"file": "test.txt"})
        sealed = gate.seal(receipt, {"result": "success"}, "success")
        result = gate.verify(sealed)
        assert result["overall"] is True

    def test_delegation_chain(self, gate):
        parent = gate.authorize("test-agent", "orchestrate", {})
        child = gate.authorize(
            "test-agent", "step_1", {}, parent_receipt_id=parent.receipt_id
        )
        chain = gate.walk_delegation_chain(child.receipt_id)
        assert len(chain) == 2
        assert chain[0].receipt_id == parent.receipt_id
        assert chain[1].receipt_id == child.receipt_id
