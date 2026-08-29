# 오늘의 뉴스 챗봇

Google News RSS(한국)에서 오늘 발행된 뉴스를 가져와 보여주고, OpenAI API로 뉴스에 대해 대화할 수 있는 웹 챗봇입니다.

## 실행 방법

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

copy .env.example .env       # .env 파일 생성 후 OPENAI_API_KEY 입력
python app.py
```

브라우저에서 http://localhost:5000 접속.

## 구조

- `app.py` - Flask 서버, `/api/chat`에서 OpenAI Chat Completions 호출
- `news.py` - Google News RSS 파싱, 오늘(KST) 기사 필터링
- `templates/index.html` - 뉴스 목록 + 채팅 UI
- `static/` - CSS, JS

## Git에 올리기

```bash
git init
git add .
git commit -m "Initial commit: 오늘의 뉴스 챗봇"
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```

`.env`는 `.gitignore`에 포함되어 있어 API 키가 커밋되지 않습니다.
