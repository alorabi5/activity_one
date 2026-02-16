from odoo import models, fields, api, exceptions
from dateutil.relativedelta import relativedelta


class Registration(models.Model):
    _name = 'registration'

    trainee_id = fields.Many2one('hr.employee', required=True)
    course_id = fields.Many2one('course', ondelete="cascade", domain=[('end_date', '>=', fields.Date.today() )])
    
    @api.model
    def create(self, valu):
        res = super(Registration, self).create(valu)

        course = res.course_id

        if(course.available_seat == 0):
            raise exceptions.ValidationError('The course seats is full.')

        course.available_seat -= 1
        self.course_id._compute_number_of_days
        
        return res
    