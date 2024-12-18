"""Tests for the Vellum Prompt Explorer.

Test coverage for:
1. Initialization
2. Prompt listing
3. Display formatting
4. Error handling

v1 - Initial test implementation
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch

from src.prompt_explorer import PromptExplorer, PromptInfo


@pytest.fixture
def mock_vellum_response():
    """Create a mock Vellum API response."""
    return Mock(
        results=[
            Mock(
                id="test-id-1",
                name="test-prompt-1",
                label="Test Prompt 1",
                created=datetime.now(),
                last_deployed_on=datetime.now(),
                status="ACTIVE",
                environment="DEVELOPMENT",
                description="Test description 1"
            ),
            Mock(
                id="test-id-2",
                name="test-prompt-2",
                label="Test Prompt 2",
                created=datetime.now(),
                last_deployed_on=datetime.now(),
                status="ACTIVE",
                environment="PRODUCTION",
                description="Test description 2"
            )
        ]
    )


def test_prompt_explorer_initialization():
    """Test PromptExplorer initialization with API key."""
    with patch.dict('os.environ', {'VELLUM_API_KEY': 'test-key'}):
        with patch('vellum.client.Client'):
            explorer = PromptExplorer()
            assert explorer.client is not None


def test_prompt_explorer_initialization_no_key():
    """Test PromptExplorer initialization without API key."""
    with patch.dict('os.environ', clear=True):
        with pytest.raises(ValueError):
            PromptExplorer()


def test_list_prompts(mock_vellum_response):
    """Test listing prompts."""
    with patch.dict('os.environ', {'VELLUM_API_KEY': 'test-key'}):
        with patch('vellum.client.Client') as mock_client:
            mock_client.return_value.deployments.list.return_value = mock_vellum_response

            explorer = PromptExplorer()
            prompts = explorer.list_prompts()

            assert len(prompts) == 2
            assert isinstance(prompts[0], PromptInfo)
            assert prompts[0].name == "test-prompt-1"
            assert prompts[1].name == "test-prompt-2"


def test_list_prompts_error():
    """Test error handling in list_prompts."""
    with patch.dict('os.environ', {'VELLUM_API_KEY': 'test-key'}):
        with patch('vellum.client.Client') as mock_client:
            mock_client.return_value.deployments.list.side_effect = Exception("API Error")

            explorer = PromptExplorer()
            prompts = explorer.list_prompts()

            assert len(prompts) == 0
