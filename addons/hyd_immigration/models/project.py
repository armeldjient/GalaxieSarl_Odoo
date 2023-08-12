from odoo import api, fields, models


class ProjectTaskType(models.Model):
	_inherit = "project.project"

	task_count = fields.Integer(compute='_compute_task_count', string="Task Count")

	def action_view_procedures(self):
        action = self.env['ir.actions.act_window'].with_context({'active_id': self.id})._for_xml_id('project.act_project_project_2_project_task_all')
        action['display_name'] = _("%(name)s", name=self.name)
        context = action['context'].replace('active_id', str(self.id))
        context = ast.literal_eval(context)
        context.update({
            'create': self.active,
            'active_test': self.active
            })
        action['context'] = context
        return action

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
 