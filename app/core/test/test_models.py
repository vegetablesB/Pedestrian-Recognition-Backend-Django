""" Tests for the models of the core app. """
from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from core import models


def create_user():
    """
    Helper function to create a user.
    """
    return get_user_model().objects.create_user(
        email='test@example.com', password='Testpass123')


class ModelTests(TestCase):
    """
    Tests for models.
    """
    def test_create_user_with_email_successful(self):
        """
        Test creating a new user with an email is successful.
        """
        email = 'test@example.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """
        Test the email for a new user is normalized.
        """
        emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@EXAMPLE.com', 'test4@example.com'],
        ]

        for email, expected in emails:
            user = get_user_model().objects.create_user(
                email=email,
                password='Testpass123'
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """
        Test creating user with no email raises error.
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'Testpass123')

    def test_create_new_superuser(self):
        """
        Test creating a new superuser.
        """
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'Testpass123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_recognition_with_user(self):
        """
        Test creating a new recognition with a user.
        """
        user = create_user()
        recognition = models.Recognition.objects.create(
            user=user,
            origin_image='example.jpg',
            update_image='example.jpg'
        )

        self.assertEqual(recognition.user, user)
        self.assertEqual(recognition.origin_image, 'example.jpg')
        self.assertEqual(recognition.update_image, 'example.jpg')

    @patch('core.models.uuid.uuid4')
    def test_recognition_str(self, mock_uuid):
        """
        Test the recognition string representation.
        """
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        origin_file_path = models.origin_image_file_path(None, 'example.jpg')
        origin_exp_path = f'predicate/recognition/{uuid}.jpg'

        update_file_path = models.update_image_file_path(None, 'example.jpg')
        update_exp_path = f'update/recognition/{uuid}.jpg'

        self.assertEqual(origin_file_path, origin_exp_path)
        self.assertEqual(update_file_path, update_exp_path)
