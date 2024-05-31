### International Database

**Behavior:**
- The program marks emails as read after processing, ensuring it only handles unread emails. You can modify this behavior, but it may compromise functionality.

**Known Issues and Fixes:**
- WhatsApp Database Error:
    - Occurs due to attempting to type a message before it's loaded. Solution: Extend load time, you can do this in the config
- PDFs Missing Images:
    - Currently under investigation and being addressed.
- Incorrect Deadline Selection:
    - The program attempts to extract deadlines from email subjects, but this can fail. In such cases, AI is relied upon, which may not always be accurate.

**Setup Instructions:**
To get a more detailed instruction watch the video I've recorded just for this.

To enable the program to access your email, Gmail API is utilized. Additionally, access to Google Sheets and Google Drive is required. Follow these steps:

1. **Enable Necessary APIs:**
    - Access the [Google Cloud Console](https://console.cloud.google.com/projectselector2/apis/credentials?supportedpurview=project) and create a project.
    - Enable the Gmail API, Google Drive API, and Google Sheets API.

2. **Set Up Gmail API Credentials:**
    - Navigate to the [credentials page](https://console.cloud.google.com/apis/credentials?project=peppy-goods-422010-e6&supportedpurview=project) and create OAuth Client ID for a Desktop App named "gmail".
    - Save the credentials as `credentials_gmail.json` in the `tokens` folder.

3. **Configure Google Drive API:**
    - Create OAuth Client ID for a Website application named "GDrive".
    - Copy the Client ID and Client Secret to `pydrive_setting.yaml` in the `tokens` folder.

4. **Service Account for Google Sheets:**
    - Create a service account and share the Google Sheet with it to allow data addition.
    - Save the credentials as `credentials_sheets.json` in the `tokens` folder.
    - Share your sheet with this service account.
    
5. **Google Apps Script**
	- Copy the Google Apps Script over into your own file.
	- Put the Internal sheets ID into the script.
	- Set up a trigger, so it runs every day.

6. **Configuration File:**
    - Customize program behavior in the config file.
    - Variables
        - There are a few variables you can use in the sheet. These are signaled by ${}. You can use the following variables
            - ${deadline}
            - ${email_subject}
            - ${email_date}
            - ${email_sender}
            - ${email_summary}
            - ${deadline}
            - ${file_link}
    - Gmail section
        - Query. let's the program know where to search
    - NLP (Natural Language Processing), I recommend not changing this
        - Models. Models are the model used for the NLP, you can find them at huggingface
        - Deadline_Question. This is the question it asks to find the deadline
    - Google Drive
        - pdf_file_path. This is the temperay path used for the pdf. I recommend to keep it the same
        - html_file_path. Here it saves the html. I recommond to keep it the same
        - file_name. This is the file name in the Google Drive.
    - Google Sheet
        - sheet_id. Replace this with the Google Sheet ID of the Google Sheet you use. You can find this in the URL
    - Whatsapp
        - Group_ID. This is the group ID for whatsapp, you can find it if you make an invite link in the url
        - Message. Here is the WhatsApp Message. You can add enters and it will also use it in the WhatsApp message. Emojis are a bit more complicated and can be used by using a colon (:) and type the emoji you want, write \t to select it. (Test this out in your WhatsApp Web for which words you should use.)
        - Wait_start. This is the time the program waits until it writes the message
        - Wait_close. How long it should wait to close WhatsApp Web
        - close. Should it close WhatsApp Web after it's done.
    - Ensure correct settings for Gmail Query, NLP, Google Drive, and WhatsApp sections.

**Google Drive Folder Structure:**
- Two sheets provided: internal version for data processing and regular version for public view.
- Customize as needed; the regular version is preformatted for IFMSA-NL use.
- You can find it [here:](https://drive.google.com/drive/folders/1PtnCCO9G2ouEJ_F30BNIOzhu37pgPJbn?usp=share_link)

**Note:** Currently, the program supports WhatsApp only. Efforts are underway to integrate Telegram as well.
