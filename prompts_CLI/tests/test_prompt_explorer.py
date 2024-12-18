# """
# Tests for the Vellum Prompt Explorer.

# This module tests:
# 1. Explorer initialization
# 2. Prompt listing functionality
# 3. Error handling
# 4. Environment configuration

# v8 - Fixed Vellum client import and error handling
# """

# import pytest
# from unittest.mock import patch, MagicMock
# from prompts_CLI.src.prompt_explorer import PromptExplorer
# import vellum


# @pytest.fixture
# def mock_vellum_response():
#     """Mock Vellum API response."""
#     return MagicMock(
#         results=[
#             MagicMock(
#                 id="test-id-1",
#                 name="test-prompt-1",
#                 label="Test Prompt 1",
#                 created=MagicMock(),
#                 last_deployed_on=MagicMock(),
#                 status="ACTIVE",
#                 environment="DEVELOPMENT",
#                 description="Test description 1"
#             ),
#             MagicMock(
#                 id="test-id-2",
#                 name="test-prompt-2",
#                 label="Test Prompt 2",
#                 created=MagicMock(),
#                 last_deployed_on=MagicMock(),
#                 status="ARCHIVED",
#                 environment="PRODUCTION",
#                 description="Test description 2"
#             )
#         ]
#     )


# def test_prompt_explorer_initialization():
#     """
#     Test PromptExplorer initialization with API key.

#     1. Mock environment with API key
#     2. Create explorer instance
#     3. Verify initialization
#     v5 - Updated Vellum client import
#     """
#     with patch.dict('os.environ', {'VELLUM_API_KEY': 'test-key'}):
#         with patch('vellum.client.Vellum') as mock_client:
#             explorer = PromptExplorer()
#             assert explorer is not None
#             mock_client.assert_called_once_with(api_key='test-key')


# def test_prompt_explorer_initialization_no_key():
#     """
#     Test PromptExplorer initialization without API key.

#     1. Clear environment variables
#     2. Attempt to create explorer
#     3. Verify error handling
#     v5 - Updated error handling
#     """
#     with patch.dict('os.environ', clear=True):
#         with patch('dotenv.load_dotenv', return_value=None):
#             with pytest.raises(ValueError) as exc:
#                 PromptExplorer()
#             assert "No API key provided" in str(exc.value)


# def test_list_prompts(mock_vellum_response):
#     """
#     Test listing prompts.

#     1. Mock Vellum client response
#     2. List prompts with filters
#     3. Verify response format
#     v5 - Updated client mocking
#     """
#     with patch.dict('os.environ', {'VELLUM_API_KEY': 'test-key'}):
#         with patch('vellum.client.Vellum') as mock_client:
#             # Set up mock response
#             mock_instance = mock_client.return_value
#             mock_instance.deployments.list.return_value = mock_vellum_response

#             # Create explorer and list prompts
#             explorer = PromptExplorer()
#             prompts = explorer.list_prompts(status="ACTIVE")

#             # Verify response
#             assert len(prompts) == 1
#             assert prompts[0].name == "test-prompt-1"
#             assert prompts[0].status == "ACTIVE"

#             # Verify API call
#             mock_instance.deployments.list.assert_called_once()


# def test_list_prompts_error():
#     """
#     Test error handling in list_prompts.

#     1. Mock API error
#     2. Attempt to list prompts
#     3. Verify error handling
#     v5 - Updated error handling
#     """
#     with patch.dict('os.environ', {'VELLUM_API_KEY': 'test-key'}):
#         with patch('vellum.client.Vellum') as mock_client:
#             # Set up mock error
#             mock_instance = mock_client.return_value
#             mock_instance.deployments.list.side_effect = Exception("API error")

#             # Create explorer
#             explorer = PromptExplorer()

#             # Test error handling
#             prompts = explorer.list_prompts()
#             assert len(prompts) == 0
