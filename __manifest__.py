{
    "name": "College Student Management",
    "version": '18.0',
    "author": 'Charan',
    "license": 'OPL-1',
    "installable": True,
    "application": True,
    "depends":['base','mail'],
    "data":
        [
            'security/ir.model.access.csv',
            'views/college_student_subject_mark_view.xml',
            'views/college_department_view.xml',
            'views/college_subject_view.xml',
            'views/college_student_view.xml'

        ],
}