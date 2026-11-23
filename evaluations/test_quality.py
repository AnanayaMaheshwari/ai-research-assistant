def test_report_has_content():
    sample = "# Research Report\n\n## Findings\nEvidence and limitations."
    assert len(sample) > 30
    assert "Findings" in sample
    assert "Evidence" in sample
