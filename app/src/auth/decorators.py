from flask import session,abort,redirect,url_for
from functools import wraps
from bson.objectid import ObjectId

# Database Connection string
from config.db.connection import weggo

def anonymous_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if '_WEGGO_USER' in session:
            weggo.db.users.find_one({'_id': ObjectId(session['_WEGGO_USER'])})
            return redirect(url_for('public.index'))
        else:
            pass
        return f(*args, **kws)
    return decorated_function


def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if '_WEGGO_USER' in session:
            u = weggo.db.users.find_one({'_id': ObjectId(session['_WEGGO_USER'])})
            if u['access']['type'] == 'user' or 'supplier':
                pass
            else:
                return redirect(url_for('auth.register'))
        if '_WEGGO_USER' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kws)
    return decorated_function


def coll_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if '_WEGGO_USER' in session:
            user = session['_WEGGO_USER']
            weggo_user = weggo.db.users.find_one({'_id': ObjectId(user)})
            if weggo_user['access']['type'] == 'collaborator':
                pass
            else:
                abort(403)
        if '_WEGGO_USER' not in session:
            return redirect(url_for('public.index'))
        return f(*args, **kws)
    return decorated_function

def moderator_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if '_WEGGO_USER' in session:
            user = session['_WEGGO_USER']
            weggo_user = weggo.db.users.find_one({'_id': ObjectId(user)})
            if weggo_user['access']['type'] == 'moderator' or weggo_user['access']['type'] == 'administrator':
                pass
            else:
                abort(403)
        if '_WEGGO_USER' not in session:
            return redirect(url_for('public.index'))
        return f(*args, **kws)
    return decorated_function

def moderator_level_3_or_administrator_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if '_WEGGO_USER' in session:
            user = session['_WEGGO_USER']
            weggo_user = weggo.db.users.find_one({'_id': ObjectId(user)})
            if weggo_user['access']['type'] == 'moderator' and weggo_user['access']['range'] > 2 or weggo_user['access']['type'] == 'administrator':
                pass
            else:
                abort(403)
        if '_WEGGO_USER' not in session:
            return redirect(url_for('public.index'))
        return f(*args, **kws)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if '_WEGGO_USER' in session:
            weggo_user = weggo.db.users.find_one({'_id': ObjectId(session['_WEGGO_USER'])})
            is_admin = weggo_user['is_admin']
            if not is_admin:
                abort(403)
            if is_admin:
                pass
        if '_WEGGO_USER' not in session:
            return redirect(url_for('public.index'))
        return f(*args, **kws)
    return decorated_function


def page_deactivated(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if '_WEGGO_USER' in session:
            return redirect(url_for('public.maintenance_page'))
        if '_WEGGO_USER' not in session:
            return redirect(url_for('public.maintenance_page'))
        return f(*args, **kws)
    return decorated_function

def coming_soon(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if '_WEGGO_USER' in session:
            return redirect(url_for('auth.coming_soon'))
        return f(*args, **kws)
    return decorated_function