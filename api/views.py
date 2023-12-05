from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Produk
from .serializers.serializers import ProdukSerializer


# Create your views here.

def home(request):
    return HttpResponse("welcome home !")

@api_view(['GET'])
def produk_list_api(request):
    produk_list = Produk.objects.all()
    serializer = ProdukSerializer(produk_list, many=True)
    return JsonResponse(serializer.data, safe=False)
