from django.db import models

class Model(models.Model):
    modelId = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=128)
    model = models.CharField(max_length=128)
    keys = models.IntegerField()
    low = models.IntegerField()
    sb = models.IntegerField()
    bRows = models.IntegerField()
    fb = models.IntegerField()
    reedsR = models.IntegerField()
    reedsL = models.IntegerField()
    reeds_fb = models.IntegerField()
    range_fb = models.IntegerField()
    fb_low = models.IntegerField()
    regR = models.IntegerField()
    regL = models.IntegerField()
    height = models.FloatField()
    width = models.FloatField()
    weight = models.FloatField()
    keyboard = models.FloatField()
    newPrice = models.FloatField()
    usedPrice = models.FloatField()
    
    class Meta:
        db_table = 'model'  # Specifies the exact table name in the database

    def __str__(self):
        return f"{self.brand} {self.model}"
    
    

class Rendipillid(models.Model):
    instrumentId = models.AutoField(primary_key=True)
    color = models.CharField(max_length=128)
    serial = models.CharField(max_length=128)
    info_est = models.TextField()
    info_eng = models.TextField()
    status = models.CharField(max_length=128)
    price_level = models.IntegerField(default=1)
    modelId = models.ForeignKey(Model, on_delete=models.CASCADE, db_column='modelId')

    class Meta:
        db_table = 'rendipillid'  # Specifies the exact table name in the database

    def __str__(self):
        return f"{self.color} - {self.serial}"

class Rates(models.Model):
    rateId = models.AutoField(primary_key=True)
    description = models.CharField(max_length=256)
    rate = models.FloatField()

class Users(models.Model):
    userId = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=128)
    lastName = models.CharField(max_length=128)
    country = models.CharField(max_length=128)
    province = models.CharField(max_length=128)
    municipality = models.CharField(max_length=128)
    settlement = models.CharField(max_length=128)
    street = models.CharField(max_length=128)
    house = models.CharField(max_length=128)
    apartment = models.CharField(max_length=128, blank=True, null=True)
    phone = models.CharField(max_length=128)
    email = models.EmailField(unique=True)
    institution = models.CharField(max_length=128, blank=True, null=True)
    teacher = models.CharField(max_length=128, blank=True, null=True)

class Agreements(models.Model):
    agreementId = models.AutoField(primary_key=True)
    referenceNr = models.IntegerField()
    userId = models.ForeignKey(Users, on_delete=models.CASCADE)
    instrumentId = models.ForeignKey(Rendipillid, on_delete=models.CASCADE)
    startDate = models.DateField()
    months = models.IntegerField()
    rate = models.IntegerField()
    info = models.TextField()
    status = models.CharField(max_length=128)

class Invoices(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    agreementId = models.ForeignKey(Agreements, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
