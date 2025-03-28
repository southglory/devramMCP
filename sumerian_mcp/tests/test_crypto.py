"""
수메르 암호화 모듈 테스트
"""
import unittest
from sumerian_mcp.crypto import (
    encrypt_password,
    decrypt_password,
    encrypt_sumerian,
    decrypt_sumerian,
    encrypt_aes,
    decrypt_aes,
)


class TestCrypto(unittest.TestCase):
    """수메르 암호화 모듈 테스트 케이스"""

    def test_aes_encryption_decryption(self):
        """AES 암호화 및 복호화 테스트"""
        password = "test123"
        key = "secret_key"
        
        # 암호화
        encrypted = encrypt_aes(password, key)
        
        # 복호화
        decrypted = decrypt_aes(encrypted, key)
        
        # 검증
        self.assertEqual(password, decrypted)
    
    def test_sumerian_transformation(self):
        """수메르어 변환 테스트"""
        text = "Hello World!"
        
        # 수메르어 변환
        sumerian = encrypt_sumerian(text)
        
        # 원래 텍스트로 복원
        original = decrypt_sumerian(sumerian)
        
        # 검증
        self.assertEqual(text, original)
    
    def test_full_encryption_decryption(self):
        """전체 암호화 및 복호화 프로세스 테스트"""
        password = "MySecretPassword123!@#"
        key = "master_key_123"
        
        # 암호화
        encrypted = encrypt_password(password, key)
        
        # 복호화
        decrypted = decrypt_password(encrypted, key)
        
        # 검증
        self.assertEqual(password, decrypted)
    
    def test_wrong_key_decryption(self):
        """잘못된 키로 복호화 시도 테스트"""
        password = "SecurePassword"
        correct_key = "correct_key"
        wrong_key = "wrong_key"
        
        # 암호화
        encrypted = encrypt_password(password, correct_key)
        
        # 잘못된 키로 복호화
        decrypted = decrypt_password(encrypted, wrong_key)
        
        # 검증 (잘못된 키로 복호화 시 None 반환)
        self.assertIsNone(decrypted)


if __name__ == "__main__":
    unittest.main() 