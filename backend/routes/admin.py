"""Admin routes for dashboard and analytics"""
from flask import Blueprint, request
from services.analytics_service import AnalyticsService
from utils.response import success_response, error_response
from middleware.auth import role_required

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/dashboard', methods=['GET'])
@role_required('admin', 'authority')
def get_dashboard():
    """Get comprehensive dashboard statistics"""
    try:
        stats = AnalyticsService.get_dashboard_stats()
        return success_response(stats, "Dashboard statistics retrieved successfully")
        
    except Exception as e:
        return error_response(f"Failed to get dashboard stats: {str(e)}", 500)

@admin_bp.route('/analytics/timeline', methods=['GET'])
@role_required('admin', 'authority')
def get_timeline():
    """Get accident timeline data"""
    try:
        period = request.args.get('period', 'daily')
        days = int(request.args.get('days', 30))
        
        if period not in ['daily', 'hourly']:
            return error_response("Period must be 'daily' or 'hourly'", 400)
        
        timeline = AnalyticsService.get_accident_timeline(period, days)
        
        return success_response(timeline, "Timeline data retrieved successfully")
        
    except Exception as e:
        return error_response(f"Failed to get timeline: {str(e)}", 500)

@admin_bp.route('/analytics/zones', methods=['GET'])
@role_required('admin', 'authority')
def get_prone_zones():
    """Get accident-prone zones"""
    try:
        min_accidents = int(request.args.get('min_accidents', 3))
        days = int(request.args.get('days', 90))
        
        zones = AnalyticsService.get_accident_prone_zones(min_accidents, days)
        
        return success_response(zones, f"Found {len(zones)} accident-prone zones")
        
    except Exception as e:
        return error_response(f"Failed to get prone zones: {str(e)}", 500)

@admin_bp.route('/analytics/severity-by-type', methods=['GET'])
@role_required('admin', 'authority')
def get_severity_by_type():
    """Get severity distribution by accident type"""
    try:
        data = AnalyticsService.get_severity_by_type()
        
        return success_response(data, "Severity distribution retrieved successfully")
        
    except Exception as e:
        return error_response(f"Failed to get severity distribution: {str(e)}", 500)

@admin_bp.route('/analytics/monthly', methods=['GET'])
@role_required('admin', 'authority')
def get_monthly_stats():
    """Get monthly statistics"""
    try:
        months = int(request.args.get('months', 12))
        
        stats = AnalyticsService.get_monthly_stats(months)
        
        return success_response(stats, "Monthly statistics retrieved successfully")
        
    except Exception as e:
        return error_response(f"Failed to get monthly stats: {str(e)}", 500)

@admin_bp.route('/analytics/peak-hours', methods=['GET'])
@role_required('admin', 'authority')
def get_peak_hours():
    """Get peak accident hours"""
    try:
        hours = AnalyticsService.get_peak_hours()
        
        return success_response(hours, "Peak hours retrieved successfully")
        
    except Exception as e:
        return error_response(f"Failed to get peak hours: {str(e)}", 500)
