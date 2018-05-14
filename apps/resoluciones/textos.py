# -*- coding: utf-8 -*-

#helpers~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
NUMEROS = ['cero', 'uno', 'dos', 'tres', 'cuatro', 'cinco',
           'seis', 'siete', 'ocho', 'nueve', 'diez',
           'once', 'doce', 'trece', 'catorce', 'quince',
           'diez y seis', 'diez y siete', 'diez y ocho', 'diez y nueve', 'veinte',
           'veinte y uno', 'veinte y dos', 'veinte y tres', 'veinte y cuantro', 'veinte y cinco',
           'veinte y seis', 'veinte y siete', 'veinte y ocho', 'veinte y nueve', 'treinta',
           'treinta y uno']

def fecha_encabezado(fecha):
    return u'Caracas, {} ({}) de {} de {}'.format(
        NUMEROS[fecha.day], fecha.day, fecha.strftime('%B'), fecha.year)

def pretty_date(fecha):
    return u'a los {} ({}) días del mes de {} de {}'.format(
        NUMEROS[fecha.day], fecha.day, fecha.strftime('%B'), fecha.year)

def pretty_meses(dates):
    dates = list(set(dates))
    dates.sort()
    t = ''
    for i in dates[:-1]:
        if i.month == 12:
            t += i.strftime('%B')
            t += ' de %s y ' % i.year
        else:
            t += i.strftime('%B') + ', '
    t += dates[-1].strftime('%B') + ' de ' + str(dates[-1].year)
    return t

#MEMBRETE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def primer_parrafo(fecha, gerente):
    texto = u'''En la ciudad de Caracas, {}
            , en la sede del Instituto Nacional de Turismo (INATUR), ente adscrito
            al Ministerio del Poder Popular para el Turismo, de conformidad con lo
            establecido en los artículos 15, 16 y 18 del Decreto Nº 9.044 con Rango,
            Valor y Fuerza de la Ley Orgánica de Turismo de fecha quince (15) de junio
            de 2012, publicado en la Gaceta Oficial de la República Bolivariana de
            Venezuela Nº 6.079 Extraordinario de igual fecha reimpresa según Gaceta
            Oficial de la República Bolivariana de Venezuela N º 39.955, en fecha
            veintinueve (29) de junio de 2012; en concordancia con el establecido
            en los artículos 93, 121 (numerales 1 y 3) y 172 al 176 del Código Orgánico
            Tributario, publicado en la Gaceta Oficial Nº 37.305 de fecha diecisiete
            (17) de octubre de 2001, la funcionaria <b>{}</b>, titular de la cedula
            de identidad Nº <b>{}</b>, actuando en su carácter de Gerente de
            Recaudación y Fiscalización del Instituto Nacional de Turismo (INATUR),
            procediendo a realizar una verificación en sede administrativa en los
            sistemas y archivos de esta Gerencia de recaudación y Fiscalización,
            constato la siguiente situación tributaria del contribuyente, para los
            periodos de imposición comprendidos desde el mes de febrero 2010 hasta
            febrero 2014, ambos inclusive:'''.format(
                pretty_date(fecha),
                gerente.get_full_name().upper(),
                gerente.cedula)
    return texto

#SECCION UNO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def seccion_uno_inicio():
    texto = u'''Del análisis de la información contenida en los sistemas
            llevados por esta Administración Tributaria a los fines de
            control fiscal, así como, de la documentación suministrada
            por el contribuyente, se constataron los siguientes hechos:'''
    return texto

