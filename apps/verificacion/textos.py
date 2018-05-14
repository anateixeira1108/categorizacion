# -*- coding: utf-8 -*-

from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER

#helpers~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
NUMEROS = ['cero', 'uno', 'dos', 'tres', 'cuatro', 'cinco',
           'seis', 'siete', 'ocho', 'nueve', 'diez',
           'once', 'doce', 'trece', 'catorce', 'quince',
           'diez y seis', 'diez y siete', 'diez y ocho', 'diez y nueve', 'veinte',
           'veinte y uno', 'veinte y dos', 'veinte y tres', 'veinte y cuantro', 'veinte y cinco',
           'veinte y seis', 'veinte y siete', 'veinte y ocho', 'veinte y nueve', 'treinta',
           'treinta y uno']

def rif_2_ci(rif):
    return '-'.join(rif.split('-')[:2])

def pretty_date(fecha):
    return u'{} ({}) días del mes de {} de {}'.format(NUMEROS[fecha.day], fecha.day, fecha.strftime('%B'), fecha.year)

def notificacion_fecha(fecha):
    if fecha == None:
        return '__/__/____'
    else:
        return fecha.strftime('%d/%m/%Y')

def pretty_observaciones(observaciones):
    if observaciones == 'ninguna' or observaciones == '':
        return ''.join(['_' for i in xrange(400)])
    else:
        return observaciones

#PROVIDENCIA~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def text_providencia(supervisor, funcionarios, apoyos):
    texto = u'''El Instituto Nacional de Turismo (INATUR), a través de la Gerencia de Recaudación y Fiscalización,
                en uso de las facultades previstas en los artículos 15, 16 y 18 del Decreto Nº 9.044 con Rango, Valor y Fuerza
                de Ley Orgánica de Turismo de fecha quince (15) de junio de 2012, publicado en la Gaceta Oficial de la República
                Bolivariana de Venezuela N° 6.079 Extraordinario, de igual fecha, reimpresa según Gaceta Oficial de la República
                Bolivariana de Venezuela N° 39.955, en fecha veintinueve (29) de junio 2012, en concordancia con los artículos 121
                , 124, 145, 169 y 172 al 176 del Código Orgánico Tributario, publicado en Gaceta Oficial Nº 37.305 del diecisiete (17)
                de octubre de 2001; autoriza '''
    if len(funcionarios) == 1:
        texto += u'''al(a) ciudadano(a) <b>{}</b>,  titular de la cédula de identidad <b>Nº {}</b>, y supervisor(a) <b>{}</b>,
                titular de la cédula de identidad <b>Nº {}</b>, funcionarios adscritos a la Gerencia, a verificar el cumplimiento de
                deberes formales a las declaraciones presentadas, a los fines de realizar los ajustes respectivos y liquidar las diferencias
                a que hubiere lugar, del sujeto pasivo arriba identificado, para los periodos  de imposición comprendidos  desde marzo 2010
                hasta marzo 2014, ambos inclusive, así como detectar y sancionar los posibles ilícitos formales cometidos.
                <br/><br/>
                '''.format(funcionarios[0].get_full_name().upper(), rif_2_ci(funcionarios[0].rif),
                                        supervisor.get_full_name().upper(), rif_2_ci(supervisor.rif))
    else:
        texto += u'''a los(as) ciudadanos(as) '''
        for funcionario in funcionarios:
            texto += u'''<b>{}</b>,  titular de la cédula de identidad <b>Nº {}</b>, '''.format(funcionario.get_full_name().upper(), rif_2_ci(funcionario.rif))
        texto += u'''y supervisor(a) <b>{}</b>,
                titular de la cédula de identidad <b>Nº {}</b>, funcionarios adscritos a la Gerencia, a verificar el cumplimiento de
                deberes formales a las declaraciones presentadas, a los fines de realizar los ajustes respectivos y liquidar las diferencias
                a que hubiere lugar, del sujeto pasivo arriba identificado, para los periodos  de imposición comprendidos  desde marzo 2010
                hasta marzo 2014, ambos inclusive, así como detectar y sancionar los posibles ilícitos formales cometidos.
                <br/><br/>'''.format(supervisor.get_full_name().upper(), rif_2_ci(supervisor.rif))
    if apoyos:
        if len(apoyos) == 1:
            texto += u'''Así mismo, se designa al(a) funcionario(a) <b>{}</b>,  titular de la cédula de identidad <b>Nº {}</b>,
                    para prestar apoyo en la ejecución del presente procedimiento.
                    <br/><br/>'''.format(apoyos[0].get_full_name().upper(), rif_2_ci(apoyos[0].rif))
        else:
            texto += u'''Así mismo, se designan los funcionarios(as):'''
            for apoyo in apoyos:
                texto += u' <b>{}</b> titular de la cédula de identidad <b>Nº {}</b>,'.format(apoyo.get_full_name().upper(), rif_2_ci(apoyo.rif))
            texto += u'''para prestar apoyo en la ejecución del presente procedimiento.
                        <br/><br/>'''
    texto += u'''A los fines legales que pudieran corresponder, se emite la presente Providencia Administrativa en tres (03) ejemplares
                de un mismo tenor y a un solo efecto, uno de los cuales queda en poder del sujeto pasivo quien firma en señal de
                notificación.'''
    return texto

