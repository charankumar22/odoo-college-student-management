from odoo import fields,models,api

class collegedepartment(models.Model):
    _name = 'college.department'
    _description = 'College Department'

    name = fields.Char(string='Department Name')
    code = fields.Char(string='Department Code')

    subject_ids = fields.Many2many('college.subject',string='Subjects',relation='college_department_subject_rel',column1='department_id',column2='subject_id')