# Embassies Mailer

This is a side project that connects with my passion for visas, passports, bureaucracy and international relations. I am on a quest to get foreign tax ID numbers in as many countries as possible. This project uses AI to send emails to all possible embassies asking whether it's possible to get the tax ID number of their country.

To replicate the results, you'll need to follow a series of steps.

## Installation

```bash
pip install -r requirements.txt
```

## Parsing the PDF list of embassies

You'll need the email addresses of all the emabassies you want to get in contact with in order to send them the mail.

To get that, it depends on your situation - you'll need to do some searching here. In my case, I was able to find a PDF with all the embassies in my country (Ireland), so I had to parse that.

I have included the PDF in the repo for reference, but you'll need to find the relevant information that applies to you.

In my case, to extract the email addresses, I used the following command:

```bash
python parse.py
```

This will create a `emails.csv` file with the email addresses.

The columns in the CSV file are as follows:
- `country_name`: The country of the embassy
- `email`: The email address of the embassy

## Writing the emails

Once you have the email addresses, you'll need to write the emails you want to send to the embassies.

Of course, this can be a cumbersome process! So we'll use some AI to help us out 😉

You should go into the `get_emails.py` file and customize the prompt there to suit your needs.

In my case, I simply wrote a brief explanation of a situation (not exactly mine) and asked the reader to provide me more information on the tax ID number of that specific country.

The advantage of using AI here is not only that it speeds up the process, but also that it can harvest its background knowledge to adapt the email to the specific country (i.e. the name of the tax ID number is not the same in every country - it can be called "NIF" in Spain, "CPF" in Brazil, etc.).

Once you have customized the prompt, you can run the following command:

```bash
python get_emails.py
```

This will edit the `emails.csv` file to contain the following columns:
- `country_name`: The country of the embassy
- `email`: The email address of the embassy
- `email_body`: The email text to send to the embassy
- `name_of_id_number`: The name of the tax ID number in that country
- `subject`: The subject of the email
- `prompt`: The prompt that was used to generate the email (for debugging purposes)

Also, it will store the email bodies as Markdown files under the `emails` folder, and the used prompts under the `prompts` folder.

## Sending the emails

This is the final step!

You'll need to customize the `.env.template` file into a `.env` file with your email credentials.

Then you can run the following command:

```bash
python send_emails.py
```

This will send the emails to the embassies using the credentials you provided and the email text you generated.

If you abort the process at any time - no worries! The script will keep track of the emails it has already sent (with a new `sent` column in the CSV file), so you can run it again and it will pick up where it left off.

## Conclusion

And that's it! You've now sent emails to all the embassies in your country.

What replies will you get? Will you get the information you need? Will you get a foreign tax ID number this easily?

Interesting questions, right? Do let me know if you get any interesting replies by getting in touch with me at [my website](https://acmc-website.web.app/contact).

In any case, I hope you found this project useful and somewhat fun. I know I did!

And remember - this is just a side project. Please don't use it for spamming purposes or to send unsolicited emails. Be respectful and use it wisely.