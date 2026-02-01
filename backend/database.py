import mysql.connector
from mysql.connector import Error, pooling
from config import Config
import logging

logger = logging.getLogger(__name__)

class Database:
    """Database connection manager with connection pooling"""
    
    _connection_pool = None
    
    @classmethod
    def init_pool(cls):
        """Initialize connection pool"""
        try:
            cls._connection_pool = pooling.MySQLConnectionPool(
                pool_name="safe_route_pool",
                pool_size=5,
                pool_reset_session=True,
                host=Config.DB_HOST,
                port=Config.DB_PORT,
                database=Config.DB_NAME,
                user=Config.DB_USER,
                password=Config.DB_PASSWORD
            )
            logger.info("Database connection pool initialized")
        except Error as e:
            logger.error(f"Error creating connection pool: {e}")
            raise
    
    @classmethod
    def get_connection(cls):
        """Get a connection from the pool"""
        if cls._connection_pool is None:
            cls.init_pool()
        
        try:
            return cls._connection_pool.get_connection()
        except Error as e:
            logger.error(f"Error getting connection from pool: {e}")
            raise
    
    @classmethod
    def execute_query(cls, query, params=None, fetch_one=False, fetch_all=False, commit=False):
        """
        Execute a database query
        
        Args:
            query: SQL query string
            params: Query parameters (tuple or dict)
            fetch_one: Return single row
            fetch_all: Return all rows
            commit: Commit transaction
            
        Returns:
            Query results or last inserted ID
        """
        connection = None
        cursor = None
        
        try:
            connection = cls.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute(query, params or ())
            
            if fetch_one:
                result = cursor.fetchone()
            elif fetch_all:
                result = cursor.fetchall()
            elif commit:
                connection.commit()
                result = cursor.lastrowid
            else:
                result = None
            
            return result
            
        except Error as e:
            if connection:
                connection.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @classmethod
    def execute_many(cls, query, params_list):
        """Execute multiple queries in a transaction"""
        connection = None
        cursor = None
        
        try:
            connection = cls.get_connection()
            cursor = connection.cursor()
            
            cursor.executemany(query, params_list)
            connection.commit()
            
            return cursor.rowcount
            
        except Error as e:
            if connection:
                connection.rollback()
            logger.error(f"Database error in execute_many: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    @classmethod
    def test_connection(cls):
        """Test database connection"""
        try:
            connection = cls.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            connection.close()
            return True
        except Error as e:
            logger.error(f"Database connection test failed: {e}")
            return False
