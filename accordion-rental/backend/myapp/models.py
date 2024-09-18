from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta
from django.contrib.auth.models import User

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
    length = models.FloatField(default=36)  # Corrected typo from lenhght
    weight = models.FloatField()
    keyboard = models.FloatField()
    folds = models.IntegerField(null=True, blank=True)  # Optional field
    deep = models.IntegerField(null=True, blank=True)  # Optional field
    bass_start_notes = models.CharField(max_length=255, null=True, blank=True)  # Optional field
    newPrice = models.FloatField(default=2000)
    usedPrice = models.FloatField(default=1000)
    
    class Meta:
        db_table = 'model'  # Specifies the exact table name in the database
        """ managed = False
 """
    def __str__(self):
        return f"{self.brand} {self.model}"
    
class Rates(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)
    rate = models.FloatField()

    class Meta:
        db_table = 'rates'
    def __str__(self):
        return f"{self.description} - {self.rate}"    

class Rendipillid(models.Model):
    instrumentId = models.AutoField(primary_key=True)
    modelId = models.ForeignKey(Model, on_delete=models.CASCADE)
    color = models.CharField(max_length=64)
    serial = models.CharField(max_length=64)
    info_est = models.TextField()
    info_eng = models.TextField()
    status = models.CharField(max_length=64, default='Available')
    price_level = models.ForeignKey(Rates, on_delete=models.CASCADE)

    class Meta:
        db_table = 'rendipillid'
    def __str__(self):
        return f"{self.modelId.brand} {self.modelId.model} - {self.color}"


class Users(models.Model):
    LANGUAGE_CHOICES = [
        ('Eesti', 'Eesti'),
        ('English', 'English'),
    ]
    phone_validator = RegexValidator(
        regex=r'^\+?\d{10,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    userId = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    firstName = models.CharField(max_length=64)
    lastName = models.CharField(max_length=64)
    country = models.CharField(max_length=64, default='Estonia')
    province = models.CharField(max_length=64)
    municipality = models.CharField(max_length=64)
    settlement = models.CharField(max_length=64)
    street = models.CharField(max_length=64)
    house = models.CharField(max_length=64)
    apartment = models.CharField(max_length=64, null=True, blank=True)
    phone = models.CharField(
        max_length=15,
        validators=[phone_validator],  # Phone number validator
        default='+372'
    )
    email = models.EmailField(
        unique=False,
        validators=[EmailValidator(message="Enter a valid email address.")]
    )
    institution = models.CharField(max_length=64, null=True, blank=True)
    teacher = models.CharField(max_length=64, null=True, blank=True)
    language = models.CharField(max_length=7, choices=LANGUAGE_CHOICES, default='Eesti')

    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return f"{self.firstName} {self.lastName}"

# Signal to create Users profile automatically when a new User is created
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Users.objects.create(user=instance)  # Create the user profile when the User is created
    else:
        instance.users.save()  # Save the profile when the User is saved
    
    

class Agreements(models.Model):
    agreementId = models.AutoField(primary_key=True)
    referenceNr = models.IntegerField(unique=True, blank=True, null=True, editable=False)
    userId = models.ForeignKey(Users, on_delete=models.CASCADE)
    instrumentId = models.ForeignKey(Rendipillid, on_delete=models.CASCADE)
    startDate = models.DateField()
    months = models.IntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2, editable=False)  # Automatically filled
    info = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=15, editable=False, choices=[
        ('Created', 'Created'),
        ('Active', 'Active'), #contract signed
        ('EndingSoon', 'Ending Soon'),
        ('Ended', 'Ended'),
        ('Finished', 'Finished')
    ], default='Created')
    invoice_interval = models.IntegerField(default=1)
    
    
    def __str__(self):
        return f"{self.agreementId} - {self.userId.firstName} {self.userId.lastName} - {self.instrumentId.modelId.brand} {self.instrumentId.modelId.model}"

    @property
    def endDate(self):
        end_date = self.startDate + timedelta(days=30 * self.invoiceInterval)
        return min(end_date, datetime.now().date())

    class Meta:
        db_table = 'agreements'

    def save(self, *args, **kwargs):
        is_new = self._state.adding

        # Temporarily set referenceNr to None (or any placeholder)
        if is_new and not self.referenceNr:
            self.referenceNr = 0  # Placeholder value to bypass the NOT NULL constraint

        # Fetch the rate for the associated instrument before saving
        if self.instrumentId:
            # Fetch the rate from the Rates table based on price_level ForeignKey in Rendipillid
            rate_instance = Rates.objects.filter(id=self.instrumentId.price_level_id).first()
            
            if rate_instance:
                # Set the base rate from the Rates table
                base_rate = rate_instance.rate

                # Apply multiplier based on the months value
                if 3 <= self.months <= 11:
                    self.rate = round(base_rate * 1.4)  # Adjusted rate for 3 to 11 months
                elif self.months < 3:
                    self.rate = round(base_rate * 2.1)  # Adjusted rate for less than 3 months
                else:
                    self.rate = round(base_rate * 1)  # Default rate for 12 months or more

        # Save the Agreement instance
        super().save(*args, **kwargs)

        # If it's a new instance and referenceNr is still the default, update it
        if is_new and self.referenceNr == 0:  # Check the placeholder value
            self.referenceNr = calculate_reference_number(self.agreementId)
            Agreements.objects.filter(agreementId=self.agreementId).update(referenceNr=self.referenceNr)

        # Update the status of the connected instrument to "Reserved"
        if self.instrumentId:
            instrument = self.instrumentId
            #NB do not forget to switch to Reserved back later !!!
            instrument.status = "Available"
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
    agreement = models.ForeignKey('Agreements', on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # New price field
    status = models.CharField(
        max_length=10,
        choices=[
            ('Issued', 'Issued'),
            ('Sent', 'Sent'),
            ('Paid', 'Paid'),
        ],
        default='Issued'
    )

    class Meta:
        db_table = 'invoices'

    def save(self, *args, **kwargs):
        # If an agreement is selected, populate price and quantity from Agreements model
        if self.agreement:
            # Set price from agreement if not already set
            if not self.price:
                self.price = self.agreement.rate
            
            # Set quantity from agreement.invoice_interval if not already set
            if not self.quantity:
                self.quantity = self.agreement.invoice_interval

        super().save(*args, **kwargs)  # Call the original save method

    def __str__(self):
        return f"{self.id} - {self.date}"
    
