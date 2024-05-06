from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class BloglyTestCase(TestCase):
    """Tests view functions for Blogly app"""

    def setUp(self):
        """Add sample users"""

        Post.query.delete()
        User.query.delete()
        
        user1 = User(first_name="Michelle", last_name="Obama", image_url="https://www.dispatch.com/gcdn/authoring/2014/01/16/NCOD/ghows-OH-8dc0e22b-d75a-4408-b0fa-5195209baa1b-25e25e82.jpeg?width=1200&disable=upscale&format=pjpg&auto=webp")

        user2 = User(first_name="Elizabeth", last_name="Woolridge")

        db.session.add_all([user1, user2])
        db.session.commit()

        self.user1 = user1
        self.user2 = user2

        post = Post(title="A Note from Michelle Obama", content="School lunches are going to get soooooooo much worse but it's okay because they'll actually be soooooo much better and you will be healthy and thank me. Thumbs up", user_id=self.user1.id)

        db.session.add(post)
        db.session.commit()

        self.post_id = post.id
        self.post = post

    def test_home_page(self):
        with app.test_client() as client:
            resp = client.get("/")

            self.assertEqual(resp.status_code, 302)


    def test_show_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Michelle Obama", html)

    def test_show_user_info(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user1.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Michelle Obama", html)
            self.assertIn("Edit", html)
            self.assertIn("Delete", html)
            self.assertIn("A Note from Michelle Obama", html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.user2.id}/delete")

            self.assertNotIn(User.query.get(self.user2.id), User.query.all())

            self.assertEqual(resp.status_code, 302)

    def test_delete_post(self):
        with app.test_client() as client:
            resp = client.post(f"/posts/{self.post_id}/delete")

            self.assertNotIn(Post.query.get(self.post_id), Post.query.all())

            self.assertEqual(resp.status_code, 302)

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()