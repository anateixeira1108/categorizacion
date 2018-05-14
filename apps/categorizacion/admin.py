from django.contrib import admin

# Register your models here.
from apps.cuentas.models import MinturUser
from registro.models import TipoPst, Pst
admin.site.register(MinturUser)
admin.site.register(TipoPst)
admin.site.register(Pst)
