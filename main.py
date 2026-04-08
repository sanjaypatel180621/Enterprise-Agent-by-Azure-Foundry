import asyncio
import time
import logging
import sys
import os
from typing import Dict, Any
from utils.env import load_env
from agents.planner_agent import build_planner_agent, classify_target
from agents.hr_agent import build_hr_agent
from agents.compliance_agent import build_compliance_agent
from agents.finance_agent import build_finance_agent

if sys.platform == "win32":
 os.environ.setdefault("PYTHONUTF8", "1")
 if sys.stdout.encoding != "utf-8":
     sys.stdout.reconfigure(encoding="utf-8")
     sys.stderr.reconfigure(encoding="utf-8")

# Configure logging with timestamp, level, and message formatting
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def run_multi_agent(query: str, agents: Dict[str, Any]) -> Dict[str, Any]:
   """
   Advanced multi-agent system with routing, timing, and comprehensive response handling.
   
   Args:
      query: The user's question or request
      agents: Dictionary containing all initialized agent instances
      
   Returns:
      Dict containing query results, routing info, response, timing, and success status
   """
   # Record start time for performance tracking
   start_time = time.time()
   
   try:
      # Step 1: Route the query to the appropriate specialist agent
      logging.info(f"Routing query: {query[:50]}...")
      target = await classify_target(agents["planner"], query)
      logging.info(f"Query routed to: {target}")
      
      # Step 2: Map the target department to the corresponding agent
      agent_mapping = {
            "HR": ("hr", "HRAgent"),
            "FINANCE": ("finance", "FinanceAgent"), 
            "COMPLIANCE": ("compliance", "ComplianceAgent")
      }
      
      # Execute the query with the appropriate specialist agent
      if target in agent_mapping:
            agent_key, agent_name = agent_mapping[target]
            answer = await agents[agent_key].run(query)
      else:
            # Fallback mechanism: Default to HR agent if routing is unclear
            logging.warning(f"Unknown target '{target}', falling back to HR")
            answer = await agents["hr"].run(query)
            target = "HR"
            agent_name = "HRAgent"
      
      # Step 3: Calculate response time and package the results
      response_time = time.time() - start_time
      
      return {
            "query": query,
            "routed_to": target,
            "agent_name": agent_name,
            "answer": str(answer),
            "response_time": round(response_time, 2),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "success": True
      }
      
   except Exception as e:
      # Handle any errors that occur during query processing
      logging.error(f"Error processing query: {e}")
      return {
            "query": query,
            "routed_to": "ERROR",
            "agent_name": "ErrorHandler",
            "answer": f"I apologize, but I encountered an error processing your request: {str(e)}",
            "response_time": round(time.time() - start_time, 2),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "success": False
      }

def format_response(result: Dict[str, Any]) -> str:
   """
   Format the agent response for user-friendly display.
   
   Args:
      result: Dictionary containing the agent's response data
      
   Returns:
      Formatted string with response summary and answer
   """
   # Use visual indicator based on success status
   status_icon = "✅" if result["success"] else "❌"
   
   # Create formatted output with structured information
   formatted = f"""
{status_icon} Agent Response Summary:
┌─ Routed to: {result['routed_to']} ({result['agent_name']})
├─ Response time: {result['response_time']}s
├─ Timestamp: {result['timestamp']}
└─ Status: {'Success' if result['success'] else 'Error'}

💬 Answer:
{result['answer']}
"""
   return formatted

async def run_interactive_mode(agents: Dict[str, Any]):
   """
   Interactive mode for real-time user queries with command-line interface.
   
   Args:
      agents: Dictionary containing all initialized agent instances
   """
   # Display welcome message and available commands
   print("\n🤖 Enterprise Agent System - Interactive Mode")
   print("Available agents: HR, Finance, Compliance")
   print("Type 'quit' to exit, 'help' for commands\n")
   
   # Main interactive loop
   while True:
      try:
            # Get user input
            query = input("Enter your question: ").strip()
            
            # Handle exit commands
            if query.lower() in ['quit', 'exit', 'q']:
               print("👋 Goodbye!")
               break
            # Handle help command
            elif query.lower() == 'help':
               print("""
📋 Available Commands:
- Ask any question about HR, Finance, or Compliance
- 'quit' or 'exit' - Exit the system
- 'help' - Show this help message

🎯 Example questions:
- "What's the travel reimbursement limit for meals?"
- "How many vacation days do employees get?"  
- "Do we need GDPR compliance for EU customers?"
""")
               continue
            # Skip empty inputs
            elif not query:
               continue
            
            # Process the query and display formatted response
            result = await run_multi_agent(query, agents)
            print(format_response(result))
            
      except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\n👋 Goodbye!")
            break
      except Exception as e:
            # Log and display any unexpected errors
            logging.error(f"Interactive mode error: {e}")
            print(f"❌ Error: {e}")

async def run_batch_tests(agents: Dict[str, Any]):
   """
   Run predefined test queries to validate agent functionality.
   
   Args:
      agents: Dictionary containing all initialized agent instances
   """
   # Define test cases covering all three specialist domains
   test_queries = [
      "How much reimbursement is allowed for international flights?",
      "Is employee data protected under GDPR?",
      "How many sick leave days do employees get?"
   ]
   
   print("🧪 Running batch tests...\n")
   
   # Execute each test query sequentially
   for i, query in enumerate(test_queries, 1):
      # Display test header with visual separation
      print(f"{'='*80}")
      print(f"TEST {i}/{len(test_queries)}: {query}")
      print(f"{'='*80}")
      
      # Run the query and display formatted results
      result = await run_multi_agent(query, agents)
      print(format_response(result))
      
      # Add delay between tests for better readability
      if i < len(test_queries):
            await asyncio.sleep(0.5)

async def main():
   """
   Main application entry point with enhanced features.
   Initializes agents and runs in either interactive or batch mode.
   """
   print("🚀 Initializing Enterprise Agent System...")
   
   try:
      # Load environment variables and initialize all agents
      load_env()
      logging.info("Building agent network...")
      
      # Create instances of all specialist agents
      agents = {
            "planner": await build_planner_agent(),
            "hr": await build_hr_agent(), 
            "compliance": await build_compliance_agent(),
            "finance": await build_finance_agent()
      }
      
      logging.info("✅ All agents initialized successfully")
      
      # Determine execution mode based on command-line arguments
      import sys
      if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
            # Run in interactive mode for real-time queries
            await run_interactive_mode(agents)
      else:
            # Run predefined batch tests by default
            await run_batch_tests(agents)
            
   except Exception as e:
      # Handle critical initialization failures
      logging.error(f"System initialization failed: {e}")
      print(f"❌ Failed to start system: {e}")

# Entry point: Run the async main function
if __name__ == "__main__":
   asyncio.run(main())