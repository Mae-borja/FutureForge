from flask import Blueprint, render_template, jsonify, session, request
from flask import Flask
import oci
import configparser
import urllib.parse
from connect import create_connection 
import oracledb
from groq import Groq
import os




skillsgap_bp = Blueprint('skillsgap_bp', __name__)

# Load OCI configuration
config = configparser.ConfigParser()
config.read('oci_config.ini')

# Create a client for the Object Storage service
object_storage_client = oci.object_storage.ObjectStorageClient(config['DEFAULT'])
namespace = config['DEFAULT']['namespace']  # Object Storage namespace
bucket_name = config['DEFAULT']['bucket_name']  # bucket name


@skillsgap_bp.route('/skills_learningpath', methods=['GET'])
def skills_learningpath():
    return render_template('SkillsLearningPath.html')


@skillsgap_bp.route('/skillsgap_report', methods=['GET'])
def skillsgap_report():
    # Call the function to get uploaded files
    uploaded_files_urls, uploaded_filenames  = view_uploaded_files()

    if isinstance(uploaded_files_urls, str):  # Check if it's an error message
        return uploaded_files_urls  # Return the error message directly
# Extract skills from the database
    extracted_skills = extract_skills_from_db()  # Extract skills here

    if extracted_skills is None:
        return "Error: Could not extract skills from the database."
    
    # Get an overview of the skills using Groq
    overview_text = general_overview()
    print(f"Extracted Skills:\n{overview_text}")


    # Render the HTML page to display the PDFs as images, passing extracted_skills
    return render_template('SkillsGapReport.html', 
                           pdf_urls=uploaded_files_urls, 
                           filenames=uploaded_filenames, 
                           extracted_skills=extracted_skills, 
                           overview_text=overview_text)
    
def view_uploaded_files():
    # PAR ID stored or fetched from your configuration
    par_id = "xBW3iAwK3ZBqVGN8jGOrvTLPfaOdrnoPRlKsTqAHQCpTUh+5KzfFDHRZkgNnbs1F"
    # Retrieve uploaded files and their URLs using the PAR
    uploaded_files_urls, uploaded_filenames = get_uploaded_files_from_oci(par_id)

    # Return uploaded file URLs or an error message
    
    return uploaded_files_urls, uploaded_filenames




def get_uploaded_files_from_oci(par_id):
    """
    Retrieves a list of uploaded files from Oracle Cloud Object Storage and generates their URLs using an existing Pre-Authenticated Request (PAR).
    
    :param par_id: The pre-authenticated request ID.
    :return: A list of URLs for the uploaded files.
    """

    try:
        # List objects in the bucket
        list_objects_response = object_storage_client.list_objects(namespace, bucket_name)
        objects = list_objects_response.data.objects
        
        # Generate URLs for each object using the PAR
        file_urls = []
        filenames = []
        
        base_url = f"https://objectstorage.us-ashburn-1.oraclecloud.com/p/eik_E0Wn7v5-CLUHE23oRpW6OME6FDfgzhVSBxHcS_EWen-Ndl997X_XVB2ARiBM/n/id5g2fkwyutp/b/SkillsPDF/o/"
        
        connection = create_connection()  # Use the reusable connection function
        cursor = connection.cursor()

        for obj in objects:
            object_name = obj.name
            to_name = obj.name.replace('.pdf', '')
            

            # Query the database to check if this file name exists in SKILL_TITLE
            cursor.execute("SELECT CERTIFICATE_TITLE FROM SKILLS WHERE SKILL_TITLE = :filename", {'filename': to_name})
            result = cursor.fetchone()

            if result:
                # If a match is found, result[0] will be the CERTIFICATE_TITLE
                certificate_title = result[0]

                # URL encode the object name in case it contains special characters
                object_name_encoded = urllib.parse.quote(object_name)
                # Generate the full URL
                file_url = base_url + object_name_encoded
                
                # Add to the lists
                file_urls.append(file_url)
                filenames.append(certificate_title)

        return file_urls, filenames

    except oci.exceptions.ServiceError as e:
        return f"Error retrieving files. Message: {e.message}"

