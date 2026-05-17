
from django.contrib import admin
from .models import Produto, Comanda, Pedido


admin.site.register(Produto)
admin.site.register(Comanda)
admin.site.register(Pedido)


