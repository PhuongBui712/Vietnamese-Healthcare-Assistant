import ast
import json
from typing import Literal


def parse_llm_json_output(raw_output: str, *, bracket_type: Literal["curly", "square"]) -> dict:
    start_idx = raw_output.find("{" if bracket_type == "curly" else "[")
    end_idx = raw_output.rfind("}" if bracket_type == "curly" else "]") + 1

    try:
        res = json.loads(raw_output[start_idx:end_idx])
    except Exception as e:
        res = ast.literal_eval(raw_output[start_idx:end_idx])

    return res