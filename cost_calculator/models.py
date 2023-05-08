from django.db import models


# Create your models here.
class Date(models.Model):
    date = models.DateField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=1000, default="")
    year = models.IntegerField(default=0)
    month = models.IntegerField(default=0)
    day = models.IntegerField(default=0)
    indonesia_days = 'Senin Selasa Rabu Kamis Jumat Sabtu Minggu'.split()
    read_only = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.read_only:
            return False
        super().save(*args, **kwargs)
        self.year = self.date.year
        self.month = self.date.month
        self.day = self.date.day
        if self.description=="":
            self.description = f'Deskripsi pengeluaran tanggal/hari ini ({self.date} - {self.indonesia_days[self.date.weekday()]})'                
        super().save(*args, **kwargs)
        return True


class CostItem(models.Model):
    the_date = models.ForeignKey(Date, on_delete=models.DO_NOTHING)
    name_id = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    unit_count = models.IntegerField(default=0)
    unit_type = models.CharField(max_length=25, default='KG')
    total_price = models.IntegerField(default=0)
    unit_price = models.IntegerField(default=0)
    additional_price = models.IntegerField(default=0)
    sort_order = models.IntegerField(default=-1)
    
    def calculate_total_price(self):
        total_price = (self.unit_price*self.unit_count)
        self.total_price = total_price
        return total_price
    
    def save(self, *args, **kwargs):
        # if self.total_price==0:
        if True:
            self.calculate_total_price()
        super().save(*args, **kwargs)

class OutcomeItem(models.Model):
    the_date = models.ForeignKey(Date, on_delete=models.DO_NOTHING)
    randemen_beras = models.FloatField(default=0)
    berat_hasil_beras = models.IntegerField(default=0)
    pemasukan = models.IntegerField(default=0)
    keuntungan = models.IntegerField(default=0)
    description = models.CharField(max_length=1000, default="")

    def save(self, *args, **kwargs):
        if self.berat_hasil_beras > 0:
            sumber_padi = [
            'padi_supadi:_ke_lokasi_petani_bandar',
            'padi_supadi:_bandar_ke_pabrik',
            'padi_supadi:_petani_ke_pabrik',
            'padi_supadi:_sendiri',
            'padi_ketan:_ke_lokasi_petani_bandar',
            'padi_ketan:_bandar_ke_pabrik',
            'padi_merah:_ke_lokasi_petani_bandar',
            'padi_merah:_bandar_ke_pabrik',
            'padi_lainnya:_ke_lokasi_petani_bandar',
            'padi_lainnya:_bandar_ke_pabrik',
            'padi_lainnya:_petani_ke_pabrik',
            'padi_lainnya:_sendiri',
            ]
            total_berat_padi = sum([CostItem.objects.get(the_date=self.the_date, name_id=padi_id).unit_count for padi_id in sumber_padi])
            self.randemen_beras = self.berat_hasil_beras/total_berat_padi
        if self.pemasukan > 0:
            total_cost = sum([cost_item.total_price for cost_item in CostItem.objects.filter(the_date=self.the_date)])
            if total_cost > 0:
                self.keuntungan = self.pemasukan - total_cost
    
        super().save(*args, **kwargs)
        if self.description=="":
            self.description = f'Deskripsi pemasukan tanggal/hari ini ({self.the_date.date} - {self.the_date.indonesia_days[self.the_date.date.weekday()]})'                
        super().save(*args, **kwargs)
