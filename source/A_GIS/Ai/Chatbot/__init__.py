"""Wraps AI chatbots into a few key interfaces.
"""
# Functions
from ._send_chat_groq import _send_chat_groq
from ._send_chat_ollama import _send_chat_ollama
from ._send_chat_openai import _send_chat_openai
from .chat import chat
from .get_info import get_info
from .init import init
from .list_models import list_models

# Classes
from ._Chatbot import _Chatbot
from ._Provider import _Provider
