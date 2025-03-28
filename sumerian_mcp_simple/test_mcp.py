#!/usr/bin/env python3
"""
Tests for Sumerian MCP
"""
import os
import pytest
import json
from unittest.mock import patch, mock_open
import asyncio

# Make sure we're using a test key
os.environ["MASTER_KEY"] = "TEST_KEY"

from sumerian_mcp import decrypt_password, encrypt_password, MCP

@pytest.fixture
def mcp():
    return MCP()

@pytest.mark.asyncio
async def test_encrypt_decrypt_text():
    """Test that encrypted text can be properly decrypted"""
    original_text = "Hello, World!"
    key = "test_key"
    
    # Encrypt the text
    encrypted = encrypt_password(original_text, key)
    
    # Make sure we got something different
    assert encrypted != original_text
    
    # Decrypt the text
    decrypted = decrypt_password(encrypted, key)
    
    # Check if decryption worked
    assert decrypted == original_text

@pytest.mark.asyncio
async def test_encrypt_tool(mcp):
    """Test the encrypt tool"""
    params = {
        "text": "Secret message",
        "key": "test_key"
    }
    
    result = await mcp.call_tool("encrypt", params)
    
    assert "original" in result
    assert "encrypted" in result
    assert "timestamp" in result
    assert result["original"] == "Secret message"
    
    # Verify the decryption works
    decrypted = decrypt_password(result["encrypted"], "test_key")
    assert decrypted == "Secret message"

@pytest.mark.asyncio
async def test_decrypt_tool(mcp):
    """Test the decrypt tool"""
    # First encrypt something
    original = "Another secret"
    encrypted = encrypt_password(original, "test_key")
    
    params = {
        "text": encrypted,
        "key": "test_key"
    }
    
    result = await mcp.call_tool("decrypt", params)
    
    assert "encrypted" in result
    assert "decrypted" in result
    assert "timestamp" in result
    assert result["decrypted"] == original

@pytest.mark.asyncio
async def test_list_tools(mcp):
    """Test listing tools"""
    result = await mcp.call_tool("list_tools")
    
    assert "tools" in result
    assert "count" in result
    assert result["count"] > 0
    
    # Check that we have our basic tools
    tool_ids = [tool["id"] for tool in result["tools"]]
    assert "encrypt" in tool_ids
    assert "decrypt" in tool_ids
    assert "list_tools" in tool_ids

@pytest.mark.asyncio
async def test_encrypt_file(mcp):
    """Test file encryption"""
    test_content = "This is test file content"
    
    # Mock the file operations
    with patch("builtins.open", mock_open(read_data=test_content)) as m:
        params = {
            "filepath": "test.txt",
            "key": "test_key"
        }
        
        result = await mcp.call_tool("encrypt_file", params)
        
        # Check the result
        assert result["status"] == "success"
        assert result["source_file"] == "test.txt"
        assert result["output_file"] == "test.txt.sumerian"
        
        # Check that file was written with encrypted content
        # Get the write calls
        write_calls = [call.args[0] for call in m().write.call_args_list]
        assert len(write_calls) == 1
        
        # The written content should be the encrypted version
        written_content = write_calls[0]
        decrypted = decrypt_password(written_content, "test_key")
        assert decrypted == test_content

@pytest.mark.asyncio
async def test_decrypt_file(mcp):
    """Test file decryption"""
    test_content = "Original test content"
    encrypted_content = encrypt_password(test_content, "test_key")
    
    # Mock the file operations
    with patch("builtins.open", mock_open(read_data=encrypted_content)) as m:
        params = {
            "filepath": "test.txt.sumerian",
            "key": "test_key"
        }
        
        result = await mcp.call_tool("decrypt_file", params)
        
        # Check the result
        assert result["status"] == "success"
        assert result["source_file"] == "test.txt.sumerian"
        assert result["output_file"] == "test.txt"
        
        # Check that file was written with decrypted content
        write_calls = [call.args[0] for call in m().write.call_args_list]
        assert len(write_calls) == 1
        assert write_calls[0] == test_content

if __name__ == "__main__":
    asyncio.run(pytest.main(["-xvs", __file__])) 