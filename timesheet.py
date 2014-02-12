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
        print str(vals)
        res = super(analytic_timesheet_task, self).write(cr, uid, ids, vals, context=context)
        return res
        
    _columns={
        'project_id': fields.many2one('project.project', 'Project'),
        'task': fields.many2one('project.task', 'Project Task'),
    }
    
analytic_timesheet_task()
