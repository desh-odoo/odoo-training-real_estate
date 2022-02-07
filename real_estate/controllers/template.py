from crypt import methods
from odoo import http
from odoo.http import request

class estate_property(http.Controller):

    @http.route('/', website=True)
    def a(self, **kw):
        return request.render("real_estate.root")
    
#------------Simple Controller------------------------
    @http.route('/hello')
    def hello(self, **kw):
        return "Welcome in Real Estate."

#-------------Dynamic Controller----------------------   
    @http.route('/hello_user', auth="user")
    def hello_user(self, **kw):
        return "Welcome %s in Real Estate." %(request.env.user.name)

#----------------Static Template----------------------------
    @http.route('/hello_template',website=True)
    def hello_template(self, **kw):
        return request.render('real_estate.hello_template')

#----------------Dynamic Template---------------------------
    @http.route('/template_dynamic')
    def template(self, **kw):
        property = request.env['estate.property'].search([('status','=','sold')])
        return request.render('real_estate.template_dynamic',{'user':request.env.user, 'property': property })

#----------------Call Dynamic Tamplate--------------------------- 
    @http.route('/call_template', method="post", website=True)
    def call_template(self, **kw):
        return request.render('real_estate.call_template_dynamic',{'property': request.env['estate.property'].search([])})

    @http.route(['/call_template/<model("estate.property"):property>', '/call_template/<string:is_static>'], auth="user", website=True)
    def property_details(self, property=False, is_static=False,**kw):
        if property:
            return request.render('real_estate.property_details', {
                'property': property,
            })
        elif is_static:
            return request.render('real_estate.property_static')#, {'property': request.env['estate.property'].sudo().search([], limit=8)})

#-------------------Delete property from Template----------------------
    @http.route('/delete/estateproperty/<model("estate.property"):property>')
    def delete_estate_property(self, property, **kw):
        property.offers_ids.unlink()
        property.unlink()
        return request.redirect('/call_template')


   