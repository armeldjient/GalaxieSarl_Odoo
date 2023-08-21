import calendar
import random
from datetime import datetime

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
        
            expense = sum(projects.mapped("task_expenses_ids").filtered(
                lambda x: x.invoice_date.strftime("%B") == _month and x.invoice_date.year == 2023).mapped("amount_total"))
            month.append(_month)
            profit.append(expense)
            income.append(0)

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
 