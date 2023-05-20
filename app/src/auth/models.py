from datetime import datetime

# Imports
import uuid,bcrypt

# Database Connection string
from config.db.connection import weggo as ws

# Import functions to create user or company id
from app.resources import functions

# Libraries
from app.libraries.sendgrid.models import Emails

class Models:

    class Newsletter:

        def neswletter_join(items):
            ws.db.newsletter.update_one({'email': items['email']}, {'$set': {
                'options': {
                    'diaryNews': items['diaryNews'],
                    'updates': items['updates'],
                    'weeklySummary': items['weeklySummary'],
                    'events': items['events'],
                    'partners': items['partners'],
                    'usersContent': items['usersContent'],
                    'lastModified': datetime.now()
                }
            }})
            return 200

    class News:

        def new_comment(items):
            ws.db.news.update_one({'slug':items['slug']},{'$push': {
                'comments': {
                    'email': items['email'],
                    'avatar': items['avatar'],
                    'fullname': items['fullname'] if items['fullname'] != None else None,
                    'body': items['body'],
                    'replies': [],
                    'updated': None,
                    'created': datetime.now()
                }   
            }})
            return 200

    class Tasks:
        def register(items):
            import uuid
            # Register a task into DB: Message, UserID, Email, Registration Data, Status.
            try:
                if ws.db.task_log.find_one({'userid': items['userid']}):
                    ws.db.task_log.update_one({'userid': items['userid']}, {'$push': {
                        'tasks': {
                            'task_id': '{}'.format(uuid.uuid1()),
                            'message': items['message'],
                            'created': datetime.now()
                        }
                    }})
                else:
                    ws.db.task_log.insert_one({
                        'username': items['username'],
                        'email': items['email'],
                        'tasks': [{
                            'task_id': '{}'.format(uuid.uuid1()),
                            'message': items['message'],
                            'created': datetime.now()
                        }],
                        'created': datetime.now()
                    })
                return 200
            except Exception as e:
                return e

        def registerError(items):
            import uuid
            # Register a task into DB: Message, UserID, Email, Registration Data, Status.
            try:
                ws.db.task_log_errors.insert_one({
                    'error_id': '{}'.format(uuid.uuid1()),
                    'message': items['message'],
                    'location': items['location'],
                    'status': items['status'],
                    'created': datetime.now()
                })
                return 200
            except Exception as e:
                return e

    class Users:

        def find_one(email):
            return ws.db.users.find_one({'email': email})

        def create(items,hash_password):
            ws.db.users.insert_one({
                'username': items['username'],
                'email': items['email'],
                'password': hash_password,
                'information': {
                    'fullname': None,
                    'agent': None,
                    'born': None,
                    'phone': None,
                    'nif': None,
                    'location': {
                        'country': None,
                        'province': None,
                        'city': None,
                        'address': None,
                        'zip': None
                    }
                },
                'profile': {
                    'avatar': None,
                    'bg': None,
                    'verified': False
                },
                'saves': [],
                'statistics': [],
                'reports': [],
                'access': {
                    'type': "user",
                    'range': 1,
                    'allowed': 1
                },
                'emails': {
                    'newsletter': True
                },
                'messages': [],
                'status': 'active',
                'updated': None,
                'created': datetime.now()
            })

            # Create user folder document
            ws.db.users_folders.insert_one({
                'username': items['username'],
                'folders': {
                    'images': [],
                    'documents': []
                },
                'status': 'active',
                'updated': None,
                'created': datetime.now()
            })

            # Create user newsletter document
            ws.db.newsletter.insert_one({
                'username': items['username'],
                'email': items['email'],
                'active': True,
                'updated': None,
                'created': datetime.now()
            })

            return 200
        
        def recover(email):
            try:
                # Try to find the email and if this exists, send new password to email
                user = ws.db.users.find_one({'email': email})
                new_password="{}".format(str(uuid.uuid4().hex))[0:15]
                hash_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

                ws.db.users.update_one({'email': email},{'$set': {
                    'password': hash_password,
                    'updated': datetime.now()
                }})

                # Send welcome and confirmation emails
                items = {
                    'email': email,
                    'user': user,
                    'password': new_password,
                    'subject': "Cambio de contraseña",
                    'template_route': "sendgrid-emails-templates/auth/recover.html"
                }
                Emails.Users.recover(items)

                return 200
            except:
                e=f'No se ha encontrado el email proporcionado'
                return e
            
        def update():
            return """ """

        class Posts:

            def create(forum,items,slug,username):
                ws.db.forums.update_one({'slug': forum},{'$push': {
                    'posts': {
                        'author': username,
                        'title': items['title'],
                        'slug': slug,
                        'section': items['section'],
                        'tags': items['tags'],
                        'body': items['body'],
                        'leafs': [],
                        'comments': [],
                        'users': [],
                        'updated': None,
                        'created': datetime.now()
                    }
                }})
                return 200

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
                    ws.db.forums.update_one({'slug': items['forum'], 'posts.slug': items['post']},{'$push': {
                        'posts.$.comments': {
                            'author': items['username'],
                            'comment': items['comment'],
                            'replies': [],
                            'updated': None,
                            'created': datetime.now()
                        }
                    }})

                    ## UPDATE LAST COMMENT
                    ws.db.forums.update_one({'slug': items['forum'], 'posts.slug': items['post']},{'$set': {
                        'posts.$.last_comment': {
                            'author': items['username'],
                            'comment': items['comment'],
                            'created': datetime.now()
                        }
                    }})
                    return 200


        class Newsletter:
            ## THIS FUNCTIONS IS ONLY TO ANONYMOUS USERS
            def add(email):
                ws.db.newsletter.insert_one({
                    'userid': None,
                    'email': email,
                    'active': True,
                    'updated': None,
                    'created': datetime.now()
                })
            ## UPDATE THE USER INFORMATION, LIKE THE 'ACTIVE' 
            def update(email):
                return """"""

    class Administration:

        class News:

            def new_thumbnail(filename,slug):
                ws.db.news.insert_one(
                    {
                    "thumbnail": filename,
                    "slug": slug,
                    "created": datetime.now()
                    }
                )
                return 200

            def new_body(items,slug):
                ws.db.news.update_one({'slug':slug},{'$set': {
                    'title': items['name'],
                    'author': items['user'],
                    'section': items['section'],
                    'tags': items['tags'],
                    'shortDescription': items['short_description'],
                    'description': items['description'],
                    'readTime': items['read_time'],
                    'likes': [],
                    'comments': [],
                    'shares': 0,
                    'updated': None
                }})
                return 200

        class Forum:

            def create(slug,items):
                ws.db.categories.update_one({'name': items['category']}, {'$push': {
                    'forums': {
                        'name': items['name'],
                    }
                }})
                id = functions.last_forum()
                if ws.db.forums.insert_one({
                    'slug': slug,
                    'category': items['category'],
                    'details': {
                        'name': items['name'],
                        'description': items['description'],
                        'icon': items['icon'],
                        'color': items['color'],
                        'type': items['type']
                    },
                    'threads': [],
                    'posts': [],
                    'show': id,
                    'statistics': {
                        'threads': 0,
                        'posts': 0,
                        'comments': 0,
                        'leafs': 0
                    },
                    'created': datetime.now()
                }):
                    return 200
                else:
                    return 400
            
            def find():
                return """ """

            def find_all():
                return """ """

            def up(slug,show):
                ws.db.forums.update_one({'slug': slug}, {'$set': {
                    'show': int(show)-1
                }})

                data = ws.db.forums.find({'show': int(show)-1})
                for i in data:
                    if i['slug'] != slug:
                        ws.db.forums.update_one({'slug': i['slug']},{'$set': {
                            'show': int(show)
                        }})

                return 200 
            
            def down(slug,show):
                ws.db.forums.update_one({'slug': slug}, {'$set': {
                    'show': int(show)+1
                }})
                
                data = ws.db.forums.find({'show': int(show)+1})
                for i in data:
                    if i['slug'] != slug:
                        ws.db.forums.update_one({'slug': i['slug']},{'$set': {
                            'show': int(show)
                        }})

                return 200

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
                    return ws.db.forums.update_one({'slug': forum, 'posts.slug': post}, {'$set': {
                        'posts.$.pinned': True
                    }})

        class Categories:

            def create(slug,items):
                if not ws.db.categories.find_one({'slug': slug}):
                    ws.db.categories.insert_one({
                        'slug': slug,
                        'name': items['name'],
                        'color': items['color'],
                        'statistics': {
                            'threads': 0,
                            'posts': 0,
                            'comments': 0,
                            'leafs': 0
                        },
                        'created': datetime.now()
                    })
                    return 200
                else:
                    return 400

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

        class Users:

            def create():
                return """ """

            def find():
                return """ """

            def find_all():
                return """ """

            def update():
                return """ """

            def temporal_ban():
                return """ """

            def permanent_ban():
                return """ """

            def delete():
                return """ """

            def delete_all():
                return """ """

        class Comments:

            def create():
                return """ """

            def find():
                return """ """

            def find_all():
                return """ """

            def edit():
                return """ """

            def delete():
                return """ """

            def delete_all():
                return """ """

        class Sections:

            def create():
                return """ """

            def find():
                return """ """

            def find_all():
                return """ """

            def update():
                return """ """

            def delete():
                return """ """

            def delete_all():
                return """ """

        class Tags:

            def create():
                return """ """

            def find():
                return """ """

            def find_all():
                return """ """

            def update():
                return """ """

            def delete():
                return """ """

            def delete_all():
                return """ """