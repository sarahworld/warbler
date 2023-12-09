"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        user1 = User(
            email="testuser1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD"
        )

        db.session.add(user1)
        db.session.commit()

        user2 = User(
            email="testuser2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        db.session.add(user2)
        db.session.commit()

        user5 = User(
            email="testuser5@test.com",
            username="testuser5",
            password="password"
        )

        uuid5 = 5555
        user5.id = uuid5
        db.session.commit()

        self.user1 = user1
        self.user2 = user2
        self.user5 = user5

        self.client = app.test_client()

    
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

        

    def test_user_model(self):
        """Does basic model work?"""
        self.user1.following.append(self.user2);
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(self.user1.messages), 0)
        self.assertEqual(len(self.user1.followers), 0)
        self.assertEqual(self.user1.__repr__(),f'<User #{self.user1.id}: testuser1, testuser1@test.com>')
        self.assertIs(self.user1.is_following(self.user2), True)
        self.assertIs(self.user2.is_followed_by(self.user1), True)

        self.user1.following.remove(self.user2);
        db.session.commit()

        self.assertIs(self.user1.is_following(self.user2), False)
        self.assertIs(self.user2.is_followed_by(self.user1), False)

    def test_user_create_valid_creds(self):

        user_test = User.signup('user_test','usertest@f.com','password', None, 'canada','Hi Its life',None)
        uuid = 1111
        user_test.id = uuid

        db.session.commit()

        user_test = User.query.get(uuid);
        self.assertIsNotNone(user_test)
        self.assertEqual(user_test.username, 'user_test');
        self.assertEqual(user_test.email, 'usertest@f.com');
        self.assertNotEqual(user_test.password, 'password');
        self.assertTrue(user_test.password.startswith, '$2b$');


    def test_user_create_invalid_creds(self):

        user_test_invalid = User.signup(None,'usertest3@f.com','password', None, 'canada','Hi Its life',None)
        uuid = 1256788955
        user_test_invalid.id = uuid

        db.session.commit()

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_user_authenticate(self):

        test = User.authenticate(self.user5.username, "password")

        self.assertIsNotNone(test)
        self.assertEqual(self.user5.id, 5555)

    def test_user_authenticate_invalid_username(self):

        self.assertFalse(User.authenticate("baduser", "password"))

    
    def test_user_authenticate_invalid_password(self):

        self.assertFalse(User.authenticate(self.user5.username, "wrongpassword"))
    


if __name__ == '__main__':
    unittest.main()