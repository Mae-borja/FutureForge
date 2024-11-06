from flask import Flask, session
from signup import signup_bp  # Import the signup blueprint
#from signup (name ng file.py) import bluprint(definition na icacall mo)
from assessment import assessment_bp
from skillsgap import skillsgap_bp

app = Flask(__name__)
app.secret_key = 'DASEKRITKEY'

# Register the signup blueprint
app.register_blueprint(signup_bp)
app.register_blueprint(assessment_bp)
app.register_blueprint(skillsgap_bp)



if __name__ == "__main__":
    app.run(debug=True)
