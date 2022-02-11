# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
 
{
   'name': 'Real Estate',
   'version': '1.0',
   'summary': 'Real estate Advertisement App',
   'description': "",
   'author':"Deepak Shah",
   'depends': ['base','website'],
   'data' : [
       'security/real_estate_security.xml',
       'security/ir.model.access.csv',
       'views/estate_property_views.xml',
       'views/estate_menus.xml',
       'wizard/property_wizard_view.xml',
       'views/inherit_partner_view.xml',
       'views/real_estate_templates.xml',
       'report/estate_property_reports.xml',
       'report/estate_property_templates.xml',
   ],

   
 
   'installable': True,
   'auto_install': False,
   'application': True,
   'license': 'LGPL-3',
}
