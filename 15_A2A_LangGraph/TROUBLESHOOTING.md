# A2A Protocol Troubleshooting Guide

Comprehensive troubleshooting guide for the A2A Protocol demonstration with three-component architecture.

## 🚨 Quick Diagnosis

### Check All Services Status

```bash
# 1. Check Parent Agent (Port 8181)
curl http://localhost:8181/.well-known/agent-card.json

# 2. Check Client Backend (Port 8000)  
curl http://localhost:8000/health

# 3. Check Frontend (Port 5173)
curl http://localhost:5173/

# 4. Check processes are running
ps aux | grep -E "(python.*app|python.*run.py|npm.*dev)" | grep -v grep
```

Expected responses:
- ✅ Parent Agent: JSON agent card with skills
- ✅ Client Backend: `{"status": "healthy", "service": "a2a-client-backend"}`
- ✅ Frontend: HTML content or redirect to Vite dev server

## 🔧 Common Issues & Solutions

### 1. Parent Agent Connection Issues

**🚨 Problem**: Client backend fails to connect to parent agent
```
ERROR: HTTP Error 503: Network communication error fetching agent card
ERROR: Failed to initialize A2A integration
```

**✅ Solutions**:

**Check if parent agent is running:**
```bash
curl http://localhost:8181/.well-known/agent-card.json
```

**Start parent agent if missing:**
```bash
# In main project directory
uv run python -m app --host 0.0.0.0 --port 8181
```

**Check environment variables:**
```bash
echo $OPENAI_API_KEY
echo $TAVILY_API_KEY

# If missing, create .env file:
cat > .env << EOF
OPENAI_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
EOF
```

**Verify API keys work:**
```bash
# Test OpenAI API
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models | jq '.data[0].id'

# Should return a model name like "gpt-4o-mini"
```

### 2. Port Conflicts

**🚨 Problem**: "Address already in use" errors
```
ERROR: [Errno 48] Address already in use
```

**✅ Solutions**:

**Check what's using the ports:**
```bash
lsof -i :8181  # Parent agent
lsof -i :8000  # Client backend  
lsof -i :5173  # Frontend
```

**Kill conflicting processes:**
```bash
# Kill specific processes
pkill -f "python.*app"        # Parent agent
pkill -f "python.*run.py"     # Client backend
pkill -f "npm.*dev"           # Frontend

# Or kill all Python processes (nuclear option)
pkill -f python
```

**Start services in correct order:**
```bash
# 1. Parent agent first
uv run python -m app --host 0.0.0.0 --port 8181 &

# 2. Wait for parent to start, then client backend
sleep 3
cd client_backend && uv run python run.py &

# 3. Start frontend
cd ../client && npm run dev
```

### 3. Client Backend Startup Failures

**🚨 Problem**: Client backend crashes on startup
```
ERROR: Application startup failed. Exiting.
```

**✅ Solutions**:

**Check dependencies:**
```bash
cd client_backend
uv sync  # Install missing dependencies
```

**Check Python version:**
```bash
python --version  # Should be 3.12+
uv --version      # Should be latest
```

**Manual startup with detailed logs:**
```bash
cd client_backend
uv run python -c "import a2a_client_backend.main; print('Import successful')"
uv run python run.py  # Run without background to see full errors
```

**Common fixes:**
```bash
# Reset virtual environment
rm -rf .venv
uv sync

# Check for missing environment variables
ls .env  # Should exist
cat .env  # Should have required keys
```

### 4. Frontend Build/Start Issues

**🚨 Problem**: Frontend fails to start or build
```
ERROR: Cannot resolve dependency
ERROR: Module not found
```

**✅ Solutions**:

**Clean install:**
```bash
cd client
rm -rf node_modules package-lock.json
npm install
```

**Check Node version:**
```bash
node --version  # Should be 18+
npm --version   # Should be latest
```

**Alternative package managers:**
```bash
# Try with yarn if npm fails
yarn install
yarn dev

# Or with pnpm
pnpm install  
pnpm dev
```

**Port conflicts:**
```bash
# Use different port if 5173 is busy
npm run dev -- --port 3000
```

