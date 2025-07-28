"""
import json
import os
import google.generativeai as genai
from dotenv import load_dotenv
from google.generativeai.types import Tool, FunctionDeclaration
from backend.models.prompt_templates import SYSTEM_INSTRUCTION
from backend.tools.sql_executor import run_sql_query  # ✅ Import instruction

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Fixed JSON schema — Gemini expects top-level "type": "object"
tools = [
    Tool(
        function_declarations=[
            FunctionDeclaration(
                name="execute_sql_query",
                description="Executes a SQL query on the dataset",
                parameters={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "SQL query to run on the dataset"
                        }
                    },
                    "required": ["query"]
                }
            ),
            FunctionDeclaration(
                name="get_static_response",
                description="Returns a static answer for general questions",
                parameters={
                    "type": "object",
                    "properties": {
                        "response": {
                            "type": "string",
                            "description": "The natural language answer to return"
                        }
                    },
                    "required": ["response"]
                }
            )
        ]
    )
]

# ✅ Create Gemini model with proper tool schema
model = genai.GenerativeModel(
    model_name="models/gemini-2.0-flash",
    tools=tools,
    system_instruction=SYSTEM_INSTRUCTION
)

# ✅ Main routing function
# ✅ Main routing function

async def gemini_route_query(query: str):
    try:
        response = model.generate_content(
            query,
            generation_config={"temperature": 0.2},
            tool_config={"function_calling_config": "AUTO"}
        )
        part = response.candidates[0].content.parts[0]

        if hasattr(part, "function_call") and part.function_call:
            return {
                "name": part.function_call.name,
                "args": dict(part.function_call.args)
            }
        else:
            return {
                "name": "get_static_response",
                "args": {
                    "response": part.text if hasattr(part, "text") else "I couldn't understand the query."
                }
            }

    except Exception as e:
        return {"type": "error", "message": str(e)}
"""
import json
import os
import re
import google.generativeai as genai
from dotenv import load_dotenv
from google.generativeai.types import Tool, FunctionDeclaration
from backend.models.prompt_templates import SYSTEM_INSTRUCTION
from backend.tools.sql_executor import run_sql_query

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Define Gemini functions properly
tools = [
    Tool(
        function_declarations=[
            FunctionDeclaration(
                name="execute_sql_query",
                description="Executes a SQL query on the dataset",
                parameters={
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "SQL query to run on the dataset"
                        }
                    },
                    "required": ["query"]
                }
            ),
            FunctionDeclaration(
                name="get_static_response",
                description="Returns a static answer for general questions",
                parameters={
                    "type": "object",
                    "properties": {
                        "response": {
                            "type": "string",
                            "description": "The natural language answer to return"
                        }
                    },
                    "required": ["response"]
                }
            )
        ]
    )
]

# ✅ Load model
model = genai.GenerativeModel(
    model_name="models/gemini-2.0-flash",
    tools=tools,
    system_instruction=SYSTEM_INSTRUCTION
)

import ast
import re

async def gemini_route_query(query: str):
    try:
        response = model.generate_content(
            query,
            generation_config={"temperature": 0.2},
            tool_config={"function_calling_config": "AUTO"}
        )

        part = response.candidates[0].content.parts[0]

        # ✅ CASE 1: Native function_call (ideal case)
        if hasattr(part, "function_call") and part.function_call:
            fn_name = part.function_call.name
            args = dict(part.function_call.args)

            if fn_name == "execute_sql_query":
                sql = args.get("query")
                result = run_sql_query(sql)
                return {"type": "sql", "query": sql, "result": result}

            elif fn_name == "get_static_response":
                return {"type": "static", "response": args.get("response")}
            
            else:
                return {"type": "error", "message": f"Unknown function '{fn_name}'"}

        # ✅ CASE 2: Gemini returns tool-call JSON in plain text
        elif hasattr(part, "text"):
            text = part.text.strip()

            # Strip ```json ... ```
            if text.startswith("```json"):
                text = text.removeprefix("```json").removesuffix("```").strip()

            try:
                # Parse stringified dict into actual dict
                parsed = ast.literal_eval(text)

                if "function_call" in parsed:
                    fn_name = parsed["function_call"]["name"]
                    args = parsed["function_call"]["arguments"]

                    if fn_name == "execute_sql_query":
                        sql = args.get("query")
                        result = run_sql_query(sql)
                        return {"type": "sql", "query": sql, "result": result}

                    elif fn_name == "get_static_response":
                        return {"type": "static", "response": args.get("response")}

                    else:
                        return {"type": "error", "message": f"Unknown function '{fn_name}'"}
                else:
                    return {"type": "static", "response": text}

            except Exception as e:
                return {"type": "error", "message": f"Error parsing inner tool-call: {e}"}

        # ✅ CASE 3: Gemini gave a random non-function text
        return {"type": "static", "response": "I couldn't understand the query."}

    except Exception as e:
        return {"type": "error", "message": str(e)}


