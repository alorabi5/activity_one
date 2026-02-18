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
    trainee_start_date = fields.Date(related='trainee_id.contract_date_start')
    course_id = fields.Many2one('course', ondelete="cascade", domain=[('end_date', '>=', fields.Date.today() )])
    
    
    def action_draft(self):
        self.state = 'draft'

    def action_pending(self):
        self.state = 'pending'
    
    def action_approve(self):
        self.state = 'approve'
    
    def action_reject(self):
        self.state = 'reject'
    

    
    @api.constrains('trainee_id')
    def is_join_before_six_month(self):
        for rec in self:
            # if (fields.Date.today() - rec.trainee_start_date).days < 180:
            if rec.trainee_start_date:
                allow_registration_date = rec.trainee_start_date + relativedelta(months=6)
                if fields.Date.today() < allow_registration_date:
                    raise exceptions.ValidationError('Enrollment in the course is only permitted after 6 months from the start date!')


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