def segundo_parrafo(sancion_numero, resolucion, sancion, ilicitos):
    texto = u'%s. ' % unicode(sancion_numero)
    reincidencia = False
    if reincidencia:
        texto += u'''Que {}, a la cual estaba sujeto, para
            los periodos fiscales {}, actos de conformidad con lo establecido en el
            artículo {} del COT. Cabe acotar
            que de la revisión exhaustiva de los documentos que reposan en el
            expediente administrativo del contribuyente <b>“{}”</b>,
            se pudo constatar que el mismo, fue sancionado por la comisión de
            ilícitos de la misma índole, según Resoluciones
            N° [NUMERO DE RESOLUCION FECHA – ejem: R0000001, de fecha ocho (08) de enero del 2013],
            [SUCESIVAMENTE SE NOMBRAN LAS RESOLUCIONES SEPARADAS POR COMA], lo cual
            en conformidad con lo establecido en el artículo 82 del COT, constituye
            la agravante de responsabilidad penal de reincidencia que implica el
            incremento de la sanción aplicable en [VALOR UT DE INCREMENTO],
            por cada nueva infracción hasta un máximo de[VALOR MAXIMO DE UT DE LA MULTA],
            sanciones que conforme a lo dispuesto en el parágrafo primero del artículo
            94 del COT, cuando las multas estén expresadas en unidades tributarias (U.T)
            se utilizará el valor de la unidad tributaria que estuviere vigente para el
            momento del pago, tal como se muestra en el siguiente cuadro descriptivo:
            '''.format(sancion.descripcion.lower(),
                       pretty_meses([ilicito.periodo for ilicito in ilicitos]),
                       sancion.cot_articulo,
                       resolucion.pst.nombre_o_razon().upper())
    else:
        texto += u'''Que {}, a la cual estaba sujeto, para
            los periodos fiscales {}, actos de conformidad con lo
            establecido en el artículo {} del COT, tal como
            se muestra en el siguiente cuadro descriptivo:
            '''.format(sancion.descripcion.lower(),
                       pretty_meses([ilicito.periodo for ilicito in ilicitos]),
                       sancion.cot_articulo)
    return texto

#SECCION DOS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def seccion_dos_inicio():
    texto = u'''Los ilícitos tributarios constatados mediante la presente
            verificación configuran la modalidad de concurrencia, prevista
            en el articulo 81 del COT, motivo por el cual esta Administración
            Tributaria procede a aplicar la sanción más grave, aumentada con
            la mitad de las otras sanciones, de conformidad con el siguiente cuadro:
            '''
    return texto

#SECCION TRES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def seccion_tres_inicio(nombre):
    texto = u'''En atención a los ilícitos constatados e imputados y en virtud
            de los ajustes y sanciones aplicados, el contribuyente
            <b>“{}”</b>, deberá proceder al pago de los
            montos que se indican en el presente cuadro por los conceptos
            descritos y especificados en la presente resolución:
            '''.format(nombre.upper())
    return texto

def seccion_tres_fin(nombre):
    texto = u'''Se hace del conocimiento del contribuyente <b>“{}”</b>,
            que en caso de disconformidad con el contenido de la presente resolución, podrá
            interponer los recursos previstos en los artículos 242 y 259 del COT, en un plazo
            de veinticinco (25) días hábiles contados a partir de la notificación de esta
            resolución, de acuerdo a lo establecido en los artículos 244 y 261 del Código
            en comento. En caso de interponer Recurso Jerárquico deberá contar con la asistencia
            o representación de abogado o cualquier profesional afín al área tributaria,
            tal como l dispone el artículo 243 ejusdem.<br/>
            A los fines legales consiguientes, se emite la presente resolución en dos (2)
            ejemplares, de un mismo tenor y a un solo efecto, una de las cuales queda en poder
            del contribuyente, quien firma en señal de notificación.
            '''.format(nombre.upper())
    return texto


# INTERESES_MORATORIOS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def seccion_intereses_moratorios_inicio(periodos):
    texto = u'''En atención a la nueva verificación a los ilícitos constatados
            e imputados y de conformidad con los artículos 66 y 175 del Código
            Orgánico Tributario, esta Administración Tributaria procede a
            determinar los intereses moratorios aplicando la tasa de interés
            activa promedio ponderada de los 6 principales bancos comerciales y
            universales del país, incrementada en un 20%, correspondientes a
            los periodos pagados por el contribuyente fuera del lapso
            establecido, para los periodos <b>{}</b>, tal y como se
            detalla a continuación:
        '''.format(', '.join(periodos))

    return texto


#FOOTER ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def footer_texto(gerente):
    texto = u'''<b>{}</b><br/>
            Gerente (E) de Recaudación y Fiscalización<br/>
            Providencia P/Nº 037-13, de fecha 26-12-13<br/>
            Gaceta Oficial de la República Bolivariana de Venezuela <br/>
            Nº 40.324 de fecha 31-12-13<br/>
            Por Delegación según, Providencia P/Nº 001-14, de fecha 08-01-14<br/>
            Gaceta Oficial de la República Bolivariana de Venezuela <br/>
            Nº 40.332 de fecha 13-01-14<br/>
            '''.format(gerente.get_full_name())
    return texto

def footer_firma():
    texto = u'''CONTRIBUYENTE O RESPONSABLE<br/>
            Nombre:__________________________<br/>
            Cédula de Identidad Nº:______________<br/>
            Cargo:____________________________<br/>
            Fecha de Notificación:_______________<br/>
            Firma:____________________________<br/>
            Sello:'''
    return texto
