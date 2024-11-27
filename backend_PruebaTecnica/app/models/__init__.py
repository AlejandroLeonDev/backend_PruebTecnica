from app import db

from .airline import Airline
from .airport import Airport
from .movement import Movement
from .flight import Flight

__all__ = ['Airline', 'Airport', 'Movement', 'Flight']