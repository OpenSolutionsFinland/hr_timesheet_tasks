from osv import fields, osv
from openerp.tools.translate import _

import logging

logger = logging.getLogger(__name__)

class analytic_timesheet_task(osv.osv):
    _name="hr.analytic.timesheet"
    _inherit="hr.analytic.timesheet"
    
    
    def write(self, cr, uid, ids, vals, context=None):
        #Your code goes here
        logger.log(logging.INFO, "saving task work")
        print str(ids)
        if hasattr(vals, 'task'):
            taskObj = self.pool.get('project.task')
            task = taskObj.browse(cr, uid, vals['task'], context)
            print 'task work lines: ' + str(task.work_ids)
        res = super(analytic_timesheet_task, self).write(cr, uid, ids, vals, context=context)
        return res
        
    _columns={
        'task_work_line_id': fields.integer('Task work line in the selected task'),
        'project_id': fields.many2one('project.project', 'Project'),
        'task': fields.many2one('project.task', 'Project Task'),
    }
    
    
analytic_timesheet_task()
