def get_prompt(country_name):
    country_name = country_name.title()
    prompt = f"""# Context
I am a resident in Ireland with Spanish citizenship.

I am looking forward to invest in {country_name}, but I want to get information on how to get an ID number for taxpayers in {country_name}.

For example, in Ireland, the ID number for taxpayers is the Personal Public Service (PPS) Number. I would like to get something like this, but for {country_name}. I have searched online but I couldn't find anything on the country.

Write an email to the embassy of {country_name} asking if they have any more information on how I should get this number. I am a citizen of Spain with permanent residence in Ireland. I am not a resident of {country_name}.

To write the email, first write some background information on the country. You should then user this information to customize the email to the embassy.

# Example
For example, for Brazil, you should write:

Background information:
Name of the ID number for taxpayers in Brazil: CPF (Cadastro de Pessoas Físicas)

Customized email to the embassy:

Subject: How should I get a CPF (Cadastro de Pessoas Físicas) in Brazil?
Body:
```md
Dear Sir/Madam,

I hope this email finds you well.

I am a Spanish citizen (Spanish passport) with permanent residence in Ireland. I am looking forward to investing in Brazil, as a foreign investor (no residence in Brazil).

In order to do that, I am trying to understand the process of obtaining the number that identifies taxpayers in Brazil, to be able to declare the relevant information to the tax authorities.

I have been told that the number I should get is the CPF (Cadastro de Pessoas Físicas). Feel free to correct me if I am wrong.

I have searched online, but I couldn't find any information on how to get a CPF from abroad. This is why I am reaching out to you for guidance. If you could provide me with information on the process or direct me to the relevant authorities, I would greatly appreciate it.

Thank you very much for your attention to this matter. I look forward to your response and any help you can provide.
```

# Task
Now, write the email to the embassy of {country_name}. Make sure to customize the information for {country_name}. Follow the template below. Make sure to replace the placeholders ([FILL]) with the correct information.

Background information:
Name of the ID number for taxpayers in {country_name}: [FILL]

Customized email to the embassy:

Subject: How should I get a [FILL] in {country_name}?
Body:
```md
[FILL]
```
"""
    return prompt


from transformers import pipeline

chatbot = pipeline(
    "text-generation",
    model="mistralai/Mistral-7B-Instruct-v0.3",
    max_new_tokens=500,
    device=0,
    #return_full_text=False
)
# Print the device used
print(f"The model is running on {chatbot.device}")
import re


def get_email(prompt):
    # Load a completion model with chat features from Hugging Face
    # Use a pipeline as a high-level helper

    messages = [
        {"role": "user", "content": prompt},
    ]
    response = chatbot(messages)
    try:
        email = response[0]["generated_text"][1]["content"]
        subject = re.search(r"Subject: (.+)", email).group(1).strip()
        email_text = re.search(r"```md\n(.+)\n```", email, re.DOTALL).group(1).strip()
        name_of_id_number = (
            re.search(r"Name of the ID number for taxpayers in (.+?): (.+)", email)
            .group(2)
            .strip()
        )
        return {
            "subject": subject,
            "email_body": email_text,
            "name_of_id_number": name_of_id_number
        }
    except Exception as e:
        print(f"Error in the email generation: {e}")
        print(response)
        raise e


import pandas as pd

df = pd.read_csv("emails.csv", index_col=0)

# If there's no column named "email_body", "name_of_id_number", "subject", and "prompt", create them
if "email_body" not in df.columns:
    df["email_body"] = None
if "name_of_id_number" not in df.columns:
    df["name_of_id_number"] = None
if "subject" not in df.columns:
    df["subject"] = None
if "prompt" not in df.columns:
    df["prompt"] = None


for index, row in df.iterrows():
    try:
        country_name = row["country_name"]
        prompt = get_prompt(country_name)
        # Save it in prompts/{country_name}.md

        with open(f"prompts/{country_name}.md", "w") as file:
            file.write(prompt)
        print(f"Prompt for {country_name} saved!")

        print(f"Email for {country_name}")
        email = get_email(prompt)
        with open(f"emails/{country_name}.md", "w") as file:
            file.write(email['email_body'])
        print(f"Email for {country_name} saved!")

        df.at[index, "prompt"] = prompt
        df.at[index, "email_body"] = email['email_body']
        df.at[index, "name_of_id_number"] = email['name_of_id_number']
        df.at[index, "subject"] = email['subject']

        df.to_csv("emails.csv", index=True)
    except Exception as e:
        print(f"Error in {country_name}: {e}")
        continue
