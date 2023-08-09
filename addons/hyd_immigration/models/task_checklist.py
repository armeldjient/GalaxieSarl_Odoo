from odoo import api, fields, models


class TaskChecklist(models.Model):
	_inherit = "task.checklist"

	task_types_ids = fields.Many2many(
	    comodel_name='project.task.type',
	    string='Check stage for this list',
	    relation="tasktype_to_checklist"
	)
 