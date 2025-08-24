from extensions import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

# associaton table for posts and tags table to connect
post_tags = db.Table(
    "post_tags",
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True),
)


# association table for self referential many to many (a user can follow other user)
follows = db.Table(
    "follows",
    db.Column("follower_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("followed_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
)


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    profile_picture = db.Column(db.String(255))
    about_me = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    # create a new attribute (posts) -> one to many
    posts = db.relationship("Post", back_populates="owner", cascade="all, delete-orphan")

    # create a new attribute (followers) -> self-referential many to many
    followers = db.relationship(
        "User",
        secondary="follows",
        primaryjoin = (follows.c.followed_id == id),
        secondaryjoin = (follows.c.follower_id == id),
        back_populates = "following"

    )

    # create a new attribute (following) -> self-referential many to many
    following = db.relationship(
        "User",
        secondary="follows",
        primaryjoin = (follows.c.follower_id == id),
        secondaryjoin = (follows.c.followed_id == id),
        back_populates = "followers"
    )


    # generate password hash
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # check password
    def check_password(self, password):
        return check_password_hash(self.password, password)



    def __repr__(self):
        return f"<User({self.username}, {self.created_at})"
    

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    is_published = db.Column(db.Boolean())
    slug = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False) #FK

    # creating a new attribute (owner)
    owner = db.relationship("User", back_populates="posts")

    #creating a new attribute (tags)
    tags = db.relationship("Tag", secondary="post_tags", back_populates="posts")


    def __repr__(self):
        return f"<Post({self.title}, {self.created_at})"
    

class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    # creating a new attribute (posts)
    posts = db.relationship("Post", secondary="post_tags", back_populates="tags")

    
    def __repr__(self):
        return f"<Tag({self.name})"
    
class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False) #FK
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False) #FK

    def __repr__(self):
        return f"<Comment({self.body})"


    

