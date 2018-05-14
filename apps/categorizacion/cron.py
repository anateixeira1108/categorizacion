#-*- encoding: utf-8 -*-
from apps.categorizacion.helpers.validar_flujo import *
from apps.categorizacion.models import *
from registro.models import RepresentanteContacto
from apps.categorizacion.views import correo
from registro.models import Pst
from django.template.loader import get_template
from django.db.models import Q
from django.template import Context
from django.core.mail import EmailMultiAlternatives
from dateutil import rrule
from registro.models import Direccion as Registro_Direccion
import datetime
import threading
import fcntl

def diasLaborales(fechaInicio, fechaFin, festivos=0, vacaciones=None):
    if vacaciones is None:
        vacaciones= 5, 6         # si no tienes vacaciones no trabajas sab y dom
    laborales = [dia for dia in range(7) if dia not in vacaciones]
    totalDias = rrule.rrule(rrule.DAILY,
        dtstart=fechaInicio,
        until=fechaFin, byweekday=laborales
    )
    return totalDias.count() - festivos

def my_scheduled_job():
    print 'Some'

def print_else():
    p = Pst.objects.all()
    for ps in p:
        print ps.nombres + " " + ps.apellidos
    print 'Else'

def requisitos_documentales():
    """
        Si a las 2 semanas no se han subido todos los requisitos documentales se envia un correo
    """
    solicitudes = Solicitud.objects.filter(
        Q(estatus__abreviacion='SC') | Q(estatus__abreviacion='EC')
    )
    dprint(solicitudes)
    hoy = datetime.datetime.now()
    for s in solicitudes:
        if not validate_requisitos_documentales(s):
            fecha_ultima_modificacion = s.fecha_modificacion_estado.replace(tzinfo=None)
            dias = (hoy - fecha_ultima_modificacion).days

            print dias
            print fecha_ultima_modificacion
            #REVISAR CONDICION!!!!!!!
            if dias!=0 and dias%14==0:
                #<---- Envio de Correo ---->
                direc = Registro_Direccion.objects.filter(pst=s.pst).first()
                direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                    +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                    + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                    +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                    +str(direc.codigo_postal)
                #licencia = dt_licencia(solicitud.pst, solicitud.sucursal)
                if Asignacion.objects.filter(solicitud=s) is None:
                    tipo="consignación"
                    asunto="[MINTUR] Ausencia de Requisitos Documentales"
                else:
                    tipo="corrección"
                    asunto="[MINTUR] Corrección de Requisitos Documentales"
                #<--- Envio de Correo --->
                htmly = get_template('correo/cron_requisitos_docs.html')
                text_plain = get_template('correo/cron_requisitos_docs.txt')

                context = Context({
                    'razon_social': s.pst.razon_social,
                    'direccion': direccionPST,
                    'contacto': RepresentanteContacto.objects.filter(pst=s.pst).first(),
                    'tipo': tipo
                 })

                html_content = htmly.render(context)
                text_content = text_plain.render(context)

                thread_correo = threading.Thread(
                    name='thread_correo', 
                    target=correo, 
                    args=(
                        asunto, 
                        html_content, 
                        text_content, 
                        'gccdev@cgtscorp.com', 
                        ['gccdev@cgtscorp.com'], 
                        None, 
                        None
                    )
                )                
                thread_correo.start()
                """
                lic = LicenciaAsignada.objects.filter(usuario_pst=s.pst.user, 
                    sucursal_id=s.sucursal_id
                ).first()
                if lic:
                    dprint(lic=lic)
                    if s.sucursal_id:
                        licencia = lic.numero_licencia
                        suc= s.pst.denominacion_comercial
                        direccion = "%s, %s, %s, %s" %(s.sucursal.urbanizacion, s.sucursal.avenida_calle, s.sucursal.edificio, s.sucursal.oficina_apartamento)
                    else:
                        licencia = lic.numero_licencia
                        suc= "Sede Principal"
                        direccs = Registro_Direccion.objects.get(pst=s.pst)
                        direccion = "%s, %s, %s, %s, %s, %s" %(direccs.estado.estado, direccs.municipio.municipio, direccs.urbanizacion, direccs.avenida_calle, direccs.edificio, direccs.oficina_apartamento)
                
                <--- Envio de Correo --->
                htmly = get_template('correo/cron_requisitos_docs.html')
                text_plain = get_template('correo/cron_requisitos_docs.txt')

                context = Context({
                 'licencia': licencia,
                 'nombre_pst': s.pst.nombres+" "+s.pst.apellidos,
                 'nombre_establecimiento': suc,
                 'direccion': direccion
                 })

                html_content = htmly.render(context)
                text_content = text_plain.render(context)
                
                Busqueda de correo en parametros de configuracion
                try:
                    corr = ParametroConfiguracion.objects.get(
                        clave="correo_interno"
                        )
                except corr.DoesNotExist:
                    raise e
                corrs = str(corr.valor)
                

                thread_correo = threading.Thread(name='thread_correo', target=correo, args=(u'[MINTUR] Ausencia de Requisitos Documentales', html_content, text_content, 'gccdev@cgtscorp.com', ['gccdev@cgtscorp.com'], None, None))
                thread_correo.start()
                """

