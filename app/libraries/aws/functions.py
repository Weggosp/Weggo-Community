from flask import request,redirect,render_template
from app import app
import boto3

s3 = boto3.client("s3")

### CONFIGURATION

app.config.update(
    # Flask-Dropzone config:
    DROPZONE_UPLOAD_MULTIPLE = True,
    DROPZONE_ALLOWED_FILE_CUSTOM = True,
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MIN_FILES=1,
    DROPZONE_MAX_FILES=10,
)

app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

### END CONFIGURATION

def upload_files(file_name, route, bucket):
    """
    Function to upload a file to an S3 bucket
    """
    object_name = route+'/'+file_name # Ruta de guardado en S3
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(file_name, bucket, object_name)
    
    return response


def upload_vehicle_images(image_name, wUser, vehicleid, bucket):
    """
    Function to images from vehicles or offer route
    """
    object_name = "weggo.es/images/{}/{}/{}".format(wUser['userid'],vehicleid,image_name) # Ruta de guardado en S3
    s3_client = boto3.client('s3')
    response = s3_client.upload_file(image_name, bucket, object_name)

    return response



def download_file(file_name, bucket):
    """
    Function to download a given file from an S3 bucket
    """
    s3 = boto3.resource('s3')
    output = file_name
    s3.Bucket(bucket).download_file(file_name, output)

    return output

def delete_image(wUser, offerid, image_name):
    object_name = "weggo.es/images/{}/offers/{}/{}".format(wUser['userid'],offerid,image_name) # Ruta de guardado en S3
    s3 = boto3.resource('s3')
    response = s3.Object('europe-weggo-bucket', object_name).delete()

    return response

def list_user_vehicles_images():
    """
    Function to list files in a given S3 bucket
    """
    s3 = boto3.client('s3')
    contents = []
    bucket = "europe-weggo-bucket"
    prefix = "weggo.es/images"
    for item in s3.list_objects(Bucket=bucket,Prefix=prefix)['Contents']:
        print(item)
        contents.append(item)

    return contents

def list_vehicles_images(bucket,userid):
    """
    Function to list files in a given S3 bucket
    """
    s3 = boto3.client('s3')
    contents = []
    prefix = "weggo.es/images/{}/".format(userid)
    for item in s3.list_objects(Bucket=bucket,Prefix=prefix)['Contents']:
        contents.append(item)

    return contents

## Esto va a ROUTES
"""
@app.route("/storage")
def storage():
    contents = list_files("europe-weggo-bucket")
    return render_template('storage.html', contents=contents)

@app.route("/upload", methods=['POST'])
def upload():
    if request.method == "POST":
        from werkzeug.utils import secure_filename
        file=request.files['file']
        file_name=(secure_filename(file.filename)).replace(' ','-').lower()
        file.save(file_name)
        upload_file(f"{file_name}", BUCKET)
        return redirect("/storage")

@app.route("/download/<filename>", methods=['GET'])
def download(filename):
    if request.method == 'GET':
        output = download_file(filename, BUCKET)

        return send_file(output, as_attachment=True)"""