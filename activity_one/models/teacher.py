from odoo import models, fields, api, exceptions

class Teacher(models.Model):
    _name = 'teacher'

    name = fields.Char()
    teacher_user_id = fields.Many2one('res.users')
    course_ids = fields.One2many('course', 'teacher_id')
    code = fields.Char(default='T0000', readonly=1)

    @api.model
    def create(self, vals):
        res = super(Teacher, self).create(vals)
        if res.code == 'T0000':
            res.code = self.env['ir.sequence'].next_by_code('teacher_seq')
        
        return res