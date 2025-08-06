#!/usr/bin/env python3
"""
Enhanced Backend Testing Suite for AI-powered PRD/BRD Analysis Application
Tests all backend API endpoints including authentication and enhanced document parsing
"""

import requests
import json
import time
import tempfile
import os
from datetime import datetime
from typing import Dict, Any, Optional
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from docx import Document as DocxDocument

# Configuration
BACKEND_URL = "https://f800b529-c05c-42da-a95a-92830f186bd2.preview.emergentagent.com/api"

# Sample PRD content for testing
SAMPLE_PRD_CONTENT = """# Social Media Management Platform - PRD

## Executive Summary
Build a comprehensive social media management platform that allows businesses to manage multiple social media accounts, schedule posts, track analytics, and engage with their audience from a single dashboard.

## Business Goals
- Increase social media engagement for small to medium businesses
- Provide unified social media management solution
- Generate revenue through subscription-based model

## Core Features
- Multi-platform social media account integration
- Post scheduling and publishing
- Analytics dashboard
- Content calendar
- Team collaboration tools

## User Stories
- As a social media manager, I want to schedule posts across multiple platforms
- As a business owner, I want to see analytics for all my social media accounts
- As a team member, I want to collaborate on content creation

## Technical Requirements
- Support for Facebook, Twitter, Instagram, LinkedIn
- Real-time analytics
- Mobile responsive design
- API integrations with social platforms
"""

