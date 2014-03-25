# -*- coding: utf-8 -*-

from osv import fields, osv


class oemedical_agenda(osv.osv):
    _name = 'oemedical.agenda'

    def _get_duracion(self, cr, uid, ids, field_name, arg, context=None):

        res = {}
        for record in self.browse(cr, uid, ids, context=context):
            if record.tipo_cita == 'Obstetricia':
                duracion = 1.0

            if record.tipo_cita == 'Puerperio':
                duracion = 0.5

            if record.tipo_cita == 'Ginecologia':
                duracion = 0.75

            res[record.id] = duracion

        return duracion

    def _citas_unicas(self, cr, uid, ids, context=None):
        blr = self.pool.get('oemedical.agenda')
        for record in self.browse(cr, uid, ids, context=context):
            ids = blr.search(cr,uid,[('tipo_cita', '=', record.tipo_cita),
                ('date', '=', record.date),
                ('date', '=', record.paciente_id.id)])
            if (len(ids)>1):
                return False
        return True

    _columns = {
        'tipo_cita': fields.selection([
                                          ('Obstetricia', 'obstetricia'),
                                          ('Puerperio', 'Puerperio'),
                                          ('Ginecologia', 'Ginecologia'),
                                      ], 'Tipo de Cita', select=True),
        'date': fields.datetime('Fecha de cita', required=True),
        'duracion': fields.float(string='Duracion de la cita', readonly=True),
        'paciente_id': fields.many2one('oemedical.paciente', 'paciente', required=True),

    }

    _constraints = [(_citas_unicas, 'Error: Este paciente ya tiene una cita asignada igual', ('tipo_cita','date','paciente_id'))]

oemedical_agenda()