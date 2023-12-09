from django.core.management.base import BaseCommand
#noinspection PyUnresolvedReferences
from api.models import Produk,  Kategori, Status
#noinspection PyUnresolvedReferences
from api.serializers.serializers import ProdukSerializer
import requests
import hashlib
from datetime import datetime, timedelta

current_date = datetime.now() + timedelta(hours=7) #UTC
new_datetime = current_date + timedelta(hours=1)

class Command(BaseCommand):
    help = 'Populated the database'

    def handle(self, *args, **kwargs):
        username = 'tesprogrammer'+new_datetime.strftime("%d%m%yC%H"),
        password_encoded = ('bisacoding-'+current_date.strftime("%d-%m-%y")).encode('utf-8')
        response = requests.post('https://recruitment.fastprint.co.id/tes/api_tes_programmer',
                                 {
                                     'username': username,
                                     'password': hashlib.md5(password_encoded).hexdigest()
                                 })

        result = response.json()
        if(result['error'] != 0):
            print('something wrong : ', result)
            return

        if(result['data']):
            try:
                print('start seeds')
                for item in result['data']:
                    item['kategori'] = {'nama_kategori': item['kategori']}
                    item['status'] = {'nama_status': item['status']}

                    serializer = ProdukSerializer(data=item)
                    if serializer.is_valid():
                        try:
                            serializer.save()
                        except Exception as e:
                            print('something wrong', e)
                print('seeding data successfull')
            except Exception as e:
                print('something wrong', e)
