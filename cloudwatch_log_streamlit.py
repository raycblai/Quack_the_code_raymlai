import streamlit as st
from mcp import stdio_client, StdioServerParameters
from strands import Agent
from strands.tools.mcp import MCPClient
import boto3
import os
import json
from datetime import datetime
import logging
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def extract_last_assistant_content(conversation_data):
    """Extract the last content from the assistant's response."""
    try:
        # Find the last message with role 'assistant'
        assistant_messages = [msg for msg in conversation_data if msg['role'] == 'assistant']
        if not assistant_messages:
            logger.warning("No assistant messages found")
            return None

        last_assistant_message = assistant_messages[-1]
        content = last_assistant_message['content']

        # Find the last text content
        text_contents = [item['text'] for item in content if 'text' in item]
        if not text_contents:
            logger.warning("No text content found in assistant's message")
            return None

        last_text = text_contents[-1]
        logger.info("Successfully extracted last assistant content")
        return last_text

    except Exception as e:
        logger.error(f"Error extracting assistant content: {str(e)}")
        return None

def extract_json_from_text(text):
    """Extract JSON data from text content."""
    try:
        # Find JSON block between triple backticks
        json_pattern = r'```json\n(.*?)\n```'
        match = re.search(json_pattern, text, re.DOTALL)
        
        if match:
            json_str = match.group(1)
            logger.info("Found JSON block in content")
            return json.loads(json_str)
        else:
            logger.warning("No JSON block found in content")
            return None
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error extracting JSON: {str(e)}")
        return None
# Set page config
st.set_page_config(
    page_title="CloudWatch Logs Query Tool",
    page_icon="🔍",
    layout="wide"
)

# Set AWS profile
os.environ['AWS_PROFILE'] = 'bedrockuser'

def initialize_aws_client():
    """Initialize AWS client and verify credentials."""
    try:
        session = boto3.Session(profile_name='bedrockuser')
        sts_client = session.client('sts')
        identity = sts_client.get_caller_identity()
        logger.info(f"AWS Identity: {json.dumps(identity, indent=2)}")
        return session, identity
    except Exception as e:
        logger.error(f"Error initializing AWS client: {str(e)}")
        st.error(f"Error initializing AWS client: {str(e)}")
        return None, None

def initialize_mcp_client():
    """Initialize MCP client for CloudWatch Logs."""
    try:
        logger.info("Initializing MCP client...")
        return MCPClient(lambda: stdio_client(
            StdioServerParameters(
                command="uvx", 
                args=["awslabs.cloudwatch-logs-mcp-server@latest"],
                env={"AWS_PROFILE": "bedrockuser", "AWS_REGION": "us-west-2"}
            )
        ))
    except Exception as e:
        logger.error(f"Error initializing MCP client: {str(e)}")
        st.error(f"Error initializing MCP client: {str(e)}")
        return None

def list_log_groups(logs_client):
    """List CloudWatch log groups."""
    try:
        logger.info("Listing CloudWatch log groups...")
        response = logs_client.describe_log_groups(limit=10)
        log_groups = response.get('logGroups', [])
        logger.info(f"Found {len(log_groups)} log groups")
        return log_groups
    except Exception as e:
        logger.error(f"Error listing log groups: {str(e)}")
        st.error(f"Error listing log groups: {str(e)}")
        return []

def format_timestamp(timestamp):
    """Convert millisecond timestamp to readable datetime."""
    try:
        return datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return timestamp

