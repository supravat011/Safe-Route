"""User statistics routes"""
from flask import Blueprint, request
from services.user_stats_service import UserStatsService
from utils.response import success_response, error_response
from middleware.auth import token_required, role_required, get_current_user

stats_bp = Blueprint('stats', __name__, url_prefix='/api/stats')

@stats_bp.route('/user', methods=['GET'])
@token_required
def get_user_stats():
    """Get current user's statistics"""
    try:
        user_id = get_current_user()
        stats = UserStatsService.get_user_statistics(user_id)
        
        return success_response(stats, "User statistics retrieved successfully")
        
    except Exception as e:
        return error_response(f"Failed to get user stats: {str(e)}", 500)

@stats_bp.route('/user/<int:user_id>', methods=['GET'])
@role_required('admin', 'authority')
def get_specific_user_stats(user_id):
    """Get statistics for a specific user (admin/authority only)"""
    try:
        stats = UserStatsService.get_user_statistics(user_id)
        
        return success_response(stats, "User statistics retrieved successfully")
        
    except Exception as e:
        return error_response(f"Failed to get user stats: {str(e)}", 500)

@stats_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get top contributing users leaderboard"""
    try:
        limit = int(request.args.get('limit', 10))
        leaderboard = UserStatsService.get_leaderboard(limit)
        
        return success_response(
            leaderboard,
            f"Top {len(leaderboard)} contributors retrieved"
        )
        
    except Exception as e:
        return error_response(f"Failed to get leaderboard: {str(e)}", 500)

@stats_bp.route('/platform', methods=['GET'])
@role_required('admin', 'authority')
def get_platform_stats():
    """Get platform-wide statistics (admin/authority only)"""
    try:
        stats = UserStatsService.get_platform_statistics()
        
        return success_response(stats, "Platform statistics retrieved successfully")
        
    except Exception as e:
        return error_response(f"Failed to get platform stats: {str(e)}", 500)
