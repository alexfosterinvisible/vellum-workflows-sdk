# """
# Tests for OpenAI helper functionality.

# This module tests:
# 1. Initialization with and without API key
# 2. Documentation querying
# 3. Error handling
# 4. Parallel processing

# v8 - Fixed mocking and import paths
# """

# import pytest
# from unittest.mock import patch, MagicMock
# from prompts_CLI.src.openai_helper import OpenAIHelper, DocQuery
# import glob


# @pytest.fixture
# def mock_openai_client():
#     """Mock OpenAI client for testing."""
#     with patch('openai.OpenAI') as mock:
#         # Mock successful API response
#         mock_response = MagicMock()
#         mock_response.choices = [
#             MagicMock(
#                 message=MagicMock(
#                     content='{"answer": "Test answer", "quotes": [], "confidence": {"answer_quality": "high", "source_quality": "high", "completeness": "high", "code_examples": "none"}}'
#                 )
#             )
#         ]
#         mock.return_value.chat.completions.create.return_value = mock_response
#         yield mock


# @pytest.fixture
# def mock_file_system():
#     """Mock file system operations."""
#     with patch('prompts_CLI.src.openai_helper.find_md_files') as mock_find:
#         mock_find.return_value = ['test1.md', 'test2.md']
#         with patch('builtins.open', create=True) as mock_open:
#             mock_open.return_value.__enter__.return_value.read.return_value = "Test content"
#             yield mock_find


# def test_init_no_api_key():
#     """
#     Test initialization without API key.

#     1. Attempt creation without key
#     2. Verify error handling
#     v6 - Updated error message and environment handling
#     """
#     with patch.dict('os.environ', clear=True):
#         with patch('dotenv.load_dotenv', return_value=None):
#             with pytest.raises(ValueError) as exc:
#                 OpenAIHelper(testing=True)
#             assert "No API key provided" in str(exc.value)


# def test_init_with_api_key(mock_openai_client):
#     """
#     Test initialization with API key.

#     1. Create helper with test key
#     2. Verify client initialization
#     v6 - Updated for new client initialization
#     """
#     helper = OpenAIHelper(api_key="test_key", testing=True)
#     assert helper is not None
#     mock_openai_client.assert_called_once_with(api_key="test_key")


# def test_query_docs_parallel(mock_openai_client, mock_file_system):
#     """
#     Test parallel documentation querying.

#     1. Create test query
#     2. Verify response format
#     3. Check API call parameters
#     v4 - Updated mocking for file system
#     """
#     helper = OpenAIHelper(api_key="test_key", testing=True)

#     # Test query
#     result = helper.query_docs_parallel("How do I list prompts?")

#     # Verify response structure
#     assert isinstance(result, dict)
#     assert "answer" in result
#     assert "quotes" in result
#     assert "confidence" in result

#     # Verify API calls
#     mock_client = mock_openai_client.return_value
#     assert mock_client.chat.completions.create.called


# def test_query_docs_error(mock_openai_client, mock_file_system):
#     """
#     Test error handling in parallel querying.

#     1. Mock API error
#     2. Verify error handling
#     3. Check error response format
#     v4 - Updated error handling for parallel queries
#     """
#     helper = OpenAIHelper(api_key="test_key", testing=True)

#     # Make the query fail with a specific error
#     mock_client = mock_openai_client.return_value
#     mock_client.chat.completions.create.side_effect = Exception("API error")

#     # Test error handling
#     result = helper.query_docs_parallel("Test query")

#     # Verify error response format
#     assert isinstance(result, dict)
#     assert "answer" in result
#     assert "Error occurred" in result["answer"]
#     assert result["confidence"]["answer_quality"] == "low"
