from flask import Flask, render_template, url_for, redirect, flash, request
from forms import RegisterForm, LoginForm, PostForm
from extensions import db
from models import User, Post
from flask_login import LoginManager, login_user, logout_user, current_user, login_required


# create applicaton object
app = Flask(__name__)

# secret key
app.config["SECRET_KEY"] = "a-secret-key-for-flaskform"

# set up database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///my_database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# integrate db with app
db.init_app(app)

# integrate login manager to app. (it loads the user, set/clear cookies, redirection for unauthenticated user)
login_manager = LoginManager(app)

# redirect unauthenticated user to this page.
login_manager.login_view = "login"

# NEW AND CORRECT WAY
@login_manager.user_loader
def load_user(user_id):
    user = db.session.get(User, int(user_id))
    return user

@app.route("/")
def home():
    posts = Post.query.all()
    return render_template("home.html", title="New Post", posts=posts)


@app.route("/register", methods=["GET", "POST"])
def register():
    # if already logged in
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    form = RegisterForm()
    # it checks for [post request, validators, csrf tokens]
    if form.validate_on_submit():
        flash(f"{form.username.data}, Successfully registered.")
        flash(f"Now Log In, To enjoy reading other posts")

        # collecting data from flaskform
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # create a user object and store it in db.
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        # add and commit it.
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html", title="Register", form=form)



@app.route("/login", methods=["GET", "POST"])
def login():
    # if already logged in
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    

    form = LoginForm()
    # it checks for [post request, validators, csrf tokens]
    if form.validate_on_submit():
        #collecting data from flaskform
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data

        # check is user exist.
        existing_user = User.query.filter_by(email=email).first()

        if existing_user and existing_user.check_password(password):
            login_user(existing_user, remember=remember_me)
            flash(f"Successfully Logged In as {existing_user.username}.", "success")
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for("home"))
        else:
            flash("Invalid email or password. Please try again.", "danger")
        
    return render_template("login.html", title="Log In", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/create_post", methods = ["GET", "POST"])
@login_required
def create_post():
    form = PostForm()

    if form.validate_on_submit(): 
        # collecting data from flaskform
        title = form.title.data
        body = form.body.data

        # check does title exist
        existing_title = Post.query.filter_by(title=title).first()

        if existing_title:
            return "beta title chori mat kar, apna utha"
        
        # add to database
        new_post = Post(title=title, body=body)
        new_post.owner = current_user
        db.session.add(new_post)
        db.session.commit()

        flash(f"Successfully created post at {new_post.created_at}")

        return redirect(url_for("home"))


    return render_template("post.html", title="Create Post", form=form)




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

