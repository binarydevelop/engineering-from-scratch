"""
Instruction & Chat Formatting Engine (Phase 86).
Applies and validates chat templates:
1. ChatML standard (<|im_start|>role\ncontent<|im_end|>)
2. Llama-3 style (<|start_header_id|>role<|end_header_id|>\ncontent<|eot_id|>)
3. Plain Instruction style (### Instruction:\n... ### Response:)
Demonstrates how prompt formatting mismatch destroys fine-tuned model accuracy.
"""

from typing import List, Dict

class ChatFormatter:
    @staticmethod
    def format_chatml(messages: List[Dict[str, str]]) -> str:
        """Standard ChatML formatting used by Qwen, Yi, and OpenAI fine-tuning."""
        formatted = []
        for m in messages:
            role = m["role"]
            content = m["content"]
            formatted.append(f"<|im_start|>{role}\n{content}<|im_end|>")
        return "\n".join(formatted) + "\n<|im_start|>assistant\n"

    @staticmethod
    def format_llama3(messages: List[Dict[str, str]]) -> str:
        """Llama-3 special header format."""
        formatted = ["<|begin_of_text|>"]
        for m in messages:
            role = m["role"]
            content = m["content"]
            formatted.append(f"<|start_header_id|>{role}<|end_header_id|>\n\n{content}<|eot_id|>")
        formatted.append("<|start_header_id|>assistant<|end_header_id|>\n\n")
        return "".join(formatted)

    @staticmethod
    def format_alpaca(instruction: str, input_text: str = "") -> str:
        if input_text:
            return f"### Instruction:\n{instruction}\n\n### Input:\n{input_text}\n\n### Response:\n"
        return f"### Instruction:\n{instruction}\n\n### Response:\n"
