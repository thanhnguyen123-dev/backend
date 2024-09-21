from openai import OpenAI, openai
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()

class OpenAIService:
