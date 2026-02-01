"""Export service for generating reports"""
import csv
import io
from datetime import datetime
from database import Database

class ExportService:
    """Service for exporting data to various formats"""
    
    @staticmethod
    def export_accidents_csv(filters=None):
        """
        Export accidents to CSV format
        
        Args:
            filters: Optional filters for accidents
            
        Returns:
            CSV string
        """
        # Build query
        query = """
            SELECT 
                a.id,
                a.timestamp,
                a.latitude,
                a.longitude,
                a.accident_type,
                a.severity,
                a.description,
                a.status,
                u.username as reported_by
            FROM accidents a
            JOIN users u ON a.user_id = u.id
            WHERE 1=1
        """
        params = []
        
        if filters:
            if 'severity' in filters:
                query += " AND a.severity = %s"
                params.append(filters['severity'])
            
            if 'accident_type' in filters:
                query += " AND a.accident_type = %s"
                params.append(filters['accident_type'])
            
            if 'start_date' in filters:
                query += " AND a.timestamp >= %s"
                params.append(filters['start_date'])
            
            if 'end_date' in filters:
                query += " AND a.timestamp <= %s"
                params.append(filters['end_date'])
        
        query += " ORDER BY a.timestamp DESC"
        
        # Get data
        accidents = Database.execute_query(query, tuple(params), fetch_all=True) or []
        
        # Create CSV
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([
            'ID', 'Timestamp', 'Latitude', 'Longitude', 
            'Type', 'Severity', 'Description', 'Status', 'Reported By'
        ])
        
        # Write data
        for accident in accidents:
            writer.writerow([
                accident['id'],
                accident['timestamp'],
                accident['latitude'],
                accident['longitude'],
                accident['accident_type'],
                accident['severity'],
                accident['description'] or '',
                accident['status'],
                accident['reported_by']
            ])
        
        return output.getvalue()
    
    @staticmethod
    def export_analytics_csv(start_date=None, end_date=None):
        """
        Export analytics summary to CSV
        
        Returns:
            CSV string with analytics data
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Summary statistics
        writer.writerow(['SAFE ROUTE Analytics Report'])
        writer.writerow(['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        writer.writerow([])
        
        # Total accidents
        query = "SELECT COUNT(*) as total FROM accidents"
        result = Database.execute_query(query, fetch_one=True)
        writer.writerow(['Total Accidents:', result['total'] if result else 0])
        
        # By severity
        writer.writerow([])
        writer.writerow(['Accidents by Severity'])
        writer.writerow(['Severity', 'Count'])
        
        query = "SELECT severity, COUNT(*) as count FROM accidents GROUP BY severity"
        results = Database.execute_query(query, fetch_all=True) or []
        for row in results:
            writer.writerow([row['severity'], row['count']])
        
        # By type
        writer.writerow([])
        writer.writerow(['Accidents by Type'])
        writer.writerow(['Type', 'Count'])
        
        query = "SELECT accident_type, COUNT(*) as count FROM accidents GROUP BY accident_type"
        results = Database.execute_query(query, fetch_all=True) or []
        for row in results:
            writer.writerow([row['accident_type'], row['count']])
        
        return output.getvalue()
    
    @staticmethod
    def get_heatmap_data(days=30, grid_size=0.01):
        """
        Get accident data formatted for heatmap visualization
        
        Args:
            days: Number of days to include
            grid_size: Grid size in degrees (0.01 ≈ 1km)
            
        Returns:
            List of heatmap points with intensity
        """
        query = """
            SELECT 
                ROUND(latitude / %s) * %s as lat,
                ROUND(longitude / %s) * %s as lon,
                COUNT(*) as intensity,
                SUM(CASE WHEN severity = 'high' THEN 3 
                         WHEN severity = 'medium' THEN 2 
                         ELSE 1 END) as weighted_intensity
            FROM accidents
            WHERE timestamp >= DATE_SUB(NOW(), INTERVAL %s DAY)
            GROUP BY lat, lon
            HAVING intensity > 0
            ORDER BY weighted_intensity DESC
        """
        
        results = Database.execute_query(
            query, 
            (grid_size, grid_size, grid_size, grid_size, days),
            fetch_all=True
        ) or []
        
        return [
            {
                'lat': float(row['lat']),
                'lng': float(row['lon']),
                'intensity': row['intensity'],
                'weight': row['weighted_intensity']
            }
            for row in results
        ]
