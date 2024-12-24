# aplic/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Funcionario, RegistroPonto  # Certifique-se de que os modelos estão configurados corretamente

# View para carregar a página de ponto
def ponto_view(request):
    return render(request, 'ponto.html')  # Renderiza a página de ponto (GET)

# View para registrar o ponto
def registrar_ponto(request):
    if request.method == 'POST':  # Aceita apenas POST para registrar o ponto
        tipo_ponto = request.POST.get('tipo_ponto')

        if tipo_ponto == 'entrada':
            # Lógica para registrar a entrada
            message = 'Entrada registrada com sucesso.'
            status = 'entrada'
        elif tipo_ponto == 'saida':
            # Lógica para registrar a saída
            message = 'Saída registrada com sucesso.'
            status = 'saida'
        else:
            return JsonResponse({'error': 'Tipo de ponto inválido.'}, status=400)

        return JsonResponse({'message': message, 'status': status})

    return JsonResponse({'error': 'Método inválido.'}, status=405)  # Retorna erro se o método não for POST
