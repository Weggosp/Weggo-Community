from flask import request,session,render_template,redirect,url_for,flash,jsonify,abort
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from bson.objectid import ObjectId
from datetime import datetime
from . import auth_wg

# Imports
import bcrypt,os

# Database Connection string
from config.db.connection import weggo as ws
# Decorators
from app.src.auth.decorators import anonymous_required, moderator_required
# Functions
from app.src.auth.functions import Functions
# Forms
from app.src.auth.forms import LoginForm,UserSignup
# Libraries
from app.libraries.sendgrid.models import Emails

# * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * 
# * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * 

from app.src.auth.loads import USERS_PROCESSOR

@auth_wg.context_processor
def LOAD_USER():
    return USERS_PROCESSOR()

from bson.objectid import ObjectId
@auth_wg.before_request
def USER():
    global wUser
    if '_WEGGO_USER' in session:
        wUser = ws.db.users.find_one({'_id': ObjectId(session['_WEGGO_USER'])})
    elif '_WEGGO_USER' not in session:
        wUser = {'not_login': True}


# * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * 
# * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * 

from flask_breadcrumbs import register_breadcrumb,default_breadcrumb_root
# Breadcrumbs load
default_breadcrumb_root(auth_wg, '.auth')

class Connection:

    @auth_wg.route('/login', methods=['GET','POST'])
    @register_breadcrumb(auth_wg, '.auth.login', 'Conexión')
    @anonymous_required
    def login():
        form = LoginForm()
        if request.method == 'POST':
            items = {
                'email': str(request.form.get('email')).lower(),
                'password': form.password.data
            }

            if Functions.Users.login(items) == 200:
                return redirect(url_for('public.index'))
            else:
                return jsonify({'error': 'No existe coincidencia en la base de datos o la contraseña es incorrecta'})
        return render_template('login.html',title="Conectar a mi cuenta", form=form)

    @auth_wg.route('/register/user', methods=['GET', 'POST'])
    @register_breadcrumb(auth_wg, '.auth.register.user', 'Registro cómo usuario')
    @anonymous_required
    def register():
        error = None
        form = UserSignup()
        if form.validate_on_submit():
            items = {
                'email': str(form.email.data).lower(),
                'username': form.username.data,
                'password': form.password.data
            }

            error = Functions.Users.register(items)
            return redirect(url_for('auth.login'))

        return render_template('register.html',form=form,error=error,
        title="Registro cómo usuario")

    @auth_wg.route('/recover', methods=['GET', 'POST'])
    @register_breadcrumb(auth_wg, '.auth.recover', 'Recover')
    @anonymous_required
    def recover():
        if '_WEGGO_USER' not in session:
            error = None
            if request.method == 'POST':
                email = request.form.get('email')
                try:
                    # Try find the email. if True, send the password to email. Else, return error
                    # Return user that we send by email
                    from app.src.auth.models import Models
                    Models.Users.recover(email)
                    print("Pasa el recover")
                    next_page = request.args.get('next', None)
                    if not next_page or url_parse(next_page).netloc != '':
                        next_page = url_for('auth.recover')
                        flash(u'Se ha enviado la nueva contraseña al email facilitado', 'success')
                        return redirect(next_page)
                        
                except Exception as e:
                    Models.Tasks.registerError({
                        'message': 'An unexpected error has occurred while user recover his password',
                        'location': 'Line 355-389 - Function: recover; [routes.py in auth]',
                        'status': 'priority'
                    })
                    return e

                return render_template("recover.html", error=e)
            return render_template("recover.html", error=error)
        else:
            return redirect(url_for('public.index'))

    ############# ////
    @auth_wg.route('/logout')
    @register_breadcrumb(auth_wg, '.auth.logout', 'Desconexión')
    def logout():
        session.clear()
        return redirect(url_for('public.index'))

