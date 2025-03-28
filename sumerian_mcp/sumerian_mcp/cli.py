"""
CLI 모듈 - 명령줄 인터페이스를 통해 Sumerian MCP 서버 실행
"""
import argparse
from .server import SumerianMCPServer
from .crypto import encrypt_password, decrypt_password


def main():
    """수메르 암호화 MCP 서버 또는 직접 암호화/복호화 명령 실행"""
    parser = argparse.ArgumentParser(
        description="수메르 암호화 시스템 (AES-256 + CBC + 수메르어) - MCP 서버 또는 직접 암호화/복호화"
    )
    
    # 서브커맨드 설정
    subparsers = parser.add_subparsers(dest="command", help="명령")
    
    # MCP 서버 실행 명령
    server_parser = subparsers.add_parser("server", help="MCP 서버 실행")
    server_parser.add_argument(
        "--transport", 
        choices=["stdio", "sse"], 
        default="stdio",
        help="MCP 전송 프로토콜 (기본값: stdio)"
    )
    server_parser.add_argument(
        "--host", 
        default="localhost", 
        help="SSE 서버 호스트 (기본값: localhost)"
    )
    server_parser.add_argument(
        "--port", 
        type=int, 
        default=8000, 
        help="SSE 서버 포트 (기본값: 8000)"
    )
    server_parser.add_argument(
        "--name", 
        default="Sumerian Encryption", 
        help="MCP 서버 이름 (기본값: Sumerian Encryption)"
    )
    
    # 직접 암호화 명령
    encrypt_parser = subparsers.add_parser("encrypt", help="직접 암호화 실행")
    encrypt_parser.add_argument("password", help="암호화할 비밀번호")
    encrypt_parser.add_argument("key", help="암호화 키")
    
    # 직접 복호화 명령
    decrypt_parser = subparsers.add_parser("decrypt", help="직접 복호화 실행")
    decrypt_parser.add_argument("encrypted_text", help="암호화된 텍스트")
    decrypt_parser.add_argument("key", help="복호화 키")
    
    # 테스트 명령
    test_parser = subparsers.add_parser("test", help="암호화 및 복호화 테스트")
    test_parser.add_argument("password", help="테스트할 비밀번호")
    test_parser.add_argument("key", help="테스트 키")
    
    args = parser.parse_args()
    
    # 명령에 따라 실행
    if args.command == "server":
        # MCP 서버 실행
        server = SumerianMCPServer(name=args.name)
        
        if args.transport == "stdio":
            print(f"Sumerian MCP 서버를 stdio 모드로 실행합니다...")
            server.run_stdio()
        elif args.transport == "sse":
            print(f"Sumerian MCP 서버를 SSE 모드로 실행합니다 (http://{args.host}:{args.port})...")
            server.run_sse(host=args.host, port=args.port)
    
    elif args.command == "encrypt":
        # 직접 암호화
        encrypted = encrypt_password(args.password, args.key)
        print(f"암호화된 비밀번호: {encrypted}")
    
    elif args.command == "decrypt":
        # 직접 복호화
        decrypted = decrypt_password(args.encrypted_text, args.key)
        if decrypted:
            print(f"복호화된 비밀번호: {decrypted}")
        else:
            print("복호화 실패: 키가 잘못되었거나 암호화된 데이터가 손상되었습니다.")
    
    elif args.command == "test":
        # 테스트 모드
        print("테스트 모드")
        encrypted = encrypt_password(args.password, args.key)
        print(f"암호화된 비밀번호: {encrypted}")
        
        # 테스트 목적으로 바로 복호화 검증
        print("\n암호화 검증:")
        decrypted = decrypt_password(encrypted, args.key)
        if decrypted == args.password:
            print(f"✅ 검증 성공: '{args.password}' → '{decrypted}'")
        else:
            print(f"❌ 검증 실패: '{args.password}' → '{decrypted}'")
    
    else:
        # 명령어가 없을 경우 도움말 표시
        parser.print_help()


if __name__ == "__main__":
    main() 