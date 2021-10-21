from unittest import TestCase

from app import app
from models import db, User, DEFAULT_IMG_URL

# Use test database and don't clutter tests with SQL
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_ECHO"] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Testing User Model"""

    def setUp(self):
        """Clean"""

        User.query.delete()

    def tearDown(self):
        """roll back if there are any bad entries"""

        db.session.rollback()

    def test_show_user(self):
        user = User(first_name="Test", last_name="User", img_url=DEFAULT_IMG_URL)
        self.assertEqual(user.show_user(), "Test User")
