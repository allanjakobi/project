from django.db import models

class Model(models.Model):
    modelId = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=64)
    model = models.CharField(max_length=128)
    keys = models.IntegerField()
    low = models.IntegerField()
    sb = models.IntegerField()
    bRows = models.IntegerField()
    fb = models.IntegerField(default=0)
    reedsR = models.IntegerField()
    reedsL = models.IntegerField()
    reeds_fb = models.IntegerField(default=0)
    range_fb = models.IntegerField(default=0)
    fb_low = models.IntegerField(default=0)
    regR = models.IntegerField()
    regL = models.IntegerField()
    height = models.FloatField(default=36)
    width = models.FloatField(default=18)
    weight = models.FloatField()
    keyboard = models.FloatField()
    newPrice = models.FloatField(default=2000)
    usedPrice = models.FloatField(default=100)
    
    class Meta:
        db_table = 'model'  # Specifies the exact table name in the database
        managed = False

    def __str__(self):
        return f"{self.brand} {self.model}"
    
    

class Rendipillid(models.Model):
    instrumentId = models.AutoField(primary_key=True)
    modelId = models.ForeignKey(Model, on_delete=models.CASCADE)
    color = models.CharField(max_length=64)
    serial = models.CharField(max_length=64)
    info_est = models.TextField()
    info_eng = models.TextField()
    status = models.CharField(max_length=64)
    price_level = models.IntegerField(default=1)

    class Meta:
        db_table = 'rendipillid'  # Specifies the exact table name in the database
    def __str__(self):
        return f"{self.color} - {self.serial}"

class Rates(models.Model):
    id = models.AutoField(primary_key=True)
    rateId = models.IntegerField()
    description = models.CharField(max_length=256)
    rate = models.FloatField()
    startDate = models.DateField()
    
    class Meta:
        db_table = 'rates'       
    def __str__(self):
        return f"{self.firstName} {self.lastName}"

class Users(models.Model):
    userId = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=128)
    lastName = models.CharField(max_length=128)
    country = models.CharField(max_length=128, default='Estonia')
    province = models.CharField(max_length=128)
    municipality = models.CharField(max_length=128)
    settlement = models.CharField(max_length=128)
    street = models.CharField(max_length=128)
    house = models.CharField(max_length=128)
    apartment = models.CharField(max_length=128, null=True, blank=True)
    phone = models.CharField(max_length=128, default='+372')
    email = models.EmailField(unique=True)
    institution = models.CharField(max_length=128, null=True, blank=True)
    teacher = models.CharField(max_length=128, null=True, blank=True)
    useful_info = models.CharField(max_length=128, null=True, blank=True)
    
    class Meta:
        db_table = 'users'       
    def __str__(self):
        return f"{self.firstName} {self.lastName}"
    

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
    invoice_interval = models.IntegerField(default=1)  # Default value can be adjusted
    info = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'agreements'       

class Invoices(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    agreementId = models.ForeignKey(Agreements, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    status = models.TextField()
    
    class Meta:
        db_table = 'invoices'       
   
