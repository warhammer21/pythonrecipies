from http import HTTPStatus
import json
import os
import random
from web_service import deck,cards
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


from wsgiref.simple_server import make_server
httpd = make_server('', 8080, deal_cards)
httpd.serve_forever()
