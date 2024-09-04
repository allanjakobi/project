from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

#from .models import Rendipillid
import datetime

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
    usedPrice = models.FloatField(default=1000)
    
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
        return f"{self.modelId.brand} {self.modelId.model} - {self.color}"

class Rates(models.Model):
    id = models.AutoField(primary_key=True)
    rateId = models.IntegerField()
    description = models.CharField(max_length=256)
    rate = models.FloatField()
    startDate = models.DateField()
    
    class Meta:
        db_table = 'rates'       
    def __str__(self):
        return f"ID{self.rateId}: {self.description} {self.rate} EUR"

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
    referenceNr = models.IntegerField(unique=True, editable=False, default=1)  # Default value set to 1
    userId = models.ForeignKey(Users, on_delete=models.CASCADE)
    instrumentId = models.ForeignKey(Rendipillid, on_delete=models.CASCADE)
    startDate = models.DateField()
    months = models.IntegerField(default=12)
    rate = models.IntegerField(editable=False)
    status = models.CharField(max_length=128, editable=False, default="Created")
    invoice_interval = models.IntegerField(default=1)
    info = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'agreements'

    def save(self, *args, **kwargs):
        is_new = self._state.adding

        # Fetch the rate for the associated instrument before saving
        if self.instrumentId:
            rate_instance = Rates.objects.filter(rateId=self.instrumentId.price_level).first()
            if rate_instance:
                self.rate = rate_instance.rate
                
                # Apply multipliers based on the months value
                if 3 <= self.months <= 11:
                    self.rate = round(self.rate * 1.4)
                elif self.months < 3:
                    self.rate = round(self.rate * 2.1)

        super().save(*args, **kwargs)

        # If it's a new instance and referenceNr is still the default value, update it
        if is_new and self.referenceNr == 1:
            self.referenceNr = calculate_reference_number(self.agreementId)
            Agreements.objects.filter(agreementId=self.agreementId).update(referenceNr=self.referenceNr)
        
        # Update the status of the connected instrument to "Reserved"
        if self.instrumentId:
            instrument = self.instrumentId
            instrument.status = "Reserved"
            instrument.save()







def calculate_reference_number(agreementId):
    year = datetime.datetime.now().year
    base_number = f"{year}{agreementId}"

    if not base_number.isdigit():
        raise ValueError("Base number must be numeric")

    # Calculating control digit (modulo 10 approach)
    weights = [7, 3, 1]
    total = 0
    for i, digit in enumerate(reversed(base_number)):
        total += int(digit) * weights[i % len(weights)]

    control_digit = (10 - (total % 10)) % 10
    reference_number = f"{base_number}{control_digit}"

    return int(reference_number)



class Invoices(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    agreementId = models.ForeignKey(Agreements, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    status = models.TextField()
    
    class Meta:
        db_table = 'invoices'       
   
