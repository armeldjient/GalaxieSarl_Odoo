from odoo import api, fields, models, _


class ProjectTask(models.Model):
    _inherit = "project.task"

    invoicesp_ids = fields.One2many(
        comodel_name='account.move',
        inverse_name='taskp_id',
        string='Invoice',
    )
    amount_invoice = fields.Float(
        string='Amount Invoice',
        compute="_compute_amount_invoice"
    )
    image_dossier = fields.Image(
        name="Image procedure")

    def _compute_amount_invoice(self):
        for rec in self:
            rec.amount_invoice = sum(rec.invoicesp_ids.mapped("amount_total"))

    def open_invoices(self):
        self.ensure_one()

        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
        action['name'] = _("Depenses procedures"),
        action['domain'] = [('id', 'in', self.invoicesp_ids.ids)]
        return action

    def add_expense(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("hyd_immigration.action_add_expense_task_wizard")
        action['context'] = {'default_task_id': self.id}
        return action
