#!/usr/bin/env python3
"""
Test the exact sample request from the review request
"""

import requests
import json

# Configuration
BACKEND_URL = "https://f800b529-c05c-42da-a95a-92830f186bd2.preview.emergentagent.com/api"

# Exact sample request from the review
sample_request = {
    "document_content": "# Social Media Management Platform - PRD\n\n## Executive Summary\nBuild a comprehensive social media management platform that allows businesses to manage multiple social media accounts, schedule posts, track analytics, and engage with their audience from a single dashboard.\n\n## Core Features\n- Multi-platform social media account integration\n- Post scheduling and publishing\n- Analytics dashboard\n- Content calendar\n- Team collaboration tools",
    "workflow_type": "user_journey"
}

def test_exact_sample():
    """Test the exact sample request provided"""
    print("🧪 TESTING EXACT SAMPLE REQUEST FROM REVIEW")
    print("=" * 50)
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/generate-workflow", 
            json=sample_request, 
            timeout=60
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ SUCCESS: Workflow generated successfully!")
            print(f"Response structure:")
            print(f"- id: {data.get('id')}")
            print(f"- workflow_type: {data.get('workflow_type')}")
            print(f"- document_length: {data.get('document_length')}")
            print(f"- timestamp: {data.get('timestamp')}")
            print(f"- user_id: {data.get('user_id')}")
            print(f"- workflow_nodes count: {len(data.get('workflow_nodes', []))}")
            
            # Show detailed node structure
            nodes = data.get('workflow_nodes', [])
            if nodes:
                print(f"\nWorkflow Nodes:")
                for i, node in enumerate(nodes):
                    print(f"  Node {i+1}:")
                    print(f"    - id: {node.get('id')}")
                    print(f"    - type: {node.get('type')}")
                    print(f"    - label: {node.get('label')}")
                    print(f"    - position: ({node.get('x')}, {node.get('y')})")
                    print(f"    - connections: {node.get('connections')}")
            
            # Verify JSON structure is proper
            try:
                json_str = json.dumps(data, indent=2)
                print(f"\n✅ JSON structure is valid and properly formatted")
                return True
            except Exception as e:
                print(f"❌ JSON serialization error: {e}")
                return False
                
        else:
            print(f"❌ FAILED: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_exact_sample()
    print(f"\nTest Result: {'PASSED' if success else 'FAILED'}")