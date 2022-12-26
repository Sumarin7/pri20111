from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


class login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    comm = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Login %r>' % self.id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/contacs')
def contacs():
    return render_template("contacs.html")
@app.route('/admin#/<int:id>')
def login(id):
    article = Article.query.get(id)
    return render_template("login.html", article=article)

@app.route('/admin', methods=['POST', 'GET'])
def admin():
    username = request.form.get('username')
    password = request.form.get('password')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
    if username == 'root' and password == 'pass':
        return render_template("login.html")

    return render_template("admin.html")

@app.route('/about')
def about():
    return render_template("about.html")
@app.route('/reviews_post')
def reviews_post():
    return render_template("/reviews_post.html")

@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)

@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)

@app.route('/posts/<int:id>/del')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении статьи произошла ошибка"

@app.route('/posts/<int:id>/update', methods=['POST','GET'])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "При редактировании статьи произошла ошибка"
    else:
        return render_template("post_update.html", article=article)


@app.route('/create_article', methods=['POST','GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return "При добавление статьи произошла ошибка"
    else:
        return render_template("create_article.html")

@app.route('/reviews', methods=['POST','GET'])
def reviews():
    if request.method == "POST":
        name = request.form['name']
        text = request.form['text']

        reviews = Reviews(name=name, text=text)

        try:
            db.session.add(reviews)
            db.session.commit()
            return redirect('/reviews')
        except:
            return "При добавление статьи произошла ошибка"
    else:
        return render_template("/reviews.html")



if __name__ == "__main__":
    app.run(debug=True)

