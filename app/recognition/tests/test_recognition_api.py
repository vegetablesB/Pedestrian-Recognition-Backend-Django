""" Tests for the recognition API """
import tempfile
import os

from PIL import Image

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Recognition
from recognition.serializers import (
    RecognitionSerializer,
    RecognitionDetailSerializer,
)


RECOGNITION_API = reverse('recognition:recognition-list')


def detail_url(recognition_id):
    """ Return recognition detail URL """
    return reverse('recognition:recognition-detail', args=[recognition_id])


def predicate_url(recognition_id):
    """ Return recognition detail URL """
    return reverse('recognition:recognition-predicate', args=[recognition_id])


def upload_image_url(recognition_id):
    """ Return recognition detail URL """
    return reverse(
        'recognition:recognition-upload-image',
        args=[recognition_id])


def create_user(**params):
    """ Helper function to create a user """
    return get_user_model().objects.create_user(**params)


class PublicRecognitionApiTests(TestCase):
    """ Test unauthenticated recognition API access """

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """ Test that authentication is required """
        res = self.client.get(RECOGNITION_API)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecognitionApiTests(TestCase):
    """ Test authenticated recognition API access """

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='password')
        self.client.force_authenticate(self.user)

    def test_retrieve_recognitions(self):
        """ Test retrieving a list of recognitions """
        Recognition.objects.create(user=self.user)
        Recognition.objects.create(user=self.user)

        res = self.client.get(RECOGNITION_API)

        recognitions = Recognition.objects.all().order_by('-id')
        serializer = RecognitionSerializer(recognitions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recognitions_limited_to_user(self):
        """ Test retrieving recognitions for user """
        user2 = create_user(email='user2@example.com', password='password')
        Recognition.objects.create(user=user2)
        Recognition.objects.create(user=self.user)

        res = self.client.get(RECOGNITION_API)
        recognitions = Recognition.objects.filter(user=self.user)
        serializer = RecognitionSerializer(recognitions, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_view_recognition_detail(self):
        """ Test viewing a recognition detail """
        recognition = Recognition.objects.create(user=self.user)

        url = detail_url(recognition.id)
        res = self.client.get(url)

        serializer = RecognitionDetailSerializer(recognition)
        self.assertEqual(res.data, serializer.data)

    def test_create_recognition(self):
        """ Helper function to create a new recognition """
        recognition = Recognition.objects.create(user=self.user)
        url = predicate_url(recognition.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            # img = Image.open('/app/model/image.jpeg')
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            res = self.client.post(
                url,
                {'origin_image': ntf},
                format='multipart'
            )

        recognition.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('origin_image', res.data)
        self.assertTrue(os.path.exists(recognition.origin_image.path))

    def test_update_recognition(self):
        """ Test updating a recognition """
        recognition = Recognition.objects.create(user=self.user)
        url = upload_image_url(recognition.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            res = self.client.post(
                url,
                {'update_image': ntf},
                format='multipart'
            )

        recognition.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('update_image', res.data)
        self.assertTrue(os.path.exists(recognition.update_image.path))
