# Google ADK AI Agent

A basic AI agent built with Google's Agent Development Kit (ADK) that can chat, perform calculations, and tell the time.

## Features

- 🤖 Conversational AI powered by Gemini 2.0
- 🧮 Calculator tool for math operations
- ⏰ Time retrieval tool
- 💬 Maintains conversation context
- 🛠️ Extensible tool system

## Setup

### 1. Get Your Google API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Copy the key

### 2. Configure Environment

1. Open the `.env` file
2. Replace `your_api_key_here` with your actual API key:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

Run the agent:

```bash
python agent.py
```

### Example Interactions

```
You: What's 15 multiplied by 8?
Agent: The result of 15 multiplied by 8 is 120.

You: What time is it?
Agent: The current time is 2026-01-21 14:30:45.

You: Tell me a joke
Agent: Why did the programmer quit his job? Because he didn't get arrays! 😄
```

Type `quit`, `exit`, or `bye` to end the conversation.

## Adding Custom Tools

To add new tools to your agent:

1. Define a function with type hints and a docstring:
   ```python
   def my_tool(param: str) -> str:
       """
       Description of what the tool does.
       
       Args:
           param: Parameter description
       
       Returns:
           Return value description
       """
       # Your implementation
       return result
   ```

2. Add it to the `tools` list in `agent_config`:
   ```python
   'tools': [calculator, get_current_time, my_tool],
   ```

## Customization

- **Model**: Change `gemini-2.0-flash-exp` to other Gemini models
- **System Instructions**: Modify the agent's behavior and personality
- **Tools**: Add or remove tools based on your needs

## Troubleshooting

- **API Key Error**: Make sure your `.env` file has the correct API key
- **Import Error**: Run `pip install -r requirements.txt` to install dependencies
- **Connection Error**: Check your internet connection

## License

MIT