def gaceta(pdf, text_end, gerente):
    p = ParagraphStyle('test')
    p.textColor = 'black'
    p.alignment = TA_CENTER
    p.fontSize = 8
    p.leading = 9
    para = Paragraph(gaceta_text(gerente), p)
    para.wrapOn(pdf, 300, 50)
    para.drawOn(pdf, 155, text_end - 10 - para.height)
    return text_end - 10 - para.height

def gaceta_text(gerente):
    GACETA = u'''<b><font size=12>{}</font></b> <br/>
            Gerente (E) de Recaudación y Fiscalización <br/>
            Providencia P/Nº 037-13, de fecha 26-12-13 <br/>
            Gaceta Oficial de la República Bolivariana de Venezuela <br/>
            Nº 40.324 de fecha 31-12-13 <br/>
            Por Delegación según, Providencia P/Nº 001-14, de fecha 08-01-14 <br/>
            Gaceta Oficial de la República Bolivariana de Venezuela <br/>
            Nº 40.332 de fecha 13-01-14'''.format(gerente.get_full_name())
    return GACETA

def notificacion(pdf, gaceta_end):
    p = ParagraphStyle('test')
    p.textColor = 'black'
    p.alignment = TA_LEFT
    p.fontSize = 10
    para = Paragraph(NOTIFICACION, p)
    para.wrapOn(pdf, 450, 200)
    para.drawOn(pdf, 100, gaceta_end - 10 - para.height)


NOTIFICACION = u'''<b>NOTIFICACIÓN:</b> <br/>
                <br/>
                Sujeto Pasivo:_______________________ Nombre y Apellido ____________________ <br/>
                Rif. Nº:_____________________________ Cédula:_____________________________ <br/>
                Fecha:_____________________________ Cargo:______________________________ <br/>
                Sello: &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
                &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
                &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
                Teléfono:____________________________ 
                '''

def label(pdf, gaceta_end, page):
    p = ParagraphStyle('test')
    p.textColor = 'black'
    p.alignment = TA_CENTER
    p.fontSize = 12
    p.borderColor = 'black'
    p.borderWidth = 1
    p.borderPadding = 4
    para = Paragraph(LABEL[page], p)
    para.wrapOn(pdf, 150, 200)
    para.drawOn(pdf, 380, gaceta_end - 10 - para.height)

LABEL = [u'CONTRIBUYENTE', u'EXPEDIENTE', u'COORD. FISCALIZACIÓN']

