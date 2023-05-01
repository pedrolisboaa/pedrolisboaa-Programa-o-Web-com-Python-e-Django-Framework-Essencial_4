from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import Postagem
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from .forms import CustomUsuarioCreateForm, CustomUsuarioChangeForm
from .models import CustomUsuario

@admin.register(CustomUsuario)
class CustomUsuarioAdmin(UserAdmin):
    add_form = CustomUsuarioCreateForm
    form = CustomUsuarioChangeForm
    model = CustomUsuario
    list_display = ('first_name', 'last_name', 'email', 'telefone', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'fone')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(Postagem)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', '_autor')
    #excluído que vai logar
    exclude =   ['autor',]
    
    # Retornando o nome completo
    def _autor(self, instancia):
        return f'{instancia.autor.get_full_name()}'
    
    # Somente o usuáro vai ver seus proprios posts
    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(autor=request.user)
    
    #excluído que vai logar
    def save_model(self, request: Any, obj: Any, form: Any, change: Any):
        obj.autor = request.user
        return super().save_model(request, obj, form, change)
