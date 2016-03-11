import __builtin__
from qpylib import get_app_base_url, q_url_for
__author__ = 'IBM'
__version__ = '0.10+fb50554cc8764c44f9be25a386311a802baf40bd'

__builtin__.get_app_base_url = qpylib.get_app_base_url
__builtin__.q_url_for = qpylib.q_url_for