### 5. A2A Communication Failures

**🚨 Problem**: Routing works but A2A calls fail
```
ERROR: A2A delegation failed
WARNING: A2A Communication Failed - Processed Locally
```

**✅ Solutions**:

**Check parent agent logs:**
```bash
# Look for errors in parent agent terminal
# Common issues: API key problems, tool failures
```

**Test parent agent directly:**
```bash
# Test with curl
curl -X POST http://localhost:8181/ \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "task.submit", 
    "params": {
      "message": {
        "role": "user",
        "parts": [{"kind": "text", "text": "Hello"}]
      }
    },
    "id": "test"
  }'
```

**Check network connectivity:**
```bash
# Test if services can reach each other
curl http://localhost:8181/  # From client backend host
telnet localhost 8181        # Test port connectivity
```

**Enable debug logging:**
```bash
export LANGCHAIN_VERBOSE=true
uv run python run.py  # Client backend with verbose logs
```

### 6. Response Formatting Issues

**🚨 Problem**: Raw JSON shown instead of clean text
```
"Unexpected response format: {'id': '123', 'jsonrpc': '2.0'...}"
```

**✅ Solutions**:

**Check A2A integration code:**
```python
# In a2a_integration.py, verify _extract_response_content method
# Should handle artifacts, message parts, and history properly
```

**Test response parsing:**
```bash
# Check if parent agent returns expected format
curl -X POST http://localhost:8181/ ... | jq '.result.artifacts[0].parts[0].text'
```

**Restart with latest code:**
```bash
cd client_backend
pkill -f "run.py"
uv run python run.py &
```

### 7. Routing Decision Issues

**🚨 Problem**: Queries routed to wrong agent
```
Simple math going to parent agent (slow)
Research queries staying local (no results)
```

**✅ Solutions**:

**Test routing logic:**
```bash
# Test routing decisions without execution
curl -X POST http://localhost:8000/routing-decision \
  -H "Content-Type: application/json" \
  -d '{"query": "What is 5 + 3?"}'  # Should route to client

curl -X POST http://localhost:8000/routing-decision \
  -H "Content-Type: application/json" \
  -d '{"query": "Find AI papers"}'  # Should route to parent
```

**Check capability detection:**
```python
# In local_capabilities.py
# Verify determine_local_capability function logic
# Add debug prints to see what's being detected
```

**Update routing indicators:**
```python
# In graph.py, modify complex_indicators list
complex_indicators = [
    'research', 'papers', 'arxiv', 'search', 'web', 'internet',
    'latest', 'recent', 'news', 'find', 'analyze documents'
]
```

## 🔍 Debug Mode & Logging

### Enable Comprehensive Logging

**Environment variables:**
```bash
export LANGCHAIN_VERBOSE=true
export PYTHONPATH="${PYTHONPATH}:."
export LOG_LEVEL=DEBUG
```

**Client backend debug mode:**
```python
# In main.py, add detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

**Parent agent debug mode:**
```bash
# Start with debug logging
uv run python -m app --host 0.0.0.0 --port 8181 --log-level debug
```

### Log Analysis

**Key log messages to look for:**

✅ **Successful startup:**
```
INFO:a2a_client_backend.main:A2A Client Backend initialized successfully
INFO:a2a_client_backend.a2a_integration:Successfully connected to parent agent
```

✅ **Successful routing:**
```
INFO:a2a_client_backend.graph:Delegating to parent agent via A2A
INFO:a2a_client_backend.a2a_integration:Received response from parent agent
```

❌ **Connection problems:**
```
ERROR:a2a_client_backend.a2a_integration:Failed to initialize A2A integration
ERROR:httpx:HTTP Request failed
```

❌ **API key issues:**
```
ERROR:openai:Authentication failed
ERROR:tavily:Invalid API key
```

## 🚀 Performance Optimization

### Speed Up Development

**Use smaller models:**
```bash
export TOOL_LLM_NAME=gpt-4o-mini
export OPENAI_CHAT_MODEL=gpt-4o-mini
```

**Reduce search results:**
```python
# In app/tools.py
tavily_tool = TavilySearchResults(max_results=3)  # Down from 5
```

**Cache responses during development:**
```python
# Add simple caching to avoid repeated API calls
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_search(query):
    return actual_search(query)