def reparacion_prorroga():
    """
        Si una solicitud se encuentra en reparacion o prorroga y ha culminado los 30 dias
        correspondientes. Se devolvera el flujo al coordinador_ct
    """
    solicitudes = Solicitud.objects.filter(
        Q(estatus__abreviacion='ER') | Q(estatus__abreviacion='EP')
    )
    hoy = datetime.datetime.now()
    for s in solicitudes:
        fecha_ultima_modificacion = s.fecha_modificacion_estado.replace(tzinfo=None)
        dias = diasLaborales(fechaInicio=fecha_ultima_modificacion,fechaFin=hoy)
        if dias >= s.dias_prorroga:
            estatus=Estatus.objects.get(abreviacion='SEAR')
            coordinador_ct=Asignacion.objects.get(solicitud=s, 
                funcionario__tiporol__nombre='coordinador_ct', asignacion_habilitada=True
            ).funcionario
            notificacion = Notificacion(
                emisor=s.pst.user,
                receptor=coordinador_ct.user,
                solicitud=s,
                estatus_actual=estatus
            )
            notificacion.save()
            s.estatus=estatus
            s.funcionario = coordinador_ct
            s.fecha_modificacion_estado=datetime.datetime.now()
            s.save()

            #<--- Envio de Correo --->
            direc = Registro_Direccion.objects.filter(pst=solicitud.pst).first()
            direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                +str(direc.codigo_postal)
            #licencia = dt_licencia(solicitud.pst, solicitud.sucursal)

            #<--- Envio de Correo --->
            htmly = get_template('correo/cron_reparacion_prorroga.html')
            text_plain = get_template('correo/cron_reparacion_prorroga.txt')

            context = Context({
                'razon_social': solicitud.pst.razon_social,
                'direccion': direccionPST,
                'contacto': RepresentanteContacto.objects.filter(pst=solicitud.pst).first()
             })

            html_content = htmly.render(context)
            text_content = text_plain.render(context)

            thread_correo = threading.Thread(
                name='thread_correo', 
                target=correo, 
                args=(
                    u'[MINTUR] Culminación de Proceso de Reparación', 
                    html_content, 
                    text_content, 
                    'gccdev@cgtscorp.com', 
                    ['gccdev@cgtscorp.com'], 
                    None, 
                    None
                )
            )                
            thread_correo.start()
            """
            lic = LicenciaAsignada.objects.filter(usuario_pst=s.pst.user, 
                sucursal_id=s.sucursal_id
            ).first()
            if lic:
                dprint(lic=lic)
                if s.sucursal_id:
                    licencia = lic.numero_licencia
                    suc= s.pst.denominacion_comercial
                    direccion = "%s, %s, %s, %s" %(s.sucursal.urbanizacion, s.sucursal.avenida_calle, s.sucursal.edificio, s.sucursal.oficina_apartamento)
                else:
                    licencia = lic.numero_licencia
                    suc= "Sede Principal"
                    direccs = Registro_Direccion.objects.get(pst=s.pst)
                    direccion = "%s, %s, %s, %s, %s, %s" %(direccs.estado.estado, direccs.municipio.municipio, direccs.urbanizacion, direccs.avenida_calle, direccs.edificio, direccs.oficina_apartamento)
            
            #<!---- Envio de Correo ---->
            htmly = get_template('correo/cron_reparacion_prorroga.html')
            text_plain = get_template('correo/cron_reparacion_prorroga.txt')

            context = Context({
             'licencia': licencia,
             'nombre_pst': s.pst.nombres+" "+s.pst.apellidos,
             'nombre_establecimiento': suc,
             'direccion': direccion
             })

            html_content = htmly.render(context)
            text_content = text_plain.render(context)
            
            Busqueda de correo en parametros de configuracion
            try:
                corr = ParametroConfiguracion.objects.get(
                        clave="correo_interno"
                        )
            except corr.DoesNotExist:
                raise e
            corrs = str(corr.valor)
            
            thread_correo = threading.Thread(name='thread_correo', target=correo, args=(u'[MINTUR] Culminación de Proceso de Reparación', html_content, text_content, 'gccdev@cgtscorp.com', ['gccdev@cgtscorp.com'], None, None))
            thread_correo.start()
            """


