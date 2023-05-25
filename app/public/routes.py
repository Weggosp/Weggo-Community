from flask import render_template,flash,request,session,redirect,url_for,abort,send_from_directory
from flask_breadcrumbs import register_breadcrumb, default_breadcrumb_root
from app.src.auth.decorators import page_deactivated
from werkzeug.urls import url_parse
from datetime import datetime
from . import public_wg

from app import app

# Database Connection
from config.db.connection import weggo as ws


# * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * 
# * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * 

from app.src.auth.loads import USERS_PROCESSOR,FORUMS_PROCESSOR

@public_wg.context_processor
def LOAD_FORUMS():
    return FORUMS_PROCESSOR()

@public_wg.context_processor
def LOAD_USER():
    return USERS_PROCESSOR()

from bson.objectid import ObjectId
@public_wg.before_request
def USER():
    global wUser
    if '_WEGGO_USER' in session:
        wUser = ws.db.users.find_one({'_id': ObjectId(session['_WEGGO_USER'])})
    elif '_WEGGO_USER' not in session:
        wUser = {'not_login': True}


# * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * 
# * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * # * 

# Breadcrumbs load
default_breadcrumb_root(public_wg, '.')


@public_wg.route("/", methods=['GET','POST'])
@register_breadcrumb(public_wg, '.', 'Comunidad')
def index():
    if 'community_index' in session:
        return redirect(url_for('public.community'))
    else:
        news = []

        for i in ws.db.news.find().limit(9).sort("likes",-1):
            news.append({
                'title': i['title'],
                'slug': i['slug'],
                'section': i['section'],
                'shortDescription': i['shortDescription'],
                'likes': i['likes'],
                'comments': i['comments'],
                'shares': i['shares']
            })

        users = []
        leafs = []
        for i in ws.db.users.find():
            users.append(1)
        for i in ws.db.leafs.find():
            leafs.append(1)

        return render_template('landing.html',
        title="Weggo España",
        header_landing=True,
        users=users,leafs=leafs,news=news)


@public_wg.route("/comunidad")
@public_wg.route("/comunidad/", methods=['GET','POST'])
@register_breadcrumb(public_wg, '.community', 'Comunidad')
def community():
    session['community_index']=True

    forums = []
    for i in ws.db.forums.find().sort("show", 1):
        forums.append(i)

    categories = []
    for i in ws.db.categories.find():
        categories.append(i)

    return render_template('landing-community.html',
    title="Comunidad de Weggo",   
    returned='community',
    now=datetime.now(),str=str,ws=ws,
    forums=forums,categories=categories,
    favorite_set_cookie_off=True)

class Sections:

    def view_item(*args, **kwargs):
        item = request.view_args['slug']
        return [{'text': " ".join((item.replace('-', ' ')).split(' ')[0:-1]).capitalize(), ' url ': '#'}]
    
    @public_wg.route("/<string:slug>/", methods=['GET'])
    @register_breadcrumb(public_wg, '.forums', '', dynamic_list_constructor=view_item)
    def forums(slug):
        try:
            forum=ws.db.forums.find_one({'slug': slug})
            return render_template('community/forums.html',
                                title=forum['details']['name']+' | Weggo España',
                                forum=forum,
                                categories=ws.db.categories.find(),
                                now=datetime.now(),str=str)
        except:
            return redirect(url_for('public.index'))

    @public_wg.route("/<string:slug>/<string:post_slug>", methods=['GET'])
    @register_breadcrumb(public_wg, '.forums.post', '', dynamic_list_constructor=view_item)
    def forums_post(slug,post_slug):
        try:
            forum = ws.db.forums.find_one({'slug': slug, 'posts.slug': post_slug})

            title = None
            for i in forum['posts']:
                if i['slug'] == post_slug:
                    title = i['title']

            return render_template('community/forums_post.html',title=title+' | Weggo España',
                                now=datetime.now(),str=str,ws=ws,
                                forum=forum,post_slug=post_slug)
        except:
            flash('Lo sentimos, no hemos podido encontrar la publicación :/','danger')
            return redirect(url_for('public.forums', slug=slug))

    @public_wg.route("/<string:slug>/", methods=['GET'])
    @register_breadcrumb(public_wg, '.slugs', '', dynamic_list_constructor=view_item)
    def slugs(slug):
        try:
            object = ws.db.slugs.find_one({'slug': slug})

            type = object['type']
            if type == 'section':
                return render_template('community/sections.html')
            elif type == 'category':
                return """ """
            elif type == 'section':
                return """ """
            else:
                return """ NO SE PASADO EL PARÁMETRO TYPE """
        except:
            return abort(415)

