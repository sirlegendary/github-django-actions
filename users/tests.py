from django.test import TestCase
from django.contrib.auth.models import User
from users.models import Board, BoardText, StickyNotes, Url, Image, Video
from users.forms import CustomUserCreationForm


# Create your tests here.

class UserTestCase(TestCase):
    def test_user(self):
        username = 'shetu'
        password = 'hello'
        email    = 'test@test.com'
        u = User(username=username)
        # u = User(email=email)
        u.set_password(password)
        u.save()
        self.assertEqual(u.username, username)
        self.assertTrue(u.check_password(password))
    
    def test_createboard(self):
        title = 'Test Board'
        user_id = 1
        board = Board.objects.create(title=title, user_id=user_id)
        board.save()
        self.assertEqual(board.title, title)