from flask import Flask, jsonify
import oci
import configparser

app = Flask(__name__)

# Load OCI configuration from the 'oci_config' file
config = oci.config.from_file('oci_config.ini', 'DEFAULT')

# Replace with your Oracle Cloud REST API base URL if needed
BASE_URL = f'https://dbmgmt.us-ashburn-1.oci.oraclecloud.com'

# Function to get a token if needed (for example, using API keys or oci SDK)
def oci_auth():
    # Create an OCI identity client
    identity_client = oci.identity.IdentityClient(config)
    # Example: List user information to verify authentication works
    user = identity_client.get_user(config['user']).data
    return user

@app.route('/')
def home():
    return "Flask is running!"

@app.route('/example')
def example_route():
    # Perform some action with the authenticated session
    user_info = oci_auth()  # Example call to verify the user identity
    return jsonify({
        "base_url": BASE_URL,
        "user_info": user_info.name
    })

if __name__ == '__main__':
    app.run(debug=True)
