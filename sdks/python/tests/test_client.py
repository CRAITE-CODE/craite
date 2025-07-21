"""Tests for CRAITE Python SDK"""

import pytest
from craite import create_client, CRAITEClient


def test_create_client():
    """Test client creation"""
    client = create_client("test-api-key")
    assert isinstance(client, CRAITEClient)
    assert client.api_key == "test-api-key"


def test_client_with_custom_provider():
    """Test client with custom provider"""
    client = create_client(
        api_key="test-key",
        provider="anthropic"
    )
    assert client.provider == "anthropic"


@pytest.mark.asyncio
async def test_generate_mock():
    """Test generate with mock response"""
    client = create_client("test-key")
    # Add mock test implementation
    pass
