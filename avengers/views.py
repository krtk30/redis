# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from avengers.models import Hero


class Heroes(viewsets.ModelViewSet):
    queryset = Hero.objects.all()
    permission_classes = (AllowAny, )