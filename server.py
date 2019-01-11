import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

SESSION='D19-1'
PROJECTS=['TDs', 'TriviaApp']
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['zip'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'Aucun fichier rendu'
        if 'student' not in request.form.keys():
            return 'Aucun nom d\'etudiant renseigne'
        if 'project' not in request.form.keys():
            return 'Aucun projet renseigne'
        file = request.files['file']
        student = request.form['student']
        project = request.form['project']
        if len(student) < 2:
            return 'Nom d\'etudiant ou de groupe invalide'
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return 'Aucun fichier rendu'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], '%s_%s_%s.zip' %(SESSION, project, student)))
            return 'Votre rendu a bien ete pris en compte. Merci!'
        else:
            return 'L\extension du fichier de rendu doit etre .zip'
    projects_form = '<select name="project">'
    for project in PROJECTS:
        projects_form += '<option value"'+project+'">' + project + '</option>'
    projects_form += '</select><br/>'

    return '''
    <!doctype html>
    <title>Rendu {session} </title>
    <h1>Rendu {session} </h1>
    <form method=post enctype=multipart/form-data> 
      {projects_form}
      <input name="student" placeholder="nom_etudiants"/><br/>
      <input type="file" name="file" accept=".zip"/><br/>
      <input type="submit" value="upload"/>
    </form>
    '''.format(session=SESSION, projects_form=projects_form)


app.run(port=8095, threaded=True, debug=False)