# -*- coding: utf-8 -*-

import time

from report import report_sxw

class order(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context=None):
        super(order, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
        })

report_sxw.report_sxw('report.oemedical.order', 'oemedical.order', 'other-addons/gynecology_and_obstetrics/report/oemedical_order.rml', parser=order, header="external")

