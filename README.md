# devramMCP

## 수메르어를 활용한 고급 암호화 시스템

이 프로젝트는 강력한 AES-256 CBC 모드 암호화와 고대 수메르 문자 변환을 결합한 독특한 암호화 솔루션을 제공합니다.

### 주요 기능

- **강력한 AES-256 암호화**: 산업 표준 대칭키 암호화 알고리즘을 사용
- **CBC 운영 모드**: 랜덤 초기화 벡터(IV)로 높은 보안성 보장
- **수메르 문자 변환**: 암호화된 텍스트를 고대 수메르 쐐기문자로 변환하여 시각적 보안 레이어 추가
- **이중 보안 레이어**: 암호화 후 인코딩을 통한 추가 보안 강화
- **MCP 프로토콜 지원**: Model Context Protocol을 통해 Claude와 같은 LLM에서 암호화 기능 사용 가능

### 기술적 특징

- PKCS7 패딩을 통한 블록 크기 최적화
- 랜덤 IV 생성으로 동일 평문의 다른 암호문 생성 (예측 공격 방지)
- Base64 인코딩 중간 처리로 바이너리 데이터 안전 처리
- 최종 출력을 수메르 쐐기문자로 변환하여 시각적 난독화

## 사용 방법

### 기존 명령줄 도구 (단독 스크립트)

```powershell
# 테스트 모드 (암호화 후 즉시 복호화 검증)
python sumerian.py test "password" "secretKey123"

# 암호화 모드
python sumerian.py encrypt "password" "secretKey123"

# 복호화 모드
python sumerian.py decrypt "𒁀VXKD𒄿𒌋𒀹B𒁀BN𒍝TE𒀻𒈬X𒌝K𒍪𒊏F𒇷AJF𒁀HJ𒌝𒌋𒌋𒅈IDB𒌷KVO𒉿I𒈦" "secretKey123"
```

### MCP 서버 사용 (패키지 설치 후)

#### 설치

```bash
# 현재 디렉토리에서 패키지 설치
pip install -e sumerian_mcp/
```

#### MCP 서버 실행

```bash
# stdio 모드 (Claude와 같은 LLM에서 사용)
sumerian-mcp server

# SSE 모드
sumerian-mcp server --transport sse --host localhost --port 8000
```

#### 명령줄에서 직접 암호화/복호화

```bash
# 암호화
sumerian-mcp encrypt "password" "secretKey123"

# 복호화
sumerian-mcp decrypt "𒁀VXKD𒄿𒌋𒀹B𒁀BN𒍝TE𒀻𒈬X𒌝K𒍪𒊏F𒇷AJF𒁀HJ𒌝𒌋𒌋𒅈IDB𒌷KVO𒉿I𒈦" "secretKey123"
```

### Claude에서 MCP 서버 사용하기

1. 터미널에서 서버 실행:
   ```bash
   sumerian-mcp server
   ```

2. Claude 웹사이트에서 "MCP 서버 연결" 버튼을 클릭하고 "로컬 커맨드 라인 서버 추가"를 선택합니다.

3. 서버 이름(예: "Sumerian Encryption")을 입력하고 연결합니다.

4. 이제 Claude에서 다음과 같이 암호화/복호화 도구를 사용할 수 있습니다:
   "비밀번호 'my_secret'를 키 'master_key'로 암호화해줘"

## 작동 원리

1. 입력된 평문을 AES-256 CBC 모드로 암호화 (랜덤 IV 사용)
2. 암호화된 바이너리 데이터를 Base64 인코딩
3. Base64 인코딩된 문자열을 고대 수메르 문자로 치환
4. 복호화 시 위 과정을 역순으로 진행

이 프로젝트는 현대 암호화 기술과 고대 문자 체계를 결합하여 독특하고 안전한 암호화 솔루션을 제공합니다.
