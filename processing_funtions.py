from langchain import hub
from langchain.agents import create_tool_calling_agent

from langchain.agents import AgentExecutor, create_tool_calling_agent, create_structured_chat_agent
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from custom_tools import tools
from slack_messaging import send_message

from my_llms import get_llama, get_openai


def get_recommendations(params):
    llama = get_llama()
    llm = get_openai()

    llama_agent_prompt = hub.pull("hwchase17/structured-chat-agent")

    # query = request.args.get('query')


    query = "Request from Technician ID " + str(params['technician_id']) + " : " + params['query']

    orchestrator_agent_prompt = hub.pull("hwchase17/openai-tools-agent")

    slack_standards = """
    	BOLD: *your text*
    	ITALICS: _your text_
    	CODE: `your text`
    	BULLETED LIST: - your text
    	"""

    final_response_structure = f"""
            1. Recommend 3 courses from the available course catalog (each course from a different focus area). DO NOT recommend courses from your own knowledge. Look for the right tool.
        	2. For course recommendations for a Technician, Include
        	    a. Skills they learn
        	    b. Hours
        	    c. Peer Completion
        	    d. Reason for recommendation
                e. Enrollement Link
        	3. Refer to the skills that the technician already possesses before recommending.
            4. Always recommend the class: Advanced Network Troubleshooting
        	5. Recommendations should be in decreasing order of priority.
        	6. Do not use any formatting in your output. Just plain text with numbering or bullets where required.
        	7. The "action_input" should always be a json of the arguments the tool accepts. If the tool does not require any argument, use an empty json.
        """

    orchestrator_agent_prompt.messages[0].prompt.template = orchestrator_agent_prompt.messages[
                                                                0].prompt.template + "\nYou specialize in providing counselling and course recommendations. You answer the user's question in detail and provide reasoning. Remember, whenever you provide recommendations, do so in decreasing order of priority and always provide reasoning behind the recommendation."

    orchestrator_agent_prompt.messages[0].prompt.template = orchestrator_agent_prompt.messages[
                                                                0].prompt.template + f"\nAdditional instructions:{final_response_structure}"
    agent = create_tool_calling_agent(llm, tools, orchestrator_agent_prompt)
    # Create an agent executor by passing in the agent and tools

    for i, p in enumerate(llama_agent_prompt.messages):

        if type(p) == SystemMessagePromptTemplate:
            if i == 0:
                p.prompt.template = "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n" + p.prompt.template + "<|eot_id|>"
            else:
                p.prompt.template = "<|start_header_id|>system<|end_header_id|>\n\n" + p.prompt.template + "<|eot_id|>"
        elif type(p) == HumanMessagePromptTemplate:
            p.prompt.template = "<|start_header_id|>human<|end_header_id|>\n\n" + p.prompt.template + "<|eot_id|>"

    llama_agent_prompt.messages[
        0].prompt.template = f"<|start_header_id|>system<|end_header_id|> You specialize in providing counselling and course recommendations. You answer the user's question in detail and provide reasoning. Remember, whenever you provide recommendations, do so in decreasing order of priority and always provide reasoning behind the recommendation.\nResponse Instructions: {final_response_structure}<|eot_id|> " + \
                              llama_agent_prompt.messages[0].prompt.template
    llama_agent_prompt.messages[
        -1].prompt.template = "<|start_header_id|>system<|end_header_id|>Additional Format Instruction: The 'action_input' should always be a json of the arguments the tool accepts. If the tool does not require any argument, use an empty json.<|eot_id|> " + \
                              llama_agent_prompt.messages[-1].prompt.template


    agent_llama = create_structured_chat_agent(llm=get_llama(), tools=tools, prompt=llama_agent_prompt,
                                               stop_sequence=["Observation:"])

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    suggestions = agent_executor.invoke({"input": query})

    slack_message = llm.invoke(f"""
    	        Convert the following 3rd person text into 2nd person :
    	        '''
    	        {suggestions['output']}
    	        '''

    	        Additional instructions:
    	        1. The message formatting standards below should be followed - 
    	        {slack_standards}
    	        2. DO NOT use your own formatting.
    	        3. Use the formatting standards mentioned in point 1 to make the message more appealing.
    	        """)

    slack_message = slack_message.content.replace("####", "*").replace("###", "*").replace("##", "*").replace("***",
                                                                                                              "*").replace(
        "**", "*")

    send_message("Hello Derek, thank you for using Verizon Employee Connect.\n" + slack_message)
    send_message("I can help you schedule any classes as well")

    print("DONE")
