from django.contrib.auth.models import AbstractUser
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class User(AbstractUser):
    PET_OWNER = "Pet Owner"
    VET = "Vet"
    THIRD_PARTY = "Third Party/Groomer"
    ROLE_CHOICES = (
        (PET_OWNER, PET_OWNER),
        (VET, VET),
        (THIRD_PARTY, THIRD_PARTY),
    )

    role = models.CharField(choices=ROLE_CHOICES, max_length=200)
    ssn = models.CharField(max_length=200, null=True)
    license_no = models.CharField(max_length=200, null=True, blank=True)
    service_provider = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        if not self.service_provider:
            return self.username
        return f'{self.first_name} {self.last_name} ({self.service_provider})'


class Pet(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    breed = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    # ... you can add more fields as required

    def __str__(self):
        return f'{self.name}-{self.pk}'


class Vaccination(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    vaccination_name = models.CharField(max_length=100)
    vaccination_no = models.CharField(max_length=100, null=True)
    vaccination_date = models.DateField()
    next_vaccination_date = models.DateField(null=True)
    vet = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vaccinations_given')
    # date_administered = models.DateField(null=True)
    notes = models.TextField()


class Appointment(models.Model):
    APPOINTMENT_TYPES = (
        ('vet', 'Vet Visit'),
        ('groomer', 'Groomer/Third Party Visit'),
    )
    APPROVED = 'approved'
    PENDING = 'pending'
    STATUS_CHOICES = (
        (APPROVED, APPROVED),
        (PENDING, PENDING),
    )
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    type = models.CharField(choices=APPOINTMENT_TYPES, max_length=10)
    notes = models.TextField()
    status = models.CharField(choices=STATUS_CHOICES, default=PENDING, max_length=200)
    service_provider = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='appointments')

    @property
    def is_approved(self):
        return self.status == self.APPROVED


class SearchHistory(models.Model):
    ssn = models.CharField(max_length=500, null=True)
    pet_name = models.CharField(max_length=500, null=True)
    vaccination_name = models.CharField(max_length=500, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
