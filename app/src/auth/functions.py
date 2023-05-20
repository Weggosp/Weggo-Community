from flask import Response,session,flash
from slugify import slugify
import random, hashlib, bcrypt

# MODELS
from app.src.auth.models import Models

# LIBRARIES
from app.libraries.aws.functions import upload_files

class Functions: 

    class Newsletter:

        def newsletter_join(items):
            Models.Newsletter.neswletter_join(items)

            return 200

    class Uploads:

        class Images:

            def new_thumbnail(filename,name):
                BUCKET = "europe-weggo-bucket"
                slug = slugify(name)

                # Upload filename to DB
                Models.Administration.News.new_thumbnail(filename,slug)
                route = "weggo.es/images/news"
                upload_files(filename, route, BUCKET)
                return 200

    class Users:

        def login(items):
            try:
                user = Models.Users.find_one(items['email'])
                if bcrypt.checkpw(items['password'].encode('utf-8'), user['password']):
                    Models.Tasks.register({
                        'userid': user['userid'],
                        'email': user['email'],
                        'message': 'An user just logged in'
                    })
                    session['_WEGGO_USER'] = str(user['_id'])
                    return 200
                else:
                    return 400
            except:
                Models.Tasks.registerError({
                    'message': 'Something was wrong while user tried connect to his account',
                    'location': 'Line 56-109 - Function: login; [routes.py in auth]',
                    'status': 'priority'
                })
                return 400


        def register(items):
            try:
                Models.Users.find_one(items['email'])
                email = items['email']
                return f'El email {email} ya está siendo utilizado'
            except:
                hash_password = bcrypt.hashpw(items['password'].encode('utf-8'), bcrypt.gensalt())
                user = Models.Users.create(items,hash_password)

                Models.Tasks.register({
                    'username': items['username'],
                    'email': email,
                    'message': 'An user just registered as normal user'
                })

                flash("¡Genial! Ya puedes iniciar sesión","success")

                # Add Mocks
                return user['_id']


        class Posts:

            def create(forum,items,username):
                slug = slugify(items['title'])
                Models.Users.Posts.create(forum,items,slug,username)

                return slug

            def find():
                return """ """

            def find_all():
                return """ """

            def edit():
                return """ """

            def close():
                return """ """

            def delete():
                return """ """

            def delete_all():
                return """ """

            class Comments:

                def create(items):
                    Models.Users.Posts.Comments.create(items)

                    return 200

    class News:

        class Comments:
            
            def create(items):
                Models.News.new_comment(items)

                return 200

    class Administration:

        class News:

            def create(items):
                Models.Administration.News.new_body(items,slugify(items['name']))

                return 200

        class Forum:

            def create(items):
                from slugify import slugify
                txt = items['name']
                slug = slugify(txt)

                response = Models.Administration.Forum.create(slug,items)
                if response == 200:
                    return flash('Foro creado con éxito','success'), 200
                else:
                    return flash('No se ha podido crear el foro','danger'), 400
            
            def find():
                return """ """

            def find_all():
                return """ """

            def up(slug,show):
                response = Models.Administration.Forum.up(slug,show)
                if response == 200:
                    return 200
                else:
                    return flash('No se ha podido realizar la acción. Contacta con soporte','danger'), 400
            
            def down(slug,show):
                response = Models.Administration.Forum.down(slug,show)
                if response == 200:
                    return 200
                else:
                    return flash('No se ha podido realizar la acción. Contacta con soporte','danger'), 400


            def edit():
                return """ """

            def close():
                return """ """

            def desactivate():
                return """ """

            def delete():
                return """ """

            def delete_all():
                return """ """

            class Posts:

                def pin(forum,post):
                    response = Models.Administration.Forum.Posts.pin(forum,post)

                    flash('Post fijado','success')
                    return 200

        class Category:

            def create(items):
                from slugify import slugify
                txt = items['name']
                slug = slugify(txt)

                response = Models.Administration.Categories.create(slug,items)
                if response == 200:
                    return flash('Categoría creada con éxito','success'), 200
                else:
                    return flash('Esa categoría ya existe. Intenta con otro nombre','danger'), 400
            
            def find():
                return """ """

            def find_all():
                return """ """

            def edit():
                return """ """

            def close():
                return """ """

            def desactivate():
                return """ """

            def delete():
                return """ """

            def delete_all():
                return """ """
            
    class Tokens:

        
        def generate_token():
            chars = list(
                'ABCDEFGHIJKLMNOPQRSTUVWYZabcdefghijklmnopqrstuvwyz01234567890'
            )
            random.shuffle(chars)
            chars = ''.join(chars)
            sha1 = hashlib.sha1(chars.encode('utf8'))
            token = sha1.hexdigest()
            response = Response(token, content_type='text/plain')
            response.set_cookie('token_name', 'Anonymous_vehicle_post')
            response.set_cookie('token_id', token)
            return response
