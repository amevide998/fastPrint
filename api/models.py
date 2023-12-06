from django.db import models

# Create your models here.

class Kategori(models.Model):
    id_kategori = models.AutoField(primary_key=True)
    nama_kategori = models.CharField(max_length=255)

class Status(models.Model):
    id_status = models.AutoField(primary_key=True)
    nama_status = models.CharField(max_length=255)

class Produk(models.Model):
    id_produk = models.AutoField(primary_key=True)
    nama_produk = models.CharField(max_length=255)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.id_produk:
            max_id = Produk.objects.aggregate(models.Max('id_produk'))['id_produk__max']
            next_id = 1 if max_id is None else max_id + 1
            self.id_produk = next_id

        super().save(*args, **kwargs)
