"""Backup routes"""
from flask import Blueprint, send_file
from utils.backup import BackupUtility
from utils.response import success_response, error_response
from middleware.auth import role_required
import os

backup_bp = Blueprint('backup', __name__, url_prefix='/api/backup')

@backup_bp.route('/create', methods=['POST'])
@role_required('admin')
def create_backup():
    """Create a new backup (admin only)"""
    try:
        filename = BackupUtility.create_backup()
        
        return success_response(
            {'filename': filename},
            "Backup created successfully",
            201
        )
        
    except Exception as e:
        return error_response(f"Failed to create backup: {str(e)}", 500)

@backup_bp.route('/list', methods=['GET'])
@role_required('admin')
def list_backups():
    """List all available backups (admin only)"""
    try:
        backups = BackupUtility.get_backup_info()
        
        return success_response(
            backups,
            f"Found {len(backups)} backup(s)"
        )
        
    except Exception as e:
        return error_response(f"Failed to list backups: {str(e)}", 500)

@backup_bp.route('/download/<filename>', methods=['GET'])
@role_required('admin')
def download_backup(filename):
    """Download a backup file (admin only)"""
    try:
        filepath = os.path.join('backups', filename)
        
        if not os.path.exists(filepath):
            return error_response("Backup file not found", 404)
        
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return error_response(f"Failed to download backup: {str(e)}", 500)

@backup_bp.route('/cleanup', methods=['POST'])
@role_required('admin')
def cleanup_backups():
    """Clean up old backups, keeping only recent ones (admin only)"""
    try:
        removed = BackupUtility.cleanup_old_backups(keep_count=5)
        
        return success_response(
            {'removed_count': removed},
            f"Cleaned up {removed} old backup(s)"
        )
        
    except Exception as e:
        return error_response(f"Failed to cleanup backups: {str(e)}", 500)
