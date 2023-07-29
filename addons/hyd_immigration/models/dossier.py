from odoo import api, fields, models


class Dossier(models.Model):
    _inherit = ['mail.thread', 'mail.activity.mixin']
	_name = "hyd_immigration.dossier"

	name = fields.Char(string='Libelle du dossier')
	partner_id = fields.Many2one(
	    comodel_name='res.partner',
	    string='Candidat',
	)
	date_start = fields.Date(
	    string='Field Label'
	)
	check_step_ids = fields.Many2many(
	    comodel_name='hyd_immigration.check_process',
	    string='Check Done',
	)
	stage_id = fields.Many2one(
		comodel_name='hyd_immigration.stage', string='Stage', ondelete='restrict',
        tracking=True,
        # default=_default_stage_id,
        # group_expand='_read_group_stage_ids'
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
    )


class DossierCharge(models.Model):
	_name = "hyd_immigration.dossier_charge"

	date = fields.Date(string='Date')
	product_id = fields.Many2one(
	    comodel_name='product.product',
	    string='Produit',
	)
	name = fields.Char(string='Description')
	quantity = fields.Float(string='Uantity')
	uom_id_id = fields.Many2one(
	    comodel_name='product.product',
	    string='Produit',
	)
	subtotal = fields.Float(
	    string='Subtotal',
	)
	total_tax = fields.Float(
	    string='Total tax',
	)
	price_total = fields.Float(
	    string='Total',
	)


class DossierRevenu(models.Model):
	_name = "hyd_immigration.dossier_revenu"

	date = fields.Date(string='Date')
	product_id = fields.Many2one(
	    comodel_name='product.product',
	    string='Produit',
	)
	name = fields.Char(string='Description')
	quantity = fields.Float(string='Uantity')
	uom_id_id = fields.Many2one(
	    comodel_name='product.product',
	    string='Produit',
	)
	subtotal = fields.Float(
	    string='Subtotal',
	)
	field_name = fields.Float(
	    string='Total tax',
	)
	price_total = fields.Float(
	    string='Total',
	)
