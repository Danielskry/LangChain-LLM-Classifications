""" LLM configuration. """

import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

load_dotenv()

class LLMConfig(object):
    """ Backend LLM configuration parameters. """
    pass

class OpenAIConfig(LLMConfig):
    """ Configuration for OpenAI LLM. """
    OPENAI_API_KEY = os.getenv('APP_OPENAI_API_KEY')
    OPENAI_ORGANIZATION = os.getenv('APP_OPENAI_ORGANIZATION')
    OPENAI_LLM_MODEL = os.getenv('APP_OPENAI_LLM_MODEL')

    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        organization=OPENAI_ORGANIZATION,
        model=OPENAI_LLM_MODEL,
        temperature=0
    )
