"""
<!-- -| 
  
  * WEGGO is a registered trademark in Spain as Plataforma Weggo Espana, S.L
  * Any disclosure of this code violates intellectual property laws.
  * By Ruben Ayuso. 
  
|- -->
"""

from flask import url_for, request
from werkzeug.utils import secure_filename
from app import app
import os

# Database Connection string
from config.db.connection import weggo

app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

# (( is not funcional ))
app.config.update(
    # Flask-Dropzone config:
    DROPZONE_UPLOAD_MULTIPLE = True,
    DROPZONE_ALLOWED_FILE_CUSTOM = True,
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MIN_FILES=1,
    DROPZONE_MAX_FILES=10,
)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# Route that will process the file upload is located on Collaborator/Routes/GALLERY IMAGE UPLOAD
def upload_image(userid,offerid,local,url_from):
    # Get the name of the uploaded files
    uploaded_files = request.files.getlist("gallery[]")
    filenames = []

    for file in uploaded_files:
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # Move the file form the temporal folder to the upload
            # folder we setup
            if local:
                image_route = os.path.abspath('app\\static\\uploads\\offers\\{}\\{}\\{}'.format(userid,offerid,filename))
            else:
                image_route = os.path.abspath('/var/app/current/app/static/uploads/offers/{}/{}/{}'.format(userid,offerid,filename))
            html_route = '{}'.format(filename)
            file.save(image_route)
            if file.filename != '':
                gallery_route = html_route # VARIABLE to new-offer
            else:
                pass

            
        # Save the filename into a list, we'll use it later
        filenames.append(filename)
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file

    # Secure filenames to save on database
    a=secure_filename(uploaded_files[0].filename)
    b=secure_filename(uploaded_files[1].filename)
    c=secure_filename(uploaded_files[2].filename)
    d=secure_filename(uploaded_files[3].filename)
    e=secure_filename(uploaded_files[4].filename) 

    gallery = weggo.db.offers_gallery.insert({
        "offerid": offerid,
        "g1": a,
        "g2": b,
        "g3": c,
        "g4": d,
        "g5": e,
    })
    # Return the information to our function
    return url_for(url_from, filenames=filenames,gallery=gallery)


def upload_images_publications(wUser, postid, local, url_from, section):
    # Get the name of the uploaded files
    uploaded_files = request.files.getlist("gallery[]")
    filenames = []
    routes = []
    
    for file in uploaded_files:
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # Move the file form the temporal folder to the upload
            # folder we setup
            if local:
                image_route = os.path.abspath('app\\static\\uploads\\community\\publications\\{}\\{}\\{}'.format(wUser['userid'], postid, filename))
            else:
                image_route = os.path.abspath('/var/app/current/app/static/uploads/community/publications/{}/{}/{}'.format(wUser['userid'], postid, filename))
            html_route = '{}'.format(filename)
            file.save(image_route)
            if file.filename != '':
                gallery_route = html_route # VARIABLE to new-offer
                routes.append(gallery_route)
            else:
                pass

            
        # Save the filename into a list, we'll use it later
        filenames.append(filename)
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file

    # Secure filenames to save on database
    weggo.db.community_publications_routes_gallery.update_one(
        {'postid': postid}, {'$set': 
            {
            "images": [filenames]
            }
        }
    )
    # Return the information to our function
    from flask import session
    session['filenames'] = filenames
    return url_for(url_from, section=section)



def upload_images_offers(wUser, offerid, local, url_from):
    uploaded_files = request.files.getlist("gallery[]")
    filenames = []
    routes = []
    
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if local:
                image_route = os.path.abspath('app\\static\\uploads\\offers\\{}\\{}\\{}'.format(wUser['userid'], offerid, filename))
            else:
                image_route = os.path.abspath('/var/app/current/app/static/uploads/offers/{}/{}/{}'.format(wUser['userid'], offerid, filename))
            html_route = '{}'.format(filename)
            file.save(image_route)
            if file.filename != '':
                gallery_route = html_route
                routes.append(gallery_route)
            else:
                pass

            filenames.append(filename)

    weggo.db.offers.update_one(
        {'offerid': offerid}, {'$set': 
            {
            "images": [filenames]
            }
        }
    )

    from flask import session
    session['filenames'] = filenames
    return url_for(url_from)

