from flask import render_template, request, redirect, url_for, session
from connect import create_connection  # Import the database connection logic
from flask import Blueprint
from assessment import assessment_bp
from skillsgap import skillsgap_report
import oracledb

signup_bp = Blueprint('signup_bp', __name__)

@signup_bp.route('/', methods=['GET'])
def LoginSignin():
    return render_template('LoginSignin.html')

@signup_bp.route('/signup', methods=['POST'])
def signup():  # This function handles signup logic
    email = request.form['email']
    password = request.form['password']
    user_id = insert_user_credentials(email, password)

    if user_id:  # Check if user_id is returned
        session['user_id'] = user_id  # Store user_id in session
        print(f"User ID returned: {user_id}")  # Print the user_id to the console
        return redirect(url_for('assessment_bp.career_assessment'))  # Redirect after insertion
    else:
        # Handle the case where the user could not be inserted
        print("Error during signup: user_id not returned.")
        return "Error during signup", 400  # Respond with an error

@signup_bp.route('/login', methods=['POST'])
def login():  # This function handles login logic
    email = request.form['email']
    password = request.form['password']
    user_id = authenticate_user(email, password)
    
    if user_id:  # Check if user_id is returned
        session['user_id'] = user_id  # Store user_id in session
        print(f"User ID logged in: {user_id}")  # Print the user_id to the console
        return redirect(url_for('skillsgap_bp.skillsgap_report'))  # Redirect after login
    else:
        print("Login failed: invalid credentials.")  # Print error message
        return render_template('LoginSignin.html', error="Invalid email or password")  # Render the same page with an error message



def insert_user_credentials(email, password):
    try:
        connection = create_connection()  # Use the reusable connection function
        if connection:
            cursor = connection.cursor()
            query = "INSERT INTO USERCREDENTIALS (email, password) VALUES (:1, :2)"
            cursor.execute(query, (email, password))
            connection.commit()  # Commit the transaction

              # Retrieve the user_id of the last inserted row
            cursor.execute("SELECT user_id FROM USERCREDENTIALS WHERE email = :1", (email,))
            user_id = cursor.fetchone()[0]  # Assuming user_id is in the first column
            return user_id
    except oracledb.Error as e:
        print("Error occurred while inserting data:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def authenticate_user(email, password):
    try:
        connection = create_connection()  # Use the reusable connection function
        if connection:
            cursor = connection.cursor()
            # Query to check if the email and password match
            query = "SELECT user_id FROM USERCREDENTIALS WHERE email = :1 AND password = :2"
            cursor.execute(query, (email, password))
            result = cursor.fetchone()  # Fetch the result
            
            if result:
                return result[0]  # Return user_id if credentials match
            else:
                return None  # Return None if no match
    except oracledb.Error as e:
        print("Error occurred during authentication:", e)
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

