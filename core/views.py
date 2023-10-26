from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.db.models import Q

from .models import Pet, Appointment, Vaccination
from .forms import (PetForm, AppointmentForm, SignUpForm, VaccinationSearchForm, VaccinationForm)  # We'll define these forms later

# Register/Login View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib import messages


from django.urls import reverse_lazy
from django.views import generic

User = get_user_model()


class SignUpView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


@login_required
def dashboard(request):
    print(request.user.role)
    if request.user.role == User.VET:
        return redirect('core:vet_dashboard')
    if request.user.role == User.THIRD_PARTY:
        return redirect('core:third_party_dashboard')
    user_pets = Pet.objects.filter(owner=request.user)
    upcoming_appointments = Appointment.objects.filter(pet__in=user_pets).order_by('date', 'time')
    context = {
        'user_pets': user_pets,
        'upcoming_appointments': upcoming_appointments,
    }
    return render(request, 'dashboard.html', context)

@login_required
def add_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            messages.success(request, f"{pet.name} successfully added")
            return redirect('core:dashboard')
    else:
        form = PetForm()
    return render(request, 'add_pet.html', {'form': form})


@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST, user=request.user)
        if form.is_valid():
            appointment = form.save()
            messages.success(request, f'Appointment booked with {appointment.service_provider}')
            return redirect('core:dashboard')
    else:
        form = AppointmentForm(user=request.user)
    return render(request, 'book_appointment.html', {'form': form})


def third_party_dashboard(request):
    # Ensure user is a third party/groomer
    if not request.user.is_authenticated or request.user.role != User.THIRD_PARTY:
        return HttpResponseForbidden("You are not allowed to view this page")

    # Fetch all pets with their vaccination information
    pets = Pet.objects.select_related('owner').prefetch_related('vaccination_set').all()

    upcoming_appointments = Appointment.objects.filter(service_provider=request.user).order_by('date', 'time')

    context = {
        'pets': pets, 'upcoming_appointments': upcoming_appointments,
    }
    return render(request, 'third_party_dashboard.html', context)


def vet_dashboard(request):
    # Ensure user is a vet
    if not request.user.is_authenticated or request.user.role != User.VET:
        return HttpResponseForbidden("You are not allowed to view this page")

    if request.method == 'POST':
        form = VaccinationForm(request.POST)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.vet = request.user
            form_obj.save()
            # Redirect to the same page to see the newly added record and to add more records
            messages.success(request, f'Info successfully entered for {form_obj.pet.name}')
            return redirect('core:vet_dashboard')
    else:
        form = VaccinationForm()

    # Fetch all pets with their vaccination information
    pets = Pet.objects.select_related('owner').prefetch_related('vaccination_set').all()
    upcoming_appointments = Appointment.objects.filter(service_provider__in=[request.user]).order_by('date', 'time')

    context = {
        'form': form,
        'pets': pets,
        'upcoming_appointments': upcoming_appointments
    }
    return render(request, 'vet_dashboard.html', context)


def approve_appointment(request, appointment_id):
    if not request.user.is_authenticated or request.user.role not in [User.VET, User.THIRD_PARTY]:
        messages.warning(request, 'Not allowed')
        return redirect('core:dashboard')

    try:
        appointment = Appointment.objects.filter(service_provider=request.user).get(id=appointment_id)
        appointment.status = Appointment.APPROVED
        appointment.save()
        messages.success(request, f'The appointment approved with {appointment.pet.name}')
        return redirect('core:dashboard')
    except Appointment.DoesNotExist:
        messages.warning(request, 'Appointment does not exist')
        return redirect('core:dashboard')


class VaccinationSearchView(ListView):
    model = Vaccination
    template_name = 'vaccination_search.html'
    context_object_name = 'vaccinations'

    def get_queryset(self):
        queryset = super().get_queryset()

        ssn = self.request.GET.get('ssn')
        pet_name = self.request.GET.get('pet_name')
        vaccination_name = self.request.GET.get('vaccination_name')
        print(vaccination_name)

        filters = Q()
        if ssn:
            filters &= Q(pet__owner__ssn=ssn)
        if pet_name:
            filters &= Q(pet__name__icontains=pet_name)
        if vaccination_name:
            filters &= Q(vaccination_name__icontains=vaccination_name)

        return queryset.filter(filters)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VaccinationSearchForm(self.request.GET)
        return context