def display_query_results(response):
    """Display query results in a formatted way."""
    try:
        # Log the raw response
        logger.info("Raw response received:")
        logger.info(json.dumps(response, indent=2))

        # Check if response is a string and try to parse it as JSON
        if isinstance(response, str):
            try:
                response = json.loads(response)
                logger.info("Successfully parsed response as JSON")
            except json.JSONDecodeError:
                logger.info("Response is not JSON, displaying as is")
                st.write(response)
                return

        # If response is a dictionary
        if isinstance(response, dict):
            # Check for log events
            if 'logEvents' in response:
                logger.info(f"Found {len(response['logEvents'])} log events")
                st.subheader("Log Events")
                for event in response['logEvents']:
                    with st.expander(f"Event at {format_timestamp(event.get('timestamp', ''))}"):
                        st.write("Message:", event.get('message', ''))
                        st.write("Timestamp:", format_timestamp(event.get('timestamp', '')))
                        if 'eventId' in event:
                            st.write("Event ID:", event.get('eventId'))

            # Check for log groups
            if 'logGroups' in response:
                logger.info(f"Found {len(response['logGroups'])} log groups")
                st.subheader("Log Groups")
                for group in response['logGroups']:
                    with st.expander(group.get('logGroupName', 'Unnamed Group')):
                        st.json(group)

            # Display any other top-level keys
            for key, value in response.items():
                if key not in ['logEvents', 'logGroups']:
                    logger.info(f"Processing top-level key: {key}")
                    st.subheader(key.replace('_', ' ').title())
                    if isinstance(value, (dict, list)):
                        st.json(value)
                    else:
                        st.write(value)

        # If response is a list
        elif isinstance(response, list):
            logger.info(f"Processing list response with {len(response)} items")
            st.subheader("Results")
            for item in response:
                if isinstance(item, dict):
                    with st.expander(f"Item {response.index(item) + 1}"):
                        st.json(item)
                else:
                    st.write(item)

        else:
            logger.info("Displaying response as is")
            st.write(response)

    except Exception as e:
        logger.error(f"Error displaying results: {str(e)}")
        st.error(f"Error displaying results: {str(e)}")
        st.write("Raw response:", response)

def main():
    st.title("🔍 CloudWatch Logs Query Tool")
    
    # Initialize AWS client
    session, identity = initialize_aws_client()
    if not session:
        st.error("Failed to initialize AWS client. Please check your credentials.")
        return

    # Display AWS identity information
    with st.expander("AWS Account Information"):
        st.json(identity)

    # Initialize MCP client
    mcp_client = initialize_mcp_client()
    if not mcp_client:
        st.error("Failed to initialize MCP client.")
        return

    # Create tabs for different functionalities
    tab1, tab2 = st.tabs(["Query Logs", "View Log Groups"])

    with tab1:
        st.header("Query CloudWatch Logs")
        
        # Query input
        query = st.text_area(
            "Enter your query",
            placeholder="Example: Find messages with Tx_id 00002 within log group names having 'rebooking' in the us-west-2 region",
            height=100
        )

        if st.button("Run Query"):
            if not query:
                st.warning("Please enter a query first.")
            else:
                with st.spinner("Running query..."):
                    try:
                        logger.info(f"Executing query: {query}")
                        with mcp_client:
                            tools = mcp_client.list_tools_sync()
                            agent = Agent(tools=tools)
                            response = agent(query)                                    
                            logger.info(f"Response: {response}")
                            st.subheader("Query Results")
                            logger.info("Query completed successfully")
                            logger.info(f"Agent.messages: {agent.messages}")

                            last_content = extract_last_assistant_content(agent.messages)
                            if last_content:
                                print("\nLast Assistant Content:")
                                print(last_content)
                                
                                # Extract JSON from the content
                                json_data = extract_json_from_text(last_content)
                                if json_data:
                                    print("\nExtracted JSON Data:")
                                    print(json.dumps(json_data, indent=2))
                            else:
                                print("Failed to extract assistant content")
                            display_query_results(last_content)
                    except Exception as e:
                        logger.error(f"Error running query: {str(e)}")
                        st.error(f"Error running query: {str(e)}")

    with tab2:
        st.header("Available Log Groups")
        
        if st.button("Refresh Log Groups"):
            logs_client = session.client('logs', region_name='us-west-2')
            log_groups = list_log_groups(logs_client)
            
            if log_groups:
                st.write(f"Found {len(log_groups)} log groups:")
                for group in log_groups:
                    with st.expander(group.get('logGroupName')):
                        st.json(group)
            else:
                st.info("No log groups found.")

if __name__ == "__main__":
    main() 