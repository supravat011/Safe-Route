"""Export routes for data download"""
from flask import Blueprint, request, Response
from services.export_service import ExportService
from utils.response import success_response, error_response
from middleware.auth import role_required
from datetime import datetime

export_bp = Blueprint('export', __name__, url_prefix='/api/export')

@export_bp.route('/accidents/csv', methods=['GET'])
@role_required('admin', 'authority')
def export_accidents_csv():
    """Export accidents to CSV (admin/authority only)"""
    try:
        # Get filters
        filters = {}
        
        if request.args.get('severity'):
            filters['severity'] = request.args.get('severity')
        
        if request.args.get('accident_type'):
            filters['accident_type'] = request.args.get('accident_type')
        
        if request.args.get('start_date'):
            filters['start_date'] = request.args.get('start_date')
        
        if request.args.get('end_date'):
            filters['end_date'] = request.args.get('end_date')
        
        # Generate CSV
        csv_data = ExportService.export_accidents_csv(filters)
        
        # Create response
        filename = f"accidents_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        return Response(
            csv_data,
            mimetype='text/csv',
            headers={
                'Content-Disposition': f'attachment; filename={filename}'
            }
        )
        
    except Exception as e:
        return error_response(f"Failed to export accidents: {str(e)}", 500)

@export_bp.route('/analytics/csv', methods=['GET'])
@role_required('admin', 'authority')
def export_analytics_csv():
    """Export analytics summary to CSV (admin/authority only)"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        csv_data = ExportService.export_analytics_csv(start_date, end_date)
        
        filename = f"analytics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        return Response(
            csv_data,
            mimetype='text/csv',
            headers={
                'Content-Disposition': f'attachment; filename={filename}'
            }
        )
        
    except Exception as e:
        return error_response(f"Failed to export analytics: {str(e)}", 500)

@export_bp.route('/heatmap', methods=['GET'])
def get_heatmap_data():
    """Get heatmap data for visualization"""
    try:
        days = int(request.args.get('days', 30))
        grid_size = float(request.args.get('grid_size', 0.01))
        
        heatmap_data = ExportService.get_heatmap_data(days, grid_size)
        
        return success_response(
            heatmap_data,
            f"Heatmap data retrieved for last {days} days"
        )
        
    except Exception as e:
        return error_response(f"Failed to get heatmap data: {str(e)}", 500)
