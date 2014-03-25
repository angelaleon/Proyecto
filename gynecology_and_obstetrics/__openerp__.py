# -*- coding: utf-8 -*-

{
    'name': 'Ginecologia y Obstetricia',
    'version': '0.1',
    'category': 'Base',
    'complexity': 'easy',
    'depends': ['base'],
    'author': 'Angela León Torralbo',
    'website': 'www.angelaleon.com',
    'description':
        '''
            Sistema de información ginecologico ambulatorio.
        ''',
    "init_xml": [],
    'update_xml': [
        'oemedical_gynecology_and_obstetrics_view.xml',
        'oemedical_vademecum_view.xml',
        'oemedical_consentimientos_view.xml',
        'oemedical_agenda_view.xml',
        'oemedical_agenda2_view.xml',
    ],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
    'active': False,
}