import pytest
from fastapi import Request, BackgroundTasks
from unittest.mock import Mock, patch, AsyncMock
import httpx

from main import incoming_request
from utils.lib import process_analysis

# Mock data for testing
SAMPLE_SETTINGS = [
  {"label": "agent", "default": "test_agent"},
  {"label": "api_key", "default": "test_key"},
  {"label": "channel_id", "default": "test_channel"}
]

SAMPLE_REQUEST = {
  "message": "test",
  "settings": [
    {
      "label": "setting_label",
      "type": "text",
      "default": "setting_value",
      "required": True
    }
  ]
}
@pytest.fixture
def mock_background_tasks():
  return Mock(spec=BackgroundTasks)

@pytest.fixture
async def mock_request():
  mock = AsyncMock(spec=Request)
  mock.json.return_value = SAMPLE_REQUEST
  return mock

@pytest.mark.asyncio
async def test_incoming_request_valid_command():
    # Arrange
  mock_request = AsyncMock(spec=Request)
  mock_request.json.return_value = {
      "message": "/levels test command",
      "settings": SAMPLE_SETTINGS
  }
  background_tasks = Mock(spec=BackgroundTasks)
  
  # Act
  with patch('utils.lib.is_valid_command', return_value=True):
    response = await incoming_request(mock_request, background_tasks)
  
  # Assert
  assert response["event_name"] == "Levels_processing"
  # assert "test command" in response["message"]
  assert response["status"] == "success"
  assert response["username"] == "Levels"
  background_tasks.add_task.assert_called_once()

@pytest.mark.asyncio
async def test_incoming_request_invalid_command():
    # Arrange
  mock_request = AsyncMock(spec=Request)
  mock_request.json.return_value = {
    "message": "invalid command",
    "settings": SAMPLE_SETTINGS
  }
  background_tasks = Mock(spec=BackgroundTasks)
  
  # Act
  with patch('utils.lib.is_valid_command', return_value=False):
      response = await incoming_request(mock_request, background_tasks)
  
  # Assert
  assert response["event_name"] == "Levels_processing"
  assert response["message"] == "invalid command"
  assert not background_tasks.add_task.called

@pytest.mark.asyncio
async def test_incoming_request_with_ratio_command():
    # Arrange
  mock_request = AsyncMock(spec=Request)
  mock_request.json.return_value = {
    "message": "/ratio analyze this",
    "settings": SAMPLE_SETTINGS
  }
  background_tasks = Mock(spec=BackgroundTasks)
  
  # Act
  with patch('utils.lib.is_valid_command', return_value=True):
    response = await incoming_request(mock_request, background_tasks)
  
  # Assert
  assert  response["message"] == "analyze this <strong style=\"color: green\">-- Received (app: Levels-im)</strong>"
  assert "Received (app: Levels-im)" in response["message"]

    # Arrange
  agent = "gemini"
  api_key = "test_key"
  msg = "/levels test"
  channel_id = "test_channel"
  mock_response = "Analysis complete"
  
  # Act
  with patch('utils.lib.run_agent', return_value=mock_response) as mock_run_agent, \
    patch('httpx.Client') as mock_client:
    mock_client.return_value.__enter__.return_value.post.return_value.status_code = 200
    with patch('utils.lib.process_analysis', return_value=f'Task completed. Channel ID: {channel_id}'):
      result = process_analysis(agent, api_key, msg, channel_id)
  
  # Assert
  assert result == f'Task completed. Channel ID: {channel_id}'
  mock_run_agent.assert_called_once()
  called_args = mock_run_agent.call_args[0]
  print(called_args)
  assert called_args[0] == agent
  assert called_args[1] == api_key
  assert called_args[3] == msg
    # Test the settings extraction logic
  settings_list = [
      {"label": "agent", "default": "test_agent"},
      {"label": "api_key", "default": "test_key"},
      {"label": "channel_id", "default": "test_channel"}
  ]
    
  defaults = {"agent": "", "api_key": "", "channel_id": ""}
  values = {
      key: next((item.get("default", default)
          for item in settings_list if item.get("label") == key), default)
      for key, default in defaults.items()
  }
    
  assert values["agent"] == "test_agent"
  assert values["api_key"] == "test_key"
  assert values["channel_id"] == "test_channel"