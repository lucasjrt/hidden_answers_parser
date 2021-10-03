import json
import os

from pprint import pprint
from bs4 import BeautifulSoup

from src.models.question import Question
from src.schemas.question import QuestionSchema

RESULTS_PATH = './no-script/'
if not RESULTS_PATH.endswith('/'):
    RESULTS_PATH += '/'

INTERESTING_PATH = './interesting/'
if not INTERESTING_PATH.endswith('/'):
    INTERESTING_PATH += '/'

post_tags = os.listdir(RESULTS_PATH)

interesting = []
all_posts = []
maximum = 100
current = 0
for tag in post_tags:
    tag_path = RESULTS_PATH + tag

    all_posts_path = os.listdir(tag_path)
    for html_file in all_posts_path:
        if current >= maximum:
            break
        html_path = '{}/{}'.format(tag_path, html_file)

        with open(html_path, 'r') as html_file:
            html_lines = html_file.readlines()

        html_content = ''.join(html_lines)

        parsed_html = BeautifulSoup(html_content, 'html.parser')

        print(html_path)
        question = Question(parsed_html)
        schema = QuestionSchema()
        result = schema.dump(question)

        if not question.category == 'Hacking':
            all_posts.append(result)
            current += 1
            continue
        print('===============================================================')
        print(question.title)
        print('===============================================================')
        pprint(result)
        print('===============================================================')

        interesting.append(result)
        current += 1
    if current >= maximum:
        break

if not os.path.exists(INTERESTING_PATH):
    os.makedirs(INTERESTING_PATH)

with open('{}output.json'.format(INTERESTING_PATH), 'w') as interesting_file_handler:
    json.dump(interesting, interesting_file_handler)

with open('{}general.json'.format(INTERESTING_PATH), 'w') as general_file_handler:
    json.dump(all_posts, general_file_handler)
