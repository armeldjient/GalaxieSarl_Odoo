from odoo import api, fields, models, _


class ProjectTask(models.Model):
    _inherit = "project.task"

    invoicesp_ids = fields.One2many(
        comodel_name='account.move',
        inverse_name='taskp_id',
        string='Invoice',
    )
    amount_invoice = fields.Monetary(
        string='Amount Invoice',
        compute="_compute_amount_invoice"
    )
    image_dossier = fields.Image(
        name="Image procedure")
    checklist_progress = fields.Float(
        compute="checklist_progress_imm", string='Progress',
        store=True, default=0.0
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        related="company_id.currency_id"
    )

    def _compute_amount_invoice(self):
        for rec in self:
            rec.amount_invoice = sum(rec.invoicesp_ids.mapped("amount_total"))

    def open_invoices(self):
        self.ensure_one()

        action = self.env["ir.actions.actions"]._for_xml_id("hyd_immigration.open_view_invoice_task_imm")
        action['name'] = _("Depenses procedures"),
        action['domain'] = [('id', 'in', self.invoicesp_ids.ids)]
        return action

    def add_expense(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("hyd_immigration.action_add_expense_task_wizard")
        action['context'] = {'default_task_id': self.id}
        return action

    @api.depends('task_checklist', 'stage_id')
    def checklist_progress_imm(self):
        checklist = self.env['task.checklist'].search([])
        for rec in self:

            stage_checklist = checklist.filtered(lambda x: not x.optional and x.id in rec.stage_id.check_ids.ids)
            total_len = len(stage_checklist)
            if total_len != 0:
                check_list_len = len(rec.task_checklist.filtered(
                    lambda x: not x.optional and rec.stage_id.id in x.task_types_ids.ids))
                rec.update({'checklist_progress': (check_list_len * 100) / total_len})
            else:
                rec.checklist_progress = 0
