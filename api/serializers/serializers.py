from rest_framework import serializers
#noinspection PyUnresolvedReferences
from api.models import Produk, Kategori, Status


class KategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategori
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class ProdukSerializer(serializers.ModelSerializer):
    kategori = KategoriSerializer()
    status = StatusSerializer()
    formatted_harga = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Produk
        fields = ['id_produk', 'nama_produk', 'harga', 'kategori', 'status', 'formatted_harga']



    def create(self, validated_data):
        kategori_data = validated_data.pop('kategori')
        status_data = validated_data.pop('status')

        kategori_instance, _ = Kategori.objects.get_or_create(**kategori_data)
        status_instance, _ = Status.objects.get_or_create(**status_data)

        produk_instance = Produk.objects.create(
            kategori=kategori_instance,
            status=status_instance,
            **validated_data
        )
        return produk_instance

    def update(self, instance, validated_data):
        kategori_data = validated_data.pop('kategori', None)
        status_data = validated_data.pop('status', None)

        instance = super().update(instance, validated_data)

        if kategori_data:
            instance.kategori = Kategori.objects.get_or_create(**kategori_data)[0]
        if status_data:
            instance.status = Status.objects.get_or_create(**status_data)[0]

        instance.save()
        return instance

    def get_formatted_harga(self, obj):
        harga_str = obj.harga
        try:
            harga_float = float(harga_str)
            return harga_float
        except ValueError:
            return harga_str