def renovacion():
    """
        A los 4 años de la aprobacion de una solicitud de categorizacion, se enviara un correo
        y debera renovar el proceso de categorizacion
    """
    solicitudes = Solicitud.objects.filter(
        Q(estatus__abreviacion='Ap') | Q(estatus__abreviacion='SN')
        | Q(estatus__abreviacion='NPI')
    )
    hoy = datetime.datetime.now()
    for s in solicitudes:
        fecha_ultima_modificacion = s.fecha_modificacion_estado.replace(tzinfo=None)
        dias = (hoy - fecha_ultima_modificacion).days
        tiempoRenovacion=365*4
        print dias
        if dias>=tiempoRenovacion and s.renovar==False:

            s.renovar=True
            s.save()

            #<----- Envio de Correo ----->
            direc = Registro_Direccion.objects.filter(pst=s.pst).first()
            direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                +str(direc.codigo_postal)
            #licencia = dt_licencia(solicitud.pst, solicitud.sucursal)

            #<--- Envio de Correo --->
            htmly = get_template('correo/iniciar_renovacion.html')
            text_plain = get_template('correo/iniciar_renovacion.txt')

            context = Context({
                'razon_social': s.pst.razon_social,
                'direccion': direccionPST,
                'contacto': RepresentanteContacto.objects.filter(pst=s.pst).first()
             })

            html_content = htmly.render(context)
            text_content = text_plain.render(context)

            thread_correo = threading.Thread(
                name='thread_correo', 
                target=correo, 
                args=(
                    u'[MINTUR] Proceso de Renovación de Categorización', 
                    html_content, 
                    text_content, 
                    'gccdev@cgtscorp.com', 
                    ['gccdev@cgtscorp.com'], 
                    None, 
                    None
                )
            )                
            thread_correo.start()
            """
            lic = LicenciaAsignada.objects.filter(usuario_pst=s.pst.user, 
                sucursal_id=s.sucursal_id
            ).first()
            if lic:
                if s.sucursal_id:
                    licencia = lic.numero_licencia
                    suc= s.pst.denominacion_comercial
                    direccion = "%s, %s, %s, %s" %(s.sucursal.urbanizacion, s.sucursal.avenida_calle, s.sucursal.edificio, s.sucursal.oficina_apartamento)
                else:
                    licencia = lic.numero_licencia
                    suc= "Sede Principal"
                    direccs = Registro_Direccion.objects.get(pst=s.pst)
                    direccion = "%s, %s, %s, %s, %s, %s" %(direccs.estado.estado, direccs.municipio.municipio, direccs.urbanizacion, direccs.avenida_calle, direccs.edificio, direccs.oficina_apartamento)
            
            #<--- Envio de Correo --->
            htmly = get_template('correo/iniciar_renovacion.html')
            text_plain = get_template('correo/iniciar_renovacion.txt')

            context = Context({
             'licencia': licencia,
             'nombre_pst': s.pst.nombres+" "+s.pst.apellidos,
             'nombre_establecimiento': suc,
             'direccion': direccion
             })

            html_content = htmly.render(context)
            text_content =text_plain.render(context)
            
            Busqueda de correo en parametros de configuracion
            try:
                corr = ParametroConfiguracion.objects.get(
                        clave="correo_interno"
                        )
            except corr.DoesNotExist:
                raise e
            corrs = str(corr.valor)
    

            thread_correo = threading.Thread(name='thread_correo', target=correo, args=(u'[MINTUR] Proceso de Renovación de Categorización', html_content, text_content, 'gccdev@cgtscorp.com', ['gccdev@cgtscorp.com'], None, None))
            thread_correo.start()
            """

