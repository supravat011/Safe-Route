"""Backup and restore utilities"""
import json
import os
from datetime import datetime
from database import Database

class BackupUtility:
    """Utility for backing up and restoring data"""
    
    @staticmethod
    def create_backup(backup_dir='backups'):
        """
        Create a JSON backup of all data
        
        Args:
            backup_dir: Directory to store backups
            
        Returns:
            Backup filename
        """
        # Create backup directory if it doesn't exist
        os.makedirs(backup_dir, exist_ok=True)
        
        backup_data = {}
        
        # Backup users (without passwords)
        query = "SELECT id, username, email, role, created_at FROM users"
        backup_data['users'] = Database.execute_query(query, fetch_all=True) or []
        
        # Backup accidents
        query = "SELECT * FROM accidents"
        backup_data['accidents'] = Database.execute_query(query, fetch_all=True) or []
        
        # Backup alerts
        query = "SELECT * FROM alerts"
        backup_data['alerts'] = Database.execute_query(query, fetch_all=True) or []
        
        # Backup emergency services
        query = "SELECT * FROM emergency_services"
        backup_data['emergency_services'] = Database.execute_query(query, fetch_all=True) or []
        
        # Backup awareness content
        query = "SELECT * FROM awareness_content"
        backup_data['awareness_content'] = Database.execute_query(query, fetch_all=True) or []
        
        # Add metadata
        backup_data['metadata'] = {
            'backup_date': datetime.now().isoformat(),
            'version': '1.0'
        }
        
        # Convert datetime objects to strings
        backup_data = json.loads(json.dumps(backup_data, default=str))
        
        # Save to file
        filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(backup_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(backup_data, f, indent=2)
        
        return filename
    
    @staticmethod
    def get_backup_info(backup_dir='backups'):
        """
        Get information about available backups
        
        Returns:
            List of backup files with metadata
        """
        if not os.path.exists(backup_dir):
            return []
        
        backups = []
        for filename in os.listdir(backup_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(backup_dir, filename)
                file_stats = os.stat(filepath)
                
                backups.append({
                    'filename': filename,
                    'size': file_stats.st_size,
                    'created': datetime.fromtimestamp(file_stats.st_mtime).isoformat()
                })
        
        return sorted(backups, key=lambda x: x['created'], reverse=True)
    
    @staticmethod
    def cleanup_old_backups(backup_dir='backups', keep_count=5):
        """
        Remove old backups, keeping only the most recent ones
        
        Args:
            backup_dir: Directory containing backups
            keep_count: Number of recent backups to keep
        """
        backups = BackupUtility.get_backup_info(backup_dir)
        
        if len(backups) > keep_count:
            for backup in backups[keep_count:]:
                filepath = os.path.join(backup_dir, backup['filename'])
                os.remove(filepath)
        
        return len(backups) - keep_count if len(backups) > keep_count else 0
