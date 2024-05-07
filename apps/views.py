import os
from dotenv import load_dotenv

from django.shortcuts import render

load_dotenv()
print(os.getenv("REPLICATE_API_KEY"))