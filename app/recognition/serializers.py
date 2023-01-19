"""
Serializers for the recipe app
"""
from rest_framework import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile
from core.models import Recognition

from model.fastrcnnapi import ped
from model.pic_rectan import rectan
import cv2
import numpy as np
from PIL import Image
import io
import sys


class RecognitionSerializer(serializers.ModelSerializer):
    """ Serializer for Recognition objects """

    class Meta:
        model = Recognition

        fields = ['id', 'description', 'date']
        read_only_fields = ['id']

    # def create(self, validated_data):
    #     """ Create a new recognition """
    #     recipe = Recognition.objects.create(**validated_data)
    #     return recipe

    # def update(self, instance, validated_data):
    #     """ Update a recognition """
    #     instance = super().update(instance, validated_data)

    #     instance.save()
    #     return instance

    def to_internal_value(self, data):
        instance = super().to_internal_value(data)
        print(data)
        img = data['origin_image']
        print(img)
        img = cv2.imdecode(
            np.frombuffer(img.file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        pic_location, num = ped.fastrcnn_api(img)
        result_img = rectan(img, pic_location)
        result_img1 = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
        result_pil = Image.fromarray(result_img1)
        output = io.BytesIO()
        result_pil.save(output, format='JPEG')
        output.seek(0)
        cv2.imwrite('model/result.jpeg', result_img)

        instance['origin_pos'] = str(pic_location)
        instance['update_image'] = InMemoryUploadedFile(
            output, None, '123'+'.jpg', 'image/jpeg',
            sys.getsizeof(output), None)

        return instance


class RecognitionDetailSerializer(RecognitionSerializer):
    """ Serializer for recipe detail """

    class Meta(RecognitionSerializer.Meta):
        fields = RecognitionSerializer.Meta.fields + \
                ['origin_image', 'origin_pos',
                    'update_image', 'update_pos', 'qualified']


class RecognitionPredictionImageSerializer(serializers.ModelSerializer):
    """ Serializer for uploading images to recognition """
    """separate serializer for uploading images since we don't want to
    allow users to update different kinds of types of data in the
    same request """

    class Meta:
        model = Recognition
        fields = ['id', 'origin_image', 'origin_pos', 'update_image']
        read_only_fields = ['id']
        extra_kwargs = {'origin_image': {'required': True}}


class RecognitionUpdateImageSerializer(serializers.ModelSerializer):
    """ Serializer for uploading images to recognition """
    """separate serializer for uploading images since we don't want to
    allow users to update different kinds of types of data in the
    same request """

    class Meta:
        model = Recognition
        fields = ['id', 'update_image', 'update_pos']
        read_only_fields = ['id']
        extra_kwargs = {'update_iamge': {'required': True}}