class BackendTester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.auth_token = None
        self.test_user_data = {
            "email": "sarah.johnson@productdesign.com",
            "password": "SecurePass123!",
            "name": "Sarah Johnson"
        }
        
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test results"""
        result = {
            "test_name": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat(),
            "response_data": response_data
        }
        self.test_results.append(result)
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
        if details:
            print(f"   Details: {details}")
        if not success and response_data:
            print(f"   Response: {response_data}")
        print()

    def set_auth_header(self, token: str):
        """Set authorization header for authenticated requests"""
        self.auth_token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def clear_auth_header(self):
        """Clear authorization header"""
        self.auth_token = None
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]

    def create_test_pdf(self, content: str) -> str:
        """Create a test PDF file with given content"""
        temp_file = tempfile.NamedTemporaryFile(mode='wb', suffix='.pdf', delete=False)
        
        # Create PDF using reportlab
        c = canvas.Canvas(temp_file.name, pagesize=letter)
        width, height = letter
        
        # Split content into lines and add to PDF
        lines = content.split('\n')
        y_position = height - 50
        
        for line in lines:
            if y_position < 50:  # Start new page if needed
                c.showPage()
                y_position = height - 50
            c.drawString(50, y_position, line[:80])  # Limit line length
            y_position -= 20
        
        c.save()
        temp_file.close()
        return temp_file.name

    def create_test_docx(self, content: str) -> str:
        """Create a test DOCX file with given content"""
        temp_file = tempfile.NamedTemporaryFile(mode='wb', suffix='.docx', delete=False)
        temp_file.close()
        
        # Create DOCX using python-docx
        doc = DocxDocument()
        
        # Split content into paragraphs
        paragraphs = content.split('\n\n')
        for paragraph in paragraphs:
            if paragraph.strip():
                doc.add_paragraph(paragraph.strip())
        
        doc.save(temp_file.name)
        return temp_file.name

    def test_health_check(self):
        """Test the enhanced health check endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check basic health status
                if data.get("status") != "healthy":
                    self.log_test("Health Check", False, "API not healthy", data)
                    return False
                
                # Check enhanced features
                features = data.get("features", {})
                expected_features = {
                    "authentication": True,
                    "document_parsing": ["PDF", "DOCX", "TXT", "MD"],
                    "analysis_types": ["gap_analysis", "requirements_extraction", "summary"],
                    "workflow_generation": ["user_journey", "service_blueprint", "feature_flow"]
                }
                
                # Verify authentication feature
                if not features.get("authentication"):
                    self.log_test("Health Check", False, "Authentication feature not enabled", data)
                    return False
                
                # Verify document parsing features
                doc_parsing = features.get("document_parsing", [])
                missing_formats = [fmt for fmt in expected_features["document_parsing"] if fmt not in doc_parsing]
                if missing_formats:
                    self.log_test("Health Check", False, f"Missing document formats: {missing_formats}", data)
                    return False
                
                # Verify analysis types
                analysis_types = features.get("analysis_types", [])
                missing_types = [typ for typ in expected_features["analysis_types"] if typ not in analysis_types]
                if missing_types:
                    self.log_test("Health Check", False, f"Missing analysis types: {missing_types}", data)
                    return False
                
                # Verify workflow generation types
                workflow_types = features.get("workflow_generation", [])
                missing_workflow_types = [typ for typ in expected_features["workflow_generation"] if typ not in workflow_types]
                if missing_workflow_types:
                    self.log_test("Health Check", False, f"Missing workflow types: {missing_workflow_types}", data)
                    return False
                
                self.log_test("Health Check", True, 
                            f"Enhanced health check passed. Features: {features}")
                return True
            else:
                self.log_test("Health Check", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Health Check", False, f"Connection error: {str(e)}")
            return False

    def test_user_registration(self):
        """Test user registration endpoint"""
        try:
            response = self.session.post(
                f"{self.base_url}/auth/register",
                json=self.test_user_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check required fields
                required_fields = ["access_token", "token_type", "user"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("User Registration", False, f"Missing fields: {missing_fields}", data)
                    return False
                
                # Check user data
                user_data = data["user"]
                if (user_data.get("email") == self.test_user_data["email"] and 
                    user_data.get("name") == self.test_user_data["name"] and
                    data.get("token_type") == "bearer"):
                    
                    # Store token for future tests
                    self.set_auth_header(data["access_token"])
                    
                    self.log_test("User Registration", True, 
                                f"User registered successfully. ID: {user_data.get('id')}")
                    return data["access_token"]
                else:
                    self.log_test("User Registration", False, "Invalid user data in response", data)
                    return False
            elif response.status_code == 400:
                # User might already exist, try login instead
                self.log_test("User Registration", True, "User already exists (expected for repeated tests)")
                return self.test_user_login()
            else:
                self.log_test("User Registration", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("User Registration", False, f"Error: {str(e)}")
            return False

    def test_user_login(self):
        """Test user login endpoint"""
        try:
            login_data = {
                "email": self.test_user_data["email"],
                "password": self.test_user_data["password"]
            }
            
            response = self.session.post(
                f"{self.base_url}/auth/login",
                json=login_data,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check required fields
                required_fields = ["access_token", "token_type", "user"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("User Login", False, f"Missing fields: {missing_fields}", data)
                    return False
                
                # Store token for future tests
                self.set_auth_header(data["access_token"])
                
                self.log_test("User Login", True, 
                            f"User logged in successfully. Token type: {data.get('token_type')}")
                return data["access_token"]
            else:
                self.log_test("User Login", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("User Login", False, f"Error: {str(e)}")
            return False

    def test_get_current_user(self):
        """Test getting current user profile"""
        try:
            if not self.auth_token:
                self.log_test("Get Current User", False, "No auth token available")
                return False
            
            response = self.session.get(f"{self.base_url}/auth/me", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check required fields
                required_fields = ["id", "email", "name", "created_at", "is_active"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Get Current User", False, f"Missing fields: {missing_fields}", data)
                    return False
                
                if data.get("email") == self.test_user_data["email"]:
                    self.log_test("Get Current User", True, 
                                f"User profile retrieved successfully. Active: {data.get('is_active')}")
                    return data
                else:
                    self.log_test("Get Current User", False, "Email mismatch in user profile", data)
                    return False
            elif response.status_code == 401:
                self.log_test("Get Current User", False, "Unauthorized - token invalid", response.text)
                return False
            else:
                self.log_test("Get Current User", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Get Current User", False, f"Error: {str(e)}")
            return False

    def test_protected_route_without_auth(self):
        """Test that protected routes require authentication"""
        try:
            # Temporarily clear auth header
            original_token = self.auth_token
            self.clear_auth_header()
            
            response = self.session.get(f"{self.base_url}/auth/me", timeout=10)
            
            # Restore auth header
            if original_token:
                self.set_auth_header(original_token)
            
            if response.status_code == 401:
                self.log_test("Protected Route Without Auth", True, 
                            "Protected route correctly requires authentication")
                return True
            else:
                self.log_test("Protected Route Without Auth", False, 
                            f"Expected 401, got {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Protected Route Without Auth", False, f"Error: {str(e)}")
            return False

    def test_basic_api_endpoint(self):
        """Test the basic API root endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if "PRD/BRD AI Analysis API" in data.get("message", ""):
                    self.log_test("Basic API Endpoint", True, "Root endpoint responding correctly")
                    return True
                else:
                    self.log_test("Basic API Endpoint", False, "Unexpected response message", data)
                    return False
            else:
                self.log_test("Basic API Endpoint", False, f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Basic API Endpoint", False, f"Connection error: {str(e)}")
            return False

    def test_document_analysis_with_auth(self):
        """Test document analysis with user authentication"""
        try:
            if not self.auth_token:
                self.log_test("Document Analysis With Auth", False, "No auth token available")
                return False
            
            payload = {
                "document_content": SAMPLE_PRD_CONTENT,
                "analysis_type": "gap_analysis"
            }
            
            response = self.session.post(
                f"{self.base_url}/analyze-document", 
                json=payload, 
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check that user_id is included in response
                if data.get("user_id"):
                    self.log_test("Document Analysis With Auth", True, 
                                f"Analysis completed with user authentication. User ID: {data['user_id']}")
                    return data["id"]
                else:
                    self.log_test("Document Analysis With Auth", False, 
                                "Analysis completed but user_id missing", data)
                    return False
            else:
                self.log_test("Document Analysis With Auth", False, 
                            f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Document Analysis With Auth", False, f"Error: {str(e)}")
            return False

    def test_pdf_parsing(self):
        """Test PDF document parsing"""
        try:
            # Create test PDF
            pdf_path = self.create_test_pdf(SAMPLE_PRD_CONTENT)
            
            try:
                with open(pdf_path, 'rb') as file:
                    files = {'file': ('test_prd.pdf', file, 'application/pdf')}
                    data = {'analysis_type': 'gap_analysis'}
                    
                    response = self.session.post(
                        f"{self.base_url}/analyze-document-file",
                        files=files,
                        data=data,
                        timeout=60
                    )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if (result.get("filename") == "test_prd.pdf" and 
                        isinstance(result.get("analysis_result"), dict) and
                        result.get("document_length", 0) > 0):
                        
                        self.log_test("PDF Parsing", True, 
                                    f"PDF parsed successfully. Content length: {result['document_length']}")
                        return result["id"]
                    else:
                        self.log_test("PDF Parsing", False, "Invalid PDF parsing result", result)
                        return False
                else:
                    self.log_test("PDF Parsing", False, 
                                f"HTTP {response.status_code}", response.text)
                    return False
                    
            finally:
                os.unlink(pdf_path)
                
        except Exception as e:
            self.log_test("PDF Parsing", False, f"Error: {str(e)}")
            return False

    def test_docx_parsing(self):
        """Test DOCX document parsing"""
        try:
            # Create test DOCX
            docx_path = self.create_test_docx(SAMPLE_PRD_CONTENT)
            
            try:
                with open(docx_path, 'rb') as file:
                    files = {'file': ('test_prd.docx', file, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')}
                    data = {'analysis_type': 'summary'}
                    
                    response = self.session.post(
                        f"{self.base_url}/analyze-document-file",
                        files=files,
                        data=data,
                        timeout=60
                    )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    if (result.get("filename") == "test_prd.docx" and 
                        isinstance(result.get("analysis_result"), dict) and
                        result.get("document_length", 0) > 0):
                        
                        self.log_test("DOCX Parsing", True, 
                                    f"DOCX parsed successfully. Content length: {result['document_length']}")
                        return result["id"]
                    else:
                        self.log_test("DOCX Parsing", False, "Invalid DOCX parsing result", result)
                        return False
                else:
                    self.log_test("DOCX Parsing", False, 
                                f"HTTP {response.status_code}", response.text)
                    return False
                    
            finally:
                os.unlink(docx_path)
                
        except Exception as e:
            self.log_test("DOCX Parsing", False, f"Error: {str(e)}")
            return False

    def test_unsupported_file_type(self):
        """Test error handling for unsupported file types"""
        try:
            # Create a fake image file
            temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.jpg', delete=False)
            temp_file.write("This is not actually an image file")
            temp_file.close()
            
            try:
                with open(temp_file.name, 'rb') as file:
                    files = {'file': ('test_image.jpg', file, 'image/jpeg')}
                    data = {'analysis_type': 'gap_analysis'}
                    
                    response = self.session.post(
                        f"{self.base_url}/analyze-document-file",
                        files=files,
                        data=data,
                        timeout=30
                    )
                
                if response.status_code == 400:
                    error_data = response.json()
                    if "Unsupported file type" in error_data.get("detail", ""):
                        self.log_test("Unsupported File Type", True, 
                                    "Correctly rejected unsupported file type")
                        return True
                    else:
                        self.log_test("Unsupported File Type", False, 
                                    "Wrong error message for unsupported file", error_data)
                        return False
                else:
                    self.log_test("Unsupported File Type", False, 
                                f"Expected 400, got {response.status_code}", response.text)
                    return False
                    
            finally:
                os.unlink(temp_file.name)
                
        except Exception as e:
            self.log_test("Unsupported File Type", False, f"Error: {str(e)}")
            return False

    def test_user_specific_analyses(self):
        """Test retrieving user-specific analysis history"""
        try:
            if not self.auth_token:
                self.log_test("User Specific Analyses", False, "No auth token available")
                return False
            
            response = self.session.get(f"{self.base_url}/analyses", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, list):
                    # Check if analyses belong to the authenticated user
                    user_analyses = [analysis for analysis in data if analysis.get("user_id")]
                    
                    self.log_test("User Specific Analyses", True, 
                                f"Retrieved {len(user_analyses)} user-specific analyses out of {len(data)} total")
                    return data
                else:
                    self.log_test("User Specific Analyses", False, "Response is not a list", data)
                    return False
            else:
                self.log_test("User Specific Analyses", False, 
                            f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("User Specific Analyses", False, f"Error: {str(e)}")
            return False

    def test_analyses_without_auth(self):
        """Test analyses endpoint without authentication"""
        try:
            # Temporarily clear auth header
            original_token = self.auth_token
            self.clear_auth_header()
            
            response = self.session.get(f"{self.base_url}/analyses", timeout=10)
            
            # Restore auth header
            if original_token:
                self.set_auth_header(original_token)
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, list):
                    # Should return public analyses (those without user_id)
                    public_analyses = [analysis for analysis in data if not analysis.get("user_id")]
                    
                    self.log_test("Analyses Without Auth", True, 
                                f"Retrieved {len(public_analyses)} public analyses without authentication")
                    return True
                else:
                    self.log_test("Analyses Without Auth", False, "Response is not a list", data)
                    return False
            else:
                self.log_test("Analyses Without Auth", False, 
                            f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Analyses Without Auth", False, f"Error: {str(e)}")
            return False

    def test_workflow_generation_user_journey(self):
        """Test workflow generation with user_journey type"""
        try:
            payload = {
                "document_content": SAMPLE_PRD_CONTENT,
                "workflow_type": "user_journey"
            }
            
            response = self.session.post(
                f"{self.base_url}/generate-workflow", 
                json=payload, 
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check required fields
                required_fields = ["id", "workflow_nodes", "workflow_type", "document_length", "timestamp"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Workflow Generation - User Journey", False, f"Missing fields: {missing_fields}", data)
                    return False
                
                # Check workflow nodes structure
                workflow_nodes = data["workflow_nodes"]
                if not isinstance(workflow_nodes, list) or len(workflow_nodes) == 0:
                    self.log_test("Workflow Generation - User Journey", False, 
                                "workflow_nodes should be a non-empty list", data)
                    return False
                
                # Check node structure
                for i, node in enumerate(workflow_nodes):
                    required_node_fields = ["id", "type", "label", "x", "y", "connections"]
                    missing_node_fields = [field for field in required_node_fields if field not in node]
                    
                    if missing_node_fields:
                        self.log_test("Workflow Generation - User Journey", False, 
                                    f"Node {i} missing fields: {missing_node_fields}", node)
                        return False
                    
                    # Check node type is valid
                    valid_types = ["start", "process", "decision", "end"]
                    if node["type"] not in valid_types:
                        self.log_test("Workflow Generation - User Journey", False, 
                                    f"Invalid node type: {node['type']}", node)
                        return False
                
                # Check workflow type matches request
                if data["workflow_type"] != "user_journey":
                    self.log_test("Workflow Generation - User Journey", False, 
                                f"Workflow type mismatch. Expected: user_journey, Got: {data['workflow_type']}", data)
                    return False
                
                self.log_test("Workflow Generation - User Journey", True, 
                            f"User journey workflow generated successfully. {len(workflow_nodes)} nodes created")
                return data["id"]
            else:
                self.log_test("Workflow Generation - User Journey", False, 
                            f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Workflow Generation - User Journey", False, f"Error: {str(e)}")
            return False

    def test_workflow_generation_service_blueprint(self):
        """Test workflow generation with service_blueprint type"""
        try:
            payload = {
                "document_content": SAMPLE_PRD_CONTENT,
                "workflow_type": "service_blueprint"
            }
            
            response = self.session.post(
                f"{self.base_url}/generate-workflow", 
                json=payload, 
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check basic structure
                if not isinstance(data.get("workflow_nodes"), list):
                    self.log_test("Workflow Generation - Service Blueprint", False, 
                                "workflow_nodes should be a list", data)
                    return False
                
                if data.get("workflow_type") != "service_blueprint":
                    self.log_test("Workflow Generation - Service Blueprint", False, 
                                f"Workflow type mismatch. Expected: service_blueprint, Got: {data.get('workflow_type')}", data)
                    return False
                
                workflow_nodes = data["workflow_nodes"]
                if len(workflow_nodes) == 0:
                    self.log_test("Workflow Generation - Service Blueprint", False, 
                                "No workflow nodes generated", data)
                    return False
                
                self.log_test("Workflow Generation - Service Blueprint", True, 
                            f"Service blueprint workflow generated successfully. {len(workflow_nodes)} nodes created")
                return data["id"]
            else:
                self.log_test("Workflow Generation - Service Blueprint", False, 
                            f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Workflow Generation - Service Blueprint", False, f"Error: {str(e)}")
            return False

    def test_workflow_generation_feature_flow(self):
        """Test workflow generation with feature_flow type"""
        try:
            payload = {
                "document_content": SAMPLE_PRD_CONTENT,
                "workflow_type": "feature_flow"
            }
            
            response = self.session.post(
                f"{self.base_url}/generate-workflow", 
                json=payload, 
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check basic structure
                if not isinstance(data.get("workflow_nodes"), list):
                    self.log_test("Workflow Generation - Feature Flow", False, 
                                "workflow_nodes should be a list", data)
                    return False
                
                if data.get("workflow_type") != "feature_flow":
                    self.log_test("Workflow Generation - Feature Flow", False, 
                                f"Workflow type mismatch. Expected: feature_flow, Got: {data.get('workflow_type')}", data)
                    return False
                
                workflow_nodes = data["workflow_nodes"]
                if len(workflow_nodes) == 0:
                    self.log_test("Workflow Generation - Feature Flow", False, 
                                "No workflow nodes generated", data)
                    return False
                
                self.log_test("Workflow Generation - Feature Flow", True, 
                            f"Feature flow workflow generated successfully. {len(workflow_nodes)} nodes created")
                return data["id"]
            else:
                self.log_test("Workflow Generation - Feature Flow", False, 
                            f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Workflow Generation - Feature Flow", False, f"Error: {str(e)}")
            return False

    def test_workflow_generation_with_auth(self):
        """Test workflow generation with user authentication"""
        try:
            if not self.auth_token:
                self.log_test("Workflow Generation With Auth", False, "No auth token available")
                return False
            
            payload = {
                "document_content": SAMPLE_PRD_CONTENT,
                "workflow_type": "user_journey"
            }
            
            response = self.session.post(
                f"{self.base_url}/generate-workflow", 
                json=payload, 
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check that user_id is included in response
                if data.get("user_id"):
                    self.log_test("Workflow Generation With Auth", True, 
                                f"Workflow generated with user authentication. User ID: {data['user_id']}")
                    return data["id"]
                else:
                    self.log_test("Workflow Generation With Auth", False, 
                                "Workflow generated but user_id missing", data)
                    return False
            else:
                self.log_test("Workflow Generation With Auth", False, 
                            f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Workflow Generation With Auth", False, f"Error: {str(e)}")
            return False

    def test_get_all_workflows(self):
        """Test retrieving all workflows"""
        try:
            response = self.session.get(f"{self.base_url}/workflows", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, list):
                    self.log_test("Get All Workflows", True, 
                                f"Retrieved {len(data)} workflows from database")
                    return data
                else:
                    self.log_test("Get All Workflows", False, "Response is not a list", data)
                    return False
            else:
                self.log_test("Get All Workflows", False, 
                            f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Get All Workflows", False, f"Error: {str(e)}")
            return False

    def test_get_specific_workflow(self, workflow_id: str):
        """Test retrieving a specific workflow by ID"""
        try:
            response = self.session.get(f"{self.base_url}/workflows/{workflow_id}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("id") == workflow_id:
                    self.log_test("Get Specific Workflow", True, 
                                f"Successfully retrieved workflow {workflow_id}")
                    return True
                else:
                    self.log_test("Get Specific Workflow", False, 
                                f"ID mismatch. Expected: {workflow_id}, Got: {data.get('id')}", data)
                    return False
            elif response.status_code == 404:
                self.log_test("Get Specific Workflow", False, 
                            f"Workflow {workflow_id} not found", response.text)
                return False
            else:
                self.log_test("Get Specific Workflow", False, 
                            f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Get Specific Workflow", False, f"Error: {str(e)}")
            return False

    def test_user_specific_workflows(self):
        """Test retrieving user-specific workflow history"""
        try:
            if not self.auth_token:
                self.log_test("User Specific Workflows", False, "No auth token available")
                return False
            
            response = self.session.get(f"{self.base_url}/workflows", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, list):
                    # Check if workflows belong to the authenticated user
                    user_workflows = [workflow for workflow in data if workflow.get("user_id")]
                    
                    self.log_test("User Specific Workflows", True, 
                                f"Retrieved {len(user_workflows)} user-specific workflows out of {len(data)} total")
                    return data
                else:
                    self.log_test("User Specific Workflows", False, "Response is not a list", data)
                    return False
            else:
                self.log_test("User Specific Workflows", False, 
                            f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("User Specific Workflows", False, f"Error: {str(e)}")
            return False
        """Test document analysis with gap_analysis type"""
        try:
            payload = {
                "document_content": SAMPLE_PRD_CONTENT,
                "analysis_type": "gap_analysis"
            }
            
            response = self.session.post(
                f"{self.base_url}/analyze-document", 
                json=payload, 
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check required fields
                required_fields = ["id", "analysis_result", "document_length", "analysis_type", "timestamp"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Document Analysis - Gap Analysis", False, f"Missing fields: {missing_fields}", data)
                    return False
                
                # Check analysis result structure for gap analysis
                analysis_result = data["analysis_result"]
                expected_gap_fields = ["business_gaps", "design_ambiguities", "missing_requirements", "edge_cases", "recommendations"]
                
                if isinstance(analysis_result, dict):
                    # Check if it has gap analysis structure or raw analysis
                    has_gap_structure = any(field in analysis_result for field in expected_gap_fields)
                    has_raw_analysis = "raw_analysis" in analysis_result
                    
                    if has_gap_structure or has_raw_analysis:
                        self.log_test("Document Analysis - Gap Analysis", True, 
                                    f"Analysis completed successfully. Document length: {data['document_length']}")
                        return data["id"]  # Return ID for further testing
                    else:
                        self.log_test("Document Analysis - Gap Analysis", False, 
                                    "Analysis result doesn't have expected structure", analysis_result)
                        return False
                else:
                    self.log_test("Document Analysis - Gap Analysis", False, 
                                "Analysis result is not a dictionary", analysis_result)
                    return False
            else:
                self.log_test("Document Analysis - Gap Analysis", False, 
                            f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Document Analysis - Gap Analysis", False, f"Error: {str(e)}")
            return False

    def test_document_analysis_requirements_extraction(self):
        """Test document analysis with requirements_extraction type"""
        try:
            payload = {
                "document_content": SAMPLE_PRD_CONTENT,
                "analysis_type": "requirements_extraction"
            }
            
            response = self.session.post(
                f"{self.base_url}/analyze-document", 
                json=payload, 
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                analysis_result = data["analysis_result"]
                
                # Check if analysis was performed
                if isinstance(analysis_result, dict) and (
                    any(key in analysis_result for key in ["functional_requirements", "business_requirements"]) or
                    "raw_analysis" in analysis_result
                ):
                    self.log_test("Document Analysis - Requirements Extraction", True, 
                                "Requirements extraction completed successfully")
                    return data["id"]
                else:
                    self.log_test("Document Analysis - Requirements Extraction", False, 
                                "Invalid analysis result structure", analysis_result)
                    return False
            else:
                self.log_test("Document Analysis - Requirements Extraction", False, 
                            f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Document Analysis - Requirements Extraction", False, f"Error: {str(e)}")
            return False

    def test_document_analysis_summary(self):
        """Test document analysis with summary type"""
        try:
            payload = {
                "document_content": SAMPLE_PRD_CONTENT,
                "analysis_type": "summary"
            }
            
            response = self.session.post(
                f"{self.base_url}/analyze-document", 
                json=payload, 
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                analysis_result = data["analysis_result"]
                
                # Check if analysis was performed
                if isinstance(analysis_result, dict) and (
                    any(key in analysis_result for key in ["executive_summary", "key_features"]) or
                    "raw_analysis" in analysis_result
                ):
                    self.log_test("Document Analysis - Summary", True, 
                                "Summary analysis completed successfully")
                    return data["id"]
                else:
                    self.log_test("Document Analysis - Summary", False, 
                                "Invalid analysis result structure", analysis_result)
                    return False
            else:
                self.log_test("Document Analysis - Summary", False, 
                            f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Document Analysis - Summary", False, f"Error: {str(e)}")
            return False

    def test_file_upload_analysis(self):
        """Test document file upload and analysis"""
        try:
            # Create a temporary file with sample content
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
                temp_file.write(SAMPLE_PRD_CONTENT)
                temp_file_path = temp_file.name
            
            try:
                # Upload and analyze the file
                with open(temp_file_path, 'rb') as file:
                    files = {'file': ('test_prd.txt', file, 'text/plain')}
                    data = {'analysis_type': 'gap_analysis'}
                    
                    response = self.session.post(
                        f"{self.base_url}/analyze-document-file",
                        files=files,
                        data=data,
                        timeout=60
                    )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Check required fields
                    required_fields = ["id", "filename", "analysis_result", "document_length", "analysis_type"]
                    missing_fields = [field for field in required_fields if field not in result]
                    
                    if missing_fields:
                        self.log_test("File Upload Analysis", False, f"Missing fields: {missing_fields}", result)
                        return False
                    
                    if result["filename"] == "test_prd.txt" and isinstance(result["analysis_result"], dict):
                        self.log_test("File Upload Analysis", True, 
                                    f"File analysis completed. Length: {result['document_length']}")
                        return result["id"]
                    else:
                        self.log_test("File Upload Analysis", False, "Invalid response structure", result)
                        return False
                else:
                    self.log_test("File Upload Analysis", False, 
                                f"HTTP {response.status_code}", response.text)
                    return False
                    
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
                
        except Exception as e:
            self.log_test("File Upload Analysis", False, f"Error: {str(e)}")
            return False

    def test_get_all_analyses(self):
        """Test retrieving all analyses"""
        try:
            response = self.session.get(f"{self.base_url}/analyses", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, list):
                    self.log_test("Get All Analyses", True, 
                                f"Retrieved {len(data)} analyses from database")
                    return data
                else:
                    self.log_test("Get All Analyses", False, "Response is not a list", data)
                    return False
            else:
                self.log_test("Get All Analyses", False, 
                            f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Get All Analyses", False, f"Error: {str(e)}")
            return False

    def test_get_specific_analysis(self, analysis_id: str):
        """Test retrieving a specific analysis by ID"""
        try:
            response = self.session.get(f"{self.base_url}/analyses/{analysis_id}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("id") == analysis_id:
                    self.log_test("Get Specific Analysis", True, 
                                f"Successfully retrieved analysis {analysis_id}")
                    return True
                else:
                    self.log_test("Get Specific Analysis", False, 
                                f"ID mismatch. Expected: {analysis_id}, Got: {data.get('id')}", data)
                    return False
            elif response.status_code == 404:
                self.log_test("Get Specific Analysis", False, 
                            f"Analysis {analysis_id} not found", response.text)
                return False
            else:
                self.log_test("Get Specific Analysis", False, 
                            f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Get Specific Analysis", False, f"Error: {str(e)}")
            return False

    def test_document_analysis_gap_analysis(self):
        """Test document analysis with gap_analysis type"""
        try:
            payload = {
                "document_content": SAMPLE_PRD_CONTENT,
                "analysis_type": "gap_analysis"
            }
            
            response = self.session.post(
                f"{self.base_url}/analyze-document", 
                json=payload, 
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check required fields
                required_fields = ["id", "analysis_result", "document_length", "analysis_type", "timestamp"]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test("Document Analysis - Gap Analysis", False, f"Missing fields: {missing_fields}", data)
                    return False
                
                # Check analysis result structure for gap analysis
                analysis_result = data["analysis_result"]
                expected_gap_fields = ["business_gaps", "design_ambiguities", "missing_requirements", "edge_cases", "recommendations"]
                
                if isinstance(analysis_result, dict):
                    # Check if it has gap analysis structure or raw analysis
                    has_gap_structure = any(field in analysis_result for field in expected_gap_fields)
                    has_raw_analysis = "raw_analysis" in analysis_result
                    
                    if has_gap_structure or has_raw_analysis:
                        self.log_test("Document Analysis - Gap Analysis", True, 
                                    f"Analysis completed successfully. Document length: {data['document_length']}")
                        return data["id"]  # Return ID for further testing
                    else:
                        self.log_test("Document Analysis - Gap Analysis", False, 
                                    "Analysis result doesn't have expected structure", analysis_result)
                        return False
                else:
                    self.log_test("Document Analysis - Gap Analysis", False, 
                                "Analysis result is not a dictionary", analysis_result)
                    return False
            else:
                self.log_test("Document Analysis - Gap Analysis", False, 
                            f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Document Analysis - Gap Analysis", False, f"Error: {str(e)}")
            return False

    def test_file_upload_analysis(self):
        """Test document file upload and analysis"""
        try:
            # Create a temporary file with sample content
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as temp_file:
                temp_file.write(SAMPLE_PRD_CONTENT)
                temp_file_path = temp_file.name
            
            try:
                # Upload and analyze the file
                with open(temp_file_path, 'rb') as file:
                    files = {'file': ('test_prd.txt', file, 'text/plain')}
                    data = {'analysis_type': 'gap_analysis'}
                    
                    response = self.session.post(
                        f"{self.base_url}/analyze-document-file",
                        files=files,
                        data=data,
                        timeout=60
                    )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Check required fields
                    required_fields = ["id", "filename", "analysis_result", "document_length", "analysis_type"]
                    missing_fields = [field for field in required_fields if field not in result]
                    
                    if missing_fields:
                        self.log_test("File Upload Analysis", False, f"Missing fields: {missing_fields}", result)
                        return False
                    
                    if result["filename"] == "test_prd.txt" and isinstance(result["analysis_result"], dict):
                        self.log_test("File Upload Analysis", True, 
                                    f"File analysis completed. Length: {result['document_length']}")
                        return result["id"]
                    else:
                        self.log_test("File Upload Analysis", False, "Invalid response structure", result)
                        return False
                else:
                    self.log_test("File Upload Analysis", False, 
                                f"HTTP {response.status_code}", response.text)
                    return False
                    
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
                
        except Exception as e:
            self.log_test("File Upload Analysis", False, f"Error: {str(e)}")
            return False

    def test_get_all_analyses(self):
        """Test retrieving all analyses"""
        try:
            response = self.session.get(f"{self.base_url}/analyses", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if isinstance(data, list):
                    self.log_test("Get All Analyses", True, 
                                f"Retrieved {len(data)} analyses from database")
                    return data
                else:
                    self.log_test("Get All Analyses", False, "Response is not a list", data)
                    return False
            else:
                self.log_test("Get All Analyses", False, 
                            f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Get All Analyses", False, f"Error: {str(e)}")
            return False

    def test_get_specific_analysis(self, analysis_id: str):
        """Test retrieving a specific analysis by ID"""
        try:
            response = self.session.get(f"{self.base_url}/analyses/{analysis_id}", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("id") == analysis_id:
                    self.log_test("Get Specific Analysis", True, 
                                f"Successfully retrieved analysis {analysis_id}")
                    return True
                else:
                    self.log_test("Get Specific Analysis", False, 
                                f"ID mismatch. Expected: {analysis_id}, Got: {data.get('id')}", data)
                    return False
            elif response.status_code == 404:
                self.log_test("Get Specific Analysis", False, 
                            f"Analysis {analysis_id} not found", response.text)
                return False
            else:
                self.log_test("Get Specific Analysis", False, 
                            f"HTTP {response.status_code}", response.text)
                return False
                
        except Exception as e:
            self.log_test("Get Specific Analysis", False, f"Error: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all enhanced backend tests"""
        print("=" * 70)
        print("ENHANCED BACKEND TESTING SUITE - AI-POWERED PRD/BRD ANALYSIS")
        print("=" * 70)
        print(f"Testing backend at: {self.base_url}")
        print(f"Started at: {datetime.now().isoformat()}")
        print()
        
        # Test basic connectivity and enhanced health check
        if not self.test_health_check():
            print("❌ Enhanced health check failed. Stopping tests.")
            return self.generate_summary()
        
        if not self.test_basic_api_endpoint():
            print("❌ Basic API endpoint failed. Stopping tests.")
            return self.generate_summary()
        
        # Test Authentication System
        print("🔐 TESTING AUTHENTICATION SYSTEM")
        print("-" * 40)
        
        auth_token = self.test_user_registration()
        if not auth_token:
            auth_token = self.test_user_login()
        
        if auth_token:
            self.test_get_current_user()
            self.test_protected_route_without_auth()
        
        # Test Enhanced Document Parsing Features
        print("📄 TESTING ENHANCED DOCUMENT PARSING")
        print("-" * 40)
        
        pdf_analysis_id = self.test_pdf_parsing()
        docx_analysis_id = self.test_docx_parsing()
        self.test_unsupported_file_type()
        
        # Test original file upload (TXT/MD)
        file_analysis_id = self.test_file_upload_analysis()
        
        # Test Enhanced Analysis Features with Authentication
        print("🤖 TESTING ENHANCED ANALYSIS FEATURES")
        print("-" * 40)
        
        analysis_ids = []
        
        # Test analysis with authentication
        if auth_token:
            auth_analysis_id = self.test_document_analysis_with_auth()
            if auth_analysis_id:
                analysis_ids.append(auth_analysis_id)
        
        # Test original analysis types
        gap_analysis_id = self.test_document_analysis_gap_analysis()
        if gap_analysis_id:
            analysis_ids.append(gap_analysis_id)
        
        req_extraction_id = self.test_document_analysis_requirements_extraction()
        if req_extraction_id:
            analysis_ids.append(req_extraction_id)
        
        summary_id = self.test_document_analysis_summary()
        if summary_id:
            analysis_ids.append(summary_id)
        
        # Test Enhanced Analysis History Features
        print("📊 TESTING ANALYSIS HISTORY FEATURES")
        print("-" * 40)
        
        # Test user-specific analysis retrieval
        if auth_token:
            self.test_user_specific_analyses()
        
        # Test public analysis retrieval
        self.test_analyses_without_auth()
        
        # Test data retrieval
        all_analyses = self.test_get_all_analyses()
        
        # Test specific analysis retrieval
        if analysis_ids:
            self.test_get_specific_analysis(analysis_ids[0])
        
        # Test Workflow Generation Features
        print("🔄 TESTING WORKFLOW GENERATION FEATURES")
        print("-" * 40)
        
        workflow_ids = []
        
        # Test all three workflow types
        user_journey_id = self.test_workflow_generation_user_journey()
        if user_journey_id:
            workflow_ids.append(user_journey_id)
        
        service_blueprint_id = self.test_workflow_generation_service_blueprint()
        if service_blueprint_id:
            workflow_ids.append(service_blueprint_id)
        
        feature_flow_id = self.test_workflow_generation_feature_flow()
        if feature_flow_id:
            workflow_ids.append(feature_flow_id)
        
        # Test workflow generation with authentication
        if auth_token:
            auth_workflow_id = self.test_workflow_generation_with_auth()
            if auth_workflow_id:
                workflow_ids.append(auth_workflow_id)
        
        # Test workflow retrieval
        print("📊 TESTING WORKFLOW HISTORY FEATURES")
        print("-" * 40)
        
        # Test user-specific workflow retrieval
        if auth_token:
            self.test_user_specific_workflows()
        
        # Test workflow data retrieval
        all_workflows = self.test_get_all_workflows()
        
        # Test specific workflow retrieval
        if workflow_ids:
            self.test_get_specific_workflow(workflow_ids[0])
        
        return self.generate_summary()

    def generate_summary(self):
        """Generate test summary"""
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print()
        
        if failed_tests > 0:
            print("FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"❌ {result['test_name']}: {result['details']}")
            print()
        
        print("DETAILED RESULTS:")
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"{status} {result['test_name']}")
        
        return {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": (passed_tests/total_tests)*100 if total_tests > 0 else 0,
            "test_results": self.test_results
        }

def main():
    """Main test execution"""
    tester = BackendTester(BACKEND_URL)
    summary = tester.run_all_tests()
    
    # Save results to file
    with open('/app/backend_test_results.json', 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    
    print(f"\nTest results saved to: /app/backend_test_results.json")
    
    return summary["failed_tests"] == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)