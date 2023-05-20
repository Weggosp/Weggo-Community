"""
<!-- -| 
  
  * WEGGO is a registered trademark in Spain as Plataforma Weggo Espana, S.L
  * Any disclosure of this code violates intellectual property laws.
  * By Ruben Ayuso. 
  
|- -->
"""

from . import auth_wg
from flask import session,redirect,url_for
from bson.objectid import ObjectId

# Database Connection string
from config.db.connection import weggo as ws

@auth_wg.context_processor
def FORUMS_PROCESSOR():
    forums = []

    for i in ws.db.forums.find().sort('created', -1):
        forums.append({
            'forum': i['details']['name'],
            'slug': i['slug']
        })

    return dict(wForums = forums)

@auth_wg.context_processor
def USERS_PROCESSOR():
    if '_WEGGO_USER' in session:
        u = ws.db.users.find_one({'_id': ObjectId(session['_WEGGO_USER'])})
        n = ws.db.newsletter.find_one({'email': u['email']})
        return dict(wUser = u, wNewsletter = n, error = None)   
    else:
        return dict(wUser = {'not_login': True}, error = 'Anonymous user')