from http import HTTPStatus
import json
import os
import random
from web_service import deck,cards
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
# https://www.toptal.com/python/pythons-wsgi-server-application-interface
def deal_cards(environ, start_response):
    global deck
    hand_size = int(environ.get('HAND_SIZE', 5))
    cards = deck.deal(hand_size)
    status = "{status.value} {status.phrase}".format(
    status=HTTPStatus.OK)
    headers = [('Content-Type', 'application/json;charset=utf-8')]
    start_response(status, headers)
    json_cards = list(card.to_json() for card in cards)
    return [json.dumps(json_cards, indent=2).encode('utf-8')]


class JSON_Filter:
    def __init__(self, json_app):
        self.json_app = json_app
    def __call__(self, environ, start_response):
        if 'HTTP_ACCEPT' in environ:
            if 'json' in environ['HTTP_ACCEPT']:
                environ['$format'] = 'json'
                return self.json_app(environ, start_response)
        decoded_query = parse_qs(environ['QUERY_STRING'])
        if '$format' in decoded_query:
            if decoded_query['$format'][0].lower() == 'json':
                environ['$format'] = 'json'
                return self.json_app(environ, start_response)
        status = "{status.value} " \
                 "{status.phrase}".format(status=HTTPStatus.BAD_REQUEST)
        headers = [('Content-Type', 'text/plain;charset=utf-8')]
        start_response(status, headers)
        return ["Request doesn't include ? $format=json or Accept header".encode('utf-8')]

# httpd = make_server('', 8080, deal_cards)
# httpd.serve_forever()
### adding change into jan5, 2023

json_wrapper = JSON_Filter(deal_cards)
httpd = make_server('', 8080, json_wrapper)
print('DONE')

# with make_server('', 8000, json_wrapper) as httpd:
#     print("Serving on port 8000...")
#     httpd.serve_forever()
