import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from openai import OpenAI

from news import fetch_today_news

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")


def build_system_prompt(articles):
    if not articles:
        news_block = "오늘 수집된 뉴스가 없습니다."
    else:
        news_block = "\n".join(
            f"{i + 1}. [{a['source']}] {a['title']} ({a['published']}) - {a['link']}"
            for i, a in enumerate(articles)
        )

    return (
        "당신은 '오늘의 뉴스' 챗봇입니다. 아래는 오늘 수집된 최신 뉴스 목록입니다.\n"
        "사용자의 질문에는 이 목록을 근거로 답하고, 목록에 없는 내용을 물으면 모른다고 솔직히 말하세요.\n"
        "요약을 요청하면 간결하게 정리하고, 관련 기사 링크를 함께 안내하세요.\n\n"
        f"[오늘의 뉴스 목록]\n{news_block}"
    )


@app.route("/")
def index():
    articles = fetch_today_news()
    return render_template("index.html", articles=articles)


@app.route("/api/news")
def api_news():
    return jsonify(fetch_today_news())


@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json(force=True) or {}
    user_message = (data.get("message") or "").strip()
    history = data.get("history") or []

    if not user_message:
        return jsonify({"error": "message is required"}), 400

    if not os.environ.get("OPENAI_API_KEY"):
        return jsonify({"error": "OPENAI_API_KEY가 설정되지 않았습니다. .env 파일을 확인하세요."}), 500

    articles = fetch_today_news()
    messages = [{"role": "system", "content": build_system_prompt(articles)}]
    messages.extend(history[-10:])
    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.4,
        )
        reply = response.choices[0].message.content
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
