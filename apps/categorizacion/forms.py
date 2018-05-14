# encode: utf-8
from django import forms
from apps.categorizacion.fields import StarsField, StarsFieldRango, RangoField, StarsFieldLogical
from apps.categorizacion.models import *

class FormFirma(forms.Form):
    user = forms.CharField(
        required=False,
        label="user",
        widget=forms.TextInput(
            attrs={'id': 'user'})
    )
    password = forms.CharField(
        required=False,
        label="password",
        widget=forms.TextInput(
            attrs={'id': 'password'})
    )
    width = forms.CharField(
        required=False,
        label="width",
        widget=forms.TextInput(
            attrs={'id': 'width'})
    )
    height = forms.CharField(
        required=False,
        label="height",
        widget=forms.TextInput(
            attrs={'id': 'height'})
    )
    server = forms.CharField(
        required=False,
        label="server",
        widget=forms.TextInput(
            attrs={'id': 'server'})
    )
    puerto = forms.CharField(
        required=False,
        label="puerto",
        widget=forms.TextInput(
            attrs={'id': 'puerto'})
    )
    rutaOrigen = forms.CharField(
        required=False,
        label="rutaOrigen",
        widget=forms.TextInput(
            attrs={'id': 'rutaOrigen'})
    )
    rutaDestino = forms.CharField(
        required=False,
        label="rutaDestino",
        widget=forms.TextInput(
            attrs={'id': 'rutaDestino'})
    )
    passwordPdf = forms.CharField(
        required=False,
        label="passwordPdf",
        widget=forms.TextInput(
            attrs={'id': 'passwordPdf'})
    )
    razon = forms.CharField(
        required=False,
        label="razon",
        widget=forms.TextInput(
            attrs={'id': 'razon'})
    )
    ubicacion = forms.CharField(
        required=False,
        label="ubicacion",
        widget=forms.TextInput(
            attrs={'id': 'ubicacion'})
    )

    mailContacto = forms.CharField(
        required=False,
        label="mailContacto",
        widget=forms.TextInput(
            attrs={'id': 'mailContacto'})
    )
    pX = forms.CharField(
        required=False,
        label="pX",
        widget=forms.TextInput(
            attrs={'id': 'pX'})
    )
    pY = forms.CharField(
        required=False,
        label="pY",
        widget=forms.TextInput(
            attrs={'id': 'pY'})
    )
    pW = forms.CharField(
        required=False,
        label="pW",
        widget=forms.TextInput(
            attrs={'id': 'pW'})
    )
    pH = forms.CharField(
        required=False,
        label="pH",
        widget=forms.TextInput(
            attrs={'id': 'pH'})
    )
    pagina = forms.CharField(
        required=False,
        label="pagina",
        widget=forms.TextInput(
            attrs={'id': 'pagina'})
    )
    tipoFirma = forms.CharField(
        required=False,
        label="tipoFirma",
        widget=forms.TextInput(
            attrs={'id': 'tipoFirma'})
    )
    metodo = forms.CharField(
        required=False,
        label="metodo",
        widget=forms.TextInput(
            attrs={'id': 'metodo'})
    )
    email = forms.CharField(
        required=False,
        label="email",
        widget=forms.TextInput(
            attrs={'id': 'email'})
    )
    serial = forms.CharField(
        required=False,
        label="serial",
        widget=forms.TextInput(
            attrs={'id': 'serial'})
    )
    clave_publica = forms.CharField(
        required=False,
        label="clave_publica",
        widget=forms.TextInput(
            attrs={'id': 'clave_publica'})
    )
    cantidad = forms.CharField(
        required=False,
        label="cantidad",
        widget=forms.TextInput(
            attrs={'id': 'cantidad'})
    )
    resultado_firma = forms.CharField(
        required=False,
        label="resultado_firma",
        widget=forms.TextInput(
            attrs={'id': 'resultado_firma'})
    )
    mayscript = forms.CharField(
        required=False,
        label="mayscript",
        widget=forms.TextInput(
            attrs={'id': 'mayscript'})
    )
    pdf_firma0 = forms.CharField(
        required=False,
        label="pdf_firma0",
        widget=forms.TextInput(
            attrs={'id': 'pdf_firma0'})
    )
    pdf_firma1 = forms.CharField(
        required=False,
        label="pdf_firma1",
        widget=forms.TextInput(
            attrs={'id': 'pdf_firma1'})
    )
    pdf_firma2 = forms.CharField(
        required=False,
        label="pdf_firma2",
        widget=forms.TextInput(
            attrs={'id': 'pdf_firma2'})
    )
    pdf_firma3 = forms.CharField(
        required=False,
        label="pdf_firma3",
        widget=forms.TextInput(
            attrs={'id': 'pdf_firma3'})
    )
    pdf_firma4 = forms.CharField(
        required=False,
        label="pdf_firma4",
        widget=forms.TextInput(
            attrs={'id': 'pdf_firma4'})
    )
    pdf_firma5 = forms.CharField(
        required=False,
        label="pdf_firma5",
        widget=forms.TextInput(
            attrs={'id': 'pdf_firma5'})
    )
    pdf_firma6 = forms.CharField(
        required=False,
        label="pdf_firma6",
        widget=forms.TextInput(
            attrs={'id': 'pdf_firma6'})
    )
    pdf_firma7 = forms.CharField(
        required=False,
        label="pdf_firma7",
        widget=forms.TextInput(
            attrs={'id': 'pdf_firma7'})
    )
    pdf_firma8 = forms.CharField(
        required=False,
        label="pdf_firma8",
        widget=forms.TextInput(
            attrs={'id': 'pdf_firma8'})
    )
    pdf_firma9 = forms.CharField(
        required=False,
        label="pdf_firma9",
        widget=forms.TextInput(
            attrs={'id': 'pdf_firma9'})
    )

