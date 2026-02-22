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

    trainee_id = fields.Many2one('hr.employee', required=True, default=lambda self: self.env.user.employee_id, readonly=True, store=True)
    trainee_start_date = fields.Date(related='trainee_id.contract_date_start')
    course_id = fields.Many2one('course', ondelete="cascade", domain=[('end_date', '>=', fields.Date.today() )])
    
    
    def action_draft(self):
        self.state = 'draft'

    def action_pending(self):
        self.state = 'pending'
    
    def action_approve(self):
        # self.state = 'approve'
        self.sudo().write({'state': 'approve'})

    
    def action_reject(self):
        # self.state = 'reject'
        self.sudo().write({'state': 'reject'})

    

    
    @api.constrains('trainee_id')
    def is_join_before_six_month(self):
        for rec in self:
            # if (fields.Date.today() - rec.trainee_start_date).days < 180:
            if rec.trainee_start_date:
                allow_registration_date = rec.trainee_start_date + relativedelta(months=6)
                if fields.Date.today() < allow_registration_date:
                    raise exceptions.ValidationError('Enrollment in the course is only permitted after 6 months from the start date!')


    def _check_and_update_seats(self, course_id):
        if not course_id:
            return
        
        course = self.env['course'].sudo().browse(course_id)

        if(course.available_seat <= 0):
            raise exceptions.ValidationError('The course seats is full.')
        
        course.sudo().write({'available_seat': course.available_seat - 1 })

    # def _is_trainee_take_course_this_year(self, course_id):
    #     if not course_id:
    #         return
        
    #     course = self.env['course'].sudo().browse(course_id)

    #     if course.

    @api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:
            course_id = vals.get('course_id')

            self._check_and_update_seats(course_id)
        
        return super(Registration, self).create(vals_list)
    

    def unlink(self):
        for rec in self:
            if rec.course_id:
                rec.course_id.available_seat += 1

        return super(Registration, self).unlink()