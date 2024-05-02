# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent, create_structured_chat_agent
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate

from processing_funtions import get_recommendations
from custom_tools import tools
from custom_tools import get_schedule as scheduler
from slack_messaging import send_message
from threading import Thread

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

import os

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__072b32f36eaf4a099cca7e29b8e28035"
os.environ["LANGCHAIN_PROJECT"] = "verizon_counsellor_2024"


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/', methods=['GET', 'POST'])
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    params = request.get_json()

    thread = Thread(target=get_recommendations, kwargs={'params': params})
    thread.start()
    return 'Recommendations will be sent over soon.'


@app.route('/scheduling', methods=['GET', 'POST'])
def scheduling():
    scheduler()
    return 'hit endpoint'


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