class Newsletter:

    @auth_wg.route('/newsletter/register', methods=['GET','POST'])
    def newsletter_register():
        form = request.form.get
        items = {
            'email': form('newsletterEmail'),
            'diaryNews': form('newsletterDiary'),
            'updates': form('newsletterUpdates'),
            'weeklySummary': form('newsletterSummary'),
            'events': form('newsletterEvents'),
            'partners': form('newsletterPartners'),
            'usersContent': form('newsletterUsersContent')
        }

        try:
            u = ws.db.newsletter.find_one({'email': items['email']})
            if not 'options' in u:
                Functions.Newsletter.newsletter_join(items)
                flash('Gracias por unirte a nuestra newsletter. Te compartiremos lo mejor de lo mejor ;)','success')
            else:
                flash('¡Ya estás subscrito a la newsletter!','warning')
            return redirect(url_for('public.index'))
        except:
            return abort(403)

class News:

    @auth_wg.route('/news/like/<string:slug>', methods=['POST'])
    def new_like(slug):
        ws.db.news.update_one({'slug': slug},{'$push': {
            'likes': request.args.get('user')
        }})
        return redirect(url_for('public.news_single', slug=slug))
        
    @auth_wg.route('/news/unlike/<string:slug>', methods=['POST'])
    def new_unlike(slug):
        ws.db.news.update_one({'slug': slug},{'$pull': {
            'likes': request.args.get('user')
        }})
        return redirect(url_for('public.news_single', slug=slug))  
    
    @auth_wg.route('/news/comment/<string:slug>', methods=['POST'])
    def new_comment(slug):
        items = {
            'slug': slug,
            'email': request.form.get('email'),
            'avatar': wUser['profile']['avatar'] if 'profile' in wUser and wUser['profile']['avatar'] != None else 'anonymous',
            'fullname': request.form.get('fullname'),
            'body': request.form.get('comment')
        }

        print(items)

        Functions.News.Comments.create(items)
        flash('Se ha creado correctamente tu comentario','success')
        return redirect(url_for('public.news_single', slug=slug))  
    

class Forums:
    
    class Post:

        @auth_wg.route('/<string:forum>/post/create', methods=['POST'])
        @register_breadcrumb(auth_wg, '.auth.forum.post.create', 'Create post')
        def forum_post_create(forum):
            items = {
                'title': request.form.get('post_title'),
                'category': request.form.get('post_category'),
                'tags': request.form.get('post_tags').split(','),
                'body': request.form.get('post_body'),
            }
            print(wUser['username'])
            post_slug = Functions.Users.Posts.create(forum,items,wUser['username'])
            return redirect(url_for('public.forums_post', slug=forum, post_slug=post_slug))

        @auth_wg.route('/<string:forum>/<string:post>/comment/create', methods=['POST'])
        def forum_post_comment_create(forum,post):
            items = {
                'username': wUser['username'],
                'comment': request.form.get('comment_body'),
                'forum': forum,
                'post': post
            }

            Functions.Users.Posts.Comments.create(items)
            flash('Comentario creado con éxito','success')
            return redirect(url_for('public.forums_post', slug=forum, post_slug=post))
        
        class Actions:

            @auth_wg.route('/<string:forum>/<string:post>/giveLeaf', methods=['POST'])
            def forum_post_give_leaf(forum,post):
                items={
                    'from': wUser['username'],
                    'to': request.form.get('author_username'),
                    'forum': forum,
                    'post': post
                }

                Functions.Users.Posts.Actions.give_leaf(items)
                flash('Leaf dado con éxito','success')

                return redirect(url_for('public.forums_post', slug=forum, post_slug=post))

