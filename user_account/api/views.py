# api/views.py
from django.shortcuts import render
from rest_framework import generics
from .serializers import UserAccountSerializer
from .models import UserAccount

class CreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new user account."""
        serializer.save()

class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = UserAccount.objects.all()
    serializer_class = UserAccountSerializer
