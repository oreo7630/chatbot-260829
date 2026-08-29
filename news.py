"""Google News RSS(한국)에서 오늘 날짜 기사를 가져오는 모듈."""

from datetime import datetime, timezone, timedelta

import feedparser

GOOGLE_NEWS_RSS_URL = "https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko"
KST = timezone(timedelta(hours=9))


def _parse_entry(entry):
    published = getattr(entry, "published_parsed", None)
    if not published:
        return None

    published_dt = datetime(*published[:6], tzinfo=timezone.utc).astimezone(KST)
    source = entry.get("source", {})
    source_title = source.get("title", "") if isinstance(source, dict) else ""

    return {
        "title": entry.title,
        "link": entry.link,
        "source": source_title,
        "published_dt": published_dt,
        "published": published_dt.strftime("%H:%M"),
    }


def fetch_today_news(limit=15):
    """오늘(KST) 발행된 뉴스를 최신순으로 최대 limit개 반환.

    오늘자 기사가 부족하면 최신 기사로 채워서 빈 화면을 방지한다.
    """
    feed = feedparser.parse(GOOGLE_NEWS_RSS_URL)
    today = datetime.now(KST).date()

    parsed = [a for a in (_parse_entry(e) for e in feed.entries) if a]
    parsed.sort(key=lambda a: a["published_dt"], reverse=True)

    todays = [a for a in parsed if a["published_dt"].date() == today]
    articles = todays if todays else parsed

    result = []
    for a in articles[:limit]:
        result.append(
            {
                "title": a["title"],
                "link": a["link"],
                "source": a["source"],
                "published": a["published"],
            }
        )
    return result
