import json
import pandas as pd


def parse_response(raw: str) -> dict:
    result = {
        "visual_type": "Unknown",
        "data": {},
        "analysis": "",
        "parse_error": None
    }
    try:
        if "VISUAL_TYPE:" in raw:
            result["visual_type"] = raw.split("VISUAL_TYPE:")[1].split("DATA:")[0].strip()
        if "DATA:" in raw:
            raw_json = raw.split("DATA:")[1].split("ANALYSIS:")[0].strip()
            result["data"] = json.loads(raw_json)
        if "ANALYSIS:" in raw:
            result["analysis"] = raw.split("ANALYSIS:")[1].strip()
    except json.JSONDecodeError as e:
        result["parse_error"] = f"Could not parse data: {e}"
        result["data"] = {}
    except Exception as e:
        result["parse_error"] = f"Parsing error: {e}"
    return result


def to_dataframe(data: dict):
    try:
        if not data or "error" in data:
            return None
        if "rows" in data and "headers" in data:
            return pd.DataFrame(data["rows"], columns=data["headers"])
        if "labels" in data and "values" in data:
            series = data.get("series_name", "Value")
            return pd.DataFrame({"Label": data["labels"], series: data["values"]})
    except Exception:
        return None
    return None
