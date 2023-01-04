import openai
import requests
import base64

def wph2(text):
    code = f'<!-- wp:heading --><h2>{text}</h2><!-- /wp:heading -->'
    return code

def generate_text(prompt):
    import os
    from dotenv import load_dotenv
    load_dotenv()
    openai.api_key = os.getenv('API_key')

    completion = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5,
        top_p=1.0,
        frequency_penalty=0,
        presence_penalty=0
    )

    return completion.choices[0].text

with open('keywords.txt') as f:
    keywords = f.readlines()
keywords = [k.strip() for k in keywords]


for keyword in keywords:
    introduction = generate_text(f"Write an introduction about the {keyword}")
    modified_phrase = keyword.replace("best", "")
    first_h2 = generate_text(f"why {modified_phrase} is important write 150 words")
    second_h2 = generate_text(f"how to choose the {keyword} write 200 words")
    third_h2 = generate_text(f"what features should be considered while buying {modified_phrase} write 200 words")
    conclusion = generate_text(f"Write a conclusion about the {keyword}")

    heading1 = wph2(f'Why {modified_phrase} is Important')
    heading2 = wph2(f'How to Choose the {keyword}')
    heading3 = wph2(f'What Features Should be Considered While Buying {modified_phrase}')
    concluh2 = wph2('Conclusion')

    content = f"{introduction}\n\n{heading1}{first_h2}{heading2}{second_h2}{heading3}{third_h2}\n\n{concluh2}{conclusion}"

    wp_user = 'oviin'
    wp_password = 'GLKn SEgm xTce LtLw Es1S dFL3'
    wp_credential = f'{wp_user}:{wp_password}'
    wp_token = base64.b64encode(wp_credential.encode())
    wp_headers = {'Authorization': f'Basic {wp_token.decode("utf-8")}'}

    title = f'{keyword} in 2023'
    data = {
        'title': title.title(),
        'content': content,
        'slug': keyword.replace(' ', '-'),
        'status': 'publish'
    }
    endpoint = 'http://buyingguide.local/wp-json/wp/v2/posts'
    r = requests.post(endpoint, data=data, headers=wp_headers, verify=False)