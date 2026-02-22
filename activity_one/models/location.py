from odoo import models, fields, api, exceptions

class Location(models.Model):
    _name = 'location'

    name = fields.Char()
    code = fields.Char(default='L0000', readonly=1)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('code', 'L0000') == 'L0000':
                vals['code'] = self.env['ir.sequence'].next_by_code('location_seq')
        
        return super(Location, self).create(vals_list)
        