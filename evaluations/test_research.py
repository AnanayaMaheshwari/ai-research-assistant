def test_research_topic_validation():
    from backend.schemas.research import ResearchRequest
    request = ResearchRequest(topic="Impact of AI on education", mode="sequential")
    assert request.topic.startswith("Impact")
    assert request.mode == "sequential"

def test_invalid_mode_rejected():
    import pytest
    from pydantic import ValidationError
    from backend.schemas.research import ResearchRequest
    with pytest.raises(ValidationError):
        ResearchRequest(topic="Impact of AI on education", mode="invalid")
