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

- "Find messages with Tx_id 00002 within log group names having 'rebooking' in the us-west-2 region"
- "Show error messages from the last hour"
- "Find all logs containing 'exception' or 'error'"
- "Get recent logs from application servers"

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
