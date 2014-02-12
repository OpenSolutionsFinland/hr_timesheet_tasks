from osv import fields, osv

'''
class timesheet_task(osv.osv):
    _name='hr_timesheet_sheet.sheet'
    _inherit='hr_timesheet_sheet.sheet'
    
    def write(self, cr, uid, ids, vals, context=None):
        #Your code goes here
        res = super(timesheet_task, self).write(cr, uid, ids, vals, context=context)
        return res
        
    _columns={
        'task_id': fields.many2one('project.task', 'Project Task')#fields.related('line_id', 'workcenter', type='many2one', relation="project.task", string="Task"),
    }

timesheet_task()
'''
'''
class analytic_line(osv.osv):
    _name="account.analytic.line"
    _inherit="account.analytic.line"
    
    _columns={
        'task': fields.many2one('project.task', 'Project Task'),
    }
    
analytic_line()
'''

class analytic_timesheet_task(osv.osv):
    _name="hr.analytic.timesheet"
    _inherit="hr.analytic.timesheet"
    
    
    def write(self, cr, uid, ids, vals, context=None):
        #Your code goes here
        
        res = super(analytic_timesheet_task, self).write(cr, uid, ids, vals, context=context)
        return res
        
    _columns={
        'task': fields.many2one('project.task', 'Project Task'),
    }
    
analytic_timesheet_task()
