from typing import Type,Optional
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from supabase import create_client, Client
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Supabase URL and API Key from environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class CustomerQueryInput(BaseModel):
    """Schema for querying customer database."""
    query_type: str = Field(..., description="Type of query: 'count' or 'name_search'.")
    starts_with: Optional[str] = Field(None, description="Alphabet to filter names (e.g., 'A'). Only used if query_type is 'name_search'.")

class CustomerQueryTool(BaseTool):
    name: str = "Customer Query Tool"
    description: str = "Retrieves customer data: count or names starting with a letter."
    args_schema: Type[BaseModel] = CustomerQueryInput

    def _run(self, query_type: str, starts_with: Optional[str] = None) -> str:
        if query_type == "count":
            response = supabase.table("customers").select("id", count="exact").execute()
            count = response.count if response else 0
            return f"Total customers: {count}"

        elif query_type == "name_search" and starts_with:
            response = supabase.table("customers").select("name").ilike("name", f"{starts_with}%").execute()
            names = [cust["name"] for cust in response.data] if response.data else []
            return f"Customers starting with '{starts_with}': {', '.join(names)}" if names else f"No customers found starting with '{starts_with}'."

        else:
            return "Invalid query. Use 'count' or 'name_search'."
