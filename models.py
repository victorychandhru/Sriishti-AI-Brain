"""
SRISHTI AI OS - Database Models
Complete data schema for multi-brain AI system
"""

from datetime import datetime
from backend.app import db
import json

class User(db.Model):
    """User model for authentication and profile management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    messages = db.relationship('Message', backref='user', lazy=True)
    actions = db.relationship('Action', backref='user', lazy=True)
    agents = db.relationship('Agent', backref='user', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'is_active': self.is_active
        }

class Message(db.Model):
    """Message model for chat history and logging"""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text)
    message_type = db.Column(db.String(50), default='text')  # text, image, video, audio, code
    brain_used = db.Column(db.String(50))  # language, vision, video, voice, agent, reasoning, creative, world_model
    model_name = db.Column(db.String(100))
    tokens_input = db.Column(db.Integer, default=0)
    tokens_output = db.Column(db.Integer, default=0)
    execution_time = db.Column(db.Float)  # milliseconds
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    metadata = db.Column(db.JSON)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content': self.content,
            'response': self.response,
            'type': self.message_type,
            'brain': self.brain_used,
            'model': self.model_name,
            'tokens': {'input': self.tokens_input, 'output': self.tokens_output},
            'execution_time': self.execution_time,
            'created_at': self.created_at.isoformat(),
            'metadata': self.metadata
        }

class Action(db.Model):
    """Action model for tracking user and system actions"""
    __tablename__ = 'actions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action_type = db.Column(db.String(100), nullable=False)  # generate_image, create_doc, etc.
    status = db.Column(db.String(20), default='pending')  # pending, processing, completed, failed
    input_data = db.Column(db.JSON)
    output_data = db.Column(db.JSON)
    error_message = db.Column(db.Text)
    execution_time = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type': self.action_type,
            'status': self.status,
            'input': self.input_data,
            'output': self.output_data,
            'error': self.error_message,
            'execution_time': self.execution_time,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class Log(db.Model):
    """Log model for comprehensive system logging"""
    __tablename__ = 'logs'
    
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(20))  # INFO, WARNING, ERROR, DEBUG
    message = db.Column(db.Text)
    source = db.Column(db.String(100))  # which component logged this
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    metadata = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'level': self.level,
            'message': self.message,
            'source': self.source,
            'user_id': self.user_id,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat()
        }

class Agent(db.Model):
    """Agent model for tracking agent executions"""
    __tablename__ = 'agents'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    agent_name = db.Column(db.String(100), nullable=False)  # Super Agent, AI Chat, etc.
    agent_type = db.Column(db.String(50))
    status = db.Column(db.String(20), default='idle')  # idle, running, completed, failed
    input_prompt = db.Column(db.Text)
    output_result = db.Column(db.Text)
    execution_time = db.Column(db.Float)
    tokens_used = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    metadata = db.Column(db.JSON)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.agent_name,
            'type': self.agent_type,
            'status': self.status,
            'input': self.input_prompt,
            'output': self.output_result,
            'execution_time': self.execution_time,
            'tokens': self.tokens_used,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'metadata': self.metadata
        }

class Notification(db.Model):
    """Notification model for real-time alerts"""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200))
    message = db.Column(db.Text)
    notification_type = db.Column(db.String(50))  # task_started, task_completed, task_failed, alert
    related_id = db.Column(db.Integer)  # ID of related action/agent/message
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_at = db.Column(db.DateTime)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'message': self.message,
            'type': self.notification_type,
            'related_id': self.related_id,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat(),
            'read_at': self.read_at.isoformat() if self.read_at else None
        }

class CRM(db.Model):
    """CRM model for business automation and lead management"""
    __tablename__ = 'crm'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    contact_name = db.Column(db.String(200))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    company = db.Column(db.String(200))
    status = db.Column(db.String(50))  # lead, prospect, customer, inactive
    notes = db.Column(db.Text)
    last_contact = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    metadata = db.Column(db.JSON)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.contact_name,
            'email': self.email,
            'phone': self.phone,
            'company': self.company,
            'status': self.status,
            'notes': self.notes,
            'last_contact': self.last_contact.isoformat() if self.last_contact else None,
            'created_at': self.created_at.isoformat(),
            'metadata': self.metadata
        }

class Workflow(db.Model):
    """Workflow model for business process automation"""
    __tablename__ = 'workflows'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    workflow_name = db.Column(db.String(200))
    description = db.Column(db.Text)
    steps = db.Column(db.JSON)  # Array of workflow steps
    status = db.Column(db.String(20), default='active')  # active, paused, completed
    execution_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_executed = db.Column(db.DateTime)
    metadata = db.Column(db.JSON)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.workflow_name,
            'description': self.description,
            'steps': self.steps,
            'status': self.status,
            'execution_count': self.execution_count,
            'created_at': self.created_at.isoformat(),
            'last_executed': self.last_executed.isoformat() if self.last_executed else None,
            'metadata': self.metadata
        }

class Analytics(db.Model):
    """Analytics model for system performance tracking"""
    __tablename__ = 'analytics'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    metric_name = db.Column(db.String(100))
    metric_value = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    metadata = db.Column(db.JSON)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'metric': self.metric_name,
            'value': self.metric_value,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata
        }
