"""Initialize models package"""
from models.user import User
from models.accident import Accident
from models.alert import Alert
from models.emergency_service import EmergencyService
from models.awareness import AwarenessContent

__all__ = ['User', 'Accident', 'Alert', 'EmergencyService', 'AwarenessContent']
