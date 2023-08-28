from flask import Flask, request
import requests
from bs4 import BeautifulSoup
import openai
from twilio.twiml.messaging_response import MessagingResponse
import os

# Init the Flask App
app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")
model_id = "gpt-3.5-turbo"

def ChatGPT_conversation(conversation):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
    )
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    return conversation


# Define a function to generate answers using GPT-3
def generate_answer(question):
    # print("Final Question: ", question, "\n")
    conversation = [
            {"role": "user", "content": f"Do a fact check for me for this WhatsApp forward and tell me whether it is Fake or Not Fake and a short description also provide the urls in the end- {question}"}
        ]
    response = ChatGPT_conversation(conversation)
    return response[-1]['content']


def fetch_search_results(query, source_count=6, max_attempts=10):
    attempts = 0
    while attempts < max_attempts:
        try:
            response = requests.get(f'https://www.google.com/search?q={query}')
            response.raise_for_status()
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            link_tags = soup.select('a[href^="/url"]')

            links = []
            for link_tag in link_tags:
                href = link_tag['href'][7:].split('&')[0]
                if href.startswith('http'):
                    links.append(href)

            exclude_list = ["google", "facebook", "twitter", "instagram", "youtube", "tiktok", "m.economictimes.com", "economictimes.indiatimes.com"]
            filtered_links = []
            for idx, link in enumerate(links):
                new_link = link
                if new_link not in links[:idx] and not any(site in new_link for site in exclude_list):
                    filtered_links.append(new_link)

            final_links = filtered_links[:source_count]
            # print("Final Links: ", final_links)
            return final_links

        except Exception as e:
            print('Error fetching search results:', e)
            attempts += 1

    return []


def scrape_article_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        paragraphs = soup.find_all('p')

        article_text = ''
        for p in paragraphs:
            article_text += p.get_text() + '\n'
        # print("Article Text: ", article_text)
        return article_text

    except Exception as e:
        print('Error scraping article text:', e)
        return ''


def perform_fact_check(query):
    source_count = 6
    max_attempts = 10
    search_results = fetch_search_results(query, source_count, max_attempts)
    
    sources = []
    for link in search_results:
        print("Link: ", link, "\n")
        article_text = scrape_article_text(link)
        sources.append({'url': link, 'text': article_text})

    filtered_sources = [source for source in sources if source['text'].strip()]

    for source in filtered_sources:
        source['text'] = source['text'][:1500]
    # print("Filtered Sources: ", filtered_sources, "\n")
    return generate_answer(filtered_sources)


# Define a route to handle incoming requests
@app.route('/chatgpt', methods=['POST'])
def chatgpt():
    incoming_que = request.values.get('Body', '').lower()
    print("Question: ", incoming_que, "\n")
    answer = perform_fact_check(incoming_que)
    print("BOT Answer: ", answer)
    bot_resp = MessagingResponse()
    msg = bot_resp.message()
    msg.body(answer)
    return str(bot_resp)


# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=5000)
