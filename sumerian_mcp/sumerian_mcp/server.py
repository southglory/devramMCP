"""
Sumerian MCP 서버 구현
MCP 프로토콜을 통해 수메르 암호화 기능을 제공하는 서버
"""
from mcp.server.fastmcp import FastMCP
from mcp.types import CallToolResult, TextContent
from .crypto import encrypt_password, decrypt_password


class SumerianMCPServer:
    """
    수메르 암호화 MCP 서버
    
    AES-256 CBC 암호화와 수메르어 변환을 결합한 암호화 기능을 MCP 도구로 제공
    """
    
    def __init__(self, name="Sumerian Encryption"):
        """
        MCP 서버 초기화
        
        Args:
            name: 서버 이름
        """
        self.mcp = FastMCP(name)
        self._register_tools()
        
    def _register_tools(self):
        """MCP 서버에 도구 등록"""
        
        # 암호화 도구
        @self.mcp.tool()
        def encrypt(password: str, key: str) -> str:
            """
            AES-256 CBC로 암호화 후 수메르어로 변환
            
            Args:
                password: 암호화할 비밀번호
                key: 암호화 키
                
            Returns:
                암호화 및 수메르어로 변환된 문자열
            """
            try:
                result = encrypt_password(password, key)
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text=result
                        )
                    ]
                )
            except Exception as e:
                return CallToolResult(
                    isError=True,
                    content=[
                        TextContent(
                            type="text",
                            text=f"암호화 오류: {str(e)}"
                        )
                    ]
                )
        
        # 복호화 도구
        @self.mcp.tool()
        def decrypt(encrypted_text: str, key: str) -> str:
            """
            수메르어 복호화 후 AES-256 CBC 복호화
            
            Args:
                encrypted_text: 암호화된 수메르어 텍스트
                key: 복호화 키
                
            Returns:
                복호화된 원본 텍스트
            """
            try:
                result = decrypt_password(encrypted_text, key)
                if result is None:
                    return CallToolResult(
                        isError=True,
                        content=[
                            TextContent(
                                type="text",
                                text="복호화 실패: 키가 잘못되었거나 암호화된 데이터가 손상되었습니다."
                            )
                        ]
                    )
                return CallToolResult(
                    content=[
                        TextContent(
                            type="text",
                            text=result
                        )
                    ]
                )
            except Exception as e:
                return CallToolResult(
                    isError=True,
                    content=[
                        TextContent(
                            type="text",
                            text=f"복호화 오류: {str(e)}"
                        )
                    ]
                )
    
    def run_stdio(self):
        """표준 입출력을 통해 MCP 서버 실행"""
        self.mcp.run_stdio()
    
    def run_sse(self, host="localhost", port=8000):
        """SSE를 통해 MCP 서버 실행"""
        self.mcp.run_sse(host=host, port=port) 