class RespuestaDual(forms.Form):
    enunciado=forms.CharField(
        min_length = 30, 
        max_length=2048, 
        required=True, 
        widget=forms.Textarea(attrs={'required':'true', 'rows':10})
        # widget=forms.TextInput(attrs={'required':'true'})
    )     
    valor_respuesta=forms.ModelChoiceField(
    		widget=forms.Select(
    			attrs={'class': 'select_form'}
    			),
    		queryset = ValorRespuestaConfig.objects.filter(
    			id__in=RespuestaValorRespuesta.objects.filter(
    				pregunta_config__tipo_respuesta__codigo = "D"
    			).values(
    				'respuesta_config'
    			)
    		).distinct("nombre")
    	)


class RespuestaEscala(forms.Form):
    enunciado=forms.CharField(
        min_length = 30, 
        max_length = 2048, 
        widget=forms.Textarea(attrs={'required':'true'})
        # widget=forms.TextInput(attrs={'required':'true'})
    )
    valor_respuesta= forms.ModelChoiceField(
            widget=forms.Select(attrs={'class': 'select_form'}),
            queryset = ValorRespuestaConfig.objects.filter(
            	id__in=RespuestaValorRespuesta.objects.filter(
            		pregunta_config__tipo_respuesta__codigo = "E"
            	).values(
            		'respuesta_config'
            	)
            ).distinct("nombre")
        )


class RespuestaRango(forms.Form):
    enunciado=forms.CharField(
        min_length = 30, 
        max_length=2048, 
        widget=forms.Textarea(attrs={'required':'true'})
        # widget=forms.TextInput(attrs={'required':'true'})
    )
    unidad_o_medida=forms.ModelChoiceField(
            widget=forms.Select(
                attrs={'class': 'col-xs-9', 'class': 'select_unidad'}
                ),
            queryset = TipoMedida.objects.all()
            )


class RespuestaRepetitiva(forms.Form):
    enunciado=forms.CharField(
        max_length=2048,
        widget=forms.Textarea(attrs={'required':'true', 'rows':10})
    )


class RespuestaCondicional(forms.Form):
    enunciado=forms.CharField(
        min_length = 30, 
        max_length=2048, 
        widget=forms.Textarea(attrs={'required':'true'})
        #widget=forms.TextInput(attrs={'required':'true'})
    )
    valor_respuesta=forms.ModelChoiceField(
        widget=forms.Select(
            attrs={'class': 'select_form_val'}
            ),
        queryset = ValorRespuestaConfig.objects.filter(
            id__in=RespuestaValorRespuesta.objects.filter(
                pregunta_config__tipo_respuesta__codigo = "C"
            ).values(
                'respuesta_config'
            )
        )
    )


class RespuestaFormula(forms.Form):
    enunciado = forms.CharField(
        min_length=30,
        max_length = 2048,
        widget=forms.Textarea(attrs={'required':'true'})
    )

    def __init__(
        self, 
        tabulador,
        *args, **kwargs):

        super(RespuestaFormula, self).__init__(*args, **kwargs)        
        """
            Colocar solo los indicadores que pertenecen a este tabulador
            indicado por el parametro <<tabulador>>
        """
        self.fields['operando'] = forms.ModelChoiceField(
            queryset = Indicador.objects.filter(tabulador_id=tabulador)
        )
        self.fields['operador'] = forms.ModelChoiceField(
            queryset = OperadorFormula.objects.filter( logico = False )
        )


class AspectoFundamentalForm(forms.Form):
    def __init__(
        self,
        currentTab,
        *args, **kwargs):
        super(AspectoFundamentalForm, self).__init__(*args, **kwargs)
        self.fields['nombre'] = forms.CharField( 
            min_length = 4,
            max_length = 2048,
            widget=forms.Textarea(attrs={'required':'true'})
        )

        if(currentTab == "basic-req"):
            self.fields['tipo_aspecto'] = forms.ModelChoiceField(
                queryset = TipoAspectoFundamental.objects.exclude(abreviacion__in = ["E", "VE", "RD"])
            )
            self.fields['tipo_aspecto'].widget.attrs['required'] = True
