from rest_framework import mixins, permissions, authentication, status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.exceptions import NotFound as NotFoundError
from rest_framework.pagination import PageNumberPagination
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth import get_user_model
from django.core import serializers
from .serializers import UserSerializer, ContactSerializer
from .models import Contact


User = get_user_model()


class CustomPaginator(PageNumberPagination):
    page_size = 10  # Number of objects to return in one page

    def generate_response(self, query_set, serializer_obj, request):
        try:
            page_data = self.paginate_queryset(query_set, request)
        except NotFoundError:
            return Response(
                {"error": "No results found for the requested page"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serialized_page = serializer_obj(page_data, many=True)
        return self.get_paginated_response(serialized_page.data)


class CreateUserView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserInfoView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        return Response(UserSerializer(user).data)


class UsernameAvailability(APIView):
    pemission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data["username"]
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(data={"message": False})
        else:
            return Response(data={"message": True})


class ContactView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        contacts = User.objects.get(id=request.user.id).contacts.all().order_by("id")
        paginator = CustomPaginator()
        return paginator.generate_response(contacts, ContactSerializer, request)

    def post(self, request, *args, **kwargs):
        data = request.data
        data["user"] = request.user.id
        serializer = ContactSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ContactEditView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        data["user"] = request.user.id
        instance = Contact.objects.get(id=request.data["id"])
        serializer = ContactSerializer(instance=instance, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ContactDeleteView(APIView):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        instance = Contact.objects.get(id=request.data["id"])
        serializer = ContactSerializer(instance=instance)
        instance.delete()
        return Response(serializer.data)
