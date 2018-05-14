from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, render_to_response
from django.views.generic import View
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from registro.models import Pst, PERSONA_JURIDICA, PERSONA_NATURAL, Sucursales
from django.core.urlresolvers import reverse_lazy , reverse
from apps.licencias.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.utils import timezone
from django.core import serializers
from apps.licencias.models import ArchivoRespuesta
import datetime

class SolicitudesPst(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(SolicitudesPst, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        usuario = request.user

        if usuario.is_pst():
            pst = usuario.pst_set.get()  # Obtenemos el registro PST
            natural = False
            juridica = False
            es_natural_con_firma_personal = False
            emprendedor = False
            if pst.tipo_figura == PERSONA_NATURAL:
                if pst.emprendedor:
                    emprendedor = True
                else:
                    natural = True
                if pst.tiene_firma_personal:
                    es_natural_con_firma_personal = True
            else:
                juridica = True
            #SE VERIFICA QUE EL USUARIO TENGA RTN
            if pst.rtn is not None:
                # print "*************************************************************"
                # print request.user.id
                licencias = TipoLicencia.objects.filter(padre=None) 
                s_licencias_list = SolicitudLicencia.objects.filter(usuario_pst_id=request.user.id)
                s_sucursal=Sucursales.objects.filter(pst_id=request.user.id)
                paginator = Paginator(s_licencias_list,10)

                page = request.GET.get('page')
                try:
                    s_licencias = paginator.page(page)
                except PageNotAnInteger:
                    s_licencias = paginator.page(1)
                except EmptyPage:
                    s_licencias = paginator.page(paginator.num_pages)




                context = {
                    'pst': pst,
                    'usuario': request.user,
                    'natural': natural,
                    'es_natural_con_firma_personal': es_natural_con_firma_personal,
                    'juridica': juridica,
                    'emprendedor': emprendedor,
                    's_licencias': s_licencias,
                    's_sucursal': s_sucursal,
                    'licencias' : licencias,
                }
                return render(request, 'licencias/pst/solicitudes.html', context)
            else:
                context = {
                    'pst': pst,
                    'usuario': request.user,
                    'natural': natural,
                    'es_natural_con_firma_personal': es_natural_con_firma_personal,
                    'juridica': juridica,
                    'emprendedor': emprendedor,
                    'nuevo_registro': (pst.estatus == 1),
                }
                return render(request, 'home/home_pst.html', context)

class LicenciasAsignadas(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(LicenciasAsignadas, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        usuario = request.user

        if usuario.is_pst():
            pst = usuario.pst_set.get()  # Obtenemos el registro PST
            natural = False
            juridica = False
            es_natural_con_firma_personal = False
            emprendedor = False
            if pst.tipo_figura == PERSONA_NATURAL:
                if pst.emprendedor:
                    emprendedor = True
                else:
                    natural = True
                if pst.tiene_firma_personal:
                    es_natural_con_firma_personal = True
            else:
                juridica = True
            #SE VERIFICA QUE EL USUARIO TENGA RTN
            if pst.rtn is not None:
                # print "*************************************************************"
                # print request.user.id
                licencias = TipoLicencia.objects.filter(padre=None) 
                s_licencias_list = LicenciaAsignada.objects.filter(
                    usuario_pst=request.user.id).order_by('tipo_licenciaid')
                s_sucursal=Sucursales.objects.filter(pst_id=request.user.id)
                paginator = Paginator(s_licencias_list,10)

                page = request.GET.get('page')
                try:
                    s_licencias = paginator.page(page)
                except PageNotAnInteger:
                    s_licencias = paginator.page(1)
                except EmptyPage:
                    s_licencias = paginator.page(paginator.num_pages)




                context = {
                    'pst': pst,
                    'usuario': request.user,
                    'natural': natural,
                    'es_natural_con_firma_personal': es_natural_con_firma_personal,
                    'juridica': juridica,
                    'emprendedor': emprendedor,
                    's_licencias': s_licencias,
                    'today': timezone.now(),
                    'licencias' : licencias,
                }
                return render(request, 'licencias/pst/licencias_asignadas.html', context)
            else:
                context = {
                    'pst': pst,
                    'usuario': request.user,
                    'natural': natural,
                    'es_natural_con_firma_personal': es_natural_con_firma_personal,
                    'juridica': juridica,
                    'emprendedor': emprendedor,
                    'nuevo_registro': (pst.estatus == 1),
                }
                return render(request, 'home/home_pst.html', context)


class AjaxObtenerTipoLicencias(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(AjaxObtenerTipoLicencias, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        n_id = kwargs['id_select']
        licencias = TipoLicencia.objects.filter(padre=TipoLicencia.objects.filter(codigo=n_id).values('id')).order_by('id')
        sublicencias = serializers.serialize("json", licencias, fields=('id, nombre, codigo'))
           
        return HttpResponse(sublicencias,content_type="application/json"
        )
class AjaxObtenerSucursales(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(AjaxObtenerSucursales, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        n_id = kwargs['id_select']
        tip_id = kwargs['id_otros']
        #sucursal=Sucursales.objects.filter(pst_id=n_id)

        sucursal=SolicitudLicencia.objects.filter(
            usuario_pst_id=n_id,
            tipo_licenciaid__codigo__in= [tip_id],
            estatus_solicitudid__codigo__in=['EST_POR_CERTIFICAR',
            'EST_PREAPROB_D',"EST_PREAPROB_V","EST_PREAPROB_M",
            "EST_OBSER_ANALIS","EST_OBSER_DIRECTOR","EST_OBSER_VICEM","EST_OBSER_MINIST","EST_APROB"])
        principal=sucursal.filter(usuario_pst_id=n_id,
            tipo_licenciaid__codigo__in= [tip_id],
            estatus_solicitudid__codigo__in=['EST_POR_CERTIFICAR',
            'EST_PREAPROB_D',"EST_PREAPROB_V","EST_PREAPROB_M",
            "EST_OBSER_ANALIS","EST_OBSER_DIRECTOR","EST_OBSER_VICEM","EST_OBSER_MINIST","EST_APROB"],
            sucursal_id__isnull=True)
        sucursal=sucursal.exclude(sucursal_id__isnull=True)
        solicitudexp=Sucursales.objects.exclude(id__in= sucursal.values_list('sucursal_id')).order_by('id');
        solicitudexp=solicitudexp.filter(pst_id=n_id)
        p_sucursal = serializers.serialize("json", solicitudexp, fields=('id, nombre'))
        return HttpResponse(p_sucursal,content_type="application/json")

class AjaxObtenerPrincipal(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(AjaxObtenerPrincipal, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        n_id = kwargs['id_select']
        tip_id = kwargs['id_otros']
        #sucursal=Sucursales.objects.filter(pst_id=n_id)

        principal=SolicitudLicencia.objects.filter(usuario_pst_id=n_id,
            tipo_licenciaid__codigo__in= [tip_id],
            estatus_solicitudid__codigo__in=['EST_POR_CERTIFICAR',
            'EST_PREAPROB_D',"EST_PREAPROB_V","EST_PREAPROB_M",
            "EST_OBSER_ANALIS","EST_OBSER_DIRECTOR","EST_OBSER_VICEM","EST_OBSER_MINIST","EST_APROB"],
            sucursal_id__isnull=True)
        p_sucursal = serializers.serialize("json", principal, fields=('id'))
        return HttpResponse(p_sucursal,content_type="application/json")


class FormularioLicencia(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(FormularioLicencia, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):

        formulario= kwargs['id_select']

        usuario = request.user

        if usuario.is_pst():
            pst = usuario.pst_set.get()  # Obtenemos el registro PST
            natural = False
            juridica = False
            es_natural_con_firma_personal = False
            emprendedor = False
            if pst.tipo_figura == PERSONA_NATURAL:
                if pst.emprendedor:
                    emprendedor = True
                else:
                    natural = True
                if pst.tiene_firma_personal:
                    es_natural_con_firma_personal = True
            else:
                juridica = True
            #SE VERIFICA QUE EL USUARIO TENGA RTN
            if pst.rtn is not None:


                context = {
                    'pst': pst,
                    'usuario': request.user,
                    'natural': natural,
                    'es_natural_con_firma_personal': es_natural_con_firma_personal,
                    'juridica': juridica,
                    'emprendedor': emprendedor,
                }

                return render(request, 'licencias/aet/aet_solicitud.html', context)
                



        # return HttpResponse("Forulario elegido"+ kwargs['id_select'] )
        
class SolicitudLicencias(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(SolicitudLicencias, self).dispatch(*args, **kwargs)
    def get(self, request, *args, **kwargs):
        tipo= request.session.pop('tipo')
        subtipo= request.session.pop('subtipo')
        sucur= request.session.pop('sucursales') 
        request.session.get('tipo')
        request.session['tipo']=tipo
        request.session.get('subtipo')
        request.session['subtipo']=subtipo
        request.session.get('sucursales')
        request.session['sucursales']=sucur
        if sucur == '0':
            sucur_nomb='0'
        else: 
            sucur_nomb= Sucursales.objects.get(id=sucur).nombre

        if subtipo is None:
            licencias = TipoLicencia.objects.get(codigo=tipo).url
            nombre_subtipo="Prestadores de Servicios "

        else:
            licencias = TipoLicencia.objects.get(codigo=subtipo).url
            nombre_subtipo=TipoLicencia.objects.get(codigo=subtipo).nombre


        usuario = request.user

        if usuario.is_pst():
            pst = usuario.pst_set.get()  # Obtenemos el registro PST
            natural = False
            juridica = False
            es_natural_con_firma_personal = False
            emprendedor = False
            if pst.tipo_figura == PERSONA_NATURAL:
                if pst.emprendedor:
                    emprendedor = True
                else:
                    natural = True
                if pst.tiene_firma_personal:
                    es_natural_con_firma_personal = True
            else:
                juridica = True
            #SE VERIFICA QUE EL USUARIO TENGA RTN
            if pst.rtn is not None:
                context = {
                    'pst': pst,
                    'usuario': request.user,
                    'natural': natural,
                    'es_natural_con_firma_personal': es_natural_con_firma_personal,
                    'juridica': juridica,
                    'tipo_id': tipo,
                    'subtipo_id': subtipo,
                    'sucursal_id': sucur,
                    'sucursal_nombre': sucur_nomb,
                    'subtipo_nombre': nombre_subtipo,
                    'emprendedor': emprendedor,
                }
                print licencias
                aux=licencias
                if tipo == 'LIC_AGEN_T':
                    if sucur =='0':
                        return render(request, aux+'.html', context)
                    else:
                        return render(request, aux+'_sucursal.html',
                         context)
                else:
                    return render(request, aux, context)
        
    def post(self, request, *args, **kwargs):
        vars(request.POST)

        tipo= request.POST.get('tipo_licencia',None)
        subtipo= request.POST.get('sub_tipo_licencia',None)
        sucur= request.POST.get('sucursal',None)  
        request.session.get('tipo')
        request.session['tipo']=tipo
        request.session.get('subtipo')
        request.session['subtipo']=subtipo
        request.session.get('sucursales')
        request.session['sucursales']=sucur

        if sucur == '0':
            sucur_nomb='0'
        else: 
            sucur_nomb= Sucursales.objects.get(id=sucur).nombre

        if subtipo is None:
            licencias = TipoLicencia.objects.get(codigo=tipo).url
            nombre_subtipo="Prestadores de Servicios "

        else:
            licencias = TipoLicencia.objects.get(codigo=subtipo).url
            nombre_subtipo=TipoLicencia.objects.get(codigo=subtipo).nombre


        usuario = request.user

        if usuario.is_pst():
            pst = usuario.pst_set.get()  # Obtenemos el registro PST
            natural = False
            juridica = False
            es_natural_con_firma_personal = False
            emprendedor = False
            if pst.tipo_figura == PERSONA_NATURAL:
                if pst.emprendedor:
                    emprendedor = True
                else:
                    natural = True
                if pst.tiene_firma_personal:
                    es_natural_con_firma_personal = True
            else:
                juridica = True
            #SE VERIFICA QUE EL USUARIO TENGA RTN
            if pst.rtn is not None:
                context = {
                    'pst': pst,
                    'usuario': request.user,
                    'natural': natural,
                    'es_natural_con_firma_personal': es_natural_con_firma_personal,
                    'juridica': juridica,
                    'tipo_id': tipo,
                    'subtipo_id': subtipo,
                    'sucursal_id': sucur,
                    'sucursal_nombre': sucur_nomb,
                    'subtipo_nombre': nombre_subtipo,
                    'emprendedor': emprendedor,
                }
                print licencias
                aux=licencias
                if tipo == 'LIC_AGEN_T':
                    if sucur =='0':
                        return render(request, aux+'.html', context)
                    else:
                        return render(request, aux+'_sucursal.html',
                         context)
                else:
                    return render(request, aux, context)
class SolicitudesOtorgadas(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(SolicitudesOtorgadas, self).dispatch(*args, **kwargs)
    def get(self, request, *args, **kwargs):

        usuario = request.user
        solicitudes = LicenciaAsignada.objects.all().order_by('usuario_pst').values_list('usuario_pst').distinct()
        pst = []
        for s in solicitudes:
            i = 0
            aux = 0
            for p in pst:
                if pst[i] == Pst.objects.get(pk=s[i]):
                    aux=1
                    break
                i = i+1
            if aux == 0:
                pst.append(Pst.objects.get(pk=s[i]))
        solicitudes = LicenciaAsignada.objects.all().order_by('estatus')
        paginator = Paginator(solicitudes,10)

        page = request.GET.get('page')
        try:
            s_licencias = paginator.page(page)
        except PageNotAnInteger:
            s_licencias = paginator.page(1)
        except EmptyPage:
            s_licencias = paginator.page(paginator.num_pages)


        context = {
            'solicitudes': solicitudes,
            'pst': pst,
            's_licencias': s_licencias,
        }

        return render(request, 'licencias/funcionario/licencias_otorgadas.html', context)

class AjaxObtenerBusqueda(View):
    @method_decorator(login_required(login_url=reverse_lazy('cuentas_login')))
    def dispatch(self, *args, **kwargs):
        return super(AjaxObtenerBusqueda, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        n_id = kwargs['id_select']
        tip_id = kwargs['id_otros']
        #sucursal=Sucursales.objects.filter(pst_id=n_id)

        principal=SolicitudLicencia.objects.filter(usuario_pst_id=n_id,
            tipo_licenciaid__codigo__in= [tip_id],
            estatus_solicitudid__codigo__in=['EST_POR_CERTIFICAR',
            'EST_PREAPROB_D',"EST_PREAPROB_V","EST_PREAPROB_M",
            "EST_OBSER_ANALIS","EST_OBSER_DIRECTOR","EST_OBSER_VICEM","EST_OBSER_MINIST","EST_APROB"],
            sucursal_id__isnull=True)
        p_sucursal = serializers.serialize("json", principal, fields=('id'))
        return HttpResponse(p_sucursal,content_type="application/json")


class AgregarSolicitud(View):

    def get(self, request, *args, **kwargs):

        return HttpResponse()

    def post(self, request, *args, **kwargs):
        usuario = request.user
        tabla= request.POST.get('L_DAT_EMP',None)
        Datos= request.POST
        recaudosSolicitud= request.FILES

        print "*************"
        print(tabla)
        print "DATOS: "
        print Datos
        print "Recaudos: "
        print recaudosSolicitud
        print "TIPO_LICENCIA: "
        tipo_licencia = request.POST.get('tipo_id',None)
        print tipo_licencia
        print type(tipo_licencia)
        print "SUBTIPO_LICENCIA: "
        print request.POST.get('subtipo')
        subtipo_licencia = request.POST.get('subtipo_id',None)
        print subtipo_licencia


        if (subtipo_licencia != 'None' ):
            print "SUBTIPO NONE"
            licencia=TipoLicencia.objects.get(codigo=subtipo_licencia)
        else:
            print "EN TIPO LICENCIA"
            licencia=TipoLicencia.objects.get(codigo=tipo_licencia)
            print 'Hello'
     

        #SE CREA LA SOLICITUD NUEVA *********************************

        estatus = EstatusSolicitud.objects.get(codigo='EST_POR_CERTIFICAR')
        tipoSolicitud = TipoSolicitud.objects.get(codigo='T_SOL_N')

        solicitud=SolicitudLicencia(fecha_inicio=datetime.datetime.now(),tipo_licenciaid=licencia,
            estatus_solicitudid=estatus,tipo_solicitudid=tipoSolicitud,usuario_pst_id=usuario)
        solicitud.save()


        recaudosLicencia=licencia.recaudos.all()

        for r in recaudosLicencia:
            # print "-----------------Datos Recaudos--------------------"
            # print r.codigo       
            re=recaudosSolicitud.get(r.codigo,None)

            if (re is not None):
                # print re.name
                recaudo = ArchivoRecaudo(fecha_carga=datetime.datetime.now(),recaudoid=r,
                    solicitud_licenciaid=solicitud,ruta=re,nombre=re.name)
                recaudo.save()
            else:
                print "ESTA VACIO RECAUDO"
                return HttpResponse("DATOS INCOMPLETOS")


        # if(request.FILES['L_GEN_AUT_TUR'] is not None):
        #     print "FILE NOT NULL"
        #     instance = ArchivoRespuesta(ruta=tipo,nombre=tipo.name,fecha=datetime.datetime.now())
        #     instance.save()
        # else:
        #     print "FILE NULL"


        return HttpResponse()
        

class SolicitudesFuncionario(View):

    def get(self, request, *args, **kwargs):

        solicitudes = SolicitudLicencia.objects.filter(estatus_solicitudid__codigo='EST_POR_CERTIFICAR', analista_asignado=None)
    
        pst = []
        for s in solicitudes:
            i = 0
            aux = 0
            for p in pst:
                if pst[i] == Pst.objects.get(pk=s.usuario_pst_id.id):
                    aux=1
                i = i+1
            if aux == 0:
                pst.append(Pst.objects.get(pk=s.usuario_pst_id.id))
        
        paginator = Paginator(solicitudes,10)

        page = request.GET.get('page')
        try:
            s_licencias = paginator.page(page)
        except PageNotAnInteger:
            s_licencias = paginator.page(1)
        except EmptyPage:
            s_licencias = paginator.page(paginator.num_pages)


        context = {
            'solicitudes': solicitudes,
            'pst': pst,
            's_licencias': s_licencias,
        }

        return render(request, 'licencias/funcionario/solicitudes.html', context);

class SolicitudesAsignadas(View):

    def get(self, request, *args, **kwargs):

        usuario = request.user
        solicitudes = SolicitudLicencia.objects.filter(analista_asignado=usuario)
    
        pst = []
        for s in solicitudes:
            i = 0
            aux = 0
            for p in pst:
                if pst[i] == Pst.objects.get(pk=s.usuario_pst_id.id):
                    aux=1
                i = i+1
            if aux == 0:
                pst.append(Pst.objects.get(pk=s.usuario_pst_id.id))
        
        paginator = Paginator(solicitudes,10)

        page = request.GET.get('page')
        try:
            s_licencias = paginator.page(page)
        except PageNotAnInteger:
            s_licencias = paginator.page(1)
        except EmptyPage:
            s_licencias = paginator.page(paginator.num_pages)


        context = {
            'solicitudes': solicitudes,
            'pst': pst,
            's_licencias': s_licencias,
        }

        return render(request, 'licencias/funcionario/solicitudes_asignadas.html', context)

class AsignarSolicitud(View):

    def get(self, request, *args, **kwargs):

        s_id = kwargs['ide']
        usuario = request.user
        solicitud = SolicitudLicencia.objects.filter(id=s_id)

        solicitud.update(analista_asignado=usuario)

        return HttpResponse("Forulario elegido"+ s_id )