"""User statistics service"""
from database import Database
from datetime import datetime, timedelta

class UserStatsService:
    """Service for user activity and statistics"""
    
    @staticmethod
    def get_user_statistics(user_id):
        """
        Get comprehensive statistics for a user
        
        Args:
            user_id: User ID
            
        Returns:
            Dictionary with user statistics
        """
        stats = {}
        
        # Total reports
        query = "SELECT COUNT(*) as total FROM accidents WHERE user_id = %s"
        result = Database.execute_query(query, (user_id,), fetch_one=True)
        stats['total_reports'] = result['total'] if result else 0
        
        # Reports this month
        query = """
            SELECT COUNT(*) as month_total 
            FROM accidents 
            WHERE user_id = %s 
            AND timestamp >= DATE_SUB(NOW(), INTERVAL 30 DAY)
        """
        result = Database.execute_query(query, (user_id,), fetch_one=True)
        stats['reports_this_month'] = result['month_total'] if result else 0
        
        # By severity
        query = """
            SELECT severity, COUNT(*) as count 
            FROM accidents 
            WHERE user_id = %s 
            GROUP BY severity
        """
        severity_dist = Database.execute_query(query, (user_id,), fetch_all=True) or []
        stats['by_severity'] = {item['severity']: item['count'] for item in severity_dist}
        
        # By type
        query = """
            SELECT accident_type, COUNT(*) as count 
            FROM accidents 
            WHERE user_id = %s 
            GROUP BY accident_type
        """
        type_dist = Database.execute_query(query, (user_id,), fetch_all=True) or []
        stats['by_type'] = {item['accident_type']: item['count'] for item in type_dist}
        
        # Recent activity
        query = """
            SELECT id, timestamp, accident_type, severity, status
            FROM accidents 
            WHERE user_id = %s 
            ORDER BY timestamp DESC 
            LIMIT 5
        """
        stats['recent_reports'] = Database.execute_query(query, (user_id,), fetch_all=True) or []
        
        return stats
    
    @staticmethod
    def get_leaderboard(limit=10):
        """
        Get top contributing users
        
        Args:
            limit: Number of users to return
            
        Returns:
            List of top users with report counts
        """
        query = """
            SELECT 
                u.id,
                u.username,
                u.role,
                COUNT(a.id) as report_count,
                MAX(a.timestamp) as last_report
            FROM users u
            LEFT JOIN accidents a ON u.id = a.user_id
            WHERE u.role = 'citizen'
            GROUP BY u.id, u.username, u.role
            HAVING report_count > 0
            ORDER BY report_count DESC
            LIMIT %s
        """
        
        return Database.execute_query(query, (limit,), fetch_all=True) or []
    
    @staticmethod
    def get_platform_statistics():
        """
        Get overall platform statistics
        
        Returns:
            Dictionary with platform-wide stats
        """
        stats = {}
        
        # Total users
        query = "SELECT COUNT(*) as total FROM users"
        result = Database.execute_query(query, fetch_one=True)
        stats['total_users'] = result['total'] if result else 0
        
        # Users by role
        query = "SELECT role, COUNT(*) as count FROM users GROUP BY role"
        role_dist = Database.execute_query(query, fetch_all=True) or []
        stats['users_by_role'] = {item['role']: item['count'] for item in role_dist}
        
        # Active users (reported in last 30 days)
        query = """
            SELECT COUNT(DISTINCT user_id) as active 
            FROM accidents 
            WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 30 DAY)
        """
        result = Database.execute_query(query, fetch_one=True)
        stats['active_users_30d'] = result['active'] if result else 0
        
        # Total accidents
        query = "SELECT COUNT(*) as total FROM accidents"
        result = Database.execute_query(query, fetch_one=True)
        stats['total_accidents'] = result['total'] if result else 0
        
        # Accidents today
        query = "SELECT COUNT(*) as today FROM accidents WHERE DATE(timestamp) = CURDATE()"
        result = Database.execute_query(query, fetch_one=True)
        stats['accidents_today'] = result['today'] if result else 0
        
        # Average reports per user
        if stats['total_users'] > 0:
            stats['avg_reports_per_user'] = round(stats['total_accidents'] / stats['total_users'], 2)
        else:
            stats['avg_reports_per_user'] = 0
        
        return stats
