from django.db import IntegrityError
from rest_framework.exceptions import APIException
from rest_framework import viewsets
from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly,\
    IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken

from core.models import Course, CourseEnroll
from core import serializers


class StudentRegisterView(generics.CreateAPIView):
    serializer_class = serializers.StudentRegisterSerializer


class StudentTokenView(ObtainAuthToken):
    serializer_class = serializers.StudentAuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class StudentUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.StudentRegisterSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class CourseView(viewsets.GenericViewSet, mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.DestroyModelMixin):
    serializer_class = serializers.CourseSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    authentication_classes = (TokenAuthentication,)
    queryset = Course.objects.all()

    def get_queryset(self):
        return self.queryset.filter()

    def perform_create(self, serializer):
        self.permission_classes = (IsAdminUser,)
        serializer.save()

    def perform_destroy(self, instance):
        self.permission_classes = (IsAdminUser,)
        instance.delete()


class CourseEnrollView(viewsets.ModelViewSet):
    serializer_class = serializers.CourseEnrollSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = CourseEnroll.objects.all()

    def get_queryset(self):
        return self.queryset.filter(student=self.request.user)

    def perform_create(self, serializer):
        try:
            serializer.save(student=self.request.user)
        except IntegrityError:
            raise APIException(detail='Already enrolled to this course')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.CourseEnrollDetailSerializer
        return self.serializer_class
