# -*- coding: utf-8 -*-
from odoo import api, models, fields, _
from odoo.fields import Command


class add_expense_wizard(models.TransientModel):
    """Wizard to add expenses in task."""
    _name = 'hyd_immigration.add_expense.wizard'
    _description = 'Add Expense for task'

    task_id = fields.Many2one(
        comodel_name='project.task',
        string='Procedures',
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        related="task_id.company_id.currency_id"
    )
    line_ids = fields.One2many(
        comodel_name='hyd_immigration.add_expense_line.wizard',
        inverse_name='wizard_exp_id',
        string='Lines',
    )
    note = fields.Text(
        string='Note',
        required=True
    )
    frais_honoraire = fields.Boolean(string='Frais honoraire', default=False)

    @api.onchange('frais_honoraire')
    def onchange_frais_honoraire(self):
        self.line_ids.unlink()
        if self.frais_honoraire:
            self.note = _("honoraire de gestion")
            honoraire = self.env.context.get('default_honoraire')
            product = self.env['product.product'].browse(honoraire)
            if product:
                self.update({'line_ids': [Command.create({
                    'product_id': product.id, 'qty': 1, 'price': product.lst_price,
                })]})

    def add_new_expense(self):
        self.ensure_one()
        invoice_obj = self.env["account.move"]
        invoice_line_obj = self.env["account.move.line"]
        company = self.env.company
        currency = company.currency_id
        invoice = invoice_obj.create({
            'partner_id': self.task_id.partner_id.id, 'currency_id': currency.id,
            'date': fields.Date.today(), 'invoice_date': fields.Date.today(),
            'invoice_date_due': fields.Date.today(), 'taskp_id': self.task_id.id,
            'move_type': 'out_invoice', 'resume': self.note,
            'frais_honoraire': self.frais_honoraire
        })

        inv_lines = []
        fiscal_position = invoice.fiscal_position_id
        for _line in self.line_ids:
            inv_lines.append(Command.create({
                'move_id': invoice.id, 'product_id': _line.product_id.id,
                'name': _line.product_id.name, 'quantity': _line.qty,
                'price_unit': _line.price, 'product_uom_id': _line.product_id.uom_id.id,
            }))
        invoice.update({'invoice_line_ids': inv_lines})


class add_expense_line_wizard(models.TransientModel):
    """Wizard to add expenses line in wizard."""
    _name = 'hyd_immigration.add_expense_line.wizard'
    _description = 'Add Expense line for task'

    wizard_exp_id = fields.Many2one(
        comodel_name='hyd_immigration.add_expense.wizard',
        string='Wizard',
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        related="wizard_exp_id.currency_id"
    )
    qty = fields.Float(string='Quantity', default=1)
    price = fields.Monetary(string='Price')
    total = fields.Monetary(string='Total', compute="_compute_total")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        lp_ = self.product_id.lst_price if self.product_id else 0
        self.update({'price': lp_, 'qty': 1})

        

    @api.depends("price", "qty")
    def _compute_total(self):
        for rec in self:
            rec.total = rec.qty * rec.price
