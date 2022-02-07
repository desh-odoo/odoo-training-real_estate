
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
 
{
   'name': 'Real Estate Extended',
   'version': '1.0',
   'summary': 'Real estate Advertisement App',
   'description': "",
   'author':"Deepak Shah",
   'depends': ['base','real_estate'],
   'data' : [
       'security/ir.model.access.csv',
       'views/extended_view.xml',
   ],

   
 
   'installable': True,
   'auto_install': False,
   'application': True,
   'license': 'LGPL-3',
}
