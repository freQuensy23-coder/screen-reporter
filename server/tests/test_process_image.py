import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from models import ImageProcessingResult
from usecase import process_image
from PIL import Image
import io

@pytest.fixture
def mock_image():
    # Create a small test image
    img = Image.new('RGB', (100, 100), color='white')
    return img

@pytest.fixture
def mock_openai_response():
    response = MagicMock()
    response.choices = [
        MagicMock(
            message=MagicMock(
                content="Test OpenAI response"
            )
        )
    ]
    return response

@pytest.mark.asyncio
@patch('usecase.client')
@patch('usecase.read_file_cached')
async def test_process_image_successful(mock_read_file, mock_client, mock_image, mock_openai_response):
    # Setup
    mock_read_file.return_value = "test prompt"
    mock_client.chat.completions.create = AsyncMock(return_value=mock_openai_response)
    
    # Execute
    result = await process_image(mock_image)
    
    # Assert
    assert result == "Test OpenAI response"
    mock_client.chat.completions.create.assert_called_once()
    
    # Verify the call arguments
    call_args = mock_client.chat.completions.create.call_args[1]
    assert call_args['model'] == "gpt-4o"
    assert len(call_args['messages']) == 2
    assert call_args['messages'][0]['role'] == "system"
    assert call_args['messages'][1]['role'] == "user"
    assert call_args['messages'][1]['content'][0]['text'] == "User activity screenshot"

@pytest.mark.asyncio
@patch('usecase.client')
@patch('usecase.read_file_cached')
async def test_process_image_empty_response(mock_read_file, mock_client, mock_image):
    # Setup
    mock_read_file.return_value = "test prompt"
    response = MagicMock()
    response.choices = [MagicMock(message=MagicMock(content=None))]
    mock_client.chat.completions.create = AsyncMock(return_value=response)
    
    # Execute and Assert
    with pytest.raises(ValueError, match="No response from LLM"):
        await process_image(mock_image)

@pytest.mark.asyncio
@patch('usecase.client')
@patch('usecase.read_file_cached')
async def test_process_image_api_error(mock_read_file, mock_client, mock_image):
    # Setup
    mock_read_file.return_value = "test prompt"
    mock_client.chat.completions.create = AsyncMock(side_effect=Exception("API Error"))
    
    # Execute and Assert
    with pytest.raises(Exception, match="API Error"):
        await process_image(mock_image)

