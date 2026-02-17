from odoo import models, fields, api, exceptions
from datetime import date

class Course(models.Model):
    _name = 'course'

    serial_number = fields.Integer(default=0 ,readonly=1)
    name = fields.Char(required=True)
    descrption = fields.Text()
    teacher_id = fields.Many2one('teacher')
    techer_name = fields.Char(related='teacher_id.name')
    start_date = fields.Date()
    end_date = fields.Date()
    number_of_days = fields.Integer(compute='_compute_number_of_days')
    time = fields.Datetime()
    room_id = fields.Many2one('room')
    location_id = fields.Many2one('location')
    available_seat = fields.Integer(required=True)
    targer_gender = fields.Selection([('male', 'Male'), ('female', 'Female')])
    deadline = fields.Date()
    registration_id = fields.Many2one('registration')




    @api.depends('start_date', 'end_date')
    def _compute_number_of_days(self):
        for record in self:
            if record.start_date and record.end_date:
                record.number_of_days = (record.end_date - record.start_date).days
            else:
                record.number_of_days = 0


    @api.constrains('available_seat')
    def check_valid_seat_number(self):
        for rec in self:
            if rec.available_seat < 0:
                raise exceptions.ValidationError('Please add valid seats number!')


    @api.model
    def create(self, vals):
        res = super(Course, self).create(vals)

        if res.available_seat <= 0:
            raise exceptions.ValidationError('Please make sure there are available seats for this course')

        if res.serial_number == 0:
            res.serial_number = self.env['ir.sequence'].next_by_code('course_seq')
        
        return res