def upload_images_temp_vehicles(vehicle_id, local, url_from):
    uploaded_files = request.files.getlist("gallery[]")
    filenames = []
    routes = []
    
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if local:
                image_route = os.path.abspath('app\\static\\uploads\\vehicles\\temp\\{}\\{}'.format(vehicle_id, filename))
            else:
                image_route = os.path.abspath('/var/app/current/app/static/uploads/vehicles/temp/{}/{}'.format(vehicle_id, filename))
            html_route = '{}'.format(filename)
            file.save(image_route)
            if file.filename != '':
                gallery_route = html_route
                routes.append(gallery_route)
            else:
                pass

            filenames.append(filename)

    weggo.db.TEMP_vehicles.update_one(
        {'vehicle_id': vehicle_id}, {'$set': 
            {
            "images": [filenames]
            }
        }
    )

    from flask import session
    session['filenames'] = filenames
    return url_for(url_from)

def upload_vehicle_image(f, vehicleid, wUser, url_from):
    if f and allowed_file(f.filename):
        filename = (secure_filename(wUser['userid']+'-'+f.filename)).replace(' ','-').lower()
        from datetime import datetime
        # Upload filename to DB
        weggo.db.users_folders.update_one({'userid': wUser['userid']}, {'$push': {
            "folders.images.{}".format(vehicleid): {
                "filename": filename,
                "status": "Not verified",
                "updated": None,
                "uploaded": datetime.now()
            }
        }})

        # Upload file to S3
        f.save(filename)
        from app.libraries.aws.functions import upload_file
        BUCKET = "europe-weggo-bucket"
        route = "weggo.es/images/{}/{}/".format(wUser['userid'],vehicleid)
        upload_file(f"{filename}", route, BUCKET)

        return url_for(url_from)

def upload_offer_thumbnail(f, offerid, wUser, url_from):
    if f and allowed_file(f.filename):
        filename = (secure_filename(wUser['userid']+'-'+f.filename)).replace(' ','-').lower()

        # Upload file to S3
        f.save(filename)
        from app.libraries.aws.functions import upload_files
        BUCKET = "europe-weggo-bucket"
        route = "weggo.es/images/{}/offers/{}/".format(wUser['userid'],offerid)
        upload_files(f"{filename}", route, BUCKET)

        return url_for(url_from)

def upload_file_to_account(f, wUser, url_from):
    if f and allowed_file(f.filename):
        filename = (secure_filename(wUser['userid']+'-'+f.filename)).replace(' ','-').lower()
        from datetime import datetime
        # Upload filename to DB
        weggo.db.users_folders.update_one({'userid': wUser['userid']}, {'$push': {
            "folders.documents": {
                "filename": filename,
                "status": "Not verified",
                "updated": None,
                "uploaded": datetime.now()
            }
        }})

        weggo.db.users_folders.update_one({'userid': wUser['userid']}, {'$set': {
            "status": "Pending",
            "updated": datetime.now()
        }})

        # Upload file to S3
        f.save(filename)
        from app.libraries.aws.functions import upload_file
        BUCKET = "europe-weggo-bucket"
        route = "weggo.es/documents/{}/".format(wUser['userid'])
        upload_file(f"{filename}", route, BUCKET)

        return url_for(url_from)
        
def upload_files_to_account(wUser, url_from):
    uploaded_files = request.files.getlist("files[]")
    filenames = []

    # Uploading the files to these folders
    for file in uploaded_files:
        if file and allowed_file(file.filename):
            filename = (secure_filename(wUser['userid']+'-'+file.filename)).replace(' ','-').lower()

            from datetime import datetime
            # Upload filename to DB
            weggo.db.users_folders.update_one({'userid': wUser['userid']}, {'$push': {
                "folders.documents": {
                    "filename": filename,
                    "status": "Not verified",
                    "updated": None,
                    "uploaded": datetime.now()
                }
            }})
            
            weggo.db.users_folders.update_one({'userid': wUser['userid']}, {'$set': {
                "status": "Pending",
                "updated": datetime.now()
            }})
            
            # Upload file to S3
            file.save(filename)
            from app.libraries.aws.functions import upload_file
            BUCKET = "europe-weggo-bucket"
            route = "weggo.es/documents/{}/".format(wUser['userid'])
            upload_file(f"{filename}", route, BUCKET)

            filenames.append(filename)

    weggo.db.users.update_one({'userid': wUser['userid']}, {'$set': {
        "business.0.business_documentation_files": [filenames]
    }})

    return url_for(url_from)
