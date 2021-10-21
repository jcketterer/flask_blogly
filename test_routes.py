from unittest import TestCase

from app import app
from models import DEFAULT_IMG_URL, db, User

# Use test database and don't clutter tests with SQL
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_ECHO"] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config["TESTING"] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

db.drop_all()
db.create_all()


class UserViewTestCase(TestCase):
    """Test for routes in blogly"""

    def setUp(self):
        """add sample user"""

        User.query.delete()

        user = User(first_name="Test", last_name="User", img_url=DEFAULT_IMG_URL)
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user
        self.img_url = user.img_url

    def tearDown(self):
        """Clean"""

        db.session.rollback()

    def test_user_list(self):
        with app.test_client() as client:
            res = client.get("/users")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Test User", html)

    def test_user_img(self):
        with app.test_client() as client:
            res = client.get(f"/users/{self.user.id}")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>Test User</h1>", html)

    def test_user_edit(self):
        with app.test_client() as client:
            res = client.get(f"/users/new")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("<h1>Create A User</h1>", html)
