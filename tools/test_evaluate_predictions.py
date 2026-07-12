from tools.evaluate_predictions import evaluate


def test_evaluation_counts_false_negatives_and_abstention():
    result = evaluate([
        {"expected": ["bsn"], "predicted": ["bsn"]},
        {"expected": ["email"], "predicted": []},
        {"expected": ["phone"], "predicted": None},
    ])
    assert result["micro"]["precision"] == 1.0
    assert result["micro"]["recall"] == 1 / 3
    assert result["abstained"] == 1
