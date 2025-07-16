import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from models.tshirt import TShirtDatabase
from routers.middleware import KnownAppError

class TShirtChatbot:
    
    def __init__(self, api_key=None, model="gpt-4.1"):
        load_dotenv(override=True)
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = OpenAI(api_key=self.api_key)
        self.database = TShirtDatabase()
        self.conversation_history = []
        self.function_map = self._define_function_map()
        self.tools = self._define_tools()
        self._initialize_system_message()

    def _define_function_map(self):
        return {
            "get_t_shirts": self.database.get_t_shirts,
            "add_to_cart": self.database.add_to_cart,
            "place_order": self.database.place_order
        }
    
    def _define_tools(self):
        return [
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
    
    def _initialize_system_message(self):
        system_message = {
            "role": "system",
            "content": "You are an action-oriented assistant that helps users with t-shirt orders. Your tasks include checking inventory, adding items to the cart, and placing orders. Always provide clear and complete answers. When a user wants to order a shirt, confirm its availability. If it's in stock, offer to add it to their cart. After that, ask if they'd like to place the order."
        }
        self.conversation_history.append(system_message)
    
    def get_completion(self, messages):
        llm_response = self.client.responses.create(
            model=self.model,
            input=messages,
            tools=self.tools,
        )
        return llm_response.output[0]
    
    def handle_function_call(self, response):
        func_name = response.name

        if func_name in self.function_map:
            args = json.loads(response.arguments)
            result = self.function_map[func_name](**args)
        else:
            result = f"No such function {func_name}"
            KnownAppError(f"No such function {func_name}")

        return result
    
    def process_user_input(self, user_input):
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        response = self.get_completion(self.conversation_history)
        
        while response.type == "function_call":
            self.conversation_history.append(response)
            
            result = self.handle_function_call(response)
            
            self.conversation_history.append({
                "type": "function_call_output",
                "call_id": response.call_id,
                "output": str(result),
            })
            
            response = self.get_completion(self.conversation_history)
        
        if response.type == "message":
            bot_response = response.content[0].text
            self.conversation_history.append({
                "role": "assistant",
                "content": bot_response
            })
            return bot_response
        
        return "I'm sorry, I couldn't process your request."
    
    def get_conversation_history(self):
        return [
            msg.model_dump() if hasattr(msg, "model_dump") else msg
            for msg in self.conversation_history
        ]
    
    def start_conversation(self):
        print("🤖 T-Shirt Assistant: Hello! I can help you find and order t-shirts. What are you looking for today?")
        
        while True:
            user_input = input("👤 You: ")
            
            if user_input.lower() in {"exit", "quit"}:
                print("👋 Exiting conversation.")
                break
            
            print(f"👤 (You): {user_input}")
            
            bot_response = self.process_user_input(user_input)
            print(f"🤖: {bot_response}")
        
        print("\n" + "="*50)
        print("CONVERSATION HISTORY:")
        print("="*50)
        print(json.dumps(self.get_conversation_history(), indent=2))


if __name__ == "__main__":
    chatbot = TShirtChatbot()
    chatbot.start_conversation()