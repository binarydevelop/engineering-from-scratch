"""
Structured Output Extraction & Schema Repair (Phase 123).
Extracts, validates, and repairs structured JSON responses using Pydantic.
If JSON is malformed or invalid, constructs targeted error feedback prompts
for automated schema repair.
"""

from typing import Dict, Any, Type, Optional, Tuple
import json
import re
from pydantic import BaseModel, ValidationError

class ToolCallRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]

def extract_json_block(text: str) -> Optional[str]:
    """Extracts JSON substring from markdown code fences or raw curly braces."""
    # Match ```json ... ```
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        return match.group(1).strip()
    
    # Match raw JSON object { ... }
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        return match.group(0).strip()
    return None

def parse_and_validate(text: str, schema: Type[BaseModel]) -> Tuple[Optional[BaseModel], Optional[str]]:
    raw_json = extract_json_block(text)
    if not raw_json:
        return None, "No JSON object found in model output"
    try:
        data = json.loads(raw_json)
        validated = schema.model_validate(data)
        return validated, None
    except json.JSONDecodeError as e:
        return None, f"JSON Syntax Error: {str(e)}"
    except ValidationError as e:
        return None, f"Schema Validation Error: {str(e)}"
