import smtplib
import os
import random
import time
import pandas as pd
from dotenv import load_dotenv
from email.message import EmailMessage


load_dotenv()

# Send emails using SMTP
# Now that we have the emails and the prompts, we can send the emails using the SMTP protocol.
# Set up the SMTP server
smtp_server = os.environ.get("SMTP_SERVER")
smtp_port = 587
smtp_username = os.environ.get("SMTP_USERNAME")
smtp_password = os.environ.get("SMTP_PASSWORD")


def send_email(subject, message, to_email):
    # Create a connection to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    # Construct the email headers and body
    em = EmailMessage()
    em.set_content(message)
    em["To"] = to_email
    em["From"] = f"{os.environ.get('MY_NAME')} <{smtp_username}>"
    em["Subject"] = subject

    server.send_message(em)

    # Close the connection to the SMTP server
    server.quit()


# Send the emails
if __name__ == "__main__":
    emails_df = pd.read_csv("emails.csv", index_col=0)

    if "sent" not in emails_df.columns:
        emails_df["sent"] = False

    # Each row contains: index,country_name,email,email_body,name_of_id_number,subject,prompt
    for index, row in emails_df.iterrows():
        if row["sent"]:
            continue
        message_with_closing = f"{row['email_body']}\n\nSincerely,\n{os.environ.get('MY_NAME')}\n\nSent from my iPhone"
        send_email(row["subject"], message_with_closing, row["email"])
        print(f"Email sent to {row['email']}")
        # Mark the email as sent in the emails.csv file
        emails_df.loc[index, "sent"] = True
        emails_df.to_csv("emails.csv", index=True)
        time.sleep(random.randint(25, 60))
