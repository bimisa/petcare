from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Pet, Appointment, Vaccination

User = get_user_model()


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'date_of_birth', 'breed']
        # If you add more fields to the Pet model, make sure to list them here.

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Pet Name'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'breed': forms.TextInput(attrs={'placeholder': 'Breed'}),
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['pet', 'date', 'time', 'type', 'service_provider', 'notes']

        widgets = {
            'pet': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'type': forms.Select(choices=Appointment.APPOINTMENT_TYPES, attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Any additional notes...'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # we'll pass the user when initializing the form in the view
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields['service_provider'].queryset = User.objects.filter(service_provider__isnull=False)
        if user:
            # Filter the pets dropdown to show only the pets owned by the logged-in user
            self.fields['pet'].queryset = Pet.objects.filter(owner=user)
        #     if self.initial.get('type') == User.VET:
        #         self.fields['service_provider'].queryset = User.objects.filter(role=User.VET)
        #     else:
        #         self.fields['service_provider'].queryset = User.objects.filter(role=User.THIRD_PARTY)


class SignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role', 'license_no', 'service_provider', 'ssn']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service_provider'].required = False
        self.fields['license_no'].required = False

    def clean(self):
        cleaned_data = super().clean()

        role = cleaned_data.get('role')
        service_provider = cleaned_data.get('service_provider')

        # Check if the role is not "pet_owner" and service_provider is not provided
        if role != User.PET_OWNER and not service_provider:
            self.add_error('service_provider', 'Service Provider is required for this role.')

        return cleaned_data


class VaccinationForm(forms.ModelForm):
    class Meta:
        model = Vaccination
        fields = ['pet', 'vaccination_name', 'vaccination_date', 'vaccination_no', 'next_vaccination_date', 'notes']
        widgets = {
            'vaccination_date': forms.DateInput(attrs={'type': 'date'}),
            'next_vaccination_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(VaccinationForm, self).__init__(*args, **kwargs)
        self.fields['pet'].queryset = Pet.objects.all()


class VaccinationSearchForm(forms.Form):
    ssn = forms.CharField(required=False, label="Owner SSN")
    pet_name = forms.CharField(required=False, label="Pet Name")
    vaccination_name = forms.CharField(required=False, label="Vaccination Name")

    # class Meta:
    #     widgets = {
    #         'ssn': forms.Select(attrs={'class': 'form-control'}),
    #         'pet_name': forms.Select(attrs={'class': 'form-control'}),
    #         'vaccination_name': forms.Select(attrs={'class': 'form-control'}),
    #     }
