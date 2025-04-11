import os
import pytest
from unittest.mock import Mock, patch
from main import GroqChat

@pytest.fixture
def mock_env():
    """Fixture to provide test environment variables."""
    with patch.dict(os.environ, {'GROQ_API_KEY': 'test-api-key'}):
        yield

@pytest.fixture
def mock_completion():
    """Fixture for mock completion response."""
    mock = Mock()
    mock.choices = [Mock(message=Mock(content="Test response"))]
    return mock

@pytest.fixture
def groq_chat(mock_env):
    """Fixture to provide GroqChat instance."""
    return GroqChat()

def test_init_without_api_key():
    """Test initialization without API key."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError):
            GroqChat()

def test_init_with_custom_model(mock_env):
    """Test initialization with custom model."""
    custom_model = "custom-model-name"
    chat = GroqChat(model_id=custom_model)
    assert chat.model_id == custom_model

def test_init_with_default_model(mock_env):
    """Test initialization with default model."""
    chat = GroqChat()
    assert chat.model_id == GroqChat.DEFAULT_MODEL

@pytest.mark.asyncio
async def test_generate_content(groq_chat, mock_completion):
    """Test content generation."""
    with patch.object(groq_chat.client.chat.completions, 'create', 
                     return_value=mock_completion):
        response = await groq_chat.generate_content("Test prompt")
        assert response == "Test response"

@pytest.mark.asyncio
async def test_generate_content_with_context(groq_chat, mock_completion):
    """Test content generation with context."""
    context = [
        {"user_input": "Previous question", "ai_response": "Previous answer"}
    ]
    
    with patch.object(groq_chat.client.chat.completions, 'create', 
                     return_value=mock_completion):
        response = await groq_chat.generate_content("Test prompt", context)
        assert response == "Test response"