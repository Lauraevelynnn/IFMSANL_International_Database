# import config
import configparser

# get WhatsApp Module
import pywhatkit

# get modules
from util import gmail
from util import time
from util import nlp
from util import convert_tools
from util import config_tools
from util import google_drive
from util import google_sheets

if __name__ == '__main__':
    # Setup config file
    print('The International Database was made by Laura Delvaux from IFMSA-NL.')
    print('Thank you for using the International Database :)')
    print("If there are any questions, be sure to read the README, if for some reason it doesn't work, contact me :)")

    config = configparser.ConfigParser()
    config_variables = {}
    config = config_tools.read_config('config.ini', config_variables)

    print('Opening email connection...')
    service = gmail.authenticate()
    print('Connected')
    query = config['Gmail']['query']

    print('Searching for mails...')
    results = gmail.search_messages(service, query)
    print(f'Found {len(results)} results.')
    # For each email matched, read it and run the program.
    for msg in results:
        print('Parsing emails...')
        try: 
            email_subject, email_sender, email_date, email_body_plain, email_body_html= gmail.read_message(service, msg)
        except:
            print('An error occured and this email could not be parsed')
            continue
        
        # Get deadline from email subject, if not found in subject, use NLP to get it from the body
        deadline = time.extract_deadline(email_subject)
        if deadline == None:
            deadline_question = config['NLP']['deadline_question']
            try:
                deadline_purpose = config['NLP']['deadline_purpose']
                deadline_model = config['NLP']['deadline_model']
                deadline = time.parse_date(nlp.deadline(email_body_plain, deadline_purpose, deadline_model, deadline_question))
            except:
                print('this email does not have a deadline')
                continue
        print(deadline)

        if time.has_date_passed(deadline):
            print('The date in the email has passed. Skipping this message.')
            continue
        
        # Summerize the email by using NLP
        print('Summarizing email...')
        summarization_purpose = config['NLP']['summarization_purpose']
        summarization_model = config['NLP']['summarization_model']
        email_summary = nlp.summarize_email(email_body_plain, summarization_purpose, summarization_model)
        print (email_summary)

        config_variables.update({
            'deadline': deadline,
            'email_subject': email_subject,
            'email_sender': email_sender,
            'email_date': email_date,
            'email_summary': email_summary
        })

        
        config = config_tools.read_config('config.ini', config_variables)
        file_name = config['Google Drive']['file_name']
        print(file_name)
        
        # Save as .html file
        html_file_path = config['Google Drive']['html_file_path']
        with open(html_file_path, 'w', encoding='utf-8') as file:
            file.write(str(email_body_html))
        
        # Try to save as PDF if not working return false
        print('Saving PDF...')
        pdf_file_path = config['Google Drive']['pdf_file_path']

        try:
            convert_tools.html_to_pdf(email_body_html, pdf_file_path)
            convert_success = True
        except:
            print('Error converting to PDF')
            convert_success = False

        # Check if it was able to convert to PDF
        if not convert_success:
            file_link = 'Due to an error turning this email into a PDF, there is no PDF for this opportunity.'
        else:
            try:
                # Upload PDF to Google Drive
                print('Uploading to Google Drive...')
                file_name = config['Google Drive']['file_name']
                folder_id = config['Google Drive']['folder_id']
                file_link = google_drive.upload(pdf_file_path, file_name, folder_id)
                print(file_link)
            except:
                file_link = 'Due to an error this message could not be uploaded to Google Drive. Because of this there is no PDF for this opportunity'

        
        config_variables.update({
            'file_link': file_link
        })
        config = config_tools.read_config('config.ini', config_variables)

        sheet_id = config['Google Sheets']['sheet_id']
        print('Adding to Google Sheet...')
        google_sheets.add(sheet_id, email_subject, email_date, email_sender, deadline, email_summary, file_link)

        # Send WhatsApp
        print('Sending WhatsApp message...')
        wa_group_id = folder_id = config['WhatsApp']['group_id']
        wa_message = folder_id = config['WhatsApp']['message']
        wa_wait_start = folder_id = config['WhatsApp']['wait_start']
        wa_wait_start = int(wa_wait_start)
        wa_wait_close = folder_id = config['WhatsApp']['wait_close']
        wa_wait_close = int(wa_wait_close)
        wa_close = config['WhatsApp'].getboolean('close')
        try:
            pywhatkit.sendwhatmsg_to_group_instantly(wa_group_id, wa_message, wa_wait_start, wa_close, wa_wait_close)
            print('WhatsApp message has been sent')
        except:
            print('Error! WhatsApp message could not be sent.')
        