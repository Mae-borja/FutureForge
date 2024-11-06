import oracledb

# Define your connection parameters
config_dir = "C:\\Users\\maebo\\OneDrive\\Desktop\\Documents\\ITS120L APP DEV LAB\\Final Trial\\Wallet_FutureForge"
user = "admin"
password = "Ereri4Lyfe!!!"  # Replace with your actual password
dsn = "futureforge_high"
wallet_location = config_dir
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
    
