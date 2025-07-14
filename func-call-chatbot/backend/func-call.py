import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from func import get_t_shirt, add_to_cart, place_order
from IPython.display import Markdown

load_dotenv(override=True)

api_key = os.getenv("OPENAI_API_KEY")
model = "gpt-4.1"

client = OpenAI(
    api_key=api_key
)

tools = [
    {
        "type": "function",
        "name": "get_t_shirts",
        "description": "Use this tool to get the list of available t-shirts",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the t-shirt to retrieve from the database"
                },
                "size": {
                    "type": "string",
                    "description": "The size of the t-shirt to retrieve from the database"
                },
                "color": {
                    "type": "string",
                    "description": "The color of the t-shirt to retrieve from the database"
                }
            },
            "required": ["name", "size", "color"],
            "additionalProperties": False
        },
        "strict": True
    },
    {
        "type": "function",
        "name": "add_to_cart",
        "description": "Use this tool to add the customer's user to the cart. If the customer wants more than one, provide the aggregated price into the parameters.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the t-shirt to add to the cart"
                },
                "quantity": {
                    "type": "integer",
                    "description": "The quantity of the t-shirt to add to the cart"
                },
                "size": {
                    "type": "string",
                    "description": "The size of the t-shirt to add to the cart"
                },
                "color": {
                    "type": "string",
                    "description": "The color of the t-shirt to add to the cart"
                },
                "price": {
                    "type": "string",
                    "description": "The price of the t-shirt to add to the cart"
                }
            },
            "required": ["name", "size", "color", "quantity", "price"],
            "additionalProperties": False
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "place_order",
        "description": "Use this tool to place the order for the customer's items in his or her cart.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the t-shirt to add to their order"
                },
                "quantity": {
                    "type": "integer",
                    "description": "The quantity of the t-shirt to add to their order"
                },
                "size": {
                    "type": "string",
                    "description": "The size of the t-shirt to add to their order"
                },
                "color": {
                    "type": "string",
                    "description": "The color of the t-shirt to add to their order"
                },
                "price": {
                    "type": "string",
                    "description": "The price of the t-shirt to add to their order"
                }
            },
            "required": ["name", "size", "color", "quantity", "price"],
            "additionalProperties": False
        },
        "strict": True,
    }
]

function_map = {
    "get_t_shirts": get_t_shirt,
    "add_to_cart": add_to_cart,
    "place_order": place_order
}


def get_completions(input_messages, model=model, tools=tools):
    llm_response = client.responses.create(
        model=model,
        input=input_messages,
        tools=tools,
    )

    output = llm_response.output[0]
    return output

input_messages = [
    {
        "role": "system",
        "content": "You are an action-oriented assistant that helps users with t-shirt orders. Your tasks include checking inventory, adding items to the cart, and placing orders. Always provide clear and complete answers. When a user wants to order a shirt, confirm its availability. If it’s in stock, offer to add it to their cart. After that, ask if they'd like to place the order."
    }
]

while True:
    user_input = input("👤 You: ")
    
    if user_input.lower() in {"exit", "quit"}:
        print("👋 Exiting conversation.")
        break

    print(f"👤 (You): {user_input}")
    input_messages.append({
        "role": "user", 
        "content": user_input
        })
    
    response = get_completions(input_messages)

    while response.type== "function_call":
        func_name = response.name
        input_messages.append(response)
        
        if func_name in function_map:
            args = json.loads(response.arguments)
            result = function_map[func_name](**args)

            input_messages.append({
                "type": "function_call_output",
                "call_id": response.call_id,
                "output": str(result),
            })

            response = get_completions(input_messages)
        else:
            print(f"Unknown function {func_name}")
    
    if response.type == "message":
        print(f"🤖: {response.content[0].text}")
        input_messages.append({
            "role": "assistant",
            "content": response.content[0].text
            })      

input_messages_clean = [
    msg.model_dump() if hasattr(msg, "model_dump") else msg
    for msg in input_messages
]

print(json.dumps(input_messages_clean, indent=2))