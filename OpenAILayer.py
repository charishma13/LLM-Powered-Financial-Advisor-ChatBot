import json
import openai
import datetime

def query_completion(prompt: str, engine: str = 'gpt-3.5-turbo', temperature: float = 0.2, max_tokens: int = 1500, top_p: int = 1, frequency_penalty: float = 0.2, presence_penalty: float = 0) -> object:
    """
    Function for querying GPT-3.5 Turbo.
    """
    estimated_prompt_tokens = int(len(prompt.split()) * 1.6)
    estimated_answer_tokens = 2049 - estimated_prompt_tokens
    response = openai.ChatCompletion.create(
    model=engine,
    messages=
    [{"role": "system", "content": "You are a helpful financial assistant. Note: If a particular stock name mentio question arrises, Extract the list of Stock Names from the text in this format: [stock_name, ...]"},
    {"role": "user", "content": prompt}],
    temperature=temperature,
    max_tokens=min(4096-estimated_prompt_tokens-150, max_tokens),
    top_p=top_p,
    frequency_penalty=frequency_penalty,
    presence_penalty=presence_penalty
    )
    return response
    
def lambda_handler(event, context):
    # TODO implement
    text = event['inputTranscript']
    
    # TODO implement
    openai.api_key = "sk-xxx"
    
    print("Init:")
    print(datetime.datetime.now())
    print("Event:")
    print(event)
    
    
    #    body = json.loads(event['body'])
    #   prompt = body['prompt']
    # prompt = "Can i know what is ETF ?"
        
    max_tokens = 1500
    
    response = query_completion(text)
    response_text = response['choices'][0]['message']['content'].strip()
    
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']
    
    response = {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                'name':intent,
                'slots': slots,
                'state':'Fulfilled'
                
                }
    
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": response_text
            }
        ]
    }
    return response
    