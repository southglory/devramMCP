# 수메르어 MCP (Master Control Program)

간단한 단일 스크립트 형식의 수메르어 암호화/복호화 MCP입니다.

## 기능

- AES-256 CBC 모드 암호화/복호화
- 암호화된 텍스트를 수메르어 문자로 변환
- 파일 암호화/복호화
- 대화형 모드
- API 서버 모드

## 설치

필요한 종속성 설치:

```bash
pip install -r requirements.txt
```

## 사용법

### 명령줄 모드

```bash
# 텍스트 암호화
python sumerian_mcp.py encrypt --text "Hello, World!" --key "my_secret_key"

# 텍스트 복호화
python sumerian_mcp.py decrypt --text "𒉿𒀝𒅖𒌒𒆠𒀞..." --key "my_secret_key"

# 파일 암호화
python sumerian_mcp.py encrypt_file --file "secret.txt" --key "my_secret_key"

# 파일 복호화
python sumerian_mcp.py decrypt_file --file "secret.txt.sumerian" --key "my_secret_key"

# 도구 목록 보기
python sumerian_mcp.py list_tools
```

### 대화형 모드

```bash
python sumerian_mcp.py --interactive
```

대화형 모드에서는 다음과 같은 명령어를 사용할 수 있습니다:

```
mcp> encrypt text="Hello, World!" key="my_secret_key"
mcp> decrypt text="𒉿𒀝𒅖𒌒𒆠𒀞..." key="my_secret_key"
mcp> encrypt_file filepath="secret.txt" key="my_secret_key"
mcp> decrypt_file filepath="secret.txt.sumerian" key="my_secret_key"
mcp> list_tools
mcp> help
mcp> exit
```

### 서버 모드

```bash
python sumerian_mcp.py --server
```

서버는 기본적으로 `http://localhost:8000`에서 실행됩니다.

API 엔드포인트:
- `GET /tools` - 사용 가능한 도구 목록
- `POST /tools/{tool_id}` - 도구 실행

예를 들어:
```bash
curl -X POST http://localhost:8000/tools/encrypt -H "Content-Type: application/json" -d '{"text": "Hello, World!", "key": "my_secret_key"}'
```

## 환경 변수

- `MASTER_KEY` - 기본 마스터 키 (지정하지 않으면 "sumerian_default_key" 사용) 