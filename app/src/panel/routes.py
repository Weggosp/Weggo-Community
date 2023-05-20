from flask import render_template,session
from flask_breadcrumbs import register_breadcrumb, default_breadcrumb_root
from app.src.auth.decorators import moderator_level_3_or_administrator_required
from . import panel_wg

# Database Connection
from config.db.connection import weggo as ws


# * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * 
# * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * 

from app.src.auth.loads import USERS_PROCESSOR

@panel_wg.context_processor
def LOAD_USER():
    return USERS_PROCESSOR()

from bson.objectid import ObjectId
@panel_wg.before_request
@moderator_level_3_or_administrator_required
def USER():
    global wUser
    if '_WEGGO_USER' in session:
        wUser = ws.db.users.find_one({'_id': ObjectId(session['_WEGGO_USER'])})
    elif '_WEGGO_USER' not in session:
        wUser = {'not_login': True}


# * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * 
# * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * 

default_breadcrumb_root(panel_wg, '.panel')

@panel_wg.route("/", methods=['GET','POST'])
@register_breadcrumb(panel_wg, '.panel', 'Panel de administración')
def index():    
    forums = []
    for i in ws.db.forums.find():
        forums.append(i)

    return render_template('panel.html',
                           title="Panel de administración",
                           forums=forums)

class News:
        
    @panel_wg.route("/news", methods=['GET'])
    @register_breadcrumb(panel_wg, '.news', 'Noticias')
    def news():
        news = []
        for i in ws.db.news.find():
            news.append(i)

        return render_template('news.html',
                               title="Noticias",
                               news=news)
    

    @panel_wg.route("/news/create", methods=['GET'])
    @register_breadcrumb(panel_wg, '.news.create', 'Crear noticia')
    def news_create():
        categories = []
        for i in ws.db.categories.find():
            categories.append(i['name'])

        return render_template('news_create.html',
                               title="Crear noticia",
                               categories=categories)