"""
MongoDB Database Connection
Manages database connectivity using Motor (async MongoDB driver)
"""

from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional

from app.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class Database:
    """MongoDB database connection manager"""
    
    client: Optional[AsyncIOMotorClient] = None
    database = None
    
    @classmethod
    async def connect_db(cls):
        """
        Establish database connection
        """
        try:
            logger.info(f"Connecting to MongoDB: {settings.DATABASE_NAME}")
            
            cls.client = AsyncIOMotorClient(
                settings.MONGODB_URI,
                serverSelectionTimeoutMS=5000
            )
            
            cls.database = cls.client[settings.DATABASE_NAME]
            
            # Test connection
            await cls.client.admin.command('ping')
            
            logger.info("MongoDB connection established successfully")
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise
    
    @classmethod
    async def close_db(cls):
        """
        Close database connection
        """
        if cls.client:
            cls.client.close()
            logger.info("MongoDB connection closed")
    
    @classmethod
    def get_database(cls):
        """
        Get database instance
        
        Returns:
            Database instance
        """
        return cls.database
    
    @classmethod
    async def ping(cls) -> bool:
        """
        Ping database to check connection
        
        Returns:
            True if connection is alive
        """
        try:
            await cls.client.admin.command('ping')
            return True
        except Exception:
            return False


# Dependency for FastAPI routes
async def get_database():
    """
    FastAPI dependency to get database instance
    
    Yields:
        Database instance
    """
    return Database.get_database()
