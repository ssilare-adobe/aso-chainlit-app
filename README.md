# ASO Chainlit App - LangGraph ReAct Agent

A modern Python application that implements a ReAct (Reasoning and Acting) agent using **LangGraph** and **Chainlit**. This agent can reason through problems, use tools, and provide intelligent responses through both command-line and web interfaces.

## 🚀 Features

- **🔄 ReAct Agent**: Advanced reasoning and acting capabilities powered by LangGraph
- **🌐 Dual Interface**: Command-line (CLI) and modern web interface (Chainlit)
- **🤖 Azure OpenAI Integration**: Powered by GPT-4.1 through Azure OpenAI services
- **🛠️ Tool Integration**: Built-in tools for time retrieval and mathematical calculations
- **💾 Memory Management**: In-memory checkpointing for conversation continuity
- **⚡ Streaming Responses**: Real-time streaming of agent responses in the web interface
- **🔒 Safe Execution**: Secure mathematical expression evaluation

## 🏗️ Architecture

This application demonstrates a clean separation of concerns:

- **`agent/app.py`**: Core LangGraph agent logic with ReAct capabilities
- **`app/chainlit.py`**: Modern web interface using Chainlit
- **Modular Design**: Agent functions are imported and reused across interfaces

## 🛠️ Built-in Tools

### 1. Time Tool
- **Function**: `get_current_time()`
- **Description**: Retrieves the current date and time
- **Output Format**: YYYY-MM-DD HH:MM:SS

### 2. Calculator Tool
- **Function**: `calculate(expression: str)`
- **Description**: Safely evaluates mathematical expressions
- **Supported Operations**: Basic arithmetic, mathematical functions (abs, round, min, max, sum, pow, divmod)
- **Security**: Restricted to safe mathematical operations only

## 📋 Prerequisites

- Python 3.8 or higher
- Azure OpenAI account with GPT-4.1 deployment
- Valid Azure OpenAI API credentials

## 🔧 Installation

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd aso-chainlit-app
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   AZURE_OPENAI_API_KEY=your_azure_openai_api_key
   AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
   AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
   X_API_KEY=your_mcp_api_key  # Optional: for MCP server integration
   ```

## 🚀 Usage

### 🌐 Web Interface (Recommended)

1. **Start the Chainlit web interface**
   ```bash
   chainlit run app/chainlit.py
   ```

2. **Open your browser**
   - Navigate to the URL shown in the terminal (usually http://localhost:8000)
   - The agent will initialize automatically when you start a chat

3. **Interact with the agent**
   - Type your questions in the modern chat interface
   - Enjoy real-time streaming responses
   - All ReAct capabilities available through the web UI

### 💻 Command Line Interface

1. **Start the CLI application**
   ```bash
   python agent/app.py
   ```

2. **Interact with the agent**
   - Type your questions or requests
   - View reasoning steps and tool usage
   - See the final response

3. **Exit the application**
   - Type `quit`, `exit`, or `q`
   - Use `Ctrl+C` for keyboard interrupt

## 📁 Project Structure

```
aso-chainlit-app/
├── agent/
│   └── app.py         # Core LangGraph agent logic and CLI interface
├── app/
│   └── chainlit.py    # Modern Chainlit web interface
├── .chainlit/
│   └── config.toml    # Chainlit configuration
├── requirements.txt   # Python dependencies
├── .env              # Environment variables (create this)
├── .gitignore        # Git ignore file
├── venv/             # Virtual environment directory
└── README.md         # This file
```

## 🔌 Configuration

### Environment Variables

- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL
- `AZURE_OPENAI_DEPLOYMENT_NAME`: Your GPT-4.1 deployment name
- `X_API_KEY`: API key for MCP server integration (optional)

### Chainlit Configuration

The application includes a `.chainlit/config.toml` file for customizing the web interface appearance and behavior.

## 🧠 How It Works

### LangGraph + ReAct Architecture

1. **Agent Initialization**: LangGraph creates a ReAct agent with predefined tools
2. **User Input**: Queries are processed through either CLI or web interface
3. **Reasoning Phase**: The agent analyzes the query and determines which tools to use
4. **Action Phase**: Tools are executed with appropriate parameters
5. **Response Generation**: The agent provides a reasoned response with intermediate steps
6. **Memory Management**: Conversation state is maintained using in-memory checkpointing

### Chainlit Integration

- **Real-time Streaming**: Responses are streamed word-by-word for better UX
- **Session Management**: Agent state is maintained per chat session
- **Error Handling**: Graceful error handling with user-friendly messages
- **Modern UI**: Clean, responsive web interface

## 🛡️ Security Features

- **Safe Math Evaluation**: Mathematical expressions are restricted to safe operations only
- **Environment Variable Protection**: Sensitive credentials are stored in `.env` files
- **Input Validation**: User inputs are processed safely through the agent framework
- **API Key Security**: Credentials are never exposed in the code

## 📚 Key Dependencies

- **`langgraph`**: Graph-based workflow management for agent orchestration
- **`langgraph-prebuilt`**: Pre-built ReAct agent implementations
- **`chainlit`**: Modern web interface framework for AI applications
- **`langchain`**: Core LangChain functionality and tool integration
- **`azure-openai`**: Azure OpenAI integration for GPT-4.1
- **`python-dotenv`**: Environment variable management

## 🆘 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed and virtual environment is activated
2. **API Errors**: Verify your Azure OpenAI credentials and deployment name
3. **Environment Variables**: Check that your `.env` file is properly configured
4. **Port Conflicts**: If port 8000 is busy, Chainlit will automatically use the next available port

### Getting Help

If you encounter issues:
1. Check the error messages in the console
2. Verify your Azure OpenAI configuration
3. Ensure all dependencies are correctly installed
4. Check the Chainlit documentation for web interface issues

## 🔮 Future Enhancements

- **MCP Server Integration**: Enhanced tool integration through MCP servers
- **Conversation History**: Persistent conversation storage
- **Multi-user Support**: User authentication and session management
- **Advanced Tooling**: Integration with external APIs and services
- **Custom UI Themes**: Enhanced Chainlit interface customization

## 📞 Support

For support and questions, please open an issue in the repository or contact the development team.

---

**Note**: This application requires valid Azure OpenAI credentials to function. Make sure you have the necessary permissions and quota for your Azure OpenAI deployment.
