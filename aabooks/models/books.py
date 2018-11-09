import time
import math
from odoo.osv import expression
from odoo.tools.float_utils import float_round as round
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models


class Books(models.Model):
    _name = 'books.books'
    _description = 'Free Books'
    name = fields.Char(string='Book title', required=True)
    author = fields.Char(string='Author')
    price = fields.Float(string='Price', required=True)
    number_of_pages = fields.Integer(string='Page number', required=True)
    publishing_house = fields.Char(string='Publishing House', required=True)
    publish_year = fields.Date(string='Publish date')
    info = fields.Text(placeholder='General knowledge')
    email = fields.Char(string='Email')
    phone = fields.Integer(string='Phone number')
    state = fields.Selection([('draft', 'Draft'),
                               ('order', 'Order'),
                               ('deliver', 'Deliver')], default='draft')
    delivered = fields.Integer(string='Delivered')
    total_price = fields.Integer(string='Earnings')
    copies_left = fields.Integer(string='Copies Left')
    out_of_copies = fields.Text(default='Sorry! We are out of Copies!')

    @api.one
    def order(self):
        self.write({'state': 'order'})

    @api.one
    def deliver(self):
        self.write({'state': 'deliver'})
        self.delivered += 1
        self.total_price = self.delivered * self.price * 0.8
        self.copies_left -= 1

    @api.one
    def cancel(self):
        self.write({'state': 'draft'})
