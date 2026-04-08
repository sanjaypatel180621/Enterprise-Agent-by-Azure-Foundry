import os
import asyncio
from agent_framework.azure import AzureOpenAIResponsesClient  # type: ignore

async def build_hr_agent():
   """
   Creates and configures an HR specialist agent for handling employee-related queries.
   
   Returns:
      An agent client configured with HR policy expertise and guidance instructions.
   """
   # Initialize Azure OpenAI client with credentials from environment variables
   client = AzureOpenAIResponsesClient(
      api_key=os.getenv("AZURE_OPENAI_API_KEY"),
      endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
      deployment_name=os.getenv("AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME"),
      api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
   )
   
   # Create HR specialist agent with comprehensive employment and policy knowledge
   return client.create_agent(
      name="HRAgent",
      instructions=(
            "You are an expert HR policy specialist with deep knowledge of employment law and best practices. "
            "Answer questions about:\n"
            "- Leave policies (sick, vacation, parental, bereavement)\n"
            "- Employee benefits (health insurance, retirement, wellness programs)\n" 
            "- Performance management and reviews\n"
            "- Hiring, onboarding, and termination procedures\n"
            "- Working hours, overtime, and flexible work arrangements\n"
            "- Employee relations and conflict resolution\n"
            "- Training and development programs\n\n"
            "Provide specific, actionable guidance with policy references where applicable. "
            "Be empathetic and professional in your responses."
      ),
   )