# ASO Chainlit App - LangGraph ReAct Agent

A Python application that implements a ReAct (Reasoning and Acting) agent using LangGraph and Azure OpenAI. This agent can reason through problems, use tools, and provide intelligent responses to user queries.

## 🚀 Features

- **ReAct Agent**: Implements reasoning and acting capabilities using LangGraph
- **Azure OpenAI Integration**: Powered by GPT-4.1 through Azure OpenAI services
- **Tool Integration**: Built-in tools for time retrieval and mathematical calculations
- **Interactive CLI**: Command-line interface for easy interaction with the agent
- **Memory Management**: In-memory checkpointing for conversation continuity
- **Safe Execution**: Secure mathematical expression evaluation

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
   Create a `.env` file in the project root with the following variables:
   ```env
   AZURE_OPENAI_API_KEY=your_azure_openai_api_key
   AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
   AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name
   ```

## 🚀 Usage

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Interact with the agent**
   - Type your questions or requests
   - The agent will reason through your query and use appropriate tools
   - View the reasoning steps and final response

3. **Exit the application**
   - Type `quit`, `exit`, or `q`
   - Use `Ctrl+C` for keyboard interrupt

## 📁 Project Structure

```
aso-chainlit-app/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (create this)
├── .gitignore         # Git ignore file
├── venv/              # Virtual environment directory
└── README.md          # This file
```

## 🔌 Configuration

The application uses the following environment variables:

- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL
- `AZURE_OPENAI_DEPLOYMENT_NAME`: Your GPT-4.1 deployment name
- `OPENAI_API_VERSION`: API version (set to "2024-02-01")

## 🧠 How It Works

1. **Initialization**: The app loads environment variables and initializes the Azure OpenAI model
2. **Agent Creation**: A ReAct agent is created with predefined tools
3. **User Interaction**: Users input queries through the CLI
4. **Reasoning**: The agent analyzes the query and determines which tools to use
5. **Execution**: Tools are executed with appropriate parameters
6. **Response**: The agent provides a reasoned response with intermediate steps

## 🛡️ Security Features

- **Safe Math Evaluation**: Mathematical expressions are restricted to safe operations only
- **Environment Variable Protection**: Sensitive credentials are stored in `.env` files
- **Input Validation**: User inputs are processed safely through the agent framework

## 📚 Dependencies

Key dependencies include:
- `langchain`: Core LangChain functionality
- `langgraph`: Graph-based workflow management
- `langgraph-prebuilt`: Pre-built agent implementations
- `azure-openai`: Azure OpenAI integration
- `python-dotenv`: Environment variable management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed and the virtual environment is activated
2. **API Errors**: Verify your Azure OpenAI credentials and deployment name
3. **Environment Variables**: Check that your `.env` file is properly configured

### Getting Help

If you encounter issues:
1. Check the error messages in the console
2. Verify your Azure OpenAI configuration
3. Ensure all dependencies are correctly installed

## 🔮 Future Enhancements

Potential improvements for future versions:
- Web-based interface using Streamlit or Chainlit
- Additional tool integrations
- Conversation history persistence
- Multi-user support
- Enhanced error handling and logging

## 📞 Support

For support and questions, please open an issue in the repository or contact the development team.

---

**Note**: This application requires valid Azure OpenAI credentials to function. Make sure you have the necessary permissions and quota for your Azure OpenAI deployment.
