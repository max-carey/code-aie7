# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Setup and Installation
```bash
# Quick setup (installs uv, dependencies, creates .env)
./quickstart.sh

# Manual dependency management
uv sync                    # Install dependencies
uv add <package>          # Add new dependency
```

### Running the Application
```bash
# Start A2A server (main application)
uv run python -m app

# Start with custom host/port
uv run python -m app --host 0.0.0.0 --port 8181

# Test the agent API
uv run python app/test_client.py

# Start LangGraph development server
uv run langgraph dev      # Available at http://localhost:2024
```

### Environment Validation
```bash
# Check environment configuration
uv run python check_env.py

# Test tool availability
uv run python -c "from app.tools import get_tool_belt; print([tool.name for tool in get_tool_belt()])"

# Test RAG loading
uv run python -c "from app.rag import get_rag_graph; rag = get_rag_graph(); print('RAG loaded successfully')"
```

## Architecture Overview

This codebase implements an **A2A (Agent-to-Agent) Protocol** compatible LangGraph agent with intelligent helpfulness evaluation. The core innovation is a post-response evaluation loop that determines if responses are helpful and iterates if needed.

### Core Components

**LangGraph Architecture** (`app/agent_graph_with_helpfulness.py`):
- `agent` node: Main LLM with tools (Tavily, ArXiv, RAG)
- `action` node: Tool execution (web search, academic papers, documents)  
- `helpfulness` node: A2A evaluation of response quality
- Evaluation loop: Continues if unhelpful, terminates after 10 iterations

**Agent Implementation** (`app/agent.py`):
- `ResponseFormat`: Pydantic model with status (`input_required`, `completed`, `error`)
- OpenAI model integration with streaming capabilities
- System instructions for tool usage and response formatting

**A2A Server** (`app/__main__.py`):
- FastAPI server with A2A protocol compliance
- AgentCard definition with capabilities and skills
- Push notification and task management support

**Tool Belt** (`app/tools.py`):
- Tavily Search (web search, max 5 results)
- ArXiv Query (academic papers)
- RAG retrieval (document search from `data/` directory)

**RAG System** (`app/rag.py`):
- Recursive PDF loading from `RAG_DATA_DIR`
- Token-aware chunking using tiktoken (1000 tokens, 100 overlap)
- Qdrant in-memory vector store with OpenAI embeddings
- Two-node LangGraph: retrieve → generate

### Key Technical Details

**Helpfulness Evaluation**: Uses a secondary LLM call to evaluate if responses are "extremely helpful" based on accuracy, completeness, and tool usage. Returns 'Y' (helpful) or 'N' (continue loop).

**State Management**: `AgentState` TypedDict with message history and structured response tracking.

**Loop Protection**: Hard limit of 10 message iterations prevents infinite loops.

**Token Management**: Uses tiktoken for accurate chunking, ensuring compatibility with OpenAI model token limits.

## Required Environment Variables

Create `.env` file with:
```bash
# Required
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key

# Optional (with defaults)
TOOL_LLM_NAME=gpt-4o-mini
TOOL_LLM_URL=https://api.openai.com/v1
RAG_DATA_DIR=data
OPENAI_CHAT_MODEL=gpt-4o-mini
```

## Common Development Patterns

**Adding New Tools**: Modify `app/tools.py` `get_tool_belt()` function to include new LangChain tools.

**Customizing Evaluation**: Modify the prompt template in `helpfulness_node()` to change evaluation criteria.

**RAG Document Types**: Extend `app/rag.py` to support additional document formats beyond PDF.

**Response Formats**: Modify `ResponseFormat` in `app/agent.py` for different structured outputs.

## Testing and Debugging

**API Testing**: Use `app/test_client.py` for interactive testing or curl commands against `http://localhost:2024/v1/tasks`.

**Tool Testing**: Each tool (Tavily, ArXiv, RAG) can be tested independently by checking API keys and data availability.

**Debug Mode**: Set `LANGCHAIN_VERBOSE=true` for detailed operation logging.

**Common Issues**: 
- Internal Error (-32603): Check model names and API keys
- Tool failures: Verify API keys for external services
- RAG errors: Ensure PDFs exist in `data/` directory