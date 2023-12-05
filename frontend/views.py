from django.shortcuts import render

def produk_list(request):
    return render(request, 'frontend/produk_list.html', {})
