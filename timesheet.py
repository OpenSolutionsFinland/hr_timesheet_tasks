from osv import fields, osv
from openerp.tools.translate import _

import logging

logger = logging.getLogger(__name__)

class analytic_timesheet_task(osv.osv):
    _name="hr.analytic.timesheet"
    _inherit="hr.analytic.timesheet"
    
    # Delete method override
    def unlink(self, cr, uid, ids, context=None):
        logger.log(logging.INFO, "deleting task work")
        lineObj = self.pool.get('hr.analytic.timesheet')
        line = lineObj.browse(cr, uid, ids, context)[0]
        if line.task_work_line_id != 0:
            # Delete work from task too
            self.pool.get('project.task.work').unlink(cr, uid, line.task_work_line_id, context)
        res = super(analytic_timesheet_task, self).unlink(cr, uid, ids, context=context)
        return res
        
    def create(self, cr, uid, vals, context=None):
        logger.log(logging.INFO, "creating task work")
        print str(vals)
        # Create task work
        print vals['project_id']
        print vals['task']
        if hasattr(vals, 'project_id') and hasattr(vals, 'task'):
            logger.log(logging.INFO, "creating new work line for task")
            description =  vals['name']
            date = vals['date']
            unit_amount = vals['unit_amount']
            project = vals['project_id']
            task = vals['task']
    
            workVals = {
                'name': description,
                'project_id': project,
                'task_id': task,
                'date': date,
                'hours': unit_amount,
                'user_id': uid,
            }
        
            currentWorkLineID = taskWorkObj.create(cr, uid, workVals, context)
            vals['task_work_line_id'] = currentWorkLineID
        
        res = super(analytic_timesheet_task, self).create(cr, uid, vals, context=context)
        return res
        
    def write(self, cr, uid, ids, vals, context=None):
        logger.log(logging.INFO, "updating task work")
        print str(ids)
        print str(vals)

        lineObj = self.pool.get('hr.analytic.timesheet')
        line = lineObj.browse(cr, uid, ids, context)[0]
        currentWorkLineID = line.task_work_line_id
        
        description =  vals['name'] if hasattr(vals, 'name') else line.name
        date = vals['date'] if hasattr(vals, 'date') else line.date
        unit_amount = vals['unit_amount'] if hasattr(vals, 'unit_amount') else line.unit_amount
        project = vals['project_id'] if hasattr(vals, 'project_id') else None
        task = vals['task'] if hasattr(vals, 'task') else None
    
        workVals = {
            'name': description,
            'project_id': project,
            'task_id': task,
            'date': date,
            'hours': unit_amount,
            'user_id': uid,
        }
        
        if line.project_id and line.task:
            taskObj = self.pool.get('project.task')
            task = taskObj.browse(cr, uid, line.task.id, context)
            taskWorkObj = self.pool.get('project.task.work')
            
        # if project or task has changed remove old work from previous task
        elif hasattr(vals, 'project_id') or hasattr(vals, 'task'):
            logger.log(logging.INFO, "project or task changed")
            # remove old task work
            taskWorkObj.unlink(cr, uid, currentWorkLineID, context)
            currentWorkLineID = taskWorkObj.create(cr, uid, workVals, context)
        else:
            # write to old task work
            taskWorkObj.write(cr, uid, currentWorkLineID, workVals, context)
        
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
