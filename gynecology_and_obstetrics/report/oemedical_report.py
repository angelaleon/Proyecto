# -*- coding: utf-8 -*-

import tools
from osv import fields, osv

class oemedical_report(osv.osv):
    _name = "oemedical.report"
    _description = "Informe médico"
    _auto = False
    _rec_name = 'date'
    _columns = {

    }

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'oemedical_report')
        cr.execute("""
            create or replace view oemedical_report as (
                select
                    name, firstname,
                from
                    oemedical_paciente
            )
        """)


oemedical_report()



