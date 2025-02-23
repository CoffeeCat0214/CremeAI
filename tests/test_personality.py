import pytest
from ..services.personality_service import PersonalityService

def test_base_prompt():
    service = PersonalityService()
    prompt = service.get_base_prompt()
    
    assert "Crème Brûlée" in prompt
    assert "royal" in prompt.lower()
    assert "ROYAL DECREE:" in prompt

def test_decree_prompt():
    service = PersonalityService()
    prompt = service.get_decree_prompt()
    
    assert "Please issue a Royal Decree" in prompt

def test_response_formatting():
    service = PersonalityService()
    
    # Should add French flair if missing
    response = service.format_response("This is a test")
    assert any(phrase in response.lower() for phrase in [" non?", " oui?"])
    
    # Should not modify if French flair exists
    french_response = "This is magnifique!"
    formatted = service.format_response(french_response)
    assert formatted == french_response 