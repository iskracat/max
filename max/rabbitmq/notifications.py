# -*- coding: utf-8 -*-
import pika
import json


def messageNotification(message):
    conversation_id = message['contexts'][0]['id']
    username = message['actor']['username']
    text = message['object']['content']
    message_id = message['_id']

    message = {
        'conversation': conversation_id,
        'message': text,
        'username': username,
        'messageID': message_id
    }

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost'
        )
    )
    channel = connection.channel()
    channel.basic_publish(
        exchange=conversation_id,
        routing_key='',
        body=json.dumps(message)
    )


def addConversationExchange(conversation):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost'
        )
    )
    channel = connection.channel()
    channel.exchange_declare(exchange=conversation.getIdentifier(),
                             durable=True,
                             type='fanout')

    message = {
        'conversation': conversation.getIdentifier()
    }

    for username in conversation.participants:
        if username != conversation._owner:
            channel.basic_publish(
                exchange='new',
                routing_key=username,
                body=json.dumps(message)
            )
