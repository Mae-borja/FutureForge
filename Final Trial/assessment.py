from flask import Blueprint, render_template
from flask import Flask, request
from file_upload import upload_multiple_files_to_oci
import io

assessment_bp = Blueprint('assessment_bp', __name__)

@assessment_bp.route('/career_assessment', methods=['GET'])
def career_assessment():
    return render_template('Career Assessment Form.html')
