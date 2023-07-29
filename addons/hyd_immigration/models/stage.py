from odoo import api, fields, models


class Stage(models.Model):
    # _inherit = ['mail.thread', 'mail.activity.mixin']
	_name = "hyd_immigration.stage"

	active = fields.Boolean(default=True)
    sequence = fields.Integer(default=50)
    name = fields.Char(string='Libelle du dossier')
	description = fields.Text(string='Description')
    mail_template_id = fields.Many2one('mail.template', string='Email Template', domain=[('model', '=', 'project.project')],
        help="If set, an email will be sent to the customer when the project reaches this step.")
    fold = fields.Boolean('Folded in Kanban', help="This stage is folded in the kanban view.")
