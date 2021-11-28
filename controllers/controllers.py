# -*- coding: utf-8 -*-
# from odoo import http


# class Kill4city(http.Controller):
#     @http.route('/kill4city/kill4city/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kill4city/kill4city/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('kill4city.listing', {
#             'root': '/kill4city/kill4city',
#             'objects': http.request.env['kill4city.kill4city'].search([]),
#         })

#     @http.route('/kill4city/kill4city/objects/<model("kill4city.kill4city"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kill4city.object', {
#             'object': obj
#         })