#REQUERIMIENTO ABIERTA~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def text_requerimiento_abierta(documento, supervisor, funcionarios):
    texto = u'''En Caracas, a los {}
            , conforme a lo dispuesto en los artículos 15, 16 y 18 del Decreto
            Nº 9.044 con Rango, Valor y Fuerza de Ley Orgánica de Turismo, publicado en
            la Gaceta Oficial de la República Bolivariana de Venezuela Nº 39.945, Nº 6079
            Extraordinario, ambos de fecha quince (15) de junio de 2012, publicada en la
            Gaceta Oficial de la República Bolivariana de Venezuela Nº 6.079 Extraordinario
            de igual fecha, reimpresa según Gaceta Oficial de la República Bolivariana de
            Venezuela Nº 39.955 en fecha veintinueve (29) de junio 2012, en concordancia con
            lo establecido en el Código Orgánico Tributario, publicado en la Gaceta Oficial de
            la República Bolivariana de Venezuela Nº 37.305,  de fecha diecisiete (17) de
            octubre de 2001,  en sus artículos 121, 145 numerales 3, 4 y 5, y 172 al 176; los
            funcionarios <b>{}</b>, titular de la cédula de identidad <b>Nº {}</b>, y
            supervisor <b>{}</b>, titular de la cédula de identidad <b>Nº {}</b>, adscritos
            a la Gerencia de Recaudación y Fiscalización del Instituto Nacional de Turismo (INATUR),
            debidamente autorizados, según Providencia Administrativa signada con el Nº <b>{}</b>,
            de fecha {}, notificada en fecha {}, procede
            a requerir la presentación de la documentación y/o información que se especifica a
            continuación:<br/><br/>
            <u>{}</u>
            <br/><br/>
            La información deberá ser suministrada, dentro de los próximos cinco (05) días hábiles,
            a los funcionarios actuantes, a través de una persona con cualidad para ello, en la Gerencia
            de Recaudación y Fiscalización del INATUR, ubicada en la Avenida Francisco de Miranda con Avenida
            Principal La Floresta, Complejo MINTUR, Torre Sur, Piso 1, Altamira, Municipio Chacao, Estado Miranda.
            <br/><br/>
            Se hace del conocimiento del sujeto pasivo que la inobservancia al presente requerimiento constituye
            un ilícito formal que genera la sanción prevista en el artículo 105 del Código Orgánico Tributario.
            <br/><br/>
            A los fines legales consiguientes, se emite la presente Acta en dos (02) ejemplares, de un mismo tenor
            y a un solo efecto, uno de los cuales queda en poder del sujeto pasivo, quien firma en señal de notificación:
            '''.format(pretty_date(documento.fecha_generacion),
                       funcionarios[0].get_full_name().upper(), rif_2_ci(funcionarios[0].rif),
                        supervisor.get_full_name().upper(), rif_2_ci(supervisor.rif),
                       documento.providencia.codigo,
                       pretty_date(documento.providencia.fecha_generacion),
                       notificacion_fecha(documento.providencia.fecha_notificacion),
                       pretty_observaciones(documento.observaciones)
                       )
    return texto

def pasivo(pdf, texto_end):
    p = ParagraphStyle('test')
    p.textColor = 'black'
    p.alignment = TA_LEFT
    p.fontSize = 10
    para = Paragraph(DATOS_PASIVO, p)
    para.wrapOn(pdf, 450, 200)
    para.drawOn(pdf, 100, texto_end - 10 - para.height)


DATOS_PASIVO = u'''<b>POR EL SUJERO PASIVO:</b> <br/>
                <br/>
                FIRMA:_______________________<br/>
                Normbre:_____________________<br/>
                Cédula:______________________<br/>
                Cargo:_______________________<br/>
                Fecha:_______________________<br/>
                Teléfono:____________________<br/>
                Sello:
                '''

