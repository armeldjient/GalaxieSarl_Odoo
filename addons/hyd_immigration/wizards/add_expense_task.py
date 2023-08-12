# -*- coding: utf-8 -*-
from odoo import api, models, fields
from odoo.fields import Command


class add_expense_wizard(models.TransientModel):
    """Wizard to add expenses in task."""
    _name = 'hyd_immigration.add_expense.wizard'
    _description = 'Add Expense for task'

    task_id = fields.Many2one(
        comodel_name='project.task',
        string='Procedures',
    )
    line_ids = fields.One2many(
        comodel_name='hyd_immigration.add_expense_line.wizard',
        inverse_name='wizard_exp_id',
        string='Lines',
    )

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
            'move_type': 'out_invoice'
        })

        inv_lines = []
        fiscal_position = invoice.fiscal_position_id
        for _line in self.line_ids:
            # accounts = _line.product_id.product_tmpl_id.get_product_accounts(fiscal_pos=fiscal_position)
            # if invoice.is_sale_document(include_receipts=True):
            #     # Out invoice.
            #     account = accounts['income']
            # elif invoice.is_purchase_document(include_receipts=True):
            #     # In invoice.
            #     account = accounts['expense']
            # _line_inv = invoice_line_obj.create({
            #     'move_id': invoice.id, 'product_id': _line.product_id.id,
            #     'name': _line.product_id.name, 'quantity': _line.qty,
            #     'price_unit': _line.price, 'product_uom_id': _line.product_id.uom_id.id,
            #     'account_id': account and account.id
            # })
            inv_lines.append(Command.create({
                'move_id': invoice.id, 'product_id': _line.product_id.id,
                'name': _line.product_id.name, 'quantity': _line.qty,
                'price_unit': _line.price, 'product_uom_id': _line.product_id.uom_id.id,
                # 'account_id': account and account.id
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
    qty = fields.Float(string='Quantity', default=1)
    price = fields.Float(string='Price')
    total = fields.Float(string='Total', compute="_compute_total")

    @api.depends("price", "qty")
    def _compute_total(self):
        for rec in self:
            rec.total = rec.qty * rec.price
