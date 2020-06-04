#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 17:38:27 2020

@author: etrans
"""

import os
import logging
import asyncio
import ssl as ssl_lib
import sys

import certifi
import slack

from modules.send_info import send_info, send_real_response

"""This file serves as an example for how to create the same app, but running asynchronously."""

print("sys Version:", sys.version)


# ============== Message Events ============= #
# When a user sends a DM, the event type will be 'message'.
# Here we'll link the message callback to the 'message' event.
@slack.RTMClient.run_on(event="message")
async def message(**payload):
    """Display the onboarding welcome message after receiving a message
    that contains "start".
    """
    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data.get("channel")
    user_id = data.get("user")
    text = data.get("text")
    if channel_id == os.environ['CHANNEL_ID']:  # example: 'CU51JSMA6'
        print(text)



if __name__ == "__main__":
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    slack_token = os.environ['SLACK_API_TOKEN']

    # tener los existentes
    client = slack.WebClient(token=slack_token)
    response = client.conversations_history(channel='CU61JSMM5')
    request_list = list()
    for message in response.data['messages']:
        text = message['text']
	print(text)

    # esperar los nuevos
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    rtm_client = slack.RTMClient(
        token=slack_token, ssl=ssl_context, run_async=True, loop=loop
    )
    loop.run_until_complete(rtm_client.start())
