from django.core.management.base import BaseCommand
#noinspection PyUnresolvedReferences
from api.models import Produk,  Kategori, Status
import requests

class Command(BaseCommand):
    help = 'Populated the database'

    def check_status_exists(self, status):
        try:
            Status.objects.get(nama_status=status)
            return True
        except Status.DoesNotExist:
            return False

    def check_kategori_exists(self, kategori):
        try:
            Kategori.objects.get(nama_kategori=kategori)
            return True
        except Kategori.DoesNotExist:
            return False

    def handle(self, *args, **kwargs):
        response = requests.post('https://recruitment.fastprint.co.id/tes/api_tes_programmer',
                                 {
                                     'username': 'tesprogrammer051223C20',
                                     'password': 'ae7073cb0fc55d6f35a80c6d8ee59ace'
                                 })

        result = response.json()

        if(result['error'] != 0):
            return

        if(result['data']):
            # status seeder
            Status.objects.all().delete()
            id = 1
            for item in result['data']:
                if(not self.check_status_exists(item['status'])):
                    Status.objects.create(
                        id_status=id,
                        nama_status=item['status']
                    )
                    id = id+1

            # kategori seeder
            Kategori.objects.all().delete()
            id = 1
            for item in result['data']:
                if (not self.check_kategori_exists(item['kategori'])):
                    Kategori.objects.create(
                        id_kategori=id,
                        nama_kategori=item['kategori']
                    )
                    id = id + 1

            # produk seeder
            Produk.objects.all().delete()
            for item in result['data']:
                kategori_id = Kategori.objects.get(nama_kategori=item['kategori']).id_kategori
                status_id = Status.objects.get(nama_status=item['status']).id_status
                Produk.objects.create(
                    id_produk=item['id_produk'],
                    nama_produk=item['nama_produk'],
                    harga=item['harga'],
                    kategori_id=kategori_id,
                    status_id=status_id
                )




