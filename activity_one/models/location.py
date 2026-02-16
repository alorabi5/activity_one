from odoo import models, fields, api, exceptions

class Location(models.Model):
    _name = 'location'

    name = fields.Char()
    code = fields.Char(default='L0000', readonly=1)

    @api.model
    def create(self, vals):
        res = super(Location, self).create(vals)
        if res.code == 'L0000':
            res.code = self.env['ir.sequence'].next_by_code('location_seq')
        
        return res
        