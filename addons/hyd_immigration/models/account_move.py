from odoo import api, fields, models


class AccountMove(models.Model):
	_inherit = "account.move"

	taskp_id = fields.Many2one(
	    comodel_name='project.task',
	    string='Task',
	)
