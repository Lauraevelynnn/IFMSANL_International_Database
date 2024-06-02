# 🌐 IFMSA-NL International Database

### Hello, world! 🌍
I'm Laura, the NMO-P and NC of IFMSA-NL 23/24. I created the International Database to help our amazing volunteers easily access and use the opportunities IFMSA offers. As a beginner coder, my code might not be perfect, but it works and gets the job done! 🚀

If you run into a bug or issue, you can either let me know here by opening an issue. You can also contact the NMO-P/NC of IFMSA-NL.

## Table of Contents
- [Quick Overview](#quick-overview)
- [Setup Instructions](#setup-instructions)
  - [Step 1: Enable Necessary APIs](#step-1-enable-necessary-apis)
  - [Step 2: Set Up Gmail API Credentials](#step-2-set-up-gmail-api-credentials)
  - [Step 3: Configure Google Drive API](#step-3-configure-google-drive-api)
  - [Step 4: Service Account for Google Sheets](#step-4-service-account-for-google-sheets)
  - [Step 5: Google Apps Script](#step-5-google-apps-script)
  - [Step 6: Configuration File](#step-6-configuration-file)
- [Google Drive Folder Structure](#google-drive-folder-structure)
- [Emojis](#emojis)
- [Program Behavior](#program-behavior)
- [Known Issues and Fixes](#known-issues-and-fixes)
- [Config Overview](#config-overview)
- [Images](#images)

## Quick Overview
This program does some cool things:
1. 📧 **Scans your Gmail for relevant opportunities.**
2. 🗓️ **Extracts deadlines and a summary of the opportunity.**
3. 📄 **Converts emails into PDFs.**
4. 📊 **Uploads the details to a Google Sheet for easy reference.**
5. 📲 **Sends these PDFs via WhatsApp.**

To make things even better, the program uses local AI to summarize emails, ensuring privacy and minimal environmental impact, no ChatGPT or Llama found here.

Also note that, as of now, this only works on Windows.

## Setup Instructions

I've recorded a detailed video guide for you (which you can find [here](https://youtube.com/watch?v=sMn-jyc31u8)). You can download the required files from the 'releases' tab or from [Google Drive](https://drive.google.com/drive/folders/1PtnCCO9G2ouEJ_F30BNIOzhu37pgPJbn?usp=share_link). Here’s a quick rundown:

### Step 1: Enable Necessary APIs
1. Go to the [Google Cloud Console](https://console.cloud.google.com/projectselector2/apis/credentials?supportedpurview=project) and create a project.
2. Enable the Gmail API, Google Drive API, and Google Sheets API.

### Step 2: Set Up Gmail API Credentials
1. Visit the [credentials page](https://console.cloud.google.com/apis/credentials?project=peppy-goods-422010-e6&supportedpurview=project) and create an OAuth Client ID for a Desktop App named "gmail".
2. Save these credentials as `credentials_gmail.json` in the `tokens` folder.

### Step 3: Configure Google Drive API
1. Create an OAuth Client ID for a Web application named "GDrive".
2. Copy the Client ID and Client Secret to `pydrive_setting.yaml` in the `tokens` folder.

### Step 4: Service Account for Google Sheets
1. Create a service account and share your Google Sheet with it.
2. Save the credentials as `credentials_sheets.json` in the `tokens` folder.

### Step 5: Google Apps Script
1. Copy the Google Apps Script into your own file.
2. Insert the internal sheets ID into the script.
3. Set up a trigger to run the script daily.

### Step 6: Configuration File
You can customize the functionality of the program. Here’s a quick overview:

- **Google Drive**
  - `folder_id`: Put the folder ID of the Google Drive where the PDFs will be placed.
- **Google Sheets**
  - `sheet_id`: Put the Sheet ID of the internal database sheet.
- **WhatsApp**
  - `group_id`: Put the WhatsApp Group ID, where the messages will be sent.

## Google Drive Folder Structure
- Two sheets: an internal version for data processing and a public version.
- Customize as needed; the public version is preformatted for IFMSA-NL use.
- [Access the folder here](https://drive.google.com/drive/folders/1PtnCCO9G2ouEJ_F30BNIOzhu37pgPJbn?usp=share_link).

## Emojis
- Use emoji shortcodes in WhatsApp, starting with a colon `:`. 
- [Find the full list of shortcodes here](https://gist.github.com/hkan/264423ab0ee720efb55e05a0f5f90887).
- Example: `:hour\t` for ⏰.

## Program Behavior
- Marks emails as read after processing to handle only unread emails. You can change this, but it might affect functionality.

## Known Issues and Fixes
- **WhatsApp Database Error**: Extend load time in the config.
- **PDFs Missing Images**: Trying to fix this.
- **Incorrect Deadline Selection**: AI extraction may occasionally miss deadlines.
- **WhatsApp Web logging out**: Sadly, I cannot fix this. I recommend either checking it beforehand or, if you're running it on a server, not closing the WhatsApp Web instance.

## Config Overview
Every part of the config can be changed. Here is an overview of what is in there and what it does.

### Gmail
- **query**: The query in which the program will look for messages. Default: `label:Database in:unread`

### NLP (Natural Language Processing)
Note: it will only use the NLP/AI when it cannot find a deadline in the email subject. The NLPs come from [HuggingFace](https://huggingface.co). Here you can also find different models.
- **deadline_purpose**: Enables the NLP to answer a question. Default: `question-answering`
- **deadline_model**: What model the Deadline NLP uses. Default: `deepset/roberta-base-squad2`
- **deadline_question**: Poses a question to the NLP. Default: `What is the deadline?`
- **summarization_purpose**: What the purpose of the summarization is. Default: `summarization`
- **summarization_model**: What model the summarization NLP uses. Default: `sshleifer/distilbart-cnn-12-6`

### Google Drive
- **pdf_file_path**: Where the PDF is temporarily stored. Default: `temp.pdf`
- **html_file_path**: Where the HTML is temporarily stored. Default: `temp.html`
- **file_name**: What the name of the PDF will be. Default: `Deadline: ${deadline} | Subject: ${email_subject}`
- **folder_id**: The Google Drive folder ID where the PDFs will be stored. No default value.

### Google Sheets
- **sheet_id**: The Google Sheet ID where the opportunities will be saved. No default value.

### WhatsApp
- **send_whatsapp**: If a WhatsApp message should be sent. Default: `True`
- **group_id**: The Group ID of the WhatsApp group in which the opportunities will be shared. No default value.
- **message**: The WhatsApp message template. Default: 

    ```text
    :laun\t *Exciting Opportunity Alert!* :laun\t

    :tear-\t On _${email_date} GMT_ an email was sent by _${email_sender}_ about a new exciting opportunity!
    
    :gli\t *Opportunity Description:*
    _${email_summary}_

    :hour\t *Deadline:*
    _${deadline}_ | (Note: if this is a combined call there may be multiple deadlines)
    
    :link\t *Find out the details by following the link!* :mail\t
    ${file_link}
    
    :meri\t Missed something? Check out the International Database in the group description!
    
    :rob\t _I am an automated message, and sometimes I make a little mistake, please correct me if I do :)_
    ```

- **wait_start**: How long the program should wait before typing the message. Default: `30`
- **wait_close**: How long the program should wait to close the WhatsApp window. Default: `15`
- **close**: Should WhatsApp close after the message is sent. Default: `True`

## On the usage of variables in the config
There are a few variables that can be used in the config. These are marked by using `${}`. The following variables exist:
- `${deadline}`
- `${email_subject}`
- `${email_date}`
- `${email_sender}`
- `${email_summary}`
- `${file_link}`

## Images
<details>
<summary>Pictures of the database</summary>

### Pictures of the database

<img width="664" alt="database_start" src="https://github.com/Lauraevelynnn/IFMSANL_International_Database/assets/167855057/0886a6f2-0d07-4f34-9a22-7f8074854e6a">

<sup>_(Front page of the International Database Sheet, I removed my contact information for privacy)_</sup>

<img width="969" alt="database_sheet" src="https://github.com/Lauraevelynnn/IFMSANL_International_Database/assets/167855057/ecefb937-79dc-436a-b066-48ceb39363c1">

<sup>_(All the opportunities lined up)_</sup>

<img width="644" alt="whatsapp" src="https://github.com/Lauraevelynnn/IFMSANL_International_Database/assets/167855057/dc58d5d1-14e7-4d5a-a576-c1f17d529a1e">

<sup>_(The message sent on WhatsApp)_</sup>

</details>
