from odoo import models, fields, api, exceptions

class Teacher(models.Model):
    _name = 'teacher'

    name = fields.Char()
    teacher_user_id = fields.Many2one('res.users', domain= lambda self:[('group_ids', 'in', [self.env.ref('activity_one.teacher_group').id])] )
    course_ids = fields.One2many('course', 'teacher_id')
    code = fields.Char(default='T0000', readonly=1)

    @api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:
            if vals.get('code','T0000') == 'T0000':
                vals['code'] = self.env['ir.sequence'].next_by_code('teacher_seq')
        
        return super(Teacher, self).create(vals_list)


    _teacher_unique = models.Constraint(
        'unique (teacher_user_id)',
        'This teacher is exist!'
    )