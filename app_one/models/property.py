from odoo import models, fields, api, exceptions
# from odoo.exceptions import ValidationError

class Property(models.Model):
    _name = 'property'

    name = fields.Char(required=True, default="New Property", size=20)
    description = fields.Text()
    postcode = fields.Char(required=True)
    date_availability = fields.Date()
    expected_price = fields.Float(digits=(0, 5))
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'), 
        ('south', 'South'), 
        ('east', 'East'), 
        ('west', 'West'), 
        ], default='north')
    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')


    # This no longer work on odoo 19

    # _sql_constraints = [
    #     ('unique_name', 'unique("name")', 'This name is exist!')
    # ]

    _name_unique = models.Constraint(
        'unique (name)',                # For Multipule fields: 'unique (name, postcode, ......)'
        'This name is exist!'
    )



    @api.constrains('bedrooms')
    def check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms <= 0:
                raise exceptions.ValidationError('Please add valid number of bedroom')


    # CRUD

    # Create
    @api.model_create_multi
    def create(self, valu):
        res = super(Property, self).create(valu)
        print("inside create method")
        return res

    # Read
    @api.model
    def search(self, domain, offset=0, limit=None, order=None):
        # res = super(Property, self)._search(domain, offset, limit, order)
        res = super(Property, self).search(domain, offset=offset, limit=limit, order=order)
        print("inside search method")
        return res

    
    # Update
    def write(self, vals):
        res = super(Property, self).write(vals)
        print("inside write method")
        return res
    
    # Delete
    def unlink(self):
        res = super(Property, self).unlink()
        print("inside unlink method")
        return res