class Administration:

    class News:

        @auth_wg.route('/news/create', methods=['POST'])
        @moderator_required
        def new_create():
            form = request.form.get

            items = {
                'name': form('new_name'),
                'section': form('new_section'),
                'tags': form('new_tags').split(','),
                'short_description': form('new_short_description'),
                'description': form('new_description'),
                'read_time': form('new_read_time'),
                'user': {
                    'avatar': wUser['profile']['avatar'],
                    'fullname': wUser['information']['fullname']
                }
            }
            
            # Uplaoding thumbnail to S3
            thumbnail = request.files['new_thumbnail']
            filename = (secure_filename(thumbnail.filename)).replace(' ','-').lower()
            thumbnail.save(filename)

            r = Functions.Uploads.Images.new_thumbnail(filename,items['name'])
            os.remove(filename)
            r2 = Functions.Administration.News.create(items)
            flash("Noticia creada con éxito","success")
            return redirect(url_for('panel.news'))


    class Forum:

        @auth_wg.route('/forum/create', methods=['POST'])
        @register_breadcrumb(auth_wg, '.auth.forum.create', 'Forum creation')
        @moderator_required
        def forum_create():
            if request.method == 'POST':
                items = {
                    'name': request.form.get('forum_name'),
                    'category': request.form.get('forum_category'),
                    'description': request.form.get('forum_description'),
                    'icon': request.form.get('forum_icon'),
                    'color': request.form.get('forum_color'),
                    'type': request.form.get('forum_type'),
                }
                print(items)
                Functions.Administration.Forum.create(items)
                return redirect(url_for('public.index'))

        @auth_wg.route('/forum/up', methods=['POST'])
        @register_breadcrumb(auth_wg, '.auth.forum.up', 'Forum ascend')
        @moderator_required
        def forum_up():
                Functions.Administration.Forum.up(request.form.get('forum_up_slug'),request.form.get('forum_up_show'))
                return redirect(url_for('public.index'))    
    

        @auth_wg.route('/forum/down', methods=['POST'])
        @register_breadcrumb(auth_wg, '.auth.forum.down', 'Forum descend')
        @moderator_required
        def forum_down():
                Functions.Administration.Forum.down(request.form.get('forum_down_slug'),request.form.get('forum_down_show'))
                return redirect(url_for('public.index'))    
    
        class Posts:

            @auth_wg.route('/<string:forum>/<string:post>/pin', methods=['POST'])
            @moderator_required
            def forum_posts_pin(forum,post):
                Functions.Administration.Forum.Posts.pin(forum,post)
                
                return redirect(url_for('public.index')) 
    
          
    class Category:

        @auth_wg.route('/category/create', methods=['POST'])
        @register_breadcrumb(auth_wg, '.auth.category.create', 'Category creation')
        @moderator_required
        def category_create():
            if request.method == 'POST':
                Functions.Administration.Category.create(items={
                    'name': request.form.get('category_name'),
                    'color': request.form.get('category_color'),
                })
                return redirect(url_for('public.index'))
            
class Profile:
    @auth_wg.route('/perfil/contraseña', methods=['GET', 'POST'])
    def profile_password():
        if request.method == 'POST':
            password1 = request.form.get('password')
            password2 = request.form.get('password2')
            if password1 == password2:
                hash_password = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
                ws.db.users.update_one({'username': wUser['username']}, {'$set': {
                    'password': hash_password,
                    'updated': datetime.now()
                }})
                flash('La contraseña ha sido modificada correctamente. Ya puedes iniciar sesión con tu nueva contraseña', 'success')
                return redirect(url_for('public.profile_security'))
            else:
                flash('Las contraseñas proporcionadas no coinciden. Comprueba que estén bien escritas.', 'danger')
                return redirect(url_for('public.profile_security'))
        return render_template('user/profile/reset.html')

class errors:
    def page_refresh(e):
        400
        return redirect(url_for('public.index'))

    def page_not_found(e):
        404
        return redirect(url_for('public.index'))
        
    def page_not_access(e):
        return render_template('errors/403.html', title="¡No tienes autorización para acceder!"), 403

    def page_need_arguments(e):
        return render_template('errors/401.html', title="Se ha producido un error al cargar la función. Vuelva a intentarlo"), 401

    def page_only_users_except_autor(e):
        return render_template('errors/406.html'), 406
