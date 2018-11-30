import re
from odoo.exceptions import ValidationError
from odoo import api, fields, models


class Books(models.Model):
    _name = 'books.books'
    _description = 'Free Books'
    name = fields.Char(string='Book title', required=True)
    genre_ids = fields.Many2many('books.genre', string='Genre', required=True)
    author = fields.Char(string='Author', default='Anonymous')
    price = fields.Float(string='Price', required=True)
    number_of_pages = fields.Integer(string='Page number', required=True)
    publishing_house = fields.Char(string='Publishing House', required=True, default='BookHouse')
    publish_year = fields.Date(string='Publish date')
    info = fields.Text(placeholder='General knowledge')
    email = fields.Char(string='Email')
    isbn = fields.Char(string='ISBN')
    state = fields.Selection([('draft', 'Draft'), ('order', 'Order'), ('deliver', 'Deliver')], default='draft')
    delivered = fields.Integer(string='Delivered')
    total_price = fields.Integer(string='Earnings')
    copies_left = fields.Integer(string='Copies Left')
    out_of_copies = fields.Text(default='Sorry! We are out of Copies!')
    color = fields.Integer(string='Color')

    @api.one
    def order(self):
        self.write({'state': 'order'})

    @api.one
    def deliver(self):
        self.write({'state': 'draft'})
        self.delivered += 1
        self.total_price = self.total_price + (self.price * 0.8)
        self.copies_left -= 1

    @api.one
    def cancel(self):
        self.write({'state': 'draft'})

    @api.onchange('email')
    def validate_mail(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            if match is None:
                raise ValidationError('Not a valid E-mail ID')


class Genre(models.Model):
    _name = 'books.genre'

    name = fields.Char(string='Genre', required=True)
    count = fields.Integer(string='Number of Books', compute='count_number_of_books')
    book_ids = fields.Many2many('books.books', string='Books', store=True)

    @api.depends('book_ids')
    def count_number_of_books(self):
        """ Count number of books that belong to this genre."""
        for genre in self:
            genre.count = len(genre.book_ids)
