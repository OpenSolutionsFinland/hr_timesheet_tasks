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
        print str(vals)
        currentWorkLineID = 0
        #try:
        lineObj = self.pool.get('hr.analytic.timesheet')
        line = lineObj.browse(cr, uid, ids, context)[0]
        currentWorkLineID = line.task_work_line_id
        
        if line.project_id and line.task:
            taskObj = self.pool.get('project.task')
            task = taskObj.browse(cr, uid, line.task.id, context)
            taskWorkObj = self.pool.get('project.task.work')
            
            description =  vals['name'] if hasattr(vals, 'name') else line.name
            date = vals['date'] if hasattr(vals, 'date') else line.date
            unit_amount = vals['unit_amount'] if hasattr(vals, 'unit_amount') else line.unit_amount
            project = vals['project_id'] if hasattr(vals, 'project_id') else line.project_id.id
            task = vals['task'] if hasattr(vals, 'task') else line.task.id
        
            workVals = {
                'name': description,
                'project_id': project,
                'task_id': task,
                'date': date,
                'hours': unit_amount,
                'user_id': uid,
            }
            
            if currentWorkLineID == 0:
                currentWorkLineID = taskWorkObj.create(cr, uid, workVals, context)
            # if project or task has changed remove old work from previous task
            elif hasattr(vals, 'project_id') or hasattr(vals, 'task'):
                logger.log(logging.INFO, "project or task changed")
                # remove old task work
                taskWorkObj.unlink(cr, uid, currentWorkLineID, context)
            
                currentWorkLineID = taskWorkObj.create(cr, uid, workVals, context)
            else:
                # write to old task work
                taskWorkObj.write(cr, uid, currentWorkLineID, workVals, context)
       # except e:
    #        logger.log(logging.ERROR, e)
      #      pass
        
        vals['task_work_line_id'] = currentWorkLineID
        res = super(analytic_timesheet_task, self).write(cr, uid, ids, vals, context=context)
        return res
        
    _columns={
        'task_work_line_id': fields.integer('Task work line in the selected task'),
        'project_id': fields.many2one('project.project', 'Project'),
        'task': fields.many2one('project.task', 'Project Task'),
    }
    
    _defaults = {
        'task_work_line_id': 0,
    }
    
analytic_timesheet_task()
