# -*- coding: utf-8 -*-

from osv import fields, osv


class oemedical_mechanism(osv.osv):
    _name = 'oemedical.mechanism'
    _columns = {
        'name': fields.selection([
                                     ('antiinflamatorio', 'Antiinflamatorio'),
                                     ('analgesico', 'Analgesico'),
                                     ('absorbentes', 'Absorbentes'),
                                     ('antisepticos', 'Anteisepticos'),
                                 ], 'Mecanismo de acción'),
        'mechanism_action_ids': fields.one2many('oemedical.vademecum', 'mechanism_action_id', 'mecanismo',
                                                required=True),
    }

    def name_get(self, cr, uid, ids, context={}):
        res = dict.fromkeys(ids, '')
        for obj in self.browse(cr, uid, ids, context=context):
            #nombre=obj.name
            res[obj.id] = obj.name
        return res


oemedical_mechanism()


class oemedical_laboratory(osv.osv):
    _name = 'oemedical.laboratory'
    _columns = {
        'name': fields.selection([
                                     ('Abalonpharma', 'Abalon Pharma'),
                                     ('acygen', 'Acygen'),
                                     ('alcon', 'Alcon'),
                                     ('allergan', 'Allergan'),
                                     ('arafarma', 'Arafarma'),
                                 ], 'Laboratorio'),
        'vademecum_ids': fields.one2many('oemedical.vademecum', 'laboratoy_id', 'laboratorio', required=True),
    }

    def name_get(self, cr, uid, ids, context={}):
        res = dict.fromkeys(ids, '')
        for obj in self.browse(cr, uid, ids, context=context):
            #nombre=obj.name
            res[obj.id] = obj.name
        return res


oemedical_laboratory()


class oemedical_vademecum(osv.osv):
    _name = 'oemedical.vademecum'

    def listado_laboratorios(self, cr, uid, ids, context=None):
        res = []
        for obj in self.browse(cr, uid, ids, context=context):
            #nombre=obj.name
            #res[obj.id] = obj.laboratoy_id.name
            res.append(obj.id, obj.laboratoy_id.name)
        return res

    _columns = {
        'mechanism_action_id': fields.many2one('oemedical.mechanism', string='Mecanismo de accción', required=True,
                                               ondelete='cascade'),
        'name': fields.char('Nombre', size=200),
        'laboratoy_id': fields.many2one('oemedical.laboratory', string='Laboratorio', required=True,
                                        ondelete='cascade'),
        'pactive': fields.char(size=100, string='Principio Activo'),
        'indicative': fields.text(string='Indicaciónes'),
        'characteristics': fields.text(string='Caracteristicas'),
        'posopologia': fields.text(string='Posopologia'),
        'packaging': fields.text(string='Presentación'),
        #'listado_laboratorio': fields.selection(listado_laboratorios),
    }




oemedical_vademecum()
