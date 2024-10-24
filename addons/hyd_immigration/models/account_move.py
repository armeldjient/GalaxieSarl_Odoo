from odoo import api, fields, models


class AccountMove(models.Model):
	_inherit = "account.move"

	taskp_id = fields.Many2one(
	    comodel_name='project.task',
	    string='Task',
	)
	task_project_id = fields.Many2one(
	    comodel_name='project.project',
	    related="taskp_id.project_id"
	)
	frais_honoraire = fields.Boolean(string='Frais honoraire', default=False)
	resume = fields.Text(string='Resume')
