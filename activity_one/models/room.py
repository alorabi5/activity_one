from odoo import models, fields, api, exceptions

class Room(models.Model):
    _name = 'room'

    name = fields.Char()
    code = fields.Char(default='R0000', readonly=1)


    @api.model_create_multi
    def create(self, vals_list):
        
        for vals in vals_list:
            
            if vals.get('code', 'R0000') == 'R0000':
                vals['code'] = self.env['ir.sequence'].next_by_code('room_seq')
        
        return super(Room, self).create(vals_list)