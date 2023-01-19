""" Views for the recipe APIs. """
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Recognition
from recognition import serializers


class RecognitionViewSet(viewsets.ModelViewSet):
    """ View for managing recipe attributes """
    serializer_class = serializers.RecognitionDetailSerializer
    queryset = Recognition.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def _params_to_ints(self, qs):
        """ Convert a list of string IDs to a list of integers """
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """ Return objects for the current authenticated user only """
        queryset = self.queryset
        return queryset.filter(
            user=self.request.user).order_by('-id').distinct()

    def perform_create(self, serializer):
        """ Create a new recipe """
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """ Return appropriate serializer class """
        if self.action == 'upload_image':
            return serializers.RecognitionUpdateImageSerializer
        elif self.action == 'predicate':
            return serializers.RecognitionPredictionImageSerializer
        elif self.action == 'list':
            return serializers.RecognitionSerializer

        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='prediction')
    def predicate(self, request, pk=None):
        """ Upload an image to a recipe """
        recognition = self.get_object()
        serializer = self.get_serializer(
            recognition,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(methods=['POST'], detail=True, url_path='update-image')
    def upload_image(self, request, pk=None):
        """ Upload an image to a recipe """
        recognition = self.get_object()
        serializer = self.get_serializer(
            recognition,
            data=request.data
        )
        # get image from request
        # image = request.data['image']
        # print("$$$$$$$$$$$$$$$$$$$")
        # print(request.data)
        # print("$$$$$$$$$$$$$$$$$$$")
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
