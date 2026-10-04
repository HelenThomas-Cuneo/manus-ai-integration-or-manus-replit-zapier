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

# WhatsApp Business Cloud API (Meta Graph API) configuration
WHATSAPP_ACCESS_TOKEN = os.environ.get('WHATSAPP_ACCESS_TOKEN', '')
WHATSAPP_PHONE_NUMBER_ID = os.environ.get('WHATSAPP_PHONE_NUMBER_ID', '')
WHATSAPP_VERIFY_TOKEN = os.environ.get('WHATSAPP_VERIFY_TOKEN', '')
WHATSAPP_API_BASE_URL = 'https://graph.facebook.com/v19.0'


@app.route('/')
def home():
    """Home endpoint with basic information"""
    return jsonify({
        'service': 'Manus.ai Integration',
        'status': 'running',
        'endpoints': {
            'webhook': '/webhook',
            'execute': '/execute',
            'health': '/health',
            'decompose': '/decompose',
            'whatsapp_webhook': '/whatsapp/webhook'
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


@app.route('/whatsapp/webhook', methods=['GET', 'POST'])
def whatsapp_webhook():
    """
    WhatsApp Business Cloud API (Meta Graph API) webhook endpoint

    GET: Handles Meta's webhook verification handshake. Meta calls this with
    'hub.mode', 'hub.verify_token' and 'hub.challenge' query params; we must
    echo back 'hub.challenge' when the verify token matches.

    POST: Receives inbound WhatsApp message/status notifications. Optionally
    forwards received text messages to Manus.ai as a task via execute_manus_task.
    """
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        if mode == 'subscribe' and token and WHATSAPP_VERIFY_TOKEN and token == WHATSAPP_VERIFY_TOKEN:
            logger.info("WhatsApp webhook verified successfully")
            return challenge, 200

        logger.warning("WhatsApp webhook verification failed")
        return jsonify({
            'status': 'error',
            'message': 'Verification failed'
        }), 403

    try:
        payload = request.get_json()
        logger.info(f"Received WhatsApp webhook: {payload}")

        messages = extract_whatsapp_messages(payload)

        forwarded = []
        for message in messages:
            text = message.get('text')
            from_number = message.get('from')

            if text:
                try:
                    result = execute_manus_task(
                        goal=f"Respond to WhatsApp message from {from_number}: {text}",
                        inputs=[text]
                    )
                    forwarded.append({'from': from_number, 'result': result})
                except ValueError:
                    # MANUS_API_KEY not configured - still acknowledge the webhook
                    logger.info("Skipping Manus.ai forwarding: MANUS_API_KEY not configured")

        return jsonify({
            'status': 'received',
            'messages': messages,
            'forwarded': forwarded
        }), 200

    except Exception as e:
        logger.error(f"Error processing WhatsApp webhook: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


def extract_whatsapp_messages(payload: dict):
    """
    Extract inbound text messages from a WhatsApp Cloud API webhook payload

    Args:
        payload: The raw webhook payload sent by Meta

    Returns:
        list: A list of dicts with 'from', 'id' and 'text' keys for each message
    """
    messages = []

    if not payload:
        return messages

    for entry in payload.get('entry', []):
        for change in entry.get('changes', []):
            value = change.get('value', {})
            for message in value.get('messages', []):
                messages.append({
                    'id': message.get('id'),
                    'from': message.get('from'),
                    'text': message.get('text', {}).get('body')
                })

    return messages


def send_whatsapp_message(to: str, message: str):
    """
    Send a WhatsApp message via the WhatsApp Business Cloud API

    Args:
        to: Recipient phone number in international format (no leading '+')
        message: The text message body to send

    Returns:
        dict: The API response
    """
    if not WHATSAPP_ACCESS_TOKEN:
        raise ValueError("WHATSAPP_ACCESS_TOKEN not configured in environment variables")
    if not WHATSAPP_PHONE_NUMBER_ID:
        raise ValueError("WHATSAPP_PHONE_NUMBER_ID not configured in environment variables")

    url = f"{WHATSAPP_API_BASE_URL}/{WHATSAPP_PHONE_NUMBER_ID}/messages"
    headers = {
        'Authorization': f'Bearer {WHATSAPP_ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }

    payload = {
        'messaging_product': 'whatsapp',
        'to': to,
        'type': 'text',
        'text': {'body': message}
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()

        result = response.json()
        logger.info(f"WhatsApp message sent successfully to {to}")

        return result

    except requests.exceptions.RequestException as e:
        logger.error(f"WhatsApp API request failed: {str(e)}")
        raise


if __name__ == '__main__':
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

