from django.shortcuts import render
from rest_framework.views import APIView

# Create your views here.

class HomePageView(APIView):
    def get(self, request):
        return render(request, 'base.html', {})