```

### Production Readiness

**Use production models:**
```bash
export OPENAI_CHAT_MODEL=gpt-4o
export TOOL_LLM_NAME=gpt-4o
```

**Configure proper timeouts:**
```python
# In a2a_integration.py
httpx_client = httpx.AsyncClient(timeout=httpx.Timeout(120.0))  # 2 minutes
```

**Add retry logic:**
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
async def send_message_with_retry(self, message):
    return await self.send_message_to_parent(message)
```

## 🧪 Testing & Validation

### Manual Test Suite

**1. Basic connectivity:**
```bash
# All should return 200 OK
curl -I http://localhost:8181/.well-known/agent-card.json
curl -I http://localhost:8000/health
curl -I http://localhost:5173/
```

**2. Agent capabilities:**
```bash
curl http://localhost:8000/agent-cards | jq '.client.skills | length'  # Should be 4
curl http://localhost:8000/agent-cards | jq '.parent.skills | length'  # Should be 3
```

**3. Local processing:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is 15 * 7?"}' | jq '.agent_source'  # Should be "client"
```

**4. A2A processing:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Find recent papers on AI"}' | jq '.agent_source'  # Should be "parent"
```

**5. Response quality:**
```bash
# Should contain actual paper titles, not error messages
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Find recent papers on transformers"}' | jq -r '.content' | head -5
```

### Automated Health Checks

**Create health check script:**
```bash
#!/bin/bash
# health_check.sh

echo "🔍 Checking A2A Protocol Demo Health..."

# Check services
curl -sf http://localhost:8181/.well-known/agent-card.json > /dev/null && echo "✅ Parent Agent: OK" || echo "❌ Parent Agent: FAIL"
curl -sf http://localhost:8000/health > /dev/null && echo "✅ Client Backend: OK" || echo "❌ Client Backend: FAIL"  
curl -sf http://localhost:5173/ > /dev/null && echo "✅ Frontend: OK" || echo "❌ Frontend: FAIL"

# Test routing
LOCAL_RESULT=$(curl -s -X POST http://localhost:8000/routing-decision -H "Content-Type: application/json" -d '{"query": "What is 5+3?"}' | jq -r '.route_to')
A2A_RESULT=$(curl -s -X POST http://localhost:8000/routing-decision -H "Content-Type: application/json" -d '{"query": "Find AI papers"}' | jq -r '.route_to')

[[ "$LOCAL_RESULT" == "client" ]] && echo "✅ Local Routing: OK" || echo "❌ Local Routing: FAIL ($LOCAL_RESULT)"
[[ "$A2A_RESULT" == "parent" ]] && echo "✅ A2A Routing: OK" || echo "❌ A2A Routing: FAIL ($A2A_RESULT)"

echo "🎉 Health check complete!"
```

**Run regularly:**
```bash
chmod +x health_check.sh
./health_check.sh
```

## 🆘 Emergency Recovery

### Complete Reset

If everything is broken and you need to start fresh:

```bash
# 1. Kill all processes
pkill -f python
pkill -f npm
pkill -f node

# 2. Clean all environments
cd client_backend && rm -rf .venv && uv sync
cd ../client && rm -rf node_modules && npm install

# 3. Verify environment
echo $OPENAI_API_KEY  # Must be set
echo $TAVILY_API_KEY  # Must be set

# 4. Start in correct order with delays
uv run python -m app --host 0.0.0.0 --port 8181 &
sleep 5
cd client_backend && uv run python run.py &
sleep 3  
cd ../client && npm run dev &

# 5. Wait and test
sleep 10
curl http://localhost:8000/health
```

### Contact & Support

If you're still having issues:

1. **Check the logs** in all three terminal windows
2. **Run the health check script** to identify specific problems
3. **Test each component individually** before testing integration
4. **Verify API keys** are valid and have sufficient credits
5. **Check network connectivity** between services

The A2A Protocol demo is designed to be resilient with graceful fallbacks, so most issues are related to environment setup rather than core functionality! 🚀