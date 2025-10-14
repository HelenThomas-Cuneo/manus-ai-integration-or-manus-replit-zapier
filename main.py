#!/usr/bin/env python3
"""
Manus.ai Integration - Replit Webhook Receiver
This Flask application receives webhooks from Manus.ai and can trigger agent tasks.
"""

from flask import Flask, request, jsonify
import os
import requests
import logging
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Manus.ai API configuration
MANUS_API_KEY = os.environ.get('MANUS_API_KEY', '')
MANUS_API_BASE_URL = 'https://api.manus-ai.com'


@app.route('/')
def home():
    """Home endpoint with basic information"""
    return jsonify({
        'service': 'Manus.ai Integration',
        'status': 'running',
        'endpoints': {
            'webhook': '/webhook',
            'execute': '/execute',
            'health': '/health'
        }
    })


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'api_key_configured': bool(MANUS_API_KEY)
    })


@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Webhook endpoint to receive data from external services
    This can be used to trigger Manus.ai tasks based on external events
    """
    try:
        # Get the JSON payload
        payload = request.get_json()
        
        logger.info(f"Received webhook: {payload}")
        
        # Process the webhook payload
        # You can customize this logic based on your needs
        if payload and 'trigger' in payload:
            trigger_type = payload.get('trigger')
            
            if trigger_type == 'execute_task':
                # Extract task details from payload
                task_goal = payload.get('goal', 'No goal specified')
                task_inputs = payload.get('inputs', [])
                
                # Execute Manus.ai task
                result = execute_manus_task(task_goal, task_inputs)
                
                return jsonify({
                    'status': 'success',
                    'message': 'Task executed',
                    'result': result
                }), 200
        
        return jsonify({
            'status': 'received',
            'message': 'Webhook received successfully',
            'payload': payload
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@app.route('/execute', methods=['POST'])
def execute():
    """
    Direct endpoint to execute Manus.ai tasks
    Expects JSON payload with 'goal' and optional 'inputs' and 'constraints'
    """
    try:
        # Get the JSON payload
        payload = request.get_json()
        
        if not payload or 'goal' not in payload:
            return jsonify({
                'status': 'error',
                'message': 'Missing required field: goal'
            }), 400
        
        goal = payload.get('goal')
        inputs = payload.get('inputs', [])
        constraints = payload.get('constraints', {})
        
        logger.info(f"Executing Manus.ai task: {goal}")
        
        # Execute the task
        result = execute_manus_task(goal, inputs, constraints)
        
        return jsonify({
            'status': 'success',
            'result': result
        }), 200
        
    except Exception as e:
        logger.error(f"Error executing task: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


def execute_manus_task(goal: str, inputs: list = None, constraints: dict = None):
    """
    Execute a task using the Manus.ai API
    
    Args:
        goal: The task goal/description
        inputs: Optional list of inputs for the task
        constraints: Optional constraints for the task
    
    Returns:
        dict: The API response
    """
    if not MANUS_API_KEY:
        raise ValueError("MANUS_API_KEY not configured in environment variables")
    
    # Prepare the request
    url = f"{MANUS_API_BASE_URL}/v2/execute"
    headers = {
        'X-API-Key': MANUS_API_KEY,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'goal': goal,
        'inputs': inputs or [],
        'constraints': constraints or {}
    }
    
    try:
        # Make the API request
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"Task executed successfully: {result}")
        
        return result
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        raise


@app.route('/decompose', methods=['POST'])
def decompose():
    """
    Endpoint to decompose a goal into executable steps using Manus.ai
    Expects JSON payload with 'goal' and optional 'context'
    """
    try:
        payload = request.get_json()
        
        if not payload or 'goal' not in payload:
            return jsonify({
                'status': 'error',
                'message': 'Missing required field: goal'
            }), 400
        
        goal = payload.get('goal')
        context = payload.get('context', '')
        
        logger.info(f"Decomposing goal: {goal}")
        
        # Call Manus.ai decompose endpoint
        result = decompose_goal(goal, context)
        
        return jsonify({
            'status': 'success',
            'result': result
        }), 200
        
    except Exception as e:
        logger.error(f"Error decomposing goal: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


def decompose_goal(goal: str, context: str = ''):
    """
    Decompose a goal using the Manus.ai API
    
    Args:
        goal: The goal to decompose
        context: Optional context for the goal
    
    Returns:
        dict: The API response with decomposed steps
    """
    if not MANUS_API_KEY:
        raise ValueError("MANUS_API_KEY not configured in environment variables")
    
    url = f"{MANUS_API_BASE_URL}/v2/decompose"
    headers = {
        'X-API-Key': MANUS_API_KEY,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'goal': goal,
        'context': context
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"Goal decomposed successfully")
        
        return result
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        raise


if __name__ == '__main__':
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

