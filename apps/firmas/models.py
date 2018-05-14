# ~*~ coding: UTF-8 ~*~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Author: Edinson E. Padrón Urdaneta
# Email: epadron@4geeks.co
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Módulos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from apps.configuracion import models as cfg_models
from apps.cuentas import models as cuentas_models
from datetime import datetime
from django.db import models
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


# Modelos ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Firma(models.Model):
    usuario = models.ForeignKey(cuentas_models.MinturUser)
    ministro = models.BooleanField(default=False)
    cargo = models.CharField(max_length=80)
    fecha_providencia = models.DateField()
    numero_providencia = models.CharField(max_length=80)
    numero_gaceta = models.CharField(max_length=80)
    fecha_gaceta = models.DateField()

    def __unicode__(self):
        fields = {
            key.name: getattr(self, key.name) for key in self._meta.fields
        }
        fields.update({
            'nombres': self.usuario.nombres,
            'apellidos': self.usuario.apellidos,
            'fecha_providencia': (
                fields['fecha_providencia'].strftime('%d/%m/%Y')
            ),
            'fecha_gaceta': (
                fields['fecha_gaceta'].strftime('%d/%m/%Y')
            ),
        })

        return (
            u'{nombres} {apellidos}. {cargo}.'
            u' Providencia P/Nº {numero_providencia}'
            u' de fecha {fecha_providencia}.'
            u' Gaceta Oficial de la República Bolivariana de Venezuela'
            u' Nº {numero_gaceta} de fecha {fecha_gaceta}'
        ).format(**fields)

    @classmethod
    def establecer_ministro(cls, usuario):
        ''' Establece en sistema la firma del ministro dado un usuario.

        El usuario proporcionado debe tener una firma previamente registrada.
        '''

        assert isinstance(usuario, cuentas_models.MinturUser)

        cls.objects.filter(ministro=True).update(ministro=False)
        cls.objects.filter(usuario=usuario).update(ministro=True)


class FirmaDelegada(models.Model):
    firma = models.ForeignKey(Firma)
    area = models.ForeignKey(cfg_models.Area)
    fecha_providencia = models.DateField()
    numero_providencia = models.CharField(max_length=80)
    numero_gaceta = models.CharField(max_length=80)
    fecha_gaceta = models.DateField()
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_desactivacion = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        fields = {
            key.name: getattr(self, key.name) for key in self._meta.fields
        }
        fields.update({
            'fecha_providencia': (
                fields['fecha_providencia'].strftime('%d/%m/%Y')
            ),
            'fecha_gaceta': (
                fields['fecha_gaceta'].strftime('%d/%m/%Y')
            ),
        })

        return (
            u'{firma}. Delegación de firma según'
            u' Providencia P/Nº {numero_providencia}'
            u' de fecha {fecha_providencia}.'
            u' Gaceta Oficial de la República Bolivariana de Venezuela'
            u' Nº {numero_gaceta} de fecha {fecha_gaceta}'
        ).format(**fields)

    @classmethod
    def cancelar_delegacion(
        cls, usuario=None, area=None, numero_providencia=None
    ):
        ''' Cancela una delegación de firma existente.

        Cancela la delegación de una firma para el usuario, área o número de
        providencia indicados.
        '''

        if usuario is not None:
            assert isinstance(usuario, cuentas_models.MinturUser)

            queryset = cls.objects.filter(
                firma=Firma.objects.get(usuario=usuario)
            )

        elif area is not None:
            assert isinstance(area, cfg_models.Area)

            queryset = cls.objects.filter(area=area)

        elif numero_providencia is not None:
            assert isinstance(numero_providencia, str)

            queryset = cls.objects.filter(
                numero_providencia=numero_providencia
            )

        else:
            raise AssertionError(
                'Debe indicar usuario, área o número de providencia.'
            )

        queryset.update(activo=False, fecha_desactivacion=datetime.now())

    @classmethod
    def establecer_delegacion(
        cls,
        usuario,
        area,
        numero_providencia,
        fecha_providencia,
        numero_gaceta,
        fecha_gaceta
    ):
        ''' Crea una nueva delegación de firma.

        Crea una nueva delegación de firma para el usuario y área
        proporcionados, bajo la providencia y gaceta correspondientes.
        '''

        assert isinstance(usuario, cuentas_models.MinturUser)
        assert isinstance(area, cfg_models.Area)

        cls.cancelar_delegacion(area=area)

        cls(
            firma=Firma.objects.get(usuario=usuario),
            area=area,
            numero_providencia=numero_providencia,
            fecha_providencia=fecha_providencia,
            numero_gaceta=numero_gaceta,
            fecha_gaceta=fecha_gaceta,
        ).save()

    @classmethod
    def obtener_firma(cls, area):
        ''' Determina la firma apropiada en el área proporcionada.

        Puede devolver una firma delegada si ésta existe, en caso contrario,
        devolverá la firma del ministro en gestión.
        '''

        assert isinstance(area, cfg_models.Area)

        try:
            return cls.objects.get(area=area, activo=True)

        except cls.DoesNotExist:
            return Firma.objects.get(ministro=True)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
