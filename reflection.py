""" The sole purpose of this file reflection.py is to
    contain all the functionality for AI reflection using Llama 
    and AI pattern recognising using Cerebras"""
""" Cerebras is acting as a cloud server where we can run our models 
    We will be using two different AI models each for different jobs 
    and these would be called by using Cerebras API on it's platform"""

# import useful libraries
import os
from cerebras.cloud.sdk import Cerebras

# This function below controls everything regarding the Cerebras API 
def cerebras_call(prompt, model):
    # getting the cerbras API key stored in environment variables
    client = Cerebras(
        api_key=os.environ.get("CEREBRAS_API_KEY")
    )

    # getting the result from Cerebaras
    completion = client.completions.create(
        prompt=prompt,
        max_tokens=100,
        model=model,
    )
    # now we sort the actual answer out and then just go along with our job and present it in the writing space

