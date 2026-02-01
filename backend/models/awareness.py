"""Awareness content model"""
from database import Database

class AwarenessContent:
    """Road safety awareness content model"""
    
    @staticmethod
    def create(title, content, category, created_by, is_published=True):
        """Create new awareness content"""
        query = """
            INSERT INTO awareness_content 
            (title, content, category, created_by, is_published)
            VALUES (%s, %s, %s, %s, %s)
        """
        
        try:
            content_id = Database.execute_query(
                query,
                (title, content, category, created_by, is_published),
                commit=True
            )
            return content_id
        except Exception as e:
            print(f"Error creating awareness content: {e}")
            return None
    
    @staticmethod
    def get_all(category=None, published_only=True):
        """Get all awareness content"""
        query = "SELECT * FROM awareness_content WHERE 1=1"
        params = []
        
        if published_only:
            query += " AND is_published = TRUE"
        
        if category:
            query += " AND category = %s"
            params.append(category)
        
        query += " ORDER BY created_at DESC"
        
        return Database.execute_query(query, tuple(params), fetch_all=True) or []
    
    @staticmethod
    def get_by_id(content_id):
        """Get content by ID"""
        query = "SELECT * FROM awareness_content WHERE id = %s"
        return Database.execute_query(query, (content_id,), fetch_one=True)
    
    @staticmethod
    def update(content_id, **kwargs):
        """Update awareness content"""
        allowed_fields = ['title', 'content', 'category', 'is_published']
        updates = []
        values = []
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                updates.append(f"{field} = %s")
                values.append(value)
        
        if not updates:
            return False
        
        values.append(content_id)
        query = f"UPDATE awareness_content SET {', '.join(updates)} WHERE id = %s"
        
        try:
            Database.execute_query(query, tuple(values), commit=True)
            return True
        except Exception:
            return False
    
    @staticmethod
    def delete(content_id):
        """Delete awareness content"""
        query = "DELETE FROM awareness_content WHERE id = %s"
        try:
            Database.execute_query(query, (content_id,), commit=True)
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_categories():
        """Get all unique categories"""
        query = "SELECT DISTINCT category FROM awareness_content WHERE is_published = TRUE ORDER BY category"
        results = Database.execute_query(query, fetch_all=True) or []
        return [r['category'] for r in results if r['category']]