def supervisor_firma(pdf, texto_end, supervisor):
    firma_supervisor = u'<b>FUNCIONARIOS ACTUANTES:</b> <br/><br/>'
    firma_supervisor += u'''
                                Nombre: <b>{}</b><br/>
                                Cédula: {}<br/>
                                Cargo: <br/>
                                Firma: __________________________

                                '''.format(supervisor.get_full_name().upper(), rif_2_ci(supervisor.rif))
    p = ParagraphStyle('test')
    p.textColor = 'black'
    p.alignment = TA_LEFT
    p.fontSize = 10
    para = Paragraph(firma_supervisor, p)
    para.wrapOn(pdf, 450, 200)
    para.drawOn(pdf, 350, texto_end - 10 - para.height)
    return texto_end - 10 - para.height

def funcionario_firma(pdf, texto_end, funcionario):
    firma_funcionario = u'''
                        Nombre: <b>{}</b><br/>
                        Cédula: {}<br/>
                        Cargo: <br/>
                        Firma: __________________________

                        '''.format(funcionario.get_full_name().upper(), rif_2_ci(funcionario.rif))
    p = ParagraphStyle('test')
    p.textColor = 'black'
    p.alignment = TA_LEFT
    p.fontSize = 10
    para = Paragraph(firma_funcionario, p)
    para.wrapOn(pdf, 450, 200)
    para.drawOn(pdf, 350, texto_end - 10 - para.height)
    return texto_end - 10 - para.height

#RECEPCION abierta~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def text_recepcion_abierta(documento, supervisor, funcionarios):
    texto = u'''En Caracas, a los {},
            conforme a lo dispuesto en los artículos 15, 16 y 18 del Decreto Nº 9.044 con Rango, Valor y Fuerza
            de Ley Orgánica de Turismo, publicado en la Gaceta Oficial de la República Bolivariana de Venezuela
            Nº 39.945, Nº 6079 Extraordinario, ambos de fecha quince (15) de junio de 2012, publicada en la Gaceta
            Oficial de la República Bolivariana de Venezuela Nº 6.079 Extraordinario de igual fecha, reimpresa según
            Gaceta Oficial de la República Bolivariana de Venezuela Nº 39.955 en fecha veintinueve (29) de junio 2012,
            en concordancia con el Decreto Nº 6.217 con Rango, Valor y Fuerza Ley Orgánica de la Administración Pública,
            de fecha quince (15) de julio de 2008, publicada en la Gaceta Oficial Nº 5.890, de fecha treinta y uno (31)
            de julio de 2008 y el Código Orgánico Tributario, publicado en la Gaceta Oficial de la República Bolivariana
            de Venezuela Nº 37.305 de fecha diecisiete (17) de octubre  de 2001, en sus Artículos: 121, 145 numerales
            3, 4 y 5 y 172 al 176; lo(s) funcionario(s) actuante(s) <b>{}</b>, titular de la cédula de identidad
            <b>Nº: {}</b>, supervisor <b>{}</b>, titular de la cédula de identidad <b>Nº {}</b>, adscrito(s)
            a la Gerencia de Recaudación  y  Fiscalización del  Instituto  Nacional de Turismo (INATUR), proceden conforme
            a lo solicitado en el Acta de Requerimiento Nº <b>{}</b>, notificada en fecha {},
            a dejar constancia de los documentos recibidos y de las situaciones que se describen a continuación:<br/><br/>
            <u>{}</u>
            <br/><br/>
            A los fines legales consiguientes, se emite la presente Acta en dos (2) ejemplares de un mismo tenor y a
            un solo efecto, uno de los cuales queda en poder del sujeto pasivo, quien firma a los fines de dejar constancia
            de la entrega de la documentación. 
            '''.format(pretty_date(documento.fecha_generacion),
                       funcionarios[0].get_full_name().upper(), rif_2_ci(funcionarios[0].rif),
                        supervisor.get_full_name().upper(), rif_2_ci(supervisor.rif),
                       documento.providencia.codigo,
                       notificacion_fecha(documento.providencia.fecha_notificacion),
                       pretty_observaciones(documento.observaciones)
                       )
    return texto

