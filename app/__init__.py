from flask import Flask

app = Flask(__name__, instance_relative_config=True)

from flask_dropzone import Dropzone
dropzone = Dropzone()
from flask_mail import Mail
mail = Mail()
from flask_breadcrumbs import Breadcrumbs
Breadcrumbs(app=app)

import os 

from flask_dance.contrib.google import make_google_blueprint
google_print = make_google_blueprint(
    client_id=os.environ.get('GOOGLE_CLIENT_ID'),
    client_secret=os.environ.get('GOOGLE_SECRET'),
    scope=["profile", "email"],
    redirect_url="/google-login",
)

def weggo_app():
    # Load the environment parameters configuration
    app.config.from_object('config.config')

    # Force to close session
    from datetime import timedelta
    app.permanent_session_lifetime = timedelta(minutes=120)

    ## CHANGE DATETIME LANGUAGE TO SPANISH BY DEFAULT
    import locale
    locale.setlocale(locale.LC_ALL, ("es_ES", "UTF-8"))

    from itsdangerous import URLSafeTimedSerializer
    ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])  

    # Load the MongoDatabase connection
    from config.db.connection import weggo
    weggo.init_app(app)

    app.config.update(
        # Flask-Dropzone config:
        DROPZONE_ALLOWED_FILE_TYPE='image',
        DROPZONE_MAX_FILE_SIZE=3,
        DROPZONE_MAX_FILES=15,
        DROPZONE_PARALLEL_UPLOADS=15,  # set parallel amount
        DROPZONE_UPLOAD_MULTIPLE=True,  # enable upload multiple
    )

    # Load the dropzone configuration
    dropzone.init_app(app)
    # Load the mail configuration
    mail.init_app(app)

    from .public import public_wg
    app.register_blueprint(public_wg)
    from .libraries import libraries_wg
    app.register_blueprint(libraries_wg)
    from .src.auth import auth_wg
    app.register_blueprint(auth_wg, url_prefix="/a/")
    from .src.panel import panel_wg
    app.register_blueprint(panel_wg, url_prefix="/panel/")
    from .src.api import api_wg
    app.register_blueprint(api_wg, url_prefix="/api/")

    app.register_blueprint(google_print, url_prefix="/login")

    from app.src.auth.routes import errors
    app.register_error_handler(400, errors.page_refresh)
    app.register_error_handler(404, errors.page_not_found)
    app.register_error_handler(403, errors.page_not_access)
    app.register_error_handler(401, errors.page_need_arguments)
    app.register_error_handler(406, errors.page_only_users_except_autor)

    return app