from fastapi import APIRouter

from ..constants import api_msgs
from ..utils.router_settings import get_router_settings

protected_singular = APIRouter(**get_router_settings(
  {
    'is_protected': True,
    'prefix': '/review',
    'tags': ['review'],
    'responses': api_msgs.API_RESPONSES
  }  
))
protected_plural = APIRouter(**get_router_settings(
  {
    'is_protected': True,
    'prefix': '/reviews',
    'tags': ['review'],
    'responses': api_msgs.API_RESPONSES
  }  
))

public_singular = APIRouter(**get_router_settings(
  {
    'is_protected': False,
    'prefix': '/review',
    'tags': ['review'],
    'responses': api_msgs.API_RESPONSES
  }  
))

public_plural = APIRouter(**get_router_settings(
  {
    'is_protected': False,
    'prefix': '/reviews',
    'tags': ['review'],
    'responses': api_msgs.API_RESPONSES
  }  
))