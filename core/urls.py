from django.urls import path
from . import views
from .views import SignUpView

app_name = 'core'

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    # path('register_login/', views.register_login_view, name='register_login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_pet/', views.add_pet, name='add_pet'),
    path('book_appointment/', views.book_appointment, name='book_appointment'),
    path('third_party_dashboard/', views.third_party_dashboard, name='third_party_dashboard'),
    path('vet_dashboard/', views.vet_dashboard, name='vet_dashboard'),
    path('approve_appointment/<int:appointment_id>/', views.approve_appointment, name='approve_appointment'),
    path('search_vaccinations/', views.VaccinationSearchView.as_view(), name='search_vaccinations'),
]
