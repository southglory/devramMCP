#!/usr/bin/env python3
"""
Sumerian MCP - Simple Master Control Program
A single script that handles encryption/decryption and provides a simple interface.
"""
from Crypto.Cipher import AES
import base64
import os
import json
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import argparse

# ----- Encryption/Decryption Functions -----

def pad(s):
    """AES 블록 크기(16바이트)에 맞게 패딩 추가"""
    return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

def unpad(s):
    """AES 패딩 제거"""
    return s[: -ord(s[-1])]

def encrypt_aes(password, key):
    """AES-256 CBC 암호화"""
    key = key.ljust(32)[:32].encode()
    iv = os.urandom(16)  # 랜덤 IV 생성 (CBC 모드)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(password).encode())  # PKCS7 패딩 적용
    return base64.b64encode(iv + encrypted).decode()  # Base64 변환

def decrypt_aes(encrypted_password, key):
    """AES-256 CBC 복호화"""
    key = key.ljust(32)[:32].encode()

    try:
        encrypted_password = base64.b64decode(encrypted_password)
    except Exception as e:
        print(f"[ERROR] Base64 디코딩 실패: {e}")
        return None

    iv = encrypted_password[:16]  # CBC 모드에서 IV 추출
    encrypted_text = encrypted_password[16:]  # 실제 암호문

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_bytes = cipher.decrypt(encrypted_text)  # AES 복호화

    try:
        decrypted_text = unpad(decrypted_bytes.decode())  # UTF-8 디코딩 및 패딩 제거
    except UnicodeDecodeError as e:
        print(f"[ERROR] 복호화된 데이터 UTF-8 디코딩 실패: {e}")
        return None

    return decrypted_text

# 수메르어 변환 매핑 (알파벳 + 숫자 + 특수문자 → 수메르어)
sumerian_cipher_map = {
    # 알파벳 소문자
    "a": "𒀀", "b": "𒁀", "c": "𒍝", "d": "𒁕", "e": "𒂊",
    "f": "𒆠", "g": "𒂅", "h": "𒄭", "i": "𒄿", "j": "𒋡",
    "k": "𒆪", "l": "𒇷", "m": "𒈬", "n": "𒉈", "o": "𒌷",
    "p": "𒉿", "q": "𒍪", "r": "𒊏", "s": "𒊭", "t": "𒋾",
    "u": "𒌋", "v": "𒅈", "w": "𒂗", "x": "𒐊", "y": "𒅆",
    "z": "𒍣",
    # 숫자
    "0": "𒀹", "1": "𒁹", "2": "𒀻", "3": "𒀼", "4": "𒌝",
    "5": "𒉽", "6": "𒐖", "7": "𒐗", "8": "𒐘", "9": "𒐙",
    # Base64 특수문자
    "+": "𒃻", "/": "𒁺", "=": "𒈦",
    # 공백 및 추가 특수문자
    " ": "𒌃", ".": "𒁇", ",": "𒄑", "!": "𒄠", "?": "𒅎",
    "@": "𒀭", "#": "𒂔", "$": "𒌨", "%": "𒊬", "^": "𒅖",
    "&": "𒀝", "*": "𒀯", "(": "𒐏", ")": "𒐐", "-": "𒁲",
    "_": "𒀞", "[": "𒌍", "]": "𒌌", "{": "𒍢", "}": "𒍤",
    "|": "𒌒", "\\": "𒍦", ":": "𒌓", ";": "𒌇", '"': "𒋰",
    "'": "𒋫", "<": "𒉺", ">": "𒊒", "`": "𒋛", "~": "𒀊",
}

def encrypt_sumerian(text):
    """ASCII 텍스트를 수메르 문자로 변환"""
    return "".join(sumerian_cipher_map.get(char.lower(), char) if char.lower() in sumerian_cipher_map else char for char in text)

def decrypt_sumerian(text):
    """수메르 문자에서 원래 ASCII로 복원"""
    reverse_map = {v: k for k, v in sumerian_cipher_map.items()}
    return "".join(reverse_map.get(char, char) for char in text)

def encrypt_password(password, key):
    """AES-256 + CBC로 암호화 후 수메르어 변환"""
    encrypted_aes = encrypt_aes(password, key)
    return encrypt_sumerian(encrypted_aes)

def decrypt_password(encrypted_password, key):
    """수메르어 복호화 후 AES-256 + CBC 복호화"""
    decrypted_sumerian = decrypt_sumerian(encrypted_password)
    return decrypt_aes(decrypted_sumerian, key)

# ----- MCP Interface -----

# Tools available in the MCP
class Tool:
    def __init__(self, id, name, description, handler):
        self.id = id
        self.name = name
        self.description = description
        self.handler = handler

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

