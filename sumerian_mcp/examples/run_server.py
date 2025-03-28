"""
수메르 암호화 MCP 서버 실행 예제

MCP 서버를 프로그래밍 방식으로 실행하는 방법을 보여줍니다.
"""
from sumerian_mcp import SumerianMCPServer
import argparse


def main():
    """수메르 암호화 MCP 서버 실행 예제 스크립트"""
    parser = argparse.ArgumentParser(description="수메르 암호화 MCP 서버 실행 예제")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="MCP 전송 프로토콜 (기본값: stdio)",
    )
    parser.add_argument(
        "--host", default="localhost", help="SSE 서버 호스트 (기본값: localhost)"
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="SSE 서버 포트 (기본값: 8000)"
    )
    parser.add_argument(
        "--name", default="Sumerian Encryption", help="MCP 서버 이름 (기본값: Sumerian Encryption)"
    )
    args = parser.parse_args()

    # MCP 서버 생성
    server = SumerianMCPServer(name=args.name)
    
    print(f"🔐 수메르 암호화 MCP 서버를 시작합니다...")
    print(f"서버 이름: {args.name}")
    
    # 전송 방식에 따른 서버 실행
    if args.transport == "stdio":
        print(f"📝 stdio 모드로 실행합니다...")
        print(f"수메르 암호화 MCP 서버가 준비되었습니다. Claude나 다른 MCP 클라이언트에 연결할 수 있습니다.")
        server.run_stdio()
    else:
        print(f"🌐 SSE 모드로 실행합니다 (http://{args.host}:{args.port})...")
        server.run_sse(host=args.host, port=args.port)


if __name__ == "__main__":
    main() 