from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float


app = Flask(__name__)

## Create Database
class base(DeclarativeBase):
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new-books-collection.db"

# Create the extension
db = SQLAlchemy(model_class=base)
# initialize the app with the extension
db.init_app(app)

## Create the table
class Book(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"
    
# Create table schema in the database. Requires application context.
with app.app_context():
    db.create_all()



@app.route('/', methods=["GET","POST"])
def home():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars()
    return render_template("index.html", books = all_books.all())


@app.route("/add", methods=["GET","POST"])
def add():
    if request.method == "POST":
        new_book = Book(
            title=request.form["Title"],
            author=request.form["Author"],
            rating=request.form["Rating"]
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))

    return render_template("add.html")


