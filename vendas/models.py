from django.db import models
from django.db.models import Sum, F


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.IntegerField(default=0)

    def __str__(self):
        return self.nome


class Comanda(models.Model):
    mesa = models.IntegerField()
    aberta = models.BooleanField(default=True)
    criada_em = models.DateTimeField(auto_now_add=True)

    def total_consumo(self):
        resultado = self.itens.aggregate(
            total=Sum(F('produto__preco') * F('quantidade'))
        )
        return resultado['total'] or 0

    def total_geral(self):
        return float(self.total_consumo()) * 1.10

    def __str__(self):
        return f"Comanda Mesa {self.mesa}"


class Pedido(models.Model):
    comanda = models.ForeignKey(
        Comanda,
        on_delete=models.CASCADE,
        related_name='itens'
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT
    )
    quantidade = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"


from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Pedido)
def atualizar_estoque(sender, instance, created, **kwargs):
    if created:
        instance.produto.estoque -= instance.quantidade
        instance.produto.save()
