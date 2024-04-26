from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, PromptTemplate, \
    HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain_core.prompts.chat import MessagesPlaceholder
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent, create_structured_chat_agent
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType

from my_llms import get_openai
from database_dummy import get_courses_data, get_review_data, get_goals_data

all_dfs = get_review_data(['Performance Review', 'Agent Skills', 'Job Aids'])
llm = get_openai()

courses = get_courses_data()
docx_data = get_goals_data()


@tool
def get_job_aids():
    """Gets details of the job aids available to any technician"""

    df_agent = create_pandas_dataframe_agent(
        llm,
        all_dfs['Job Aids'],
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        number_of_head_rows=10
    )

    answer = df_agent.invoke(
        {"input": f"List all the job aids available in the entire dataframe"})

    return answer['output']


@tool
def get_perfromance_reviews(technician_id: str):
    """Gets details of a technician's manager reviews regarding performance in different quarters. This can be helpful in suggesting courses to the technician"""

    questions = """
    1. What are the areas in which the technician lacks?
    2. What are the suggestions from their manager?
    3. If there is a decline in performance, explain why it could have happened.
    
    Instruction - Mention the fullname of the technician at the start
    """

    df_agent = create_pandas_dataframe_agent(
        llm,
        all_dfs['Performance Review'],
        verbose=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        number_of_head_rows=20,
    )

    answer = df_agent.invoke({"input": f"For Technician ID {technician_id}, provide a detailed summary of their performance and answer the questions : {questions}"})

    return answer['output']


@tool
def search_training_courses():
    """Retrieves all training courses available in the course catalog for technicians"""

    return courses


@tool
def get_skills_by_employee(technician_id: str):
    """Retrieves the skills that a technician possesses"""

    return """Skills:
- Basic Fiber  maintainence and installation
- Basic Fiber troubleshooting tools
- Basic email and office
- Basic safety training
- Customer service training"""


@tool
def get_job_aid_by_role(job_id: str):
    """This is job aid for a particular job role based on id"""

    return docx_data




tools = [get_job_aid_by_role, search_training_courses, get_perfromance_reviews, get_skills_by_employee]
