"""Analytics service for dashboard statistics"""
from database import Database
from datetime import datetime, timedelta

class AnalyticsService:
    """Service for generating analytics and statistics"""
    
    @staticmethod
    def get_dashboard_stats():
        """Get comprehensive dashboard statistics"""
        stats = {}
        
        # Total accidents
        query = "SELECT COUNT(*) as total FROM accidents"
        result = Database.execute_query(query, fetch_one=True)
        stats['total_accidents'] = result['total'] if result else 0
        
        # Today's accidents
        query = "SELECT COUNT(*) as today FROM accidents WHERE DATE(timestamp) = CURDATE()"
        result = Database.execute_query(query, fetch_one=True)
        stats['today_accidents'] = result['today'] if result else 0
        
        # This week's accidents
        query = "SELECT COUNT(*) as week FROM accidents WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 7 DAY)"
        result = Database.execute_query(query, fetch_one=True)
        stats['week_accidents'] = result['week'] if result else 0
        
        # Active alerts
        query = "SELECT COUNT(*) as active FROM alerts WHERE is_active = TRUE"
        result = Database.execute_query(query, fetch_one=True)
        stats['active_alerts'] = result['active'] if result else 0
        
        # Severity distribution
        query = """
            SELECT severity, COUNT(*) as count 
            FROM accidents 
            GROUP BY severity
        """
        severity_dist = Database.execute_query(query, fetch_all=True) or []
        stats['severity_distribution'] = {item['severity']: item['count'] for item in severity_dist}
        
        # Type distribution
        query = """
            SELECT accident_type, COUNT(*) as count 
            FROM accidents 
            GROUP BY accident_type
        """
        type_dist = Database.execute_query(query, fetch_all=True) or []
        stats['type_distribution'] = {item['accident_type']: item['count'] for item in type_dist}
        
        return stats
    
    @staticmethod
    def get_accident_timeline(period='daily', days=30):
        """
        Get accident timeline data
        
        Args:
            period: 'daily' or 'hourly'
            days: Number of days to include
        """
        if period == 'hourly':
            query = """
                SELECT 
                    HOUR(timestamp) as hour,
                    COUNT(*) as count
                FROM accidents
                WHERE timestamp >= DATE_SUB(NOW(), INTERVAL %s DAY)
                GROUP BY HOUR(timestamp)
                ORDER BY hour
            """
        else:  # daily
            query = """
                SELECT 
                    DATE(timestamp) as date,
                    COUNT(*) as count
                FROM accidents
                WHERE timestamp >= DATE_SUB(NOW(), INTERVAL %s DAY)
                GROUP BY DATE(timestamp)
                ORDER BY date
            """
        
        return Database.execute_query(query, (days,), fetch_all=True) or []
    
    @staticmethod
    def get_accident_prone_zones(min_accidents=3, days=90):
        """
        Identify accident-prone zones using clustering
        
        Args:
            min_accidents: Minimum accidents to consider a zone prone
            days: Number of days to analyze
        """
        query = """
            SELECT 
                ROUND(latitude, 2) as lat_zone,
                ROUND(longitude, 2) as lon_zone,
                COUNT(*) as accident_count,
                AVG(latitude) as avg_lat,
                AVG(longitude) as avg_lon
            FROM accidents
            WHERE timestamp >= DATE_SUB(NOW(), INTERVAL %s DAY)
            GROUP BY lat_zone, lon_zone
            HAVING accident_count >= %s
            ORDER BY accident_count DESC
        """
        
        return Database.execute_query(query, (days, min_accidents), fetch_all=True) or []
    
    @staticmethod
    def get_severity_by_type():
        """Get severity distribution by accident type"""
        query = """
            SELECT 
                accident_type,
                severity,
                COUNT(*) as count
            FROM accidents
            GROUP BY accident_type, severity
            ORDER BY accident_type, severity
        """
        
        return Database.execute_query(query, fetch_all=True) or []
    
    @staticmethod
    def get_monthly_stats(months=12):
        """Get monthly accident statistics"""
        query = """
            SELECT 
                DATE_FORMAT(timestamp, '%%Y-%%m') as month,
                COUNT(*) as total,
                SUM(CASE WHEN severity = 'high' THEN 1 ELSE 0 END) as high_severity,
                SUM(CASE WHEN severity = 'medium' THEN 1 ELSE 0 END) as medium_severity,
                SUM(CASE WHEN severity = 'low' THEN 1 ELSE 0 END) as low_severity
            FROM accidents
            WHERE timestamp >= DATE_SUB(NOW(), INTERVAL %s MONTH)
            GROUP BY month
            ORDER BY month
        """
        
        return Database.execute_query(query, (months,), fetch_all=True) or []
    
    @staticmethod
    def get_peak_hours():
        """Get peak accident hours"""
        query = """
            SELECT 
                HOUR(timestamp) as hour,
                COUNT(*) as count
            FROM accidents
            GROUP BY hour
            ORDER BY count DESC
            LIMIT 5
        """
        
        return Database.execute_query(query, fetch_all=True) or []
