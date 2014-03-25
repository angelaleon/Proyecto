# -*- coding: utf-8 -*-

from osv import fields, osv


class oemedical_consentimientos(osv.osv):
    _name = 'oemedical.consentimientos'
    _columns = {
        'nombre': fields.char(size=100, string='Nombre de consentimiento'),
        'texto': fields.text(string='Texto'),
    }


oemedical_consentimientos()
