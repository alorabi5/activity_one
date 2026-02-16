from odoo import models, fields, api, exceptions

class Tag(models.Model):
    _name = 'tag'

    name = fields.Char(required=True)