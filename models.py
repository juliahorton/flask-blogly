"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

default_url = "https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.pngall.com%2Fwp-content%2Fuploads%2F5%2FProfile-PNG-File.png&f=1&nofb=1&ipt=c6ad3ea13d612bf8902ee57a330331b9eb80c538bf44859b3db2269cdcbb7969&ipo=images"

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, default=default_url)

    def __repr__(self):
        """Show information about user."""
        user = self
        return f"<User {user.id} {user.first_name} {user.last_name}>"
    
    def get_full_name(self):
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"