class MCP:
    def __init__(self):
        self.tools = {}
        self.master_key = os.environ.get("MASTER_KEY", "sumerian_default_key")
        self.initialize_tools()
        
    def initialize_tools(self):
        # Register encryption tools
        self.register_tool(
            "encrypt", 
            "Encrypt Text", 
            "Encrypt text using AES-256 + CBC and convert to Sumerian cuneiform", 
            self.handle_encrypt
        )
        
        self.register_tool(
            "decrypt", 
            "Decrypt Text", 
            "Decrypt Sumerian cuneiform text back to original", 
            self.handle_decrypt
        )
        
        self.register_tool(
            "list_tools", 
            "List Available Tools", 
            "List all tools available in the MCP", 
            self.handle_list_tools
        )
        
        self.register_tool(
            "encrypt_file", 
            "Encrypt File", 
            "Encrypt file contents using AES-256 + CBC and convert to Sumerian cuneiform", 
            self.handle_encrypt_file
        )
        
        self.register_tool(
            "decrypt_file", 
            "Decrypt File", 
            "Decrypt Sumerian cuneiform file contents back to original", 
            self.handle_decrypt_file
        )
    
    def register_tool(self, id, name, description, handler):
        """Register a new tool in the MCP"""
        self.tools[id] = Tool(id, name, description, handler)
    
    async def call_tool(self, tool_id: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Call a tool with the given parameters"""
        if params is None:
            params = {}
        
        if tool_id not in self.tools:
            return {"error": f"Tool not found: {tool_id}"}
        
        try:
            result = await self.tools[tool_id].handler(params)
            return result
        except Exception as e:
            return {"error": str(e)}
    
    async def handle_encrypt(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle encrypt command"""
        text = params.get("text", "")
        key = params.get("key", self.master_key)
        
        if not text:
            return {"error": "Missing text parameter"}
        
        encrypted = encrypt_password(text, key)
        return {
            "original": text,
            "encrypted": encrypted,
            "timestamp": datetime.now().isoformat()
        }
    
    async def handle_decrypt(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle decrypt command"""
        text = params.get("text", "")
        key = params.get("key", self.master_key)
        
        if not text:
            return {"error": "Missing text parameter"}
        
        decrypted = decrypt_password(text, key)
        if decrypted is None:
            return {"error": "Decryption failed"}
        
        return {
            "encrypted": text,
            "decrypted": decrypted,
            "timestamp": datetime.now().isoformat()
        }
    
    async def handle_list_tools(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle list_tools command"""
        return {
            "tools": [tool.to_dict() for tool in self.tools.values()],
            "count": len(self.tools)
        }
    
    async def handle_encrypt_file(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle encrypt_file command"""
        filepath = params.get("filepath", "")
        key = params.get("key", self.master_key)
        output_filepath = params.get("output", filepath + ".sumerian")
        
        if not filepath:
            return {"error": "Missing filepath parameter"}
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            encrypted = encrypt_password(content, key)
            
            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write(encrypted)
            
            return {
                "source_file": filepath,
                "output_file": output_filepath,
                "status": "success",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}
    
    async def handle_decrypt_file(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle decrypt_file command"""
        filepath = params.get("filepath", "")
        key = params.get("key", self.master_key)
        output_filepath = params.get("output", "")
        
        if not filepath:
            return {"error": "Missing filepath parameter"}
        
        if not output_filepath:
            if filepath.endswith(".sumerian"):
                output_filepath = filepath[:-9]  # Remove .sumerian extension
            else:
                output_filepath = filepath + ".decrypted"
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            decrypted = decrypt_password(content, key)
            if decrypted is None:
                return {"error": "Decryption failed"}
            
            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write(decrypted)
            
            return {
                "source_file": filepath,
                "output_file": output_filepath,
                "status": "success",
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {"error": str(e)}

# ----- Command Line Interface -----

async def main():
    parser = argparse.ArgumentParser(description="Sumerian MCP - Master Control Program")
    parser.add_argument("tool", nargs="?", help="Tool to execute")
    parser.add_argument("--text", help="Text to process")
    parser.add_argument("--key", help="Encryption/decryption key")
    parser.add_argument("--file", help="File to process")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")
    parser.add_argument("--server", action="store_true", help="Run as a server")
    args = parser.parse_args()
    
    mcp = MCP()
    
    if args.server:
        # Start as a server
        import uvicorn
        from fastapi import FastAPI, Body
        
        app = FastAPI(title="Sumerian MCP")
        
        @app.post("/tools/{tool_id}")
        async def tool_endpoint(tool_id: str, params: Dict[str, Any] = Body(...)):
            return await mcp.call_tool(tool_id, params)
        
        @app.get("/tools")
        async def list_tools_endpoint():
            return await mcp.call_tool("list_tools")
        
        print("Starting Sumerian MCP server on http://localhost:8000")
        uvicorn.run(app, host="0.0.0.0", port=8000)
        return
    
    if args.interactive:
        print("Sumerian MCP Interactive Mode")
        print("Type 'exit' to quit, 'help' for available commands")
        
        while True:
            command = input("\nmcp> ").strip()
            
            if command.lower() in ["exit", "quit"]:
                break
            
            if command.lower() == "help":
                tools_result = await mcp.call_tool("list_tools")
                print("\nAvailable commands:")
                for tool in tools_result["tools"]:
                    print(f"  {tool['id']:<12} - {tool['description']}")
                continue
            
            parts = command.split()
            if not parts:
                continue
            
            tool_id = parts[0]
            params = {}
            
            # Parse key=value pairs
            for part in parts[1:]:
                if "=" in part:
                    key, value = part.split("=", 1)
                    params[key] = value
            
            result = await mcp.call_tool(tool_id, params)
            print(json.dumps(result, indent=2))
        
        print("Goodbye!")
        return
    
    # Command line mode
    if not args.tool:
        parser.print_help()
        return
    
    params = {}
    
    if args.text:
        params["text"] = args.text
    
    if args.key:
        params["key"] = args.key
    
    if args.file:
        params["filepath"] = args.file
    
    if args.output:
        params["output"] = args.output
    
    result = await mcp.call_tool(args.tool, params)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(main()) 