from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Produk, Kategori, Status
from .serializers.serializers import ProdukSerializer, KategoriSerializer, StatusSerializer


# Create your views here.

def home(request):
    return HttpResponse("welcome home !")

@api_view(['GET'])
def kategori_list(request):
    try:
        kategori_list = Kategori.objects.all()
        serializer = KategoriSerializer(kategori_list, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Exception as e:
        return HttpResponse(e)

@api_view(['GET'])
def produk_list_api(request):
    try:
        status_ready = Status.objects.get(nama_status='bisa dijual')
        produk_list = Produk.objects.filter(status_id=status_ready.id_status).order_by('id_produk')
        serializer = ProdukSerializer(produk_list, many=True)
        return JsonResponse(serializer.data, safe=False)
    except Exception as e:
        return HttpResponse(e)

@api_view(['GET'])
def get_by_id(request, produk_id):
    try:
        produk = Produk.objects.get(id_produk=produk_id)
        serializer = ProdukSerializer(produk)
        return JsonResponse(serializer.data, safe=False)
    except Exception as e:
        return HttpResponse(e)

@api_view(['DELETE'])
def produk_delete(request, produk_id):
    try:
        produk = Produk.objects.get(id_produk=produk_id)
        produk.delete()
        return JsonResponse({'message': f'Produk with ID {produk_id} deleted successfully'}, status=204)
    except Produk.DoesNotExist:
        return JsonResponse({'message': f'Produk with ID {produk_id} not found'}, status=404)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)

@api_view(['PUT'])
def produk_update(request, produk_id):
    try:
        produk = Produk.objects.get(id_produk=produk_id)
        serializer = ProdukSerializer(produk, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    except Produk.DoesNotExist:
        return JsonResponse({'message': f'Produk with ID {produk_id} not found'}, status=404)
    except Exception as e:
        return JsonResponse({'message': str(e)}, status=500)


@api_view(['POST'])
def produk_create(request):
    try:
        data = request.data
        serializer = ProdukSerializer(data=data)
        if serializer.is_valid():
            try:
                serializer.save()
                return JsonResponse(serializer.data, status=200)
            except Exception as e:
                print('ada error', e)
        return JsonResponse(serializer.errors, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({'message': str(e)}, status=500)