def folio():
    """
        Si a los 2 meses de haber subido el ultimo folio al libro de sugerencia y reclamos
        se enviara un correo
    """
    dates = datetime.datetime.now()

    if dates.month <= 2:
        month = 10 + dates.month
        year = dates.year - 1
    else:
        month = dates.month - 2
        year = dates.year

    dates_def = datetime.datetime(year, month,dates.day)

    #folios = Folio.objects.filter(fecha_carga__lte=dates_def)
    folios = Folio.objects.filter(
        fecha_carga__lte=dates_def,
        ).order_by(
        'lsr_fisico__sucursal', 
        '-fecha_carga').distinct(
            'lsr_fisico__sucursal')

    sol_libro = SolicitudLibro.objects.filter(fecha_culminacion__lte=dates_def)

    for f in folios:
        condition=False
        if f.fecha_notificacion:
            datesNoWeeks = dates - datetime.timedelta(weeks=2)
            if f.fecha_notificacion.replace(tzinfo=None) < datesNoWeeks:
                print "Se envio el correo"
                f.fecha_notificacion = dates
                f.save()
                condition=True
        else:
            print "Se envio el correo, por primera vez"
            f.fecha_notificacion = dates
            f.save()
            condition=True

        if condition == True:
            #<---- Envio de Correo ---->
            direc = Registro_Direccion.objects.filter(pst=f.lsr_fisico.pst).first()
            direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                +str(direc.codigo_postal)
            licencia = dt_licencia(f.lsr_fisico.pst, f.lsr_fisico.sucursal)

            #<--- Envio de Correo --->
            htmly = get_template('correo/cron_folio.html')
            text_plain = get_template('correo/cron_folio.txt')

            context = Context({
                'razon_social': f.lsr_fisico.pst.razon_social,
                'direccion': direccionPST,
                'contacto': RepresentanteContacto.objects.filter(pst=f.lsr_fisico.pst).first(),
                'numero_lsr': f.lsr_fisico.identificador,
                'resolucion':EspecificacionLegal.objects.filter(
                    tipo_especificacion__abreviacion='R', 
                    documento_asociado__abreviacion='CCF', 
                    tipo_pst=licencia.tipo_licenciaid.padre
                ).first(),
                'gaceta':EspecificacionLegal.objects.filter(
                    tipo_especificacion__abreviacion='GO', 
                    documento_asociado__abreviacion='CCF', 
                    tipo_pst=licencia.tipo_licenciaid.padre
                ).first(),
                'articulo':EspecificacionLegal.objects.filter(
                    tipo_especificacion__abreviacion='A', 
                    documento_asociado__abreviacion='CCF', 
                    tipo_pst=licencia.tipo_licenciaid.padre
                )
            })
            html_content = htmly.render(context)
            text_content = text_plain.render(context)
                
            thread_correo = threading.Thread(
                name='thread_correo', 
                target=correo, 
                args=(
                    u'[MINTUR] Recordatorio de Carga de Folio', 
                    html_content, 
                    text_content, 
                    'gccdev@cgtscorp.com', 
                    ['gccdev@cgtscorp.com'], 
                    None, 
                    None
                )
            )         
            thread_correo.start()
            """
            lic = LicenciaAsignada.objects.filter(usuario_pst=f.lsr_fisico.pst.user, 
                sucursal_id=f.lsr_fisico.sucursal_id
            ).first()
            if lic:
                dprint(lic=lic)
                if f.lsr_fisico.sucursal_id:
                    licencia = lic.numero_licencia
                    suc= f.lsr_fisico.pst.denominacion_comercial
                    direccion = "%s, %s, %s, %s" %(f.lsr_fisico.sucursal.urbanizacion, f.lsr_fisico.sucursal.avenida_calle, f.lsr_fisico.sucursal.edificio, f.lsr_fisico.sucursal.oficina_apartamento)
                else:
                    licencia = lic.numero_licencia
                    suc= 'Sede Principal'
                    direccs = Registro_Direccion.objects.get(pst=f.lsr_fisico.pst)
                    direccion = "%s, %s, %s, %s, %s, %s" %(direccs.estado.estado, direccs.municipio.municipio, direccs.urbanizacion, direccs.avenida_calle, direccs.edificio, direccs.oficina_apartamento)
            
            #<--- Envio de Correo --->
            htmly = get_template('correo/cron_folio.html')
            text_plain = get_template('correo/cron_folio.txt')

            context = Context({
             'nombre_pst': f.lsr_fisico.pst.nombres+" "+f.lsr_fisico.pst.apellidos,
             'nombre_establecimiento': suc,
             'direccion': direccion
             })

            html_content = htmly.render(context)
            text_content = text_plain.render(context)
            
            Busqueda de correo en parametros de configuracion
            try:
                corr = ParametroConfiguracion.objects.get(
                        clave="correo_interno"
                        )
            except corr.DoesNotExist:
                raise e
            corrs = str(corr.valor)
            

            thread_correo = threading.Thread(name='thread_correo', target=correo, args=(u'[MINTUR] Recordatorio de Carga de Folio', html_content, text_content, 'gccdev@cgtscorp.com', ['gccdev@cgtscorp.com'], None, None))
            thread_correo.start()
            """
        sol_libro = sol_libro.exclude(id = f.lsr_fisico.solicitud_libro.id)

        for s in sol_libro:
            #Envio de Correos
            direc = Registro_Direccion.objects.filter(pst=s.pst).first()
            direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                +str(direc.codigo_postal)
            licencia = dt_licencia(s.pst, s.sucursal)

            #<--- Envio de Correo --->
            htmly = get_template('correo/cron_folio.html')
            text_plain = get_template('correo/cron_folio.txt')

            context = Context({
                'razon_social': s.pst.razon_social,
                'direccion': direccionPST,
                'contacto': RepresentanteContacto.objects.filter(pst=s.pst).first(),
                'numero_lsr': LsrFisico.objects.get(solicitud_libro=s).identificador,
                'resolucion':EspecificacionLegal.objects.filter(
                    tipo_especificacion__abreviacion='R', 
                    documento_asociado__abreviacion='CCF', 
                    tipo_pst=licencia.tipo_licenciaid.padre
                ).first(),
                'gaceta':EspecificacionLegal.objects.filter(
                    tipo_especificacion__abreviacion='GO', 
                    documento_asociado__abreviacion='CCF', 
                    tipo_pst=licencia.tipo_licenciaid.padre
                ).first(),
                'articulo':EspecificacionLegal.objects.filter(
                    tipo_especificacion__abreviacion='A', 
                    documento_asociado__abreviacion='CCF', 
                    tipo_pst=licencia.tipo_licenciaid.padre
                )
            })
            html_content = htmly.render(context)
            text_content = text_plain.render(context)
                
            thread_correo = threading.Thread(
                name='thread_correo', 
                target=correo, 
                args=(
                    u'[MINTUR] Recordatorio de Carga de Folio', 
                    html_content, 
                    text_content, 
                    'gccdev@cgtscorp.com', 
                    ['gccdev@cgtscorp.com'], 
                    None, 
                    None
                )
            )         
            thread_correo.start()



