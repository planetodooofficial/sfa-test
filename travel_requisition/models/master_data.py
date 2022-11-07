from odoo import models, fields, api, _


# class DesignationMaster(models.Model):
#     _name = 'designation.master'
#     _rec_name = 'designation_value'
#     designation_value = fields.Char(string='Designation')


class GradeMaster(models.Model):
    _name = 'grade.master'
    _rec_name = 'grade_new'
    grade_new = fields.Char(string='Grade')
    cadre_id = fields.Many2one('cadre.master', 'Cadre ID')
    grade_title_id = fields.Many2one('grade.title.master', 'Grade Title ID')


class CadreMaster(models.Model):
    _name = 'cadre.master'
    _rec_name = 'cadre_new'
    cadre_new = fields.Char('Cadre')


class GradeTitleMaster(models.Model):
    _name = 'grade.title.master'
    _rec_name = 'grade_title_line'
    grade_title_line = fields.Char('Grade Title')


class ModeClassMaster(models.Model):
    _name = 'mode.class.master'
    _rec_name = 'mode_class_line'
    mode_class_line = fields.Char('Mode and Class')
