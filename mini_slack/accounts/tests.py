import uuid

from django.test import TestCase

from .models import User


class UserModelTests(TestCase):
    def test_user_gets_a_uuid_primary_key(self):
        user = User.objects.create_user(username="alice", email="alice@example.com", password="s3curePass!23")

        self.assertIsInstance(user.id, uuid.UUID)

    def test_email_uniqueness_is_enforced(self):
        User.objects.create_user(username="bob", email="dup@example.com", password="s3curePass!23")

        with self.assertRaises(Exception):
            User.objects.create_user(username="bob2", email="dup@example.com", password="s3curePass!23")
