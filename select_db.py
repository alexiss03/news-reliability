from create_db import db, News
earliest_news = db.session.query(News).order_by(News.pubdate.desc()).first()
latest_news = db.session.query(News).order_by(News.pubdate.asc()).first()

print(db.session.query(News).count())
print(earliest_news.pubdate)
print(latest_news.pubdate)

print(News.query.group_by('pubdate'))
