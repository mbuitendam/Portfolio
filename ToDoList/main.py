from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from forms import RegisterUser, loginUser, addToDo
from datetime import datetime
from typing import List


app = Flask(__name__)
app.config['SECRET_KEY'] = "f5ca17dd26a0ae6f64607a1815da5198942cac44d02fbaf18d19fb4d9553ab51"
Bootstrap5(app)

# CREATE DATABASE
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite3.db'

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)

    itemList: Mapped[List["ListedItem"]] = relationship(back_populates="author")

class ListedItem(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Foreign Key forming relationship with User
    author_id: Mapped[int] = mapped_column(db.ForeignKey("user.id"))
    author: Mapped["User"] = relationship(back_populates="itemList")

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    subheading: Mapped[str] = mapped_column(String(250), nullable=False)
    content: Mapped[str] = mapped_column(Text)
    dueDate: Mapped[datetime]

with app.app_context():
    db.create_all()


# Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)




##  Routes ##

# Login/register/Logout routes
@app.route('/', methods=["GET", "POST"])
def index():
    form = loginUser()
    if form.validate_on_submit():
        password = form.password.data
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        # Email is unqiue, so will only find single result
        user = result.scalar()
        
        if not user:
            flash("That email does not exist, plase try again")
        elif not check_password_hash(user.password, password):
            flash("Password or email incorrect, please try again")
        else:
            login_user(user)
            return redirect(url_for("get_list")) 
    return render_template("login.html", form=form, loggedIn=current_user.is_authenticated)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterUser()
    if form.validate_on_submit():
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        #If user exists
        if user:
            flash("You've already signed up, please log in!")
        
        hash_saltedPassword = generate_password_hash(
            form.password.data,
            method='scrypt',
            salt_length=8
        )

        new_user = User(
            email = form.email.data,
            name = form.name.data,
            role = form.role.data,
            password = hash_saltedPassword
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("register.html", form=form, current_user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("index"))


# main list routing
@app.route("/list", methods=["GET", "POST"])
@login_required
def get_list():
    result = db.session.execute(db.select(ListedItem).where(ListedItem.author_id == current_user.id))
    posts = result.scalars().all()
    return render_template("to_do_list.html", all_posts=posts, current_user=current_user)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add_item():
    form = addToDo()
    if form.validate_on_submit():
        new_item = ListedItem(
            title = form.title.data,
            subheading = form.subheading.data,
            content = form.content.data,
            dueDate = form.dueDate.data,
            author = current_user
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for("get_list"))
    return render_template("add_item.html", form=form)



if __name__ == "__main__":
    app.run(debug=True)