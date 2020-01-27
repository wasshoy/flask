from flask import Flask, render_template, abort, request
from flaski.models import WikiContent
from flaski.database import db_session
from datetime import datetime

app = Flask(__name__)
# 開発環境用のデバッグ(本番時False)
app.config['DEBUG'] = True

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

# rootディレクトリへのアクセスしたときの動作
@app.route('/')
def hello():
    # Base.query.all(): 全検索
    contents = WikiContent.query.all()
    return render_template('index.html', contents=contents)

# /<title> へアクセスしたときの動作
@app.route('/<title>', methods=['GET'])
def show_content(title):
    # Base.query.all(): フィルタリング
    content = WikiContent.query.filter_by(title=title).first()
    if content is None:
        # title のデータが存在しないとき404エラー
        abort(404)
    return render_template('show_content.html', content=content)

# 新規追加・更新
@app.route('/<title>', methods=['POST'])
def post_content(title=None):
    if title is None:
        abort(404)
    content = WikiContent.query.filter_by(title=title).first()
    # まだないデータなら新規作成
    if content is None:
        content = WikiContent(title,
                            request.form['body']
                            )
    # 既存のデータであれば更新
    else:
        content.body = request.form['body']
        content.date = datetime.now()
    # db更新
    db_session.add(content)
    db_session.commit()
    return content.body

if __name__ == '__main__':
    app.run()