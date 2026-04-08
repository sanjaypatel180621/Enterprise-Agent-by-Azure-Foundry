import os
import asyncio
from agent_framework.azure import AzureOpenAIResponsesClient  # type: ignore

async def build_finance_agent():
   """
   Creates and configures a Finance specialist agent for handling financial and expense queries.
   
   Returns:
      An agent client configured with finance policy and reimbursement expertise.
   """
   # Initialize Azure OpenAI client with credentials from environment variables
   client = AzureOpenAIResponsesClient(
      api_key=os.getenv("AZURE_OPENAI_API_KEY"),
      endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
      deployment_name=os.getenv("AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME"),
      api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
   )
   
   # Create Finance specialist agent with expertise in expenses and reimbursements
   return client.create_agent(
      name="FinanceAgent",
      instructions=(
            "You are a finance and reimbursement specialist. Answer questions about "
            "expense policies, reimbursement limits, budget approvals, travel expenses, "
            "meal allowances, equipment purchases, and financial procedures. Provide "
            "specific amounts, policies, and actionable guidance."
      ),
   )