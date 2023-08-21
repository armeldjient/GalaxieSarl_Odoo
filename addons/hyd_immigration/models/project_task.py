from odoo import api, fields, models, _
from odoo.exceptions import UserError


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
    amount_honoraire = fields.Monetary(
        string='Honoraire',
        compute="_compute_amount_invoice"
    )
    honoraire_paye = fields.Monetary(
        string='Honoraire payes',
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
            rec.amount_invoice = sum(rec.invoicesp_ids.filtered(lambda x: not x.frais_honoraire).mapped("amount_total"))
            rec.amount_honoraire = sum(rec.invoicesp_ids.filtered(lambda x: x.frais_honoraire).mapped("amount_total"))
            restant = sum(rec.invoicesp_ids.filtered(lambda x: x.frais_honoraire).mapped("amount_residual"))
            rec.honoraire_paye = rec.amount_honoraire - restant

    def open_invoices(self):
        self.ensure_one()
        frais_honoraire = self.env.context.get("frais_honoraire", False)
        action = self.env["ir.actions.actions"]._for_xml_id("hyd_immigration.open_view_invoice_task_imm")
        action['name'] = _("Depenses procedures"),
        inv_ids = self.invoicesp_ids.filtered(lambda x: x.frais_honoraire == frais_honoraire).ids
        action['domain'] = [('id', 'in', inv_ids)]
        return action

    def add_expense(self):
        self.ensure_one()
        frais_honoraire = self.env.context.get("frais_honoraire", False)
        action = self.env["ir.actions.actions"]._for_xml_id("hyd_immigration.action_add_expense_task_wizard")
        action['context'] = {'default_task_id': self.id}
        if frais_honoraire:
            product = self.project_id.product_id
            if not product:
                raise UserError(_("veuillez renseigner le produit honoraire dans la categorie"))
            action['context'].update({'default_frais_honoraire': frais_honoraire, 'default_honoraire': product.id})

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

    @api.model
    def get_task_amount(self):
        """

        Summery:
            when the page is loaded get the data for the timesheet graph.
        return:
            type:It is a list. This list contain data that affecting the graph of employees.

        """

        tasks_customer = []
        task_amount = []
        tasks = self.search([])
        for customer in tasks.mapped("partner_id"):
            tasks_customer.append(customer.name)
            amount = sum(
                tasks.filtered(lambda x: x.partner_id and x.partner_id.id == customer.id).mapped("amount_invoice"))
            task_amount.append(amount)
        final = [task_amount, tasks_customer]
        return final