class News:
    def view_item(*args, **kwargs):
        item = request.view_args['slug']
        return [{'text': " ".join((item.replace('-', ' ')).split(' ')).capitalize(), ' url ': '#'}]
    
    @public_wg.route("/news", methods=['GET', 'POST'])
    @register_breadcrumb(public_wg, '.news', 'Noticias')
    def news():
        categories = []
        for i in ws.db.categories.find():
            categories.append(i['name'])
        return render_template('news/news-index.html', categories=categories,
                               title="Sigue el día a día del sector camping")
    
    @public_wg.route("/news/", methods=['GET', 'POST'], defaults={'slug': None})
    @public_wg.route("/news/<string:slug>", methods=['GET', 'POST'])
    @register_breadcrumb(public_wg, '.news.single', '', dynamic_list_constructor=view_item)
    def news_single(slug):
        new = ws.db.news.find_one({'slug': slug})
        title = "".join(str(slug.replace('-',' ')).capitalize())
        return render_template('news/news-single.html',
                               title=title,
                               new=new, str=str,
                               now=datetime.now())


class Pages:

    @public_wg.route("/maintenance")
    @register_breadcrumb(public_wg, '.maintenance_page', 'Página en mantenimiento')
    def maintenance_page():
        return render_template("pages/maintenance_page.html",
        title="Lo sentimos, esta página se encuentra en mantenimiento")


    @public_wg.route("/newsletter")
    @register_breadcrumb(public_wg, '.newsletter', 'Subscripción a la newsletter')
    def newsletter():
        return render_template("pages/newsletter.html",
        title="Subscripción a la newsletter de Weggo")



    class Profile:

        from app.src.auth.decorators import user_required
        @public_wg.route('/w/dashboard')
        @user_required
        def profile():   
            return render_template('profile/profile.html')


        @public_wg.route('/w/favorites')
        @user_required
        def profile_favorites():   
            return render_template("pages/profile/profile-my-favorites.j2",
            w=True,w_favorites=True,
            title="Ver todas las ofertas guardadas",
            page_title="Mis ofertas guardadas")


        @public_wg.route("/w/bookings")
        @register_breadcrumb(public_wg, '.profile.bookings', 'Reservas realizadas')
        @user_required
        def profile_bookings():
            slugs = []
            info = []
            from datetime import datetime
            for b in ws.db.bookings.find({'customer.email': wUser['email']}).sort("created",-1):
                slugs.append(b['slug'])
                info.append({
                    'offer': ws.db.offers.find_one({'information.slug': b['slug'], 'status': 'active'}),
                    'booking': {
                        'bookingid': b['bookingid'],
                        'companyid': b['companyid'],
                        'amount': b['amount'],
                        'dates': {
                            'from': datetime.strftime(datetime.strptime(b['dates']['from'], '%d-%m-%Y'),'%d %b %Y'),
                            'to': datetime.strftime(datetime.strptime(b['dates']['to'], '%d-%m-%Y'),'%d %b %Y')
                        },      
                        'status': b['status'],
                        'created': b['created']
                    }
                })

            return render_template("pages/profile/profile-my-bookings.j2",
            w=True,w_bookings=True,
            slugs=slugs,info=info,
            title="Reservas realizadas",
            page_title="Mis reservas realizadas")


        @public_wg.route("/w/edit", methods=['GET', 'POST'])
        @page_deactivated
        def profile_edit():
            local = 0
            if wUser.is_anonymous:
                return redirect(url_for('public.index'))

            autor = wUser.nombre + "\n" + wUser.apellido
            id = wUser.id

            if request.method == 'POST':
                form = request.form.get
    
                # Seleccionamos nuestros datos del form
                tel = form("telefono")
                nif = form("documento_identidad")
                direccion = form("direccion")
                cp = form("cp")
                provincia = form("provincia")
                ciudad = form("ciudad")
                fechaActualizacion = datetime.now().strftime('%d-%m-%Y %H:%M')
                
                next_page = request.args.get('next', None)

                if not next_page or url_parse(next_page).netloc != '':
                    next_page = url_for('public.index')
                    flash('¡Tu perfil se ha actualizado correctamente!', 'success')

                return redirect(next_page) # Si todo correcto, redirigimos al index de colaborador
            else:
                print("FORMULARIO NO VALIDADO")
            return render_template("pages/perfil/editar_perfil.html")


        @public_wg.route("/w/security")
        @user_required
        def profile_security():
            return render_template("pages/profile/profile-security.j2",
            w=True,w_security=True,
            title="Cambiar contraseña de acceso")


    class Footer:
 
        @public_wg.route("/faq")
        @register_breadcrumb(public_wg, '.faq', 'FAQ')
        def support_faq():
            return render_template("pages/faq.html")


        @public_wg.route("/policies/privacity")
        @register_breadcrumb(public_wg, '.politica-de-privacidad', 'Politica de privacidad')
        def privacy():
            return render_template("pages/policy-privacy.html")


        @public_wg.route("/policies/cookies")
        @register_breadcrumb(public_wg, '.politica-de-cookies', 'Politica de cookies')
        def cookies():
            return render_template("pages/policy-cookies.html")


        @public_wg.route("/policies/terms")
        @register_breadcrumb(public_wg, '.condiciones-de-uso', 'Condiciones de uso')
        def terms():
            return render_template("pages/policy-terms.html")

