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
            print "current task " + str(line.task_work_line_id)
            taskWorkObj = self.pool.get('project.task.work')
            taskWorkLines =  taskWorkObj.search(cr, uid, [('id', '=', line.task_work_line_id)], context=context)
            print str(taskWorkLines)
            # Delete work from task too
            if len(taskWorkLines) > 0:
                taskWorkObj.unlink(cr, uid, taskWorkLines, context)
                
        res = super(analytic_timesheet_task, self).unlink(cr, uid, ids, context=context)
        return res
        
    def create(self, cr, uid, vals, context=None):
        logger.log(logging.INFO, "creating task work")
        print str(vals)
        # Create task work
        project = vals.get('project_id') or False
        task = vals.get('task') or False
        print vals['unit_amount']
        #print vals['task']
        if project or task:
            logger.log(logging.INFO, "creating new work line for task")
            description =  vals['name']
            date = vals['date']
            unit_amount = vals['unit_amount']
            taskWorkObj = self.pool.get('project.task.work')
            
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
        taskWorkObj = self.pool.get('project.task.work')
        
        description =  vals.get('name') or line.name
        date = vals.get('date') or line.date
        unit_amount = vals.get('unit_amount') or line.unit_amount
        project = vals.get('project_id') or False
        task = vals.get('name') or False
        
        workVals = {
            'name': description,
            'project_id': project,
            'task_id': task,
            'date': date,
            'hours': unit_amount,
            'user_id': uid,
        }
        
        # if project or task has changed remove old work from previous task
        if project or task:
            logger.log(logging.INFO, "project or task changed")
            # remove old task work and create new one
            taskWorkObj.unlink(cr, uid, currentWorkLineID, context)
            currentWorkLineID = taskWorkObj.create(cr, uid, workVals, context)
            vals['task_work_line_id'] = currentWorkLineID
        elif currentWorkLineID != 0:
            # write to old task work
            taskWorkLines = taskWorkObj.search(cr, uid, [('id', '=', currentWorkLineID)], context=context)
            print 'task work lines found ' + str(taskWorkLines)
            if len(taskWorkLines) > 0:
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
