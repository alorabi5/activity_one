from odoo import models, fields, api, exceptions

class Room(models.Model):
    _name = 'room'

    name = fields.Char()
    code = fields.Char(default='R0000', readonly=1)

    @api.model
    def create(self, vals):
        res = super(Room, self).create(vals)
        if res.code == 'R0000':
            res.code = self.env['ir.sequence'].next_by_code('room_seq')
        
        return res