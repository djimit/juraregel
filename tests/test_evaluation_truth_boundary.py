from api.continuous_evaluation import continuous_evaluation


def test_local_evaluation_fails_closed_without_observed_evidence():
    report = continuous_evaluation.evaluate_all()

    assert report.overall_score == 0
    assert report.overall_grade == "F"
    assert all(not result.passed for result in report.results)
    assert all(
        "Geen onafhankelijk runtimebewijs" in finding
        for result in report.results
        for finding in result.findings
    )
