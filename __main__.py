# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, request, jsonify
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent, create_structured_chat_agent
import langchain

from custom_tools import tools
from slack_messaging import send_message

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)

import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "ls__072b32f36eaf4a099cca7e29b8e28035"
os.environ["LANGCHAIN_PROJECT"]= "verizon_counsellor_2024"


def get_llama():
    parameters = {
        "decoding_method": "greedy",
        "max_new_tokens": 2000,
        "min_new_tokens": 10,
        "temperature": 0.01,
        #     "top_k": 50,
        #     "top_p": 1,
    }

    from langchain_ibm import WatsonxLLM

    llama = WatsonxLLM(
        model_id="meta-llama/llama-3-70b-instruct",
        url="https://us-south.ml.cloud.ibm.com",
        project_id="a92c8753-e724-4835-a415-ec0730333135",
        params=parameters,
        apikey="b9n-3HqQTRSMvFhUry-awqN3ZLVIr_UzddSht6OQ6CyV",
    )

    return llama


def get_openai():
    from langchain_openai import ChatOpenAI

    llm = ChatOpenAI(model="gpt-4-turbo")

    return llm


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/', methods=['GET', 'POST'])
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    llama = get_llama()
    llm = get_openai()

    # query = request.args.get('query')
    params = request.get_json()

    query = "Request from Technician ID " + str(params['technician_id']) + " : " + params['query']

    orchestrator_agent_prompt = hub.pull("hwchase17/openai-tools-agent")

    final_response_structure = """
	1. Course recommendations for Technician.
	2. Reasons for each recommendation.

	"""

    slack_standards = """
	BOLD: *your_text*
	ITALICS: _your_text_
	CODE: `your_text`
	BULLETED LIST: * your_text
	"""

    orchestrator_agent_prompt.messages[0].prompt.template = orchestrator_agent_prompt.messages[
                                                                0].prompt.template + "\nYou specialize in providing counselling and course recommendations. You answer the user's question in detail and provide reasoning. Remember, whenever you provide recommendations, do so in decreasing order of priority and always provide reasoning behind the recommendation."
    orchestrator_agent_prompt.messages[0].prompt.template = orchestrator_agent_prompt.messages[
                                                                0].prompt.template + f"\n Follow Slack formatting standards in your final output. Slack Standards: {slack_standards}"

    agent = create_tool_calling_agent(llm, tools, orchestrator_agent_prompt)
    # Create an agent executor by passing in the agent and tools
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    suggestions = agent_executor.invoke({"input": query})

    slack_message = llm.invoke(f"""
	        Convert the following 3rd person text into 2nd person :
	        '''
	        {suggestions['output']}
	        '''
	        """)

    send_message(slack_message.content)

    return slack_message.content


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()