@app.route('/robots.txt')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route("/sitemap.xml")
def xml_sitemap():
    """
        Route to dynamically generate a sitemap of your website/application.
        lastmod and priority tags omitted on static pages.
        lastmod included on dynamic content such as blog posts.
    """
    from flask import make_response, request, render_template
    from urllib.parse import urlparse

    host_components = urlparse(request.host_url)
    host_base = host_components.scheme + "://" + host_components.netloc

    # Static routes with static content
    static_urls = list()
    for rule in app.url_map.iter_rules():
        if not any(str(rule).startswith(x) for x in ['/api/', '/a/', '/w/', '/static/', '/dropzone/', '/panel/','/upload/']):
            url = {
                "loc": f"{host_base}{str(rule)}"
            }
            static_urls.append(url)

    # Dynamic routes with dynamic content
    dynamic_urls = list()
    forums = ws.db.forums.find()
    for forum in forums:
        url = {
            "title": f"{forum['details']['name']}",
            "loc": f"{host_base}/{forum['slug']}/",
            "lastmod": forum['created'].strftime("%Y-%m-%dT%H:%M:%SZ")
            }
        dynamic_urls.append(url)
        for post in forum['posts']:
            url = {
                "title": f"{post['title']}",
                "loc": f"{host_base}/{forum['slug']}/{post['slug']}/",
                "lastmod": post['created'].strftime("%Y-%m-%dT%H:%M:%SZ")
                }
            dynamic_urls.append(url)

    xml_sitemap = render_template("/sitemap.xml", static_urls=static_urls, dynamic_urls=dynamic_urls, host_base=host_base) # dynamic_urls=dynamic_urls
    response = make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"

    return response

