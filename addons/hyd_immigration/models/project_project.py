import calendar
import random
from datetime import datetime, date

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class ProjectTaskType(models.Model):
    _inherit = "project.project"

    # task_count = fields.Integer(compute='_compute_task_count', string="Task Count")
    task_expenses_ids = fields.One2many(
        comodel_name='account.move',
        inverse_name='task_project_id',
        string='Project task expense',
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Produit Honoraire',
    )

    # def action_view_procedures(self):
    #     action = self.env['ir.actions.act_window'].with_context({'active_id': self.id})._for_xml_id('project.act_project_project_2_project_task_all')
    #     action['display_name'] = _("%(name)s", name=self.name)
    #     context = action['context'].replace('active_id', str(self.id))
    #     context = ast.literal_eval(context)
    #     context.update({
    #         'create': self.active,
    #         'active_test': self.active
    #         })
    #     action['context'] = context
    #     return action

    @api.model
    def get_task_data(self):
        """

        Summery:
            when the page is loaded get the data from different models and transfer to the js file.
            return a dictionary variable.
        return:
            type:It is a dictionary variable. This dictionary contain data that affecting project task table.

        """
        self._cr.execute('''select project_task.name as task_name,pro.name as project_name from project_task
          Inner join project_project as pro on project_task.project_id = pro.id 
          Left join project_task_type as stage on project_task.stage_id = stage.id
          WHERE stage.is_closed IS null AND stage.is_cancel IS null
          ORDER BY stage.create_date DESC
          ''')
        data = self._cr.fetchall()
        project_name = []
        for rec in data:
            b = list(rec)
            project_name.append(b)
        return {
            'project': project_name
        }

    @api.model
    def get_tiles_data(self):
        """

        Summery:
            when the page is loaded get the data from different models and transfer to the js file.
            return a dictionary variable.
        return:
            type:It is a dictionary variable. This dictionary contain data that affecting the dashboard view.

        """
        all_project = self.env['project.project'].search([])
        all_task = self.env['project.task'].search([])
        analytic_project = self.env['account.analytic.line'].search([])
        report_project = self.env['project.profitability.report'].search([])
        to_invoice = sum(report_project.mapped('amount_untaxed_to_invoice'))
        invoice = sum(report_project.mapped('amount_untaxed_invoiced'))
        timesheet_cost = sum(report_project.mapped('timesheet_cost'))
        other_cost = sum(report_project.mapped('expense_cost'))
        profitability = to_invoice + invoice + timesheet_cost + other_cost
        total_time = sum(analytic_project.mapped('unit_amount'))
        employees = self.env['hr.employee'].search([])

        task = self.env['project.task'].search_read([
            ('sale_order_id', '!=', False)
        ], ['sale_order_id'])
        task_so_ids = [o['sale_order_id'][0] for o in task]
        sale_orders = self.mapped('sale_line_id.order_id') | self.env[
            'sale.order'].browse(task_so_ids)
        sale_list = [rec.id for rec in sale_orders]
        project_stage_ids = self.env['project.project.stage'].search([])
        project_stage_list = []
        for project_stage_id in project_stage_ids:
            total_projects = self.env['project.project'].search_count(
                [('stage_id', '=', project_stage_id.id)])
            project_stage_list.append({
                'name': project_stage_id.name,
                'projects': total_projects,
            })
        all_task_ended = all_task.filtered(lambda x: x.stage_id.is_closed)
        all_task_cancelled = all_task.filtered(lambda x: x.stage_id.is_cancel)
        return {
            'total_projects': len(all_project),
            'total_tasks': len(all_task),
            'total_tasks_ended': len(all_task_ended),
            'total_tasks_cancelled': len(all_task_cancelled),
            'total_hours': total_time,
            'total_profitability': profitability,
            'total_employees': len(employees),
            'total_sale_orders': len(sale_orders),
            'project_stage_list': project_stage_list,
            'sale_list': sale_list
        }

    @api.model
    def get_expense_this_year(self):
        """

        Summery:
            when the filter is applied get the data for the profitable graph.
        return:
            type:It is a dictionary variable. This dictionary contain data for  profitable graph.

        """

        month_list = []
        for i in range(11, -1, -1):
            l_month = datetime.now() - relativedelta(months=i)
            text = format(l_month, '%B')
            month_list.append(text)

        projects = self.search([])
        month = []
        profit = []
        income = []
        for _month in month_list:
            today = datetime.now()
            date_init_year = datetime.now() - relativedelta(months=12)
            d_init_date = date.today() - relativedelta(months=12)
            payments = self.env["account.payment"].search([('date', '>=', date_init_year)])
        
            current_invoice = projects.mapped("task_expenses_ids").filtered(
                lambda x: x.invoice_date.strftime("%B") == _month and x.invoice_date > d_init_date)
            _expense = sum(current_invoice.filtered(lambda x: not x.frais_honoraire).mapped("amount_total"))
            _income = sum(payments.filtered(
                lambda x: x.date.strftime("%B") == _month and x.date > d_init_date).filtered(
                lambda x: any(x.mapped("reconciled_invoice_ids.frais_honoraire"))).mapped('amount'))
            month.append(_month)
            profit.append(_expense)
            income.append(_income)

        return {
            'profit': profit,
            'income': income,
            'month': month,
        }

    # def _compute_task_count(self):
    #     domain = [('project_id', 'in', self.ids), ('is_closed', '=', False)]
    #     fields = ['project_id', 'display_project_id:count']
    #     groupby = ['project_id']
    #     task_data = self.env['project.task']._read_group(domain, fields, groupby)
    #     result_wo_subtask = defaultdict(int)
    #     result_with_subtasks = defaultdict(int)
    #     for data in task_data:
    #         result_wo_subtask[data['project_id'][0]] += data['display_project_id']
    #         result_with_subtasks[data['project_id'][0]] += data['project_id_count']
    #     task_all_data = self.env['project.task'].with_context(active_test=False)._read_group(domain, fields, groupby)
    #     all_tasks_wo_subtasks = defaultdict(int)
    #     for data in task_all_data:
    #         all_tasks_wo_subtasks[data['project_id'][0]] += data['display_project_id']

    #     for project in self:
    #         project.task_count = result_wo_subtask[project.id]
    #         project.task_count_with_subtasks = result_with_subtasks[project.id]
    #         if not project.active:
    #             project.task_count = all_tasks_wo_subtasks[project.id]
 