from odoo import api, models,fields
from odoo.exceptions import UserError
from odoo import exceptions


class OrderPopUp(models.TransientModel):
    _name = 'books.orderpopup'
    _description = 'Order PopUp'

    name = fields.Char(string='First Name', required=True)
    lastname = fields.Char(string='Last Name', required=True)
    address1 = fields.Text(string='Address1', required=True)
    address2 = fields.Text(string='Address2')
    payment = fields.Selection([('visa', 'Visa'),
                                ('paypal', 'PayPal'),
                                ('mastercard', 'MasterCard')], default='paypal', required=True)
    email = fields.Char(string='Email', required=True)
    city = fields.Char(string='City', required=True)
    country = fields.Char(string='Country', required=True)
    postalcode = fields.Integer(string='Postal Code', required=True)
    state = fields.Selection([('order', 'Order')], default='order')
    status = fields.Selection([('deliver', 'Deliver')], default='deliver')

    @api.multi
    def confirm2(self):
        for orderpopup in self:
            if orderpopup.state:
                ids = self.env['books.books'].search([('state', '=', orderpopup.state)])
                ids.write({'state': orderpopup.status})