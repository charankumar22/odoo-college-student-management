from odoo import models, fields, api
from odoo.exceptions import ValidationError


class StudentMarksWizard(models.TransientModel):
    _name = 'student.marks.wizard'
    _description = 'Student Marks Entry Wizard'

    student_id = fields.Many2one(
        comodel_name='college.student',
        string='Student',
        readonly=True,
    )
    mark_line_ids = fields.One2many(
        comodel_name='student.marks.wizard.line',
        inverse_name='wizard_id',
        string='Subject Marks',
    )

    def action_save_marks(self):
        
        self.ensure_one()
        
        
        for line in self.mark_line_ids:
            if line.subject_mark_id:
                line.subject_mark_id.write({
                    'subject_id': line.subject_id.id,
                    'internal_mark': line.internal_mark,
                    'external_mark': line.external_mark,
                })
            else:
                self.env['college.student.subject.mark'].create({
                    'student_id':self.student_id.id,
                    'subject_id':line.subject_id.id,
                    'internal_mark':line.internal_mark,
                    'external_mark':line.external_mark
                })
        
       
        
        return {'type': 'ir.actions.act_window_close'}


class StudentMarksWizardLine(models.TransientModel):
    _name = 'student.marks.wizard.line'
    _description = 'Student Marks Wizard Line'

    wizard_id = fields.Many2one(
        comodel_name='student.marks.wizard',
        string='Wizard',
        ondelete='cascade',
    )
    subject_mark_id = fields.Many2one(
        comodel_name='college.student.subject.mark',
        string='Subject Mark Record',
        
    )
    subject_id = fields.Many2one(
        comodel_name='college.subject',
        string='Subject',
        
    )
    credit = fields.Integer(
        string='Credit',
        related='subject_id.credit',
        readonly=True,
    )
    internal_mark = fields.Float(
        string='Internal Mark',
        default=0.0,
    )
    external_mark = fields.Float(
        string='External Mark',
        default=0.0,
    )
    total_mark = fields.Float(
        string='Total Mark',
        compute='_compute_total_mark',
    )
    grade_point = fields.Float(
        string='Grade Point',
        compute='_compute_grade_point',
    )

    @api.depends('internal_mark', 'external_mark')
    def _compute_total_mark(self):
        for rec in self:
            rec.total_mark = rec.internal_mark + rec.external_mark

    @api.depends('total_mark')
    def _compute_grade_point(self):
        for rec in self:
            total = rec.total_mark
            if total >= 90:
                rec.grade_point = 10.0
            elif total >= 80:
                rec.grade_point = 9.0
            elif total >= 70:
                rec.grade_point = 8.0
            elif total >= 60:
                rec.grade_point = 7.0
            elif total >= 50:
                rec.grade_point = 6.0
            else:
                rec.grade_point = 0.0

    @api.onchange('internal_mark')
    def _onchange_internal_mark(self):
        if self.internal_mark < 0 or self.internal_mark > 30:
            return {
                'warning': {
                    'title': 'Invalid Internal Mark',
                    'message': f'Internal mark must be between 0 and 30. You entered: {self.internal_mark}'
                }
            }

    @api.onchange('external_mark')
    def _onchange_external_mark(self):
        if self.external_mark < 0 or self.external_mark > 70:
            return {
                'warning': {
                    'title': 'Invalid External Mark',
                    'message': f'External mark must be between 0 and 70. You entered: {self.external_mark}'
                }
            }