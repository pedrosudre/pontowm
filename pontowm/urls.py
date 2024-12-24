# aplic/urls.py
from django.urls import path
from aplic import views

urlpatterns = [
    path('ponto/', views.ponto_view, name='ponto_view'),  # URL para carregar a página de ponto
    path('registrar-ponto/', views.registrar_ponto, name='registrar_ponto'),  # URL para registrar o ponto
]
