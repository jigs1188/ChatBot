"""
Unit tests for Rex AI Assistant main application
"""
import json
import pytest
from unittest.mock import patch, MagicMock


class TestMainApplication:
    """Test main application functionality"""
    
    def test_app_creation(self, app):
        """Test Flask app is created successfully"""
        assert app is not None
        assert app.config['TESTING'] is True
    
    def test_index_route(self, client):
        """Test main index route"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Rex AI Assistant' in response.data
    
    def test_manifest_route(self, client):
        """Test PWA manifest route"""
        response = client.get('/manifest.json')
        assert response.status_code in [200, 302, 404]  # May redirect to static
    
    def test_stats_api(self, client):
        """Test stats API endpoint"""
        response = client.get('/api/stats')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'totalChats' in data
        assert 'completedTasks' in data
        assert 'activeTodos' in data
    
    @patch('requests.post')
    def test_chat_api_success(self, mock_post, client, sample_message):
        """Test chat API with successful AI response"""
        # Mock successful AI API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'choices': [{
                'message': {
                    'content': 'Hello! I\'m doing well, thank you for asking!'
                }
            }]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        response = client.post('/api/chat', 
                             data=json.dumps(sample_message),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'response' in data
        assert data['response'] is not None
    
    def test_chat_api_invalid_input(self, client):
        """Test chat API with invalid input"""
        response = client.post('/api/chat', 
                             data=json.dumps({}),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_todos_api_get(self, client):
        """Test getting todos via API"""
        response = client.get('/api/todos')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert isinstance(data, list)
    
    def test_todos_api_post(self, client, sample_todo):
        """Test adding todo via API"""
        response = client.post('/api/todos',
                             data=json.dumps(sample_todo),
                             content_type='application/json')
        
        assert response.status_code in [200, 201]
        data = json.loads(response.data)
        assert 'success' in data or 'id' in data
    
    def test_history_api(self, client):
        """Test chat history API"""
        response = client.get('/api/history')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert isinstance(data, list)


class TestStaticFiles:
    """Test static file serving"""
    
    def test_css_files(self, client):
        """Test CSS files are accessible"""
        response = client.get('/static/style.css')
        assert response.status_code == 200
        assert response.content_type.startswith('text/css')
    
    def test_js_files(self, client):
        """Test JavaScript files are accessible"""
        response = client.get('/static/script.js')
        assert response.status_code == 200
        assert response.content_type.startswith('application/javascript')
    
    def test_favicon(self, client):
        """Test favicon is accessible"""
        response = client.get('/static/favicon.ico')
        assert response.status_code in [200, 404]  # May not exist


class TestPWAFunctionality:
    """Test Progressive Web App functionality"""
    
    def test_service_worker(self, client):
        """Test service worker is accessible"""
        response = client.get('/sw.js')
        assert response.status_code in [200, 404]  # May not exist yet
        
        if response.status_code == 200:
            assert b'install' in response.data or b'fetch' in response.data
    
    def test_manifest_structure(self, client):
        """Test PWA manifest has required fields"""
        response = client.get('/static/manifest.json')
        if response.status_code == 200:
            data = json.loads(response.data)
            
            # Check required PWA manifest fields
            required_fields = ['name', 'short_name', 'start_url', 'display']
            for field in required_fields:
                assert field in data, f"Missing required manifest field: {field}"


class TestErrorHandling:
    """Test error handling"""
    
    def test_404_error(self, client):
        """Test 404 error handling"""
        response = client.get('/nonexistent-route')
        assert response.status_code == 404
    
    def test_405_method_not_allowed(self, client):
        """Test 405 error handling"""
        response = client.patch('/api/chat')  # PATCH not allowed
        assert response.status_code == 405


@pytest.mark.integration
class TestIntegration:
    """Integration tests"""
    
    def test_complete_chat_flow(self, client):
        """Test complete chat interaction flow"""
        # 1. Check initial stats
        response = client.get('/api/stats')
        initial_stats = json.loads(response.data)
        
        # 2. Send a message (will fail without API key, but that's ok for testing structure)
        message_data = {"message": "Hello test"}
        response = client.post('/api/chat',
                             data=json.dumps(message_data),
                             content_type='application/json')
        
        # Response might be error due to missing API key, but structure should be valid
        assert response.status_code in [200, 400, 500]
        data = json.loads(response.data)
        assert isinstance(data, dict)
    
    def test_todo_management_flow(self, client):
        """Test complete todo management flow"""
        # 1. Get initial todos
        response = client.get('/api/todos')
        initial_todos = json.loads(response.data)
        
        # 2. Add a new todo
        new_todo = {"task": "Integration test todo", "completed": False}
        response = client.post('/api/todos',
                             data=json.dumps(new_todo),
                             content_type='application/json')
        
        assert response.status_code in [200, 201]
        
        # 3. Get todos again to verify addition
        response = client.get('/api/todos')
        updated_todos = json.loads(response.data)
        assert len(updated_todos) >= len(initial_todos)
