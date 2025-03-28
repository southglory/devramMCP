"""
수메르 암호화 API 사용 예제

수메르 암호화 API를 직접 사용하는 방법을 보여줍니다.
"""
from sumerian_mcp import encrypt_password, decrypt_password


def main():
    """수메르 암호화 API 사용 예제 스크립트"""
    
    # 사용자 입력 받기
    print("📋 수메르 암호화 API 사용 예제")
    print("=" * 40)
    
    password = input("암호화할 텍스트 입력: ")
    key = input("암호화 키 입력: ")
    
    print("\n🔒 암호화 중...")
    encrypted = encrypt_password(password, key)
    print(f"암호화된 결과: {encrypted}")
    
    print("\n🔑 복호화 중...")
    decrypted = decrypt_password(encrypted, key)
    
    print("\n📊 결과 검증:")
    print("-" * 40)
    print(f"원본 텍스트: {password}")
    print(f"복호화된 텍스트: {decrypted}")
    
    if password == decrypted:
        print("\n✅ 검증 성공! 원본과 복호화된 텍스트가 일치합니다.")
    else:
        print("\n❌ 검증 실패! 원본과 복호화된 텍스트가 일치하지 않습니다.")
    
    # 잘못된 키로 복호화 시도
    print("\n⚠️ 잘못된 키로 복호화 시도:")
    wrong_key = key + "_wrong"
    wrong_decrypted = decrypt_password(encrypted, wrong_key)
    
    if wrong_decrypted is None:
        print("✅ 예상대로 복호화에 실패했습니다 (잘못된 키).")
    else:
        print(f"⚠️ 잘못된 키로 복호화: {wrong_decrypted}")


if __name__ == "__main__":
    main() 