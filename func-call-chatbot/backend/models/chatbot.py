import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from models.database import Database
from rag.rag_function import RAGSystem

class TShirtChatbot:
    
    def __init__(self, api_key=None, model="gpt-4.1"):
        load_dotenv(override=True)
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.client = OpenAI(api_key=self.api_key)
        self.database = Database()
        
        # RAG system with error handling
        try:
            self.rag_system = RAGSystem()
            self.rag_available = True
            print("RAG system initialized successfully")
        except Exception as e:
            print(f"Warning: RAG system initialization failed: {e}")
            self.rag_system = None
            self.rag_available = False
        
        self.conversation_history = []
        self.function_map = self._define_function_map()
        self.tools = self._define_tools()
        self._initialize_system_message()
        self.access_token = None

    def _define_function_map(self):
        function_map = {
            "get_t_shirt": self.database.get_t_shirt,
            "add_to_cart": self.database.add_to_cart,
            "place_order": self.database.place_order,
            "update_cart_item": self.database.update_cart_item,
            "delete_cart_item": self.database.delete_cart_item,
            "update_order": self.database.update_order,
            "delete_order": self.database.delete_order,
            "update_order_item": self.database.update_order_item,
            "delete_order_item": self.database.delete_order_item,
            "get_user_cart": self.database.get_user_cart,
            "get_user_orders": self.database.get_user_orders,
        }
        
        # RAG function only if available
        if self.rag_available and self.rag_system:
            function_map["search_knowledge_base"] = self.rag_system.search
        
        return function_map
    
    def _define_tools(self):
        tools = [
            {
                "type": "function",
                "name": "get_t_shirt",
                "description": "Use this tool to get the list of available t-shirts. If the user's input does not cover all required paremeters, inform the user.",
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
                        "variant_id": {
                            "type": "string",
                            "description": "The id of the t-shirt to add to the cart"
                        },
                        "quantity": {
                            "type": "integer",
                            "description": "The quantity of the t-shirt to add to the cart"
                        }
                    },
                    "required": ["variant_id", "quantity"],
                    "additionalProperties": False
                },
                "strict": True,
            },
            {
                "type": "function",
                "name": "place_order",
                "description": "Use this tool to place an order for all items currently in the customer's active cart. This will convert the cart items into an order and clear the cart.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False
                },
                "strict": True,
            },
            {
                "type": "function",
                "name": "update_cart_item",
                "description": "Update the quantity of a cart item.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "cart_item_id": {"type": "string", "description": "The cart item ID to update"},
                        "quantity": {"type": "integer", "description": "The new quantity"}
                    },
                    "required": ["cart_item_id", "quantity"],
                    "additionalProperties": False
                },
                "strict": True,
            },
            {
                "type": "function",
                "name": "delete_cart_item",
                "description": "Delete a cart item by its ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "cart_item_id": {"type": "string", "description": "The cart item ID to delete"}
                    },
                    "required": ["cart_item_id"],
                    "additionalProperties": False
                },
                "strict": True,
            },
            {
                "type": "function",
                "name": "update_order",
                "description": "Update the status or total amount of an order.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string", "description": "The order ID to update"},
                        "status": {"type": "string", "description": "The new status"},
                        "total_amount": {"type": "number", "description": "The new total amount"}
                    },
                    "required": ["order_id", "status", "total_amount"],
                    "additionalProperties": False
                },
                "strict": True,
            },
            {
                "type": "function",
                "name": "delete_order",
                "description": "Delete an order by its ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string", "description": "The order ID to delete"}
                    },
                    "required": ["order_id"],
                    "additionalProperties": False
                },
                "strict": True,
            },
            {
                "type": "function",
                "name": "update_order_item",
                "description": "Update the quantity or price of an order item.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_item_id": {"type": "string", "description": "The order item ID to update"},
                        "quantity": {"type": "integer", "description": "The new quantity"},
                        "item_price": {"type": "number", "description": "The new item price"}
                    },
                    "required": ["order_item_id", "quantity", "item_price"],
                    "additionalProperties": False
                },
                "strict": True,
            },
            {
                "type": "function",
                "name": "delete_order_item",
                "description": "Delete an order item by its ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_item_id": {"type": "string", "description": "The order item ID to delete"}
                    },
                    "required": ["order_item_id"],
                    "additionalProperties": False
                },
                "strict": True,
            },
            {
                "type": "function",
                "name": "get_user_cart",
                "description": "Get the authenticated user's active cart and its items.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False
                },
                "strict": True,
            },
            {
                "type": "function",
                "name": "get_user_orders",
                "description": "Get all orders for the authenticated user, including their items.",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False
                },
                "strict": True,
            },
        ]
        
        if self.rag_available and self.rag_system:
            tools.append({
                "type": "function",
                "name": "search_knowledge_base",
                "description": "Search the knowledge base for product information, FAQ answers, and policy details. Use this when users ask about product details, shipping, returns, sizing, or general questions about the store.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query to find relevant information"
                        }
                    },
                    "required": ["query"],
                    "additionalProperties": False
                },
                "strict": True,
            })
        
        return tools
    
    def _initialize_system_message(self):
        base_content = "You are an action-oriented assistant that helps users with t-shirt orders. Your tasks include checking inventory, adding items to the cart, placing orders, and providing detailed information about products, policies, and frequently asked questions."
        
        formatting_instructions = """

**CRITICAL FORMATTING RULES:**
When displaying tabular data (like cart items, orders, product listings), you MUST format it as a proper markdown table. Follow these EXACT formatting rules:

1. **Table Structure**: Each table must have proper spacing and alignment
2. **Headers**: Always include descriptive column headers
3. **Separators**: Use proper markdown table separators with dashes
4. **Spacing**: Ensure proper spacing around pipes (|)

EXAMPLES:

For orders (separate table for each order, show product details not IDs):
```
**Order 1** (2025-08-04)
| product name | size | color | quantity | price | status |
|--------------|------|-------|----------|-------|--------|
| Ctrl + Alt + Elite | S | White | 4 | $22.99 | Pending |
| **Total** | | | | **$91.96** | |
```

```
**Order 2** (2025-08-03)
| product name | size | color | quantity | price | status |
|--------------|------|-------|----------|-------|--------|
| My AI is Smarter Than Your Honor Student | M | White | 1 | $24.99 | Pending |
| I Dream in Binary | S | Jet Black | 4 | $27.61 | Pending |
| **Total** | | | | **$135.43** | |
```

For product details (when showing individual product information):
```
**I'm Just Here for the Deep Learning**
| field | value |
|-------|-------|
| Design | A clever t-shirt for deep learning enthusiasts and researchers. It blends humor with technical expertise—perfect for anyone working with neural networks and machine learning. |
| Category | Humor |
| Available Sizes | S, M |
| Available Colors | White |
```

For cart details (when showing user's cart):
```
**Your Cart**
| product name | size | color | quantity | price | total |
|--------------|------|-------|----------|-------|-------|
| Ctrl + Alt + Elite | S | White | 2 | $22.99 | $45.98 |
| I Dream in Binary | M | Jet Black | 1 | $27.61 | $27.61 |
| **Total** | | | | | **$73.59** |
```

- NEVER display order IDs to the user. Use 'Order 1', 'Order 2', etc. as table titles.
- For product lists, use proper table rows with all product details clearly displayed.
- Always interpret the data and present it in clean, readable tables.
- Format dates as YYYY-MM-DD.
- Always include proper markdown table syntax with pipes and dashes.
- For orders: ALWAYS show product details (name, size, color) instead of just variant IDs.
- For orders: Create a SEPARATE TABLE for each order for better readability when there are multiple orders.
- Extract product information from the order items and display it clearly.
- Include order date in the table title and status/total as table columns.
- Use lowercase for table headers (e.g., "product name", "size", "color") to make them smaller and less prominent.
- Add a "status" column to show the order status for each item.
- Add a "Total" row at the bottom of each table with the order total amount.
- For product details: Always present product information in a table format with "field" and "value" columns.
- For product details: Include design description, category, available sizes, and available colors in the table.
- For cart details: Always present cart information in a table format with product details and totals.
- For cart details: Include product name, size, color, quantity, price, and total for each item, plus a cart total row.

When presenting order data:
1. Get the order data with items
2. Extract product details from each item (name, size, color, quantity, price)
3. Create a separate table for each order with the format: "**Order X** (date)"
4. Include a brief introduction and any relevant follow-up information

When presenting product details:
1. Get the product information (design, category, sizes, colors)
2. Create a table with "field" and "value" columns
3. Include design description, category, available sizes, and available colors
4. Include a brief introduction and any relevant follow-up information

When presenting cart details:
1. Get the cart data with items
2. Extract product details from each item (name, size, color, quantity, price)
3. Create a table with product details and calculate totals for each item
4. Add a "Total" row at the bottom with the cart total amount
5. Include a brief introduction and any relevant follow-up information

When presenting data, provide a brief introduction, then the tables, then any additional relevant information."""

        if self.rag_available:
            content = base_content + " You have access to a comprehensive knowledge base that includes product descriptions, FAQ answers, and policy information. When users ask about product details, shipping, returns, sizing, or general questions, use the search_knowledge_base function to provide accurate and helpful information." + formatting_instructions + " When a user wants to order a shirt, confirm its availability and provide relevant product information. If it's in stock, offer to add it to their cart. After that, ask if they'd like to place the order."
        else:
            content = base_content + formatting_instructions + " When a user wants to order a shirt, confirm its availability. If it's in stock, offer to add it to their cart. After that, ask if they'd like to place the order."
        
        system_message = {
            "role": "system",
            "content": content
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
        print(f"Function call: {func_name}")
        print(f"Access token available: {self.access_token is not None}")

        if func_name in self.function_map:
            args = json.loads(response.arguments)
            print(f"Original args: {args}")
            
            #  functions that require access_token
            requires_token = {
                "add_to_cart",
                "update_cart_item",
                "delete_cart_item",
                "get_user_cart",
                "get_user_orders",
                "update_order",
                "delete_order",
                "update_order_item",
                "delete_order_item",
                "place_order"
            }

            if self.access_token and func_name in requires_token:
                args["access_token"] = self.access_token
                print(f"Added access token to args")
            
            print(f"Final args: {args}")
            try:
                if func_name == "search_knowledge_base":
                    query = args.get("query", "")
                    result = self.rag_system.search(query, 3, None)  # default top_k=3 
                else:
                    result = self.function_map[func_name](**args)
                print(f"Function result: {result}")
                return result
            except Exception as e:
                print(f"Function execution error: {e}")
                return f"Error executing function {func_name}: {str(e)}"
        else:
            result = f"No such function {func_name}"
            print(f"Function not found: {func_name}")
            return result
    
    def process_user_input(self, user_input):
        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })
        
        response = self.get_completion(self.conversation_history)
        cart_updated = False
        
        while response.type == "function_call":
            self.conversation_history.append(response)
            
            result = self.handle_function_call(response)
            
            # if cart was modified
            if response.name in ["add_to_cart", "update_cart_item", "delete_cart_item", "place_order"]:
                cart_updated = True
            
            self.conversation_history.append({
                "type": "function_call_output",
                "call_id": response.call_id,
                "output": str(result),
            })
            
            response = self.get_completion(self.conversation_history)
        
        if response.type == "message":
            bot_response = response.content[0].text
            bot_response = bot_response.replace('<br>', '\n').replace('<br/>', '\n')
            bot_response = re.sub(r'\n\s*•', '  \n•', bot_response)
            
            if cart_updated:
                bot_response += "\n\n[REFRESH_CART]"
            
            # action buttons based on context
            action_buttons = self._generate_action_buttons(user_input, bot_response)
            
            self.conversation_history.append({
                "role": "assistant",
                "content": bot_response
            })
            
            return {
                "response": bot_response,
                "action_buttons": action_buttons
            }
        
        return {
            "response": "I'm sorry, I couldn't process your request.",
            "action_buttons": None
        }
    
    def _generate_action_buttons(self, user_input: str, bot_response: str) -> list:
        """Generate appropriate action buttons based on the conversation context."""
        action_buttons = []
        
        is_viewing_cart = any(keyword in user_input.lower() for keyword in ['view cart', 'my cart', 'cart']) or \
                         any(keyword in bot_response.lower() for keyword in ['your cart', 'current cart', 'cart items'])
        
        is_viewing_orders = any(keyword in user_input.lower() for keyword in ['my orders', 'orders', 'order history']) or \
                           any(keyword in bot_response.lower() for keyword in ['your orders', 'order history', 'recent orders'])
        
        is_viewing_products = any(keyword in user_input.lower() for keyword in ['show products', 'products', 'available']) or \
                             any(keyword in bot_response.lower() for keyword in ['available products', 'product details', 't-shirt'])
        
        just_placed_order = any(keyword in bot_response.lower() for keyword in ['order placed', 'successfully placed', 'order confirmed'])
        
        cart_empty = any(keyword in bot_response.lower() for keyword in ['empty cart', 'no items', 'cart is empty'])
        
        if just_placed_order:
            action_buttons = [
                {"label": "Continue Shopping", "value": "show products"},
                {"label": "View Orders", "value": "my orders"}
            ]
        
        elif is_viewing_cart:
            if cart_empty:
                action_buttons = [
                    {"label": "Show Products", "value": "show products"}
                ]
            else:
                action_buttons = [
                    {"label": "Place Order", "value": "place order"},
                    {"label": "Continue Shopping", "value": "show products"}
                ]
        
        elif is_viewing_orders:
            action_buttons = [
                {"label": "Continue Shopping", "value": "show products"},
                {"label": "View Cart", "value": "view cart"}
            ]
        
        elif is_viewing_products:
            action_buttons = [
                {"label": "View Cart", "value": "view cart"},
                {"label": "My Orders", "value": "my orders"}
            ]
        
        else:
            action_buttons = [
                {"label": "Show Products", "value": "show products"},
                {"label": "View Cart", "value": "view cart"},
                {"label": "My Orders", "value": "my orders"}
            ]
        
        return action_buttons
    
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
    chatbot.start_conversation()