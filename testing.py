# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request, jsonify
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent, create_structured_chat_agent
from langchain_ibm import WatsonxLLM
import langchain
import json 

from custom_tools import tools
from custom_tools import get_schedule as scheduler
from slack_messaging import send_message

# Flask constructor takes the name of
# current module (__name__) as argument.


import os







# ‘/’ URL is bound with hello_world() function.
def scheduling():



    # query = request.args.get('query')
    #params = request.get_json()
    #class_name = str(params['Class Name'])
    class_name = 'Dummy Class'
    duration = 50
    #duration = int(params['duration'])
    #min_class_time = 1
    events = scheduler()


scheduling()

