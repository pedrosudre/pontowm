import uuid
from django.db import models

from django.utils import timezone
from datetime import timedelta

def get_file_path(_instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return filename

class Pessoa(models.Model):
    nome = models.CharField('Nome', max_length=100)
    cpf = models.CharField('CPF', unique=True)

    class Meta:
        abstract = True
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'

    def __str__(self):
        return self.nome

class Funcionario(Pessoa):
    carga_horaria_diaria = models.IntegerField('Carga Horaria', default=8)
    saldo_horas = models.FloatField('Saldo de Horas', default=0.0)  # Saldo acumulado de horas
    data_admissao = models.DateField('Data de Admissão', auto_now_add=True)
    data_demissao = models.DateField('Data de Demissão', null=True, blank=True)
    cargo = models.CharField('Cargo', max_length=100)
    salario = models.DecimalField('Salário', max_digits=10, decimal_places=2)
    endereco = models.TextField('Endereço', null=True, blank=True)
    telefone = models.CharField('Telefone', max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.nome} - {self.cargo}"

    def atualizar_saldo(self, horas_trabalhadas):
        """Atualiza o saldo de horas do funcionário."""
        self.saldo_horas += horas_trabalhadas - self.carga_horaria_diaria
        self.save()

class RegistroPonto(models.Model):
    funcionario = models.ForeignKey(Funcionario, related_name="pontos", on_delete=models.CASCADE)
    data = models.DateField('Data', default=timezone.now)
    entrada = models.TimeField('Hora de Entrada', null=True, blank=True)
    saida = models.TimeField('Hora de Saída', null=True, blank=True)
    horas_trabalhadas = models.IntegerField('Horas Trabalhadas', null=True, blank=True)

    def calcular_horas_trabalhadas(self):
        if self.entrada and self.saida:
            # Converte as horas de entrada e saída para objetos de datetime
            entrada = timezone.make_aware(timezone.datetime.combine(self.data, self.entrada))
            saida = timezone.make_aware(timezone.datetime.combine(self.data, self.saida))

            # Calcula a diferença de tempo
            horas_trabalhadas = saida - entrada
            self.horas_trabalhadas = horas_trabalhadas.total_seconds() / 3600  # Converte para horas
            self.save()

    def salvar_ponto(self):
        self.calcular_horas_trabalhadas()
        self.funcionario.atualizar_saldo(self.horas_trabalhadas)
        self.save()


        class Meta:
            unique_together = ('funcionario', 'data')