def entradas_no_respondidas():
    """
        Si una entrada de la encuesta no se encuentra respondida a los 2 a 4 dias, se envia un correo
    """
    respuestas = RespuestaLsr.objects.all()
    dprint(respuestas)
    r = [e.entrada_id for e in respuestas]
    dprint(r)
    entradas = Entrada.objects.filter(
        Q(tipo_comentario__abreviacion='S') | Q(tipo_comentario__abreviacion='R')
    ).exclude(id__in=r)
    hoy = datetime.datetime.now()
    dprint(entradas)
    for e in entradas:
        fecha_entrada = e.fecha_entrada.replace(tzinfo=None)
        dias = (hoy - fecha_entrada).days
        if dias>=2 and dias<=4:
            #<---- Envio de Correo ---->
            direc = Registro_Direccion.objects.filter(pst=e.lsr.pst).first()
            direccionPST = "Estado " + direc.estado.estado + ", Municipio "\
                +direc.municipio.municipio + ", Parroquia " + direc.parroquia.parroquia\
                + ", " + direc.urbanizacion + ", " + direc.avenida_calle+", "\
                +direc.edificio+", "+ direc.oficina_apartamento+", Codigo postal: "\
                +str(direc.codigo_postal)
            licencia = dt_licencia(e.lsr.pst, e.lsr.sucursal)

            #<--- Envio de Correo --->
            htmly = get_template('correo/cron_entradas_respondidas.html')
            text_plain = get_template('correo/cron_entradas_respondidas.txt')

            context = Context({
                'razon_social': e.lsr.pst.razon_social,
                'direccion': direccionPST,
                'contacto': RepresentanteContacto.objects.filter(pst=e.lsr.pst).first(),
                'numero_lsr': f.lsr_fisico.identificador,
                'resolucion': EspecificacionLegal.objects.filter(
                    tipo_especificacion__abreviacion='R', 
                    documento_asociado__abreviacion='CESR', 
                    tipo_pst=licencia.tipo_licenciaid.padre
                ).first(),
                'gaceta': EspecificacionLegal.objects.filter(
                    tipo_especificacion__abreviacion='GO', 
                    documento_asociado__abreviacion='CESR', 
                    tipo_pst=licencia.tipo_licenciaid.padre
                ).first(),
                'articulo': EspecificacionLegal.objects.filter(
                    tipo_especificacion__abreviacion='A', 
                    documento_asociado__abreviacion='CESR', 
                    tipo_pst=licencia.tipo_licenciaid.padre
                ).first()
             })

            html_content = htmly.render(context)
            text_content = text_plain.render(context)

            thread_correo = threading.Thread(
                name='thread_correo', 
                target=correo, 
                args=(
                    u'[MINTUR] Recordatorio de Respuestas a Entradas de Turistas', 
                    html_content, 
                    text_content, 
                    'gccdev@cgtscorp.com', 
                    ['gccdev@cgtscorp.com'], 
                    None, 
                    None
                )
            )                
            thread_correo.start()
            """
            lic = LicenciaAsignada.objects.filter(usuario_pst=e.lsr.pst.user, 
                sucursal_id=e.lsr.sucursal_id
            ).first()
            if lic:
                dprint(lic=lic)
                if e.lsr.sucursal_id:
                    licencia = lic.numero_licencia
                    suc=e.lsr.pst.denominacion_comercial
                    direccion = "%s, %s, %s, %s" %(e.lsr.sucursal.urbanizacion, e.lsr.sucursal.avenida_calle, e.lsr.sucursal.edificio, e.lsr.sucursal.oficina_apartamento)
                else:
                    licencia = lic.numero_licencia
                    suc= 'Sede Principal'
                    direccs = Registro_Direccion.objects.get(pst=e.lsr.pst)
                    direccion = "%s, %s, %s, %s, %s, %s" %(direccs.estado.estado, direccs.municipio.municipio, direccs.urbanizacion, direccs.avenida_calle, direccs.edificio, direccs.oficina_apartamento)

            #<--- Envio de Correo --->
            htmly = get_template('correo/cron_entradas_respondidas.html')
            text_plain = get_template('correo/cron_entradas_respondidas.txt')

            context = Context({
             'nombre_pst': e.lsr.pst.nombres+" "+e.lsr.pst.apellidos,
             'nombre_establecimiento': suc,
             'direccion': direccion
             })

            html_content = htmly.render(context)
            text_content = text_plain.render(context)
            
            Busqueda de correo en parametros de configuracion
            try:
                corr = ParametroConfiguracion.objects.get(
                        clave="correo_interno"
                        )
            except corr.DoesNotExist:
                raise e
            corrs = str(corr.valor)
            
            thread_correo = threading.Thread(name='thread_correo', target=correo, args=(u'[MINTUR] Recordatorio de Respuestas a Entradas de Turistas', html_content, text_content, 'gccdev@gtscorp.com', ['gccdev@cgtscorp.com'], None, None))
            thread_correo.start()
            """