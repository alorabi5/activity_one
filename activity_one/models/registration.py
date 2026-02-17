from odoo import models, fields, api, exceptions
from dateutil.relativedelta import relativedelta


class Registration(models.Model):
    _name = 'registration'

    state = fields.Selection(
        [
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('approve', 'Approve'),
        ('reject', 'Reject')
        ], default='draft'
    )

    trainee_id = fields.Many2one('hr.employee', required=True)
    course_id = fields.Many2one('course', ondelete="cascade", domain=[('end_date', '>=', fields.Date.today() )])
    
    
    def action_draft(self):
        self.state = 'draft'

    def action_pending(self):
        self.state = 'pending'
    
    def action_approve(self):
        self.state = 'approve'
    
    def action_reject(self):
        self.state = 'reject'
    

    @api.model
    def create(self, vals):
        res = super(Registration, self).create(vals)

        course = res.course_id

        if(course.available_seat == 0):
            raise exceptions.ValidationError('The course seats is full.')

        course.available_seat -= 1
        
        return res
    
    def unlink(self):
        for rec in self:
            if rec.course_id:
                rec.course_id.available_seat += 1

        return super(Registration, self).unlink()