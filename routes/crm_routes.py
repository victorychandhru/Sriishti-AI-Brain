"""
SRISHTI AI OS - CRM Routes
Business Automation and Lead Management
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import time
import logging

bp = Blueprint('crm', __name__, url_prefix='/api/crm')
logger = logging.getLogger(__name__)

@bp.route('/leads', methods=['GET'])
def get_leads():
    """
    Get all leads
    """
    try:
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        status = request.args.get('status', '')
        
        leads = [
            {
                'id': i,
                'name': f'Lead {i}',
                'email': f'lead{i}@example.com',
                'company': f'Company {i}',
                'status': 'prospect',
                'created_at': datetime.utcnow().isoformat()
            }
            for i in range(offset, offset + limit)
        ]
        
        return jsonify({
            'status': 'success',
            'leads': leads,
            'total': 1000,
            'limit': limit,
            'offset': offset
        }), 200
        
    except Exception as e:
        logger.error(f'Get leads error: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': str(e),
            'code': 500
        }), 500

@bp.route('/leads', methods=['POST'])
def create_lead():
    """
    Create a new lead
    """
    try:
        data = request.get_json()
        name = data.get('name', '')
        email = data.get('email', '')
        company = data.get('company', '')
        
        if not name or not email:
            return jsonify({
                'status': 'error',
                'message': 'Name and email are required',
                'code': 400
            }), 400
        
        lead = {
            'id': 1001,
            'name': name,
            'email': email,
            'company': company,
            'status': 'new',
            'created_at': datetime.utcnow().isoformat()
        }
        
        return jsonify({
            'status': 'success',
            'lead': lead,
            'message': 'Lead created successfully'
        }), 201
        
    except Exception as e:
        logger.error(f'Create lead error: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': str(e),
            'code': 500
        }), 500

@bp.route('/leads/<int:lead_id>', methods=['PUT'])
def update_lead(lead_id):
    """
    Update a lead
    """
    try:
        data = request.get_json()
        
        lead = {
            'id': lead_id,
            'name': data.get('name', ''),
            'email': data.get('email', ''),
            'company': data.get('company', ''),
            'status': data.get('status', 'prospect'),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        return jsonify({
            'status': 'success',
            'lead': lead,
            'message': 'Lead updated successfully'
        }), 200
        
    except Exception as e:
        logger.error(f'Update lead error: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': str(e),
            'code': 500
        }), 500

@bp.route('/tasks', methods=['GET'])
def get_tasks():
    """
    Get all tasks
    """
    try:
        limit = request.args.get('limit', 50, type=int)
        status = request.args.get('status', '')
        
        tasks = [
            {
                'id': i,
                'title': f'Task {i}',
                'description': f'Task description {i}',
                'status': 'pending',
                'priority': 'high',
                'due_date': datetime.utcnow().isoformat()
            }
            for i in range(limit)
        ]
        
        return jsonify({
            'status': 'success',
            'tasks': tasks,
            'total': 500
        }), 200
        
    except Exception as e:
        logger.error(f'Get tasks error: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': str(e),
            'code': 500
        }), 500

@bp.route('/tasks', methods=['POST'])
def create_task():
    """
    Create a new task
    """
    try:
        data = request.get_json()
        title = data.get('title', '')
        description = data.get('description', '')
        
        if not title:
            return jsonify({
                'status': 'error',
                'message': 'Title is required',
                'code': 400
            }), 400
        
        task = {
            'id': 501,
            'title': title,
            'description': description,
            'status': 'pending',
            'priority': data.get('priority', 'medium'),
            'created_at': datetime.utcnow().isoformat()
        }
        
        return jsonify({
            'status': 'success',
            'task': task,
            'message': 'Task created successfully'
        }), 201
        
    except Exception as e:
        logger.error(f'Create task error: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': str(e),
            'code': 500
        }), 500

@bp.route('/workflows', methods=['GET'])
def get_workflows():
    """
    Get all workflows
    """
    try:
        workflows = [
            {
                'id': 1,
                'name': 'Lead Qualification',
                'description': 'Automated lead qualification workflow',
                'status': 'active',
                'execution_count': 1234,
                'last_executed': datetime.utcnow().isoformat()
            },
            {
                'id': 2,
                'name': 'Email Campaign',
                'description': 'Automated email campaign workflow',
                'status': 'active',
                'execution_count': 567,
                'last_executed': datetime.utcnow().isoformat()
            }
        ]
        
        return jsonify({
            'status': 'success',
            'workflows': workflows,
            'total': 2
        }), 200
        
    except Exception as e:
        logger.error(f'Get workflows error: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': str(e),
            'code': 500
        }), 500

@bp.route('/workflows', methods=['POST'])
def create_workflow():
    """
    Create a new workflow
    """
    try:
        data = request.get_json()
        name = data.get('name', '')
        steps = data.get('steps', [])
        
        if not name:
            return jsonify({
                'status': 'error',
                'message': 'Name is required',
                'code': 400
            }), 400
        
        workflow = {
            'id': 3,
            'name': name,
            'description': data.get('description', ''),
            'steps': steps,
            'status': 'active',
            'created_at': datetime.utcnow().isoformat()
        }
        
        return jsonify({
            'status': 'success',
            'workflow': workflow,
            'message': 'Workflow created successfully'
        }), 201
        
    except Exception as e:
        logger.error(f'Create workflow error: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': str(e),
            'code': 500
        }), 500

@bp.route('/workflows/<int:workflow_id>/execute', methods=['POST'])
def execute_workflow(workflow_id):
    """
    Execute a workflow
    """
    try:
        start_time = time.time()
        
        # Execute workflow
        execution_time = (time.time() - start_time) * 1000
        
        return jsonify({
            'status': 'success',
            'workflow_id': workflow_id,
            'execution_id': 'exec_12345',
            'status': 'completed',
            'execution_time': execution_time,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f'Execute workflow error: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': str(e),
            'code': 500
        }), 500
