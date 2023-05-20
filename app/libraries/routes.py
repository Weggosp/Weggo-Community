"""
<!-- -| 
  
  * WEGGO is a registered trademark in Spain as Plataforma Weggo Espana, S.L
  * Any disclosure of this code violates intellectual property laws.
  * By Ruben Ayuso. 
  
|- -->
"""

from flask import request,render_template
from flask.helpers import url_for
from . import libraries_wg
import os 

@libraries_wg.route('/upload/images', methods=['GET','POST'])
def publications_images_upload():
  if request.method == 'POST':
      for key, f in request.files.items():
          basedir_dropzone = os.path.abspath(os.path.dirname(__file__))
          UPLOADED_PATH=os.path.join(basedir_dropzone, url_for('static', filename='uploads/community/explore')),
          if key.startswith('file'):
              f.save(os.path.join(UPLOADED_PATH, f.filename))
  return render_template('index.html')

