"""Awareness content routes"""
from flask import Blueprint, request
from models.awareness import AwarenessContent
from utils.response import success_response, error_response
from utils.validators import sanitize_input
from middleware.auth import token_required, role_required, get_current_user

awareness_bp = Blueprint('awareness', __name__, url_prefix='/api/awareness')

@awareness_bp.route('', methods=['GET'])
def get_all_content():
    """Get all published awareness content"""
    try:
        category = request.args.get('category')
        content = AwarenessContent.get_all(category=category, published_only=True)
        
        return success_response(content, "Content retrieved successfully")
        
    except Exception as e:
        return error_response(f"Failed to get content: {str(e)}", 500)

@awareness_bp.route('/<int:content_id>', methods=['GET'])
def get_content(content_id):
    """Get specific awareness content"""
    try:
        content = AwarenessContent.get_by_id(content_id)
        
        if not content:
            return error_response("Content not found", 404)
        
        return success_response(content, "Content retrieved successfully")
        
    except Exception as e:
        return error_response(f"Failed to get content: {str(e)}", 500)

@awareness_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all content categories"""
    try:
        categories = AwarenessContent.get_categories()
        
        return success_response(categories, "Categories retrieved successfully")
        
    except Exception as e:
        return error_response(f"Failed to get categories: {str(e)}", 500)

@awareness_bp.route('', methods=['POST'])
@role_required('admin', 'authority')
def create_content():
    """Create new awareness content (admin/authority only)"""
    try:
        data = request.get_json()
        user_id = get_current_user()
        
        if not all(k in data for k in ['title', 'content']):
            return error_response("Missing required fields", 400)
        
        title = sanitize_input(data['title'], 200)
        content = sanitize_input(data['content'], 10000)
        category = sanitize_input(data.get('category', 'General'), 50)
        is_published = data.get('is_published', True)
        
        content_id = AwarenessContent.create(
            title, content, category, user_id, is_published
        )
        
        if not content_id:
            return error_response("Failed to create content", 500)
        
        return success_response(
            {"content_id": content_id},
            "Content created successfully",
            201
        )
        
    except Exception as e:
        return error_response(f"Failed to create content: {str(e)}", 500)

@awareness_bp.route('/<int:content_id>', methods=['PUT'])
@role_required('admin', 'authority')
def update_content(content_id):
    """Update awareness content (admin/authority only)"""
    try:
        data = request.get_json()
        
        update_fields = {}
        
        if 'title' in data:
            update_fields['title'] = sanitize_input(data['title'], 200)
        
        if 'content' in data:
            update_fields['content'] = sanitize_input(data['content'], 10000)
        
        if 'category' in data:
            update_fields['category'] = sanitize_input(data['category'], 50)
        
        if 'is_published' in data:
            update_fields['is_published'] = data['is_published']
        
        if not update_fields:
            return error_response("No fields to update", 400)
        
        success = AwarenessContent.update(content_id, **update_fields)
        
        if not success:
            return error_response("Failed to update content", 500)
        
        return success_response(None, "Content updated successfully")
        
    except Exception as e:
        return error_response(f"Failed to update content: {str(e)}", 500)

@awareness_bp.route('/<int:content_id>', methods=['DELETE'])
@role_required('admin')
def delete_content(content_id):
    """Delete awareness content (admin only)"""
    try:
        success = AwarenessContent.delete(content_id)
        
        if not success:
            return error_response("Failed to delete content", 500)
        
        return success_response(None, "Content deleted successfully")
        
    except Exception as e:
        return error_response(f"Failed to delete content: {str(e)}", 500)
