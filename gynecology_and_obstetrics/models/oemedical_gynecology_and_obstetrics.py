# -*- coding: utf-8 -*-

from osv import fields, osv
from dateutil.relativedelta import relativedelta
from datetime import datetime


class oemedical_paciente(osv.osv):
    _name = 'oemedical.paciente'

    def _get_edad(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        edad = ''
        now = datetime.now()

        for record in self.browse(cr, uid, ids, context=context):
            if record.fech_nac != '':
                nac = datetime.strptime(str(record.fech_nac), '%Y-%m-%d')

                delta = relativedelta(now, nac)
                ano_mes_dia = str(delta.years) + ' años '

                # Si el campo es edad devuelvo su edad correspondiente
                if field_name == 'edad':
                    edad = ano_mes_dia
                res[record.id] = edad
        return res


    _columns = {
        'name': fields.char('Nombre', size=100, required=True),
        'firstname': fields.char('Apellidos', size=200),
        'fech_nac': fields.date(string='Fecha de nacimiento'),
        'edad': fields.function(_get_edad, type='char', string='Edad', readonly=True),
        'dni': fields.char(size=9, string='D.N.I.'),
        'country': fields.char('Poblacion', size=100),
        'city': fields.char('Ciudad', size=100),
        'cp': fields.char('C.P.', size=5),
        'tlf1': fields.char('Telefono principal', size=9, required=True),
        'tlf2': fields.char('Telefono secundario', size=9),
        'fur': fields.date(string='F.U.R.'),
        'identification_code': fields.char(size=256, string='ID', help='Identificacion del paciente'),
        'antecedentes_per': fields.text(string='Antecendentes personales'),
        'antecedentes_fam': fields.text(string='Antecedentes familiares'),
        'medicacion_actual': fields.text(string='Medicación actual'),
        'cirugias_previas': fields.text(string='Cirugias previas'),
        'prenatal_ids': fields.one2many('oemedical.patient.prenatal.evaluation', 'paciente_id', 'prenatal'),
        'puerperio_ids': fields.one2many('oemedical.puerperium.monitor', 'paciente_id', 'puerperio'),
        'ginecologia_ids': fields.one2many('oemedical.ginecologia', 'paciente_id', 'genicologia'),
        'cita_ids': fields.one2many('oemedical.agenda', 'paciente_id', 'cita'),
        'anamnesis_ids': fields.one2many('oemedical.anamnesis', 'paciente_id', 'anamnesis'),
    }

    def name_get(self, cr, uid, ids, context=None):
        res = []
        for obj in self.browse(cr, uid, ids, context=context):
            nombre = obj.firstname + ', ' + obj.name
            res.append((obj.id,nombre))
        return res


    def _check_date_fur(self, cr, uid, ids, context=None):
        for rec in self.browse(cr, uid, ids):
            if rec.fur == '':
                return True
            date_start = datetime.strptime(str(rec.fur), '%Y-%m-%d')
            date_end = datetime.now()

            if date_start <= date_end:
                return True
        return False


    def _check_date_nac(self, cr, uid, ids, context=None):
        for rec in self.browse(cr, uid, ids):
            if rec.fech_nac == '':
                return True
            date_start = datetime.strptime(str(rec.fech_nac), '%Y-%m-%d')
            date_end = datetime.now()

            if date_start <= date_end:
                return True
        return False


    _constraints = [(_check_date_fur, 'Error: La F.U.R es posterior a la fecha actual', 'fur')]
    _constraints = [(_check_date_nac, 'Error: La fecha de nacimiento es posterior a la fecha actual', 'fech_nac')]


oemedical_paciente()


class oemedical_PrenatalEvaluation(osv.osv):
    _name = 'oemedical.patient.prenatal.evaluation'
    _description = 'Evaluaciones prenatales'

    def _check_gestational_weeks(self, cr, uid, ids, context=None):
        for rec in self.browse(cr, uid, ids):
            if rec.gestational_weeks == '' or rec.gestational_weeks >= 43:
                return False
        return True

    def _check_gestational_days(self, cr, uid, ids, context=None):
        for rec in self.browse(cr, uid, ids):
            if ( (rec.gestational_days == '') or (rec.gestational_days >= 7) ):
                return False
        return True


    def _get_gestacion(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        now = datetime.now()

        for record in self.browse(cr, uid, ids):
            if record.paciente_id.fur != '':
                fur = datetime.strptime(str(record.paciente_id.fur), '%Y-%m-%d')

                delta = relativedelta(now, fur)
                semanas = int(delta.months) * 4
                dias = int(delta.days)
                while dias > 7:
                    dias = dias - 7

                # Si el campo es gestational_weeks devuelvo su edad correspondiente
                if field_name == 'gestational_weeks':
                    res[record.id] = semanas

                # Si el campo es gestational_days devuelvo su edad correspondiente
                if field_name == 'gestational_days':
                    res[record.id] = dias

        return res

    # def _get_date(self, cr, uid, ids, field_name, arg, context=None):
    #     res = {}
    #     for record in self.browse(cr, uid, ids):
    #         if field_name == 'evaluation_date':
    #             res[record.id] = datetime.now()
    #
    #     return res

    _columns = {
        'evaluation_date': fields.date('Fecha de revisión', required=True),
        # 'evaluation_date': fields.function(_get_date, type='char', string='Fecha de consulta', readonly=True),
        'gestational_weeks': fields.integer(size=2, string='Semanas de gestación'),
        'gestational_days': fields.integer(size=2, string='Dias de gestación', type='integer'),
        # 'gestational_weeks': fields.function(_get_gestacion, type='char', string='Semanas de gestación', readonly=True),
        # 'gestational_days': fields.function(_get_gestacion, type='char', string='Dias de gestación', readonly=True),
        'hypertension': fields.boolean('Hypertension', help='Check de mujer hipertensa'),
        'sobrepeso': fields.boolean('Sobrepeso', help='Check de mujer con sobrepeso'),
        'diabetes': fields.boolean('Diabetes', help='Check de mujer con diabetes'),
        'placenta_previa': fields.boolean('Placenta Previa'),
        'fetal_bpd': fields.integer('BPD', help="Diametro biparental"),
        'fetal_ac': fields.integer('AC', help="Circunferencia abdominal"),
        'fetal_hc': fields.integer('HC', help="Circunferencia del corazon"),
        'fetal_fl': fields.integer('FL', help="Longitud del femur"),
        'tratamiento': fields.text('Tratamiento', help="Tramiento para el paciente"),
        'observaciones': fields.text('Observaciones', help="Observaciones para el paciente"),
        'paciente_id': fields.many2one('oemedical.paciente', 'paciente'),
    }

    _constraints = [(_check_gestational_weeks, 'Error: Las semanas de gestación debe estar entre 0 y 42', 'gestational_weeks')]
    _constraints = [(_check_gestational_days, 'Error: Los dias de gestación debe estar entre 0 y 7', 'gestational_days')]


    _order = 'evaluation_date desc'

oemedical_PrenatalEvaluation()


class oemedical_Puerperium_Monitor(osv.osv):
    _name = 'oemedical.puerperium.monitor'
    _description = 'Monitor de puerperio'

    _columns = {
        'date': fields.date('Fecha de revisión', required=True),
        'systolic': fields.integer('Presión sistolica'),
        'diastolic': fields.integer('Presión distolica'),
        'frequency': fields.integer('Frecuencia cardiaca'),
        'lochia_amount': fields.selection([
                                              ('n', 'Normal'),
                                              ('e', 'Abundante'),
                                              ('h', 'Hemorragia'),
                                          ], 'Amenorrea', select=True),
        'lochia_odor': fields.selection([
                                            ('n', 'Normal'),
                                            ('o', 'Agresivo'),
                                        ], 'Olor', select=True),
        'temperature': fields.float('Temperatura'),
        'tratamiento': fields.text('Tratamiento', help="Tramiento para el paciente"),
        'observaciones': fields.text('Observaciones', help="Observaciones para el paciente"),
        'paciente_id': fields.many2one('oemedical.paciente', 'paciente'),
    }

    _defaults = {
        'lochia_amount': lambda *a: 'n',
        'lochia_odor': lambda *a: 'n',
        # 'date': datetime.now(),
    }

    _order = 'date desc'


oemedical_Puerperium_Monitor()


class oemedical_Ginecologia(osv.osv):
    _name = 'oemedical.ginecologia'
    _description = 'Consulta ginecologia'

    _columns = {
        'date': fields.date('Fecha de consulta', required=True),
        'talla': fields.float('Talla del paciente'),
        'peso': fields.float('peso del paciente'),
        'ecografia': fields.text('Exploración ecográfica'),
        'tratamiento': fields.text('Tratamiento', help="Tramiento para el paciente"),
        'observaciones': fields.text('Observaciones', help="Observaciones para el paciente"),
        'paciente_id': fields.many2one('oemedical.paciente', 'paciente'),
    }

    _default = {
        'date':datetime.now()
    }

    _order = 'date desc'


oemedical_Ginecologia()




