from xhtml2pdf import pisa 

# Utility function
def html_to_pdf(email_body_html, pdf_file_path):
    # open output file for writing (truncated binary)
    result_file = open(pdf_file_path, 'w+b')

    # convert HTML to PDF
    pisa.CreatePDF(email_body_html,dest=result_file)
    result_file.close()
    return