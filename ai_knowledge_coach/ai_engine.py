
import os
from openai import AzureOpenAI
from utils import get_prompt_template

def generate_knowledge_content(topic, endpoint, api_key, deployment, api_version, temperature=0.2, summary_length="Medium (120 words)", quiz_difficulty="Medium"):
    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=api_key,
    )
    prompt = get_prompt_template().format(
        topic=topic,
        summary_length=summary_length,
        quiz_difficulty=quiz_difficulty
    )
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an expert knowledge coach."},
            {"role": "user", "content": prompt}
        ],
        max_completion_tokens=1200,
        temperature=temperature,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        model=deployment
    )
    return response.choices[0].message.content
