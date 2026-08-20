import os
import subprocess
import sys


def api_paths(environment: str, profile: str | None = None) -> subprocess.CompletedProcess:
    env = {**os.environ, "JURAREGEL_ENV": environment}
    if profile is None:
        env.pop("JURAREGEL_API_PROFILE", None)
    else:
        env["JURAREGEL_API_PROFILE"] = profile
    return subprocess.run(
        [
            sys.executable,
            "-c",
            "from api.main import app; print(chr(10).join(app.openapi()['paths']))",
        ],
        capture_output=True,
        cwd=os.getcwd(),
        env=env,
        text=True,
    )


def test_production_defaults_to_core_routes():
    result = api_paths("production")

    assert result.returncode == 0, result.stderr
    assert "/health" in result.stdout
    assert "/api/v1/templates/" in result.stdout
    assert "/api/v1/assessments/" not in result.stdout
    assert "/api/v1/predictive/analyze" not in result.stdout
    assert "/api/v1/digital-twin/create" not in result.stdout


def test_development_defaults_to_prototype_routes():
    result = api_paths("development")

    assert result.returncode == 0, result.stderr
    assert "/api/v1/assessments/" in result.stdout
    assert "/api/v1/predictive/analyze" in result.stdout


def test_production_rejects_prototype_profile():
    result = api_paths("production", "prototype")

    assert result.returncode != 0
    assert "production JURAREGEL_API_PROFILE must be 'core'" in result.stderr
