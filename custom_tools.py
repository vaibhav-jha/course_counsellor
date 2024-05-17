from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, PromptTemplate, \
    HumanMessagePromptTemplate, AIMessagePromptTemplate
from langchain_core.prompts.chat import MessagesPlaceholder
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent, create_structured_chat_agent
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType

import datetime
import os.path
import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

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
def get_available_training_courses():
    """
    Retrieves all training courses available in the course catalog for all technicians.
    This helps technicians improve various skills. Useful for recommending skill improvements for technicians.
    Use when determining skill-improvement suggestions for one or more technicians.
    """

    return courses


@tool
def get_skills_by_employee(technician_id: str):
    """Retrieves the skills that a technician possesses."""

    return """Skills:
- Basic Fiber  maintainence and installation
- Basic Fiber troubleshooting tools
- Basic email and office
- Basic safety training
- Customer service training"""


@tool
def get_job_aid_by_role(job_role: str):
    """
    This is job aid for a particular job role based on a position.
    Lists out the skills needed for a particular job role.
    Use this to retrieve the skill requirements for a particular job role.
    """

    return docx_data


def get_schedule():
    """Get the Calendar for the Gmai of Derek"""
    events_cal = []
    creds = None
    SCOPES = ["https://www.googleapis.com/auth/calendar","https://www.googleapis.com/auth/calendar.events"]
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:

            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
  
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w+") as token:
                token.write(creds.to_json())

        event = {
  'summary': 'Advanced Network Troubleshooting',
  'location': 'vz.com/training',
  'description': 'This course covers essential leadership skills tailored for technical environments, focusing on effective team management and strategic decision-making.',
  'start': {
    'dateTime': '2024-05-20T08:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': '2024-05-20T09:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'recurrence': [
    'RRULE:FREQ=DAILY;COUNT=5'
  ]
}
    service = build("calendar", "v3", credentials=creds)
    event = service.events().insert(calendarId='primary', body=event).execute()

    print ('Event created: %s' % (event.get('htmlLink')))
    
    return json.dumps(events_cal, default=str)


tools = [get_job_aid_by_role, get_available_training_courses, get_perfromance_reviews, get_skills_by_employee]
