"""
<!-- -| 
  
  * WEGGO is a registered trademark in Spain as Plataforma Weggo Espana, S.L
  * Any disclosure of this code violates intellectual property laws.
  * By Ruben Ayuso. 
  
|- -->
"""

from flask import Blueprint
api_wg = Blueprint('api', __name__, template_folder='templates')
from . import routes