from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import langchain_community as langchain_community
from langchain.agents import create_agent
import langchain_community
from tavily import TavilyClient
import pytesseract as pyt
import streamlit as st
import os
import time
from PIL import Image
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore")

print("Module Loaded Successfully!!")

model=ChatGoogleGenerativeAI(
    model='gemini-3.5-flash-lite',
    google_api_key=GOOGLE_API_KEY
)
response = model.invoke("hello buddy!")
response.content[-1]['text']

def search_latest_news_jobs(query):
    """This function helps to fetch latest
    news or jobs related article using
    tavily"""

    client = TavilyClient(
        api_key=TAVILY_API_KEY
    )

    response = client.search(query)
    return response

    # Agent Creation

agent = create_agent(
    model=model,
    tools=[search_latest_news_jobs]
)

agent

def main_agent(agent, query):
    """This is main agent, or leader agent
    orchestrate sub agents"""

    # Giving prompt to create detailed prompt
    # for code generation

    prompt = """You are AI assistant and
    below given is a prompt, your
    task is to give detailed prompt for
    this.

    You are a professional Resume generator
    where user will give their personal info,
    you have to create detailed Resume
    for students or professional one,
    it must be with dynamic UI and UX and,
    with advanced CSS Professional Designing.
    Make sure to give output in HTML format only
    no markdowns allowed
    """

    response = agent.invoke({
        'messages': [{
            'role': 'user',
            'content': prompt
        }]
    })

    detailed_prompt = response['messages'][-1].content[-1]['text']

    # SAVE PROMPT using File Handling
    with open("prompt.txt", "w") as f:
        f.write(detailed_prompt)

    user_details = f"""Below Given is a user details
    generate Resume based on that, if not
    given keep: Default Resume: Python Developer
    user details: {query}"""

    final_prompt = prompt + detailed_prompt + user_details

    # CODE GENERATION
    response = agent.invoke({
        'messages': [{
            'role': 'user',
            'content': final_prompt
        }]
    })

    code = response['messages'][-1].content[-1]['text']

    return code


code = main_agent(agent, "ALAN TURING, GEN AI EXPERT")

from IPython import display as DISPLAY
DISPLAY.HTML(code)

def get_jobs(agent,
             location="noida, delhi",
             profile="data analyst, ai engineer"):
  location="noida, delhi"
  profile= "data"