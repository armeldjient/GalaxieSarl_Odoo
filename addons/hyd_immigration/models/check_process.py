from odoo import api, fields, models


class CheckProcess(models.Model):
    # _inherit = ['mail.thread', 'mail.activity.mixin']
	_name = "hyd_immigration.check_process"

	name = fields.Char(string='Libelle du dossier')
	description = fields.Text(string='Description')
