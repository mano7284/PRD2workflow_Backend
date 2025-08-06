#!/usr/bin/env python3
"""
Focused Workflow Generation Testing
Tests the specific workflow generation functionality as requested
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8000/api"

# Sample PRD content for testing
SAMPLE_PRD_CONTENT = """# Social Media Management Platform - PRD

## Executive Summary
Build a comprehensive social media management platform that allows businesses to manage multiple social media accounts, schedule posts, track analytics, and engage with their audience from a single dashboard.

## Core Features
- Multi-platform social media account integration
- Post scheduling and publishing
- Analytics dashboard
- Content calendar
- Team collaboration tools"""

def test_workflow_generation():
    """Test all three workflow types as requested"""
    session = requests.Session()
    results = []
    
    print("🔄 TESTING WORKFLOW GENERATION FUNCTIONALITY")
    print("=" * 60)
    
    # Test 1: User Journey Workflow
    print("\n1. Testing User Journey Workflow...")
    try:
        payload = {
            "document_content": SAMPLE_PRD_CONTENT,
            "workflow_type": "user_journey"
        }
        
        response = session.post(f"{BACKEND_URL}/generate-workflow", json=payload, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS: User journey workflow generated")
            print(f"   - Workflow ID: {data.get('id')}")
            print(f"   - Number of nodes: {len(data.get('workflow_nodes', []))}")
            print(f"   - Document length: {data.get('document_length')}")
            
            # Verify node structure
            nodes = data.get('workflow_nodes', [])
            if nodes:
                print(f"   - Sample node: {nodes[0]}")
                
            results.append({"test": "user_journey", "success": True, "id": data.get('id')})
        else:
            print(f"❌ FAILED: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            results.append({"test": "user_journey", "success": False, "error": response.text})
            
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        results.append({"test": "user_journey", "success": False, "error": str(e)})
    
    # Test 2: Service Blueprint Workflow
    print("\n2. Testing Service Blueprint Workflow...")
    try:
        payload = {
            "document_content": SAMPLE_PRD_CONTENT,
            "workflow_type": "service_blueprint"
        }
        
        response = session.post(f"{BACKEND_URL}/generate-workflow", json=payload, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS: Service blueprint workflow generated")
            print(f"   - Workflow ID: {data.get('id')}")
            print(f"   - Number of nodes: {len(data.get('workflow_nodes', []))}")
            print(f"   - Document length: {data.get('document_length')}")
            
            results.append({"test": "service_blueprint", "success": True, "id": data.get('id')})
        else:
            print(f"❌ FAILED: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            results.append({"test": "service_blueprint", "success": False, "error": response.text})
            
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        results.append({"test": "service_blueprint", "success": False, "error": str(e)})
    
    # Test 3: Feature Flow Workflow
    print("\n3. Testing Feature Flow Workflow...")
    try:
        payload = {
            "document_content": SAMPLE_PRD_CONTENT,
            "workflow_type": "feature_flow"
        }
        
        response = session.post(f"{BACKEND_URL}/generate-workflow", json=payload, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS: Feature flow workflow generated")
            print(f"   - Workflow ID: {data.get('id')}")
            print(f"   - Number of nodes: {len(data.get('workflow_nodes', []))}")
            print(f"   - Document length: {data.get('document_length')}")
            
            results.append({"test": "feature_flow", "success": True, "id": data.get('id')})
        else:
            print(f"❌ FAILED: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            results.append({"test": "feature_flow", "success": False, "error": response.text})
            
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        results.append({"test": "feature_flow", "success": False, "error": str(e)})
    
    # Test 4: Workflow Retrieval
    print("\n4. Testing Workflow Retrieval...")
    try:
        response = session.get(f"{BACKEND_URL}/workflows", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS: Retrieved {len(data)} workflows")
            results.append({"test": "workflow_retrieval", "success": True, "count": len(data)})
        else:
            print(f"❌ FAILED: HTTP {response.status_code}")
            print(f"   Response: {response.text}")
            results.append({"test": "workflow_retrieval", "success": False, "error": response.text})
            
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        results.append({"test": "workflow_retrieval", "success": False, "error": str(e)})
    
    # Test 5: Specific Workflow Retrieval
    workflow_ids = [r.get('id') for r in results if r.get('success') and r.get('id')]
    if workflow_ids:
        print(f"\n5. Testing Specific Workflow Retrieval...")
        try:
            workflow_id = workflow_ids[0]
            response = session.get(f"{BACKEND_URL}/workflows/{workflow_id}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ SUCCESS: Retrieved specific workflow {workflow_id}")
                print(f"   - Workflow type: {data.get('workflow_type')}")
                print(f"   - Number of nodes: {len(data.get('workflow_nodes', []))}")
                results.append({"test": "specific_workflow_retrieval", "success": True})
            else:
                print(f"❌ FAILED: HTTP {response.status_code}")
                print(f"   Response: {response.text}")
                results.append({"test": "specific_workflow_retrieval", "success": False, "error": response.text})
                
        except Exception as e:
            print(f"❌ FAILED: {str(e)}")
            results.append({"test": "specific_workflow_retrieval", "success": False, "error": str(e)})
    
    # Summary
    print("\n" + "=" * 60)
    print("WORKFLOW GENERATION TEST SUMMARY")
    print("=" * 60)
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r.get('success'))
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    print("\nDetailed Results:")
    for result in results:
        status = "✅" if result.get('success') else "❌"
        print(f"{status} {result['test']}")
    
    return results

if __name__ == "__main__":
    results = test_workflow_generation()
    
    # Save results
    with open('/app/workflow_test_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\nResults saved to: /app/workflow_test_results.json")