def extract_skills_from_db():
    """
    Extracts all skills from the SKILLS table and returns them as a string.
    
    :return: A string containing all skills or None if an error occurs.
    """
    extracted_text = ""  # Initialize the extracted_text variable to store skills
    
    try:
        connection = create_connection()  # Use the reusable connection function
        cursor = connection.cursor()

        # Query the SKILLS table to fetch all skills
        cursor.execute("SELECT SKILLS FROM SKILLS")
        
        # Fetch all results
        skills = cursor.fetchall()

        # Check if any skills are found and append them to extracted_text
        if skills:
            extracted_text = "\n".join(skill[0] for skill in skills)  # Join skills with a newline
        else:
            extracted_text = "No skills found in the SKILLS table."

       # print(f"Extracted Skills:\n{extracted_text}")
        return extracted_text  # Return the final string with all skills

    except oracledb.Error as e:
        print("Error occurred while extracting skills:", e)
        return None  # Return None to indicate failure

    finally:
        if cursor:
            cursor.close()  # Ensure cursor is closed
        if connection:
            connection.close()  # Ensure connection is closed

    


def general_overview():
    # Extract the skills from the database based on the PDF filename
    extracted_text = extract_skills_from_db()
    
    # Check if extracted_text is valid before proceeding
    if extracted_text is None:
        print("Error: Could not extract skills from the database.")
        return  # Exit the function if there's an issue with the extraction

    # Set your Groq API key in the environment
    # os.environ['GROQ_API_KEY'] = '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'

    # Initialize the Groq client using the API key
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY")
    )

    # Create a chat completion request
    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{
            "role": "user",
            "content": f"give me an overview of my skills in one paragraph. Do not use asterisks. Use this: \n{extracted_text}"
        }],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
    )

    response_text = completion.choices[0].message.content  # Correct attribute access

    #def clean_raw_text(response):
    # Remove asterisks around the field names
    # cleaned_response = response.replace('**', '')  # Remove all asterisks
    # return cleaned_response.strip()  # Strip leading and trailing whitespace
    # Clean the response text
    #cleaned_response_text = clean_raw_text(response_text)
    # Print cleaned response text in the console
    #
    return response_text



@skillsgap_bp.route('/delete_multiple_pdfs', methods=['DELETE'])
def delete_multiple_pdfs():
    # Get the list of PDF URLs from the request body
    pdf_urls = request.json.get('pdf_urls', [])

    if not pdf_urls:
        return jsonify({"success": False, "message": "No PDFs provided for deletion."})

    try:
        # Delete each PDF from Oracle Cloud Object Storage and the database
        for pdf_url in pdf_urls:
            pdf_filename = pdf_url.split('/')[-1]  # Extract the filename from the URL
            
            # Delete from OCI (Object Storage)
            delete_from_oci(pdf_filename)
            
            # Remove from the database
            remove_pdf_record_from_db(pdf_filename)

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

def delete_from_oci(pdf_filename):
    """
    Deletes the file from Oracle Cloud Object Storage based on the filename.
    :param pdf_filename: The filename of the PDF to delete.
    """
    # Use the object storage client to delete the file from the bucket
    object_storage_client.delete_object(namespace, bucket_name, pdf_filename)


def remove_pdf_record_from_db(pdf_filename):
    """
    Removes the PDF record from the database based on the filename.
    
    :param pdf_filename: The filename of the PDF to remove from the database.
    :return: Number of rows deleted, or None if an error occurs.
    """
    try:
        connection = create_connection()  # Use the reusable connection function
        cursor = connection.cursor()

        # Delete the PDF record from the database where the filename matches
        cursor.execute("DELETE FROM SKILLS WHERE SKILL_TITLE = :filename", {'filename': pdf_filename})
        
        connection.commit()  # Commit the transaction

        # Return the number of rows deleted (should be 1 if successful)
        return cursor.rowcount  # This will return the number of rows affected by the DELETE statement
    except oracledb.Error as e:
        print("Error occurred while removing PDF:", e)
        return None  # Return None to indicate failure
    finally:
        if cursor:
            cursor.close()  # Ensure cursor is closed
        if connection:
            connection.close()  # Ensure connection is closed

