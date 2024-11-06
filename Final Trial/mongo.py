from flask import Flask, render_template, request, redirect, url_for
import oracledb

app = Flask(__name__)

# Define your connection parameters
config_dir = "C:\\Users\\maebo\\OneDrive\\Desktop\\Documents\\ITS120L APP DEV LAB\\Final Trial\\Wallet_FutureForge"
user = "admin"
password = "Ereri4Lyfe!!!"  # Replace with your actual password
dsn = "futureforge_high"
wallet_location = "C:\\Users\\maebo\\OneDrive\\Desktop\\Documents\\ITS120L APP DEV LAB\\Final Trial\\Wallet_FutureForge"
wallet_password = "Ereri4Lyfe!!!"  # Replace with your actual wallet password

def create_connection():
    try:
        connection = oracledb.connect(
            config_dir=config_dir,
            user=user,
            password=password,
            dsn=dsn,
            wallet_location=wallet_location,
            wallet_password=wallet_password
        )
        return connection
    except oracledb.Error as e:
        print("Error occurred while connecting to the database:", e)
        return None

@app.route('/', methods=['GET'])
def index():
    return render_template('LoginSignin.html')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']
    insert_user_credentials(email, password)
    return redirect(url_for('index'))  # Redirect to index after insertion

def insert_user_credentials(email, password):
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor()
            query = "INSERT INTO USERCREDENTIALS (email, password) VALUES (:1, :2)"
            cursor.execute(query, (email, password))
            connection.commit()  # Commit the transaction
    except oracledb.Error as e:
        print("Error occurred while inserting data:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    app.run(debug=True)
