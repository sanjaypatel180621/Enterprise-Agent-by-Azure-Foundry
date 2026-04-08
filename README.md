# Enterprise-Agent-by-Azure-Foundry
a multi-agent system using the Microsoft Agent Framework with distinct agent roles (Planner, HR, Compliance), deploy them, and configure A2A (Agent-to-Agent) communication to allow one agent to call others. I have a scenario where a user query is delegated through the agent network, and then inspect traces and logs to confirm correct routing.

# Mentioned few steps should be required for performing Enterprise Agent by Azure Foundry


##Replace the content of the .env file with the below content

AZURE_OPENAI_ENDPOINT= **-----------Your Deatils-----------**
AZURE_OPENAI_API_KEY= **-----------Your Deatils-----------**
AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2025-03-01-preview