#CONSTANCIA~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def text_constancia(documento, supervisor, funcionarios):
    texto = u'''En Caracas, a los {}, a tenor de lo dispuesto en el Artículo 121, numeral 2 del Código Orgánico Tributario,
            publicado en Gaceta Oficial Nro. 37.305 de fecha 17-10-2001, lo(s) funcionario(s) actuante(s) <b>{}</b>,
            titular de la cédula de identidad  <b>Nº: {}</b>, supervisor <b>{}</b>, titular de la cédula de identidad
            <b>Nº {}</b>, adscrito(s) a la Gerencia de Recaudación  y  Fiscalización del  Instituto  Nacional de Turismo
            (INATUR), debidamente autorizados según Providencia Administrativa signada con el Nº <b>{}</b>, de
            fecha {}, notificada en fecha {}, por medio de la presente hace constar:<br/><br/>
            <u>{}</u>
            <br/><br/>
            A los fines legales consiguientes, se emite la presente Acta en dos (2) ejemplares de un mismo tenor y a un solo
            efecto, uno de los cuales queda en poder del sujeto pasivo, quien firma a los fines de dejar constancia de la
            entrega de la documentación. 
            '''.format(pretty_date(documento.fecha_generacion),
                       funcionarios[0].get_full_name().upper(), rif_2_ci(funcionarios[0].rif),
                        supervisor.get_full_name().upper(), rif_2_ci(supervisor.rif),
                       documento.providencia.codigo,
                       pretty_date(documento.providencia.fecha_generacion),
                       notificacion_fecha(documento.providencia.fecha_notificacion),
                       pretty_observaciones(documento.observaciones)
                       )
    return texto



class NumToWord(object):

    primeros = {
        1: 'uno',
        2: 'dos',
        3: 'tres',
        4: 'cuatro',
        5: 'cinco',
        6: 'seis',
        7: 'siete',
        8: 'ocho',
        9: 'nueve',
        11: 'once',
        12: 'doce',
        13: 'trece',
        14: 'catorce',
        15: 'quince'
    }

    segundos = {
        1: 'dieci',
        2: 'veinti',
        3: 'treintai'
    }

    decenas = {
        10: 'diez',
        20: 'veinte',
        30: 'treinta'
    }

    @classmethod
    def get_month_words(cls, num):
        """
        Funcion que convierte numeros a letras para los meses
        Funcion de intervalo cerrado: [1, 31]
        """
        if num > 0 and num < 32:
            if cls.decenas.has_key(num):
                return cls.decenas.get(num, None)
            if cls.primeros.has_key(num):
                return cls.primeros.get(num, None)
            else:
                list_str = []
                for n in str(num):
                    n = int(n)
                    if cls.segundos.has_key(n):
                        if list_str:
                            list_str.append(cls.primeros.get(n, None))
                        else:
                            list_str.append(cls.segundos.get(n, None))
                    else:
                        list_str.append(cls.primeros.get(n, None))
                return ''.join(list_str)
        else:
            return None

    """
    >>>for i in xrange(0, 33):
    >>>    get_month_words(i)
    (0, None)
    (1, 'uno')
    (2, 'dos')
    (3, 'tres')
    (4, 'cuatro')
    (5, 'cinco')
    (6, 'seis')
    (7, 'siete')
    (8, 'ocho')
    (9, 'nueve')
    (10, 'diez')
    (11, 'once')
    (12, 'doce')
    (13, 'trece')
    (14, 'catorce')
    (15, 'quince')
    (16, 'dieciseis')
    (17, 'diecisiete')
    (18, 'dieciocho')
    (19, 'diecinueve')
    (20, 'veinte')
    (21, 'veintiuno')
    (22, 'veintidos')
    (23, 'veintitres')
    (24, 'veinticuatro')
    (25, 'veinticinco')
    (26, 'veintiseis')
    (27, 'veintisiete')
    (28, 'veintiocho')
    (29, 'veintinueve')
    (30, 'treinta')
    (31, 'treintaiuno')
    (32, None)
    """