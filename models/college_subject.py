from odoo import fields,api,models

class collegesubject(models.Model):
    _name = 'college.subject'
    _description = 'College Subjects'

    name = fields.Char(string='Subject Name')
    code = fields.Char(string='Subject Code')
    credit = fields.Integer(string='Subject Credits',default=3)
    department_ids = fields.Many2many('college.department',string='Departments',relation='college_department_subject_rel',column1='subject_id',column2='department_id')
                                      
