#!/usr/bin/env python3
"""
Example usage of the Manus.ai Replit integration
This script demonstrates how to call the webhook endpoints
"""

import requests
import json

# Your Replit deployment URL
REPLIT_URL = "https://your-repl-name.your-username.repl.co"


def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{REPLIT_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_execute_task():
    """Test executing a Manus.ai task"""
    print("Testing task execution...")
    
    payload = {
        "goal": "Analyze the latest tech news and summarize the top 3 stories",
        "inputs": [],
        "constraints": {
            "deadline": "2024-12-31T23:59:59"
        }
    }
    
    response = requests.post(
        f"{REPLIT_URL}/execute",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_decompose_goal():
    """Test decomposing a goal"""
    print("Testing goal decomposition...")
    
    payload = {
        "goal": "Plan a marketing campaign for a new product launch",
        "context": "Product: AI-powered productivity tool, Budget: $50k, Timeline: 3 months"
    }
    
    response = requests.post(
        f"{REPLIT_URL}/decompose",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_webhook_trigger():
    """Test triggering a task via webhook"""
    print("Testing webhook trigger...")
    
    payload = {
        "trigger": "execute_task",
        "goal": "Generate a weekly report of social media engagement",
        "inputs": ["instagram", "twitter", "linkedin"]
    }
    
    response = requests.post(
        f"{REPLIT_URL}/webhook",
        json=payload,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


if __name__ == "__main__":
    print("Manus.ai Replit Integration - Example Usage\n")
    print("=" * 50)
    print()
    
    # Update REPLIT_URL with your actual Replit deployment URL
    print(f"Using Replit URL: {REPLIT_URL}")
    print()
    
    # Run tests
    test_health_check()
    test_execute_task()
    test_decompose_goal()
    test_webhook_trigger()
    
    print("=" * 50)
    print("All tests completed!")

