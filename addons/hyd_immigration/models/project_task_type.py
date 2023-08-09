from odoo import api, fields, models


class ProjectTaskType(models.Model):
	_inherit = "project.task.type"

	check_ids = fields.Many2many(
	    comodel_name='task.checklist',
	    string='Check list for this stage',
	    relation="tasktype_to_checklist"
	)
 