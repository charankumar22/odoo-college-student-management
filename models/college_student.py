from odoo import fields,models,api

class collegestudent(models.Model):
    _name = 'college.student'
    _description = 'College Student'
    _inherit = ['mail.thread','mail.activity.mixin']

    name = fields.Char(string="Student Name",required=True)
    roll_number = fields.Char(string="Roll Number",required=True)
    dob = fields.Date(string="Date of Birth",required=True)
    gender = fields.Selection([('male','Male'),('female','Female'),('other','Other')],string='Gender',required=True)
    department_id = fields.Many2one('college.department',string='Department ID',required=True)
    semester = fields.Selection([('semester 1','Semester 1'),('semester 2','Semester 2'),('semester 3','Semester 3'),('semester 4','Semester 4'),('semester 5','Semester 5'),('semester 6','Semester 6'),('semester 7','Semester 7'),('semester 8','Semester 8')],required=True,string='Semester')
    state = fields.Selection([('draft','Draft'),('confirmed','Confirmed')],default='draft',string='state',tracking=True)
    remarks = fields.Text(string='Remarks')
    subject_mark_ids = fields.One2many('college.student.subject.mark','student_id',string='Subject Marks')
    total_marks = fields.Float(string='Total Marks',compute='_compute_total_marks',store=True)

    cgpa = fields.Float(string='CGPA',compute='_compute_cgpa',store=True,tracking=True)

    @api.depends('subject_mark_ids.total_mark')
    def _compute_total_marks(self):
        for student in self:
            student.total_marks = sum(student.subject_mark_ids.mapped('total_mark'))
    
    @api.depends('subject_mark_ids.grade_point','subject_mark_ids.credit')
    def _compute_cgpa(self):
        for student in self:
            marks = student.subject_mark_ids
            total_credit = sum(marks.mapped('credit'))
            if total_credit:
                weighted_sum = sum(m.grade_point * m.credit for m in marks)
                student.cgpa = weighted_sum / total_credit
            else:
                student.cgpa = 0.0

    @api.onchange('department_id','semester')
    def _onchange_department_semester(self):
        self.subject_mark_ids = [(5,0,0)]

        if self.department_id:
            subjects = self.department_id.subject_ids
            new_lines = []
            for subject in subjects:
                new_lines.append((0,0,{'subject_id':subject.id,'internal_mark':0.0,'external_mark':0.0}))
            self.subject_mark_ids = new_lines

    def action_confirm(self):
        for student in self:
            student.write({'state':'confirmed'})
            
    def action_reset(self):
        for student in self:
            student.write({'state':'draft'})

    def action_open_marks_wizard(self):
        self.ensure_one()
        
        return {
            'name': 'Edit Subject Marks',
            'type': 'ir.actions.act_window',
            'res_model': 'student.marks.wizard',
            'view_mode': 'form',
            'views': [(False, 'form')],
            'target': 'new',
            # 'domain': [('student_id', '=', self.id)],
            'context': {
                'default_student_id': self.id,
                'create': True,
                'edit': True,
                'delete': True,
            },
        }
