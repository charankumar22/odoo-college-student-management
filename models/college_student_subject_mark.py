from odoo import models,fields,api
from odoo.exceptions import ValidationError

class collegestudentsubjectmark(models.Model):
    _name = 'college.student.subject.mark'
    _description = 'College Student Subject Mark'

    student_id = fields.Many2one('college.student',string='Students')
    subject_id = fields.Many2one('college.subject',string='Subjects')
    internal_mark = fields.Float(string='Internal Mark',default=0.0)
    external_mark = fields.Float(string='External Mark',default=0.0)
    total_mark = fields.Float(string='Total Marks',compute='_compute_total_mark',store=True)
    grade_point = fields.Float(string='Grade Point',compute='_compute_grade_point',store=True)

    credit = fields.Integer(string='Credit',related='subject_id.credit',store=True)

    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note"),
    ], default=False)

    @api.depends('internal_mark','external_mark')
    def _compute_total_mark(self):
        for rec in self:
            rec.total_mark = rec.internal_mark + rec.external_mark
    @api.depends('total_mark')
    def _compute_grade_point(self):
        for rec in self:
            total = rec.total_mark
            if total >= 90:
                rec.grade_point = 10
            elif total >= 80:
                rec.grade_point = 9
            elif total >= 70:
                rec.grade_point = 8
            elif total >= 60:
                rec.grade_point = 7
            elif total >= 50:
                rec.grade_point = 6
            else:
                rec.grade_point = 0


    @api.onchange('internal_mark')
    def _onchange_internal(self):
        if self.internal_mark < 0 or self.internal_mark > 30:
            return {'warning':{'title':'Invalid Internal Mark','message':f'Internal mark must be between 0  and 30. You entered:{self.internal_mark}'}}
    @api.onchange('external_mark')
    def _onchange_external(self):
        if self.external_mark < 0 or self.external_mark > 70:
            return {'warning':{'title':'Invalid External Mark','message':f'External mark must be between 0  and 70. You entered:{self.external_mark}'}}
        
    @api.constrains('internal_mark','external_mark')
    def _check_valid_mark(self):
        for rec in self:
            if rec.internal_mark < 0 or rec.internal_mark > 30:
                raise ValidationError(f"Internal Marks must be between 0 to 30. You entered: {rec.internal_mark}") 
            if rec.external_mark < 0 or rec.external_mark > 70:
                raise ValidationError(f"External Marks must be between 0 to 70. You entered: {rec.external_mark}") 