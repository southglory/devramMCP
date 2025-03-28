# Sumerian MCP

## 수메르어를 활용한 고급 암호화 시스템의 MCP 서버

이 패키지는 강력한 AES-256 CBC 모드 암호화와 고대 수메르 문자 변환을 결합한 독특한 암호화 솔루션을 MCP(Model Context Protocol) 서버로 제공합니다.

### 주요 기능

- **강력한 AES-256 암호화**: 산업 표준 대칭키 암호화 알고리즘을 사용
- **CBC 운영 모드**: 랜덤 초기화 벡터(IV)로 높은 보안성 보장
- **수메르 문자 변환**: 암호화된 텍스트를 고대 수메르 쐐기문자로 변환하여 시각적 보안 레이어 추가
- **이중 보안 레이어**: 암호화 후 인코딩을 통한 추가 보안 강화
- **MCP 프로토콜 지원**: Claude와 같은 MCP 호환 LLM에서 직접 암호화/복호화 기능 사용 가능

### 설치

```bash
pip install sumerian-mcp
```

### MCP 서버 실행

#### stdio 모드 (Claude와 같은 LLM에서 사용)

```bash
sumerian-mcp server
```

#### SSE 모드 (웹 서버로 실행)

```bash
sumerian-mcp server --transport sse --host localhost --port 8000
```

### 직접 암호화/복호화 사용

#### 암호화

```bash
sumerian-mcp encrypt "password" "secretKey123"
```

#### 복호화

```bash
sumerian-mcp decrypt "𒁀VXKD𒄿𒌋𒀹B𒁀BN𒍝TE𒀻𒈬X𒌝K𒍪𒊏F𒇷AJF𒁀HJ𒌝𒌋𒌋𒅈IDB𒌷KVO𒉿I𒈦" "secretKey123"
```

#### 테스트 모드 (암호화 후 즉시 복호화 검증)

```bash
sumerian-mcp test "password" "secretKey123"
```

### Python API 사용 예제

```python
from sumerian_mcp import encrypt_password, decrypt_password

# 암호화
encrypted = encrypt_password("my_password", "my_secret_key")
print(f"암호화된 비밀번호: {encrypted}")

# 복호화
decrypted = decrypt_password(encrypted, "my_secret_key")
print(f"복호화된 비밀번호: {decrypted}")
```

### MCP 서버 프로그래밍 방식으로 실행

```python
from sumerian_mcp import SumerianMCPServer

# MCP 서버 생성
server = SumerianMCPServer(name="My Sumerian Server")

# stdio 모드로 실행
server.run_stdio()

# 또는 SSE 모드로 실행
# server.run_sse(host="localhost", port=8000)
```

### Claude에서 사용 예제

Claude에서 이 MCP 서버를 사용하려면:

1. 터미널에서 서버 실행:

   ```bash
   sumerian-mcp server
   ```

2. Claude 웹사이트에서 "MCP 서버 연결" 버튼을 클릭하고 "로컬 커맨드 라인 서버 추가"를 선택합니다.

3. 서버 이름(예: "Sumerian Encryption")을 입력하고 연결합니다.

4. 이제 Claude에서 다음과 같이 암호화/복호화 도구를 사용할 수 있습니다:
   "비밀번호 'my_secret'를 키 'master_key'로 암호화해줘"

### 기술적 세부사항

- PKCS7 패딩을 통한 블록 크기 최적화
- 랜덤 IV 생성으로 동일 평문의 다른 암호문 생성 (예측 공격 방지)
- Base64 인코딩 중간 처리로 바이너리 데이터 안전 처리
- 최종 출력을 수메르 쐐기문자로 변환하여 시각적 난독화
- MCP 프로토콜을 통한 확장 가능하고 상호운용 가능한 인터페이스

### 라이선스

MIT
