from flask import Flask, request, render_template
from file_upload import upload_multiple_files_to_oci
import io

app = Flask(__name__)

# Route to serve the HTML form
@app.route('/')
def index():
    return render_template('Career Assessment Form.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'files' not in request.files:
        return render_template('Career Assessment Form.html', message="No file part")
    
    files = request.files.getlist('files')
    
    if len(files) == 0 or files[0].filename == '':
        return render_template('Career Assessment Form.html', message="No selected file")
    
    # Call the function from file_upload.py to handle the upload of multiple files
    message = upload_multiple_files_to_oci(files)
    
    return render_template('Career Assessment Form.html', message=message)

@app.route('/SkillsGapReport')
def SkillsGapReportt():
    return render_template('SkillsGapReport.html')


if __name__ == '__main__':
    app.run(debug=True)
