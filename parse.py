import fitz  # PyMuPDF
import re

def parse_pdf(file_path):
    doc = fitz.open(file_path)
    emails = []

    for page in doc:
        try:
            # Find the name of the country and the email
            # Example text: "\n8 \nALGERIA \n \nNational Day: 1st November \n \n \nEMBASSY OF THE \nPEOPLE’S DEMOCRATIC REPUBLIC OF ALGERIA \n14 Clyde Road, Ballsbridge, Dublin 4, D04 KP74 \nTel. 01 668 92 02/01 668 6417 \nFax:  01 668 6402 \n \nE-Mail:  contact@embassyofalgeria.ie"
            text = page.get_text()
            country_name = re.search(r"\n\d+\s+\n([A-Z ]+)\n", text).group(1).strip()
            email = re.search(r"E-[Mm]ail:\s+([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", text).group(1).strip()
            info = {
                'country_name': country_name,
                'email': email
            }
            emails.append(info)
        except AttributeError:
            pass

    return emails

# Test the function
file_path = "April_updated_Diplomatic_List_April_2024.pdf"
emails = parse_pdf(file_path)
print(emails)

import pandas as pd

df = pd.DataFrame(emails)
df.to_csv('emails.csv')