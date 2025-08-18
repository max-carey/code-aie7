import logging
import re
import time
from datetime import datetime
from typing import Dict, Any

logger = logging.getLogger(__name__)

class LocalCapabilities:
    """Local processing capabilities for the client agent"""
    
    @staticmethod
    def hello_world() -> str:
        """Generate a friendly hello world message with timestamp"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"Hello World! 👋\n\nThis response was generated locally by the Client Agent.\nCurrent time: {current_time}\n\nThe Client Agent specializes in simple, local processing tasks while delegating complex queries to the Parent Agent via the A2A protocol."
    
    @staticmethod
    def basic_math(expression: str) -> str:
        """Perform basic mathematical calculations"""
        try:
            # Extract mathematical expression from the query
            # Look for patterns like "5 + 3", "15 * 7", etc.
            math_pattern = r'(\d+(?:\.\d+)?)\s*([+\-*/])\s*(\d+(?:\.\d+)?)'
            match = re.search(math_pattern, expression)
            
            if match:
                num1, operator, num2 = match.groups()
                num1, num2 = float(num1), float(num2)
                
                if operator == '+':
                    result = num1 + num2
                elif operator == '-':
                    result = num1 - num2
                elif operator == '*':
                    result = num1 * num2
                elif operator == '/':
                    if num2 == 0:
                        return "Error: Division by zero is not allowed."
                    result = num1 / num2
                
                # Format result nicely
                if result == int(result):
                    result = int(result)
                
                return f"🧮 Mathematical Calculation (Local Processing)\n\n{num1} {operator} {num2} = {result}\n\nThis calculation was performed locally by the Client Agent."
            else:
                # Try to evaluate simple expressions safely
                # Remove any non-mathematical characters for safety
                clean_expr = re.sub(r'[^0-9+\-*/.() ]', '', expression)
                if clean_expr:
                    try:
                        result = eval(clean_expr)
                        if isinstance(result, (int, float)):
                            if result == int(result):
                                result = int(result)
                            return f"🧮 Mathematical Calculation (Local Processing)\n\n{clean_expr} = {result}\n\nThis calculation was performed locally by the Client Agent."
                    except:
                        pass
                
                return "I can help with basic math! Try asking something like:\n• What is 5 + 3?\n• Calculate 15 * 7\n• What's 100 / 4?"
                
        except Exception as e:
            logger.error(f"Error in basic math calculation: {e}")
            return f"Error performing calculation: {str(e)}"
    
    @staticmethod
    def text_processing(text: str, operation: str = "analyze") -> str:
        """Perform basic text processing operations"""
        try:
            if "uppercase" in operation.lower() or "upper" in operation.lower():
                processed = text.upper()
                return f"📝 Text Processing (Local)\n\nOriginal: {text}\nUppercase: {processed}\n\nProcessed locally by the Client Agent."
            
            elif "lowercase" in operation.lower() or "lower" in operation.lower():
                processed = text.lower()
                return f"📝 Text Processing (Local)\n\nOriginal: {text}\nLowercase: {processed}\n\nProcessed locally by the Client Agent."
            
            elif "count" in operation.lower() or "words" in operation.lower():
                word_count = len(text.split())
                char_count = len(text)
                return f"📝 Text Analysis (Local)\n\nText: {text}\nWord count: {word_count}\nCharacter count: {char_count}\n\nAnalyzed locally by the Client Agent."
            
            elif "reverse" in operation.lower():
                reversed_text = text[::-1]
                return f"📝 Text Processing (Local)\n\nOriginal: {text}\nReversed: {reversed_text}\n\nProcessed locally by the Client Agent."
            
            else:
                # Default analysis
                word_count = len(text.split())
                char_count = len(text)
                return f"📝 Text Analysis (Local)\n\nText: {text}\nWord count: {word_count}\nCharacter count: {char_count}\n\nAvailable operations: uppercase, lowercase, count words, reverse\nProcessed locally by the Client Agent."
                
        except Exception as e:
            logger.error(f"Error in text processing: {e}")
            return f"Error processing text: {str(e)}"
    
    @staticmethod
    def timestamp_operations() -> str:
        """Generate various timestamp formats"""
        now = datetime.now()
        return f"""⏰ Timestamp Operations (Local Processing)

Current Date & Time Information:
• Standard: {now.strftime("%Y-%m-%d %H:%M:%S")}
• ISO Format: {now.isoformat()}
• Readable: {now.strftime("%A, %B %d, %Y at %I:%M %p")}
• Unix Timestamp: {int(now.timestamp())}

Generated locally by the Client Agent."""
    
    @staticmethod
    def system_info() -> str:
        """Provide local system information"""
        return f"""💻 Client Agent System Information

• Agent Type: Local Client Agent
• Specialization: Simple processing, A2A routing
• Capabilities: Math, text processing, timestamps, greetings
• Communication: A2A Protocol integration
• Status: Active and ready
• Local Processing: ✅ Available
• Parent Agent Connection: ✅ Connected via A2A

This agent demonstrates the A2A protocol by handling simple tasks locally while routing complex queries to specialized agents."""

def determine_local_capability(query: str) -> str:
    """Determine which local capability to use based on the query"""
    query_lower = query.lower()
    
    # Math detection
    if any(op in query_lower for op in ['+', '-', '*', '/', 'calculate', 'math', 'multiply', 'divide', 'add', 'subtract']):
        return "math"
    
    # Text processing detection
    if any(word in query_lower for word in ['uppercase', 'lowercase', 'count', 'words', 'reverse', 'text']):
        return "text_processing"
    
    # Timestamp detection
    if any(word in query_lower for word in ['time', 'date', 'timestamp', 'clock', 'when']):
        return "timestamp"
    
    # Hello/greeting detection
    if any(word in query_lower for word in ['hello', 'hi', 'greeting', 'say hello']):
        return "hello_world"
    
    # System info detection
    if any(word in query_lower for word in ['info', 'status', 'system', 'about', 'capabilities']):
        return "system_info"
    
    return None

def process_locally(query: str) -> Dict[str, Any]:
    """Process a query using local capabilities"""
    start_time = time.time()
    
    capability = determine_local_capability(query)
    local_caps = LocalCapabilities()
    
    try:
        if capability == "hello_world":
            response = local_caps.hello_world()
        elif capability == "math":
            response = local_caps.basic_math(query)
        elif capability == "text_processing":
            response = local_caps.text_processing(query, query)
        elif capability == "timestamp":
            response = local_caps.timestamp_operations()
        elif capability == "system_info":
            response = local_caps.system_info()
        else:
            response = f"🤖 Client Agent Response\n\nI can help with:\n• Simple math calculations\n• Text processing (uppercase, lowercase, word count)\n• Current time and timestamps\n• Hello world greetings\n• System information\n\nFor complex tasks like research, web search, or document analysis, I'll route your request to the Parent Agent via A2A protocol.\n\nYour query: \"{query}\""
        
        execution_time = int((time.time() - start_time) * 1000)
        
        return {
            "response": response,
            "agent_source": "client",
            "execution_time": execution_time,
            "capability_used": capability or "general_response"
        }
        
    except Exception as e:
        logger.error(f"Error in local processing: {e}")
        return {
            "response": f"Error processing locally: {str(e)}",
            "agent_source": "client",
            "execution_time": int((time.time() - start_time) * 1000),
            "capability_used": "error"
        }