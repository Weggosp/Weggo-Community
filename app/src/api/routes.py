from app.src.api import api_wg
from app.src.auth.decorators import anonymous_required
from flask import session,request,flash,redirect,url_for
import json,bcrypt

# Database Connection string
from config.db.connection import weggo as ws


## LOGIN API FUNCTION 

@api_wg.route('/login', methods=['GET', 'POST'])
@anonymous_required
def login():
    from app.src.auth.forms import LoginForm
    form = LoginForm()
    try:
        if request.method == 'POST':
            u = ws.db.users.find_one({'$or': [{"email": str(request.form.get('email_or_username')).lower()},{"username": str(request.form.get('email_or_username')) or str(request.form.get('email_or_username'))}]})
            if u is not None:
                password = form.password.data
                if bcrypt.checkpw(str(password).encode('utf-8'), u['password']):
                    session['_WEGGO_USER'] = str(u['_id'])
                    # Pass the User Saves to session
                    offers_saved = []
                    for o in u['saves']:
                        offers_saved.append(o['slug'])  

                    session['_WEGGO_USER_SAVES'] = offers_saved
                    session['community_index']=True
                    return redirect(url_for('public.index'))
                else:
                    flash(f'La contraseña es incorrecta. Vuelve a intentarlo','danger')
                    return redirect(url_for('auth.login'))
            else:
                flash(f'No existe coincidencia de {form.email.data} en la base de datos','danger')
                return redirect(url_for('auth.login'))
        else:
            return """ ERROR """
    except Exception as e:
        return (e)

from flask_dance.contrib.google import google
@api_wg.route('/login-google', methods=['GET', 'POST'])
def login_google():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    email = resp.json()["email"]
    # Aquí puedes registrar al usuario en tu base de datos
    return "You are {email} on Google".format(email=email)

from flask_dance.consumer import oauth_authorized
from app import google_print

@oauth_authorized.connect_via(google_print)
def google_logged_in(blueprint, token):
    next_url = request.args.get("next") or url_for("public.index")
    return redirect(next_url)

@api_wg.route('/register/user', methods=['GET', 'POST'])
@anonymous_required
def register():
    from app.src.auth.forms import UserSignup
    form = UserSignup()
    if request.method == 'POST':
        email=str(form.email.data).lower()
        if ws.db.users.find_one({'email': email}) is not None:
            flash(f'El email {email} ya está siendo utilizado','warning')
            return redirect(url_for('auth.register'))
        else:
            hash_password = bcrypt.hashpw(str(form.password.data).encode('utf-8'), bcrypt.gensalt())

            # Userid will be created directly on the function
            # Folderid will be created directly on the function
            # We only need define ITEMS variable; 
            # ITEMS variable contains every related information
        
            # Defining the ITEMS variable with the information
            items = {
                'email': email,
                'password': hash_password,
                'username': form.username.data,
            }
            print(items)
            # Calling the function to insert the information
            # Creating the user and relational documents
            from app.src.auth.models import Models
            Models.Users.create(items,hash_password)

            Models.Tasks.register({
                'username': items['username'],
                'email': email,
                'message': 'An user just registered as normal user'
            })
            flash("¡Genial! Ya puedes iniciar sesión","success")
            return redirect(url_for('auth.login'))

from flask import jsonify
@api_wg.route('/information/locations', methods=['GET'])
def get_locations():
    locations = []
    for i in ws.db.locations.find({"provinces.towns.label": {"$eq": str(request.args.get('city')) }}):
        for a in i['provinces']:
            for b in a['towns']:
                locations.append(b['label'])
    return jsonify(locations)

class Community:

    @api_wg.route('/v1/most-useful')
    def most_useful_v1():
        data = []
        for i in ws.db.forums.find():
            for b in i['posts']:
                if len(b['comments']) > 0:
                    data.append({
                        'title': b['title'][0:25],
                        'forum_slug': i['slug'],
                        'post_slug': b['slug'],
                        'comments': len(b['comments']),
                        'leafs': len(b['leafs']),
                        'created': b['created']
                    })
        return jsonify(data)

    def strings_mas_repetidos(lista):
        repeticiones = {}
        for string in lista:
            if string in repeticiones:
                repeticiones[string] += 1
            else:
                repeticiones[string] = 1

        max_repeticiones = max(repeticiones.values())
        return [string for string, count in repeticiones.items() if count == max_repeticiones]

    @api_wg.route('/v1/most-tags/<string:forum>')
    def most_used_in_forum(forum):
        all_tags = []
        for b in ws.db.forums.find_one({'slug': forum})['posts']:
            for c in b['tags']:
                all_tags.append(c)
                
        data = Community.strings_mas_repetidos(all_tags)
        return jsonify(data)

    @api_wg.route('/v1/most-followed')
    def most_followed():
        all_tags = []
        for i in ws.db.forums.find():
            for b in i['posts']:
                for c in b['tags']:
                    all_tags.append(c)

        data = Community.strings_mas_repetidos(all_tags)
        return jsonify(data)

class News:

    @api_wg.route('/v1/news')
    def news_v1():
        data = []
        for i in ws.db.news.find():
            import datetime
            date = i['created']
            yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
            day_before_yesterday = datetime.datetime.now() - datetime.timedelta(days=2)

            if date.date() == datetime.datetime.now().date():
                formatted_date = 'Hoy, a las ' + date.strftime('%H:%M') + ' horas'
            elif date.date() == yesterday.date():
                formatted_date = 'Ayer, a las ' + date.strftime('%H:%M') + ' horas'
            elif date.date() == day_before_yesterday.date():
                formatted_date = 'Antes de ayer, a las ' + date.strftime('%H:%M') + ' horas'
            else:
                formatted_date = date.strftime('%A, %d %B %Y')

            data.append({
                'image': i['thumbnail'],
                'title': i['title'],
                'titleUrl': i['slug'],
                'category': i['section'],
                'categoryUrl': '/undefined',
                'shortDescription': i['shortDescription'],
                'commentsCount': len(i['comments']),
                'likesCount': len(i['likes']),
                'created': formatted_date.capitalize(),
            })
        return json.dumps(data)
