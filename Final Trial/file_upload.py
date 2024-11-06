import oci
import configparser

#Load OCI configuration
config = configparser.ConfigParser()
config.read('oci_config.ini')

#Create a client for the Object Storage service
object_storage_client = oci.object_storage.ObjectStorageClient(config['DEFAULT'])
namespace = config['DEFAULT']['namespace']  #Object Storage namespace
bucket_name = config['DEFAULT']['bucket_name']  #bucket name

def upload_multiple_files_to_oci(files):
    """
    Uploads multiple files to Oracle Cloud Object Storage.

    :param files: A list of file objects (from Flask's `request.files.getlist()`)
    :return: A success message or error message.
    """
    uploaded_files = []
    
    for file in files:
        try:
            # Create a unique name for each file (use filename or generate a unique ID)
            object_name = file.filename

            # Read file and upload it to Object Storage
            object_storage_client.put_object(namespace, bucket_name, object_name, file.read())

            uploaded_files.append(file.filename)
        except oci.exceptions.ServiceError as e:
            return f"Error uploading file: {file.filename}. Message: {e.message}"

    return f"Successfully uploaded: {', '.join(uploaded_files)}"
