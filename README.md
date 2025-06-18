# CloudWatch Logs Query Tool 🔍

A Streamlit-based web application for querying and analyzing AWS CloudWatch Logs using the Model Context Protocol (MCP) and AI-powered natural language queries.

## Features

- **Natural Language Queries**: Query CloudWatch logs using plain English
- **Interactive Web Interface**: User-friendly Streamlit interface
- **AWS Integration**: Direct integration with AWS CloudWatch Logs
- **MCP Protocol**: Leverages Model Context Protocol for enhanced AI capabilities
- **Real-time Results**: View query results in formatted, expandable sections
- **Log Group Management**: Browse and explore available CloudWatch log groups

## Prerequisites

- Python 3.8+
- AWS CLI configured with appropriate credentials
- AWS profile named `bedrockuser` (or modify the code to use your profile)
- Access to AWS CloudWatch Logs service

## Installation

1. Clone this repository:
```bash
git clone https://github.com/raycblai/Quack_the_code_raymlai.git
cd Quack_the_code_raymlai
```

2. Create and activate a virtual environment:
```bash
python -m venv Quack_the_code_env
source Quack_the_code_env/bin/activate  # On Windows: Quack_the_code_env\Scripts\activate
```

3. Install required dependencies:
```bash
pip install streamlit boto3 mcp strands
```

4. Install the CloudWatch Logs MCP server:
```bash
uvx install awslabs.cloudwatch-logs-mcp-server@latest
```

## Configuration

### AWS Setup

1. Configure your AWS credentials:
```bash
aws configure --profile bedrockuser
```

2. Ensure your AWS profile has the following permissions:
   - `logs:DescribeLogGroups`
   - `logs:DescribeLogStreams`
   - `logs:FilterLogEvents`
   - `logs:StartQuery`
   - `logs:StopQuery`
   - `logs:GetQueryResults`

### Environment Variables

The application uses the following environment variables:
- `AWS_PROFILE`: Set to `bedrockuser` (or modify in code)
- `AWS_REGION`: Set to `us-west-2` (or modify in code)

## Usage

1. Start the Streamlit application:
```bash
streamlit run cloudwatch_log_streamlit.py
```

2. Open your web browser and navigate to the provided URL (typically `http://localhost:8501`)

3. Use the application:
   - **Query Logs Tab**: Enter natural language queries to search CloudWatch logs
   - **View Log Groups Tab**: Browse available log groups in your AWS account

### Example Queries

#### Basic Queries
- "Show error messages from the last hour"
- "Find all logs containing 'exception' or 'error'"
- "Get recent logs from application servers"

#### Detailed Query Example for Demo

**Assumptions for Demo:**

In this example, we assume there is a `rebooking_log` CloudWatch Log Group that contains log entries with different transaction IDs and messages in the specific format:
- `Tx_id: 000001, Starting rebooking process`
- `Tx_id: 000002, Customer ID: 12345 requested rebooking`
- `Tx_id: 000003, Processing payment for booking change`
- `Tx_id: 000004, Rebooking completed successfully`

This structured log format allows us to use LLM (Large Language Model) and MCP (Model Context Protocol) server to query and analyze the data, then return results in JSON format for easy processing and display.

For demonstration purposes, use this specific query format:

**Query:**
```
find message contain "Tx_id: 000004" for all log streams within "rebooking_log" log group from June 15, 2025 00:00:00 to June 17, 2025 00:00:00. If not found, show me the cloudwatch log query. If found, display the response in JSON format as follows:
```

**Expected JSON Response Format:**
```json
[
  {
    "Timestamp": "2025-06-14 14:20:29.444",
    "Message": "Tx_id: 000001, Starting rebooking process"
  },
  {
    "Timestamp": "2025-06-14 14:20:29.444",
    "Message": "Tx_id: 000001, Customer ID: 12345 requested rebooking"
  }
]
```

**Key Features of This Query:**
- **Specific Transaction ID Search**: Searches for exact transaction ID "Tx_id: 000004"
- **Log Group Targeting**: Focuses on the "rebooking_log" log group
- **Time Range Filtering**: Searches within a specific date range (June 15-17, 2025)
- **Fallback Behavior**: Shows the CloudWatch query if no results are found
- **Structured Output**: Returns results in a clean JSON format with timestamp and message

**Additional Query Variations:**
- "Find messages with Tx_id 00002 within log group names having 'rebooking' in the us-west-2 region"
- "Search for all transactions between June 1, 2025 and June 30, 2025 in rebooking_log"
- "Show me the CloudWatch Insights query for finding error messages in the last 24 hours"

## Architecture

The application consists of several key components:

1. **Streamlit Frontend**: Provides the web interface
2. **MCP Client**: Handles communication with the CloudWatch Logs MCP server
3. **Strands Agent**: Processes natural language queries using AI
4. **AWS Integration**: Direct connection to CloudWatch Logs service

## Key Functions

- `initialize_aws_client()`: Sets up AWS session and verifies credentials
- `initialize_mcp_client()`: Initializes the MCP client for CloudWatch Logs
- `extract_last_assistant_content()`: Extracts AI response content
- `extract_json_from_text()`: Parses JSON data from AI responses
- `display_query_results()`: Formats and displays query results
- `list_log_groups()`: Retrieves available CloudWatch log groups

## Troubleshooting

### Common Issues

1. **AWS Credentials Error**: Ensure your AWS profile is properly configured
2. **MCP Server Not Found**: Install the CloudWatch Logs MCP server using `uvx`
3. **Permission Denied**: Verify your AWS IAM permissions for CloudWatch Logs
4. **Region Issues**: Check that your AWS region is correctly set

### Logging

The application includes comprehensive logging. Check the console output for detailed error messages and debugging information.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- AWS Labs for the CloudWatch Logs MCP server
- Streamlit team for the excellent web framework
- Model Context Protocol (MCP) community

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review AWS CloudWatch Logs documentation
3. Open an issue in this repository

---

**Note**: This tool is designed for development and analysis purposes. Always follow your organization's security and compliance guidelines when accessing production logs.
