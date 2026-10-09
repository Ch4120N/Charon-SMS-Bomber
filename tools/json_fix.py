#!/usr/bin/env python3
"""
Reformat a JSON array of objects so that each object sits on a single line
while the array itself remains pretty-printed.
"""

import json
import sys
import os

def format_json_array(input_path: str, output_path: str) -> int:
    """
    Read a JSON array from `input_path`, reformat it, and write to `output_path`.

    Returns the number of objects processed.

    Raises:
        FileNotFoundError: if input_path does not exist.
        ValueError: if the input is not valid JSON or not an array of objects.
        IOError: for read/write failures.
    """

    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input file does not exist: {input_path}")

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in '{input_path}': {exc}") from exc
    except OSError as exc:
        raise IOError(f"Cannot read '{input_path}': {exc}") from exc

    if not isinstance(data, list):
        raise TypeError(
            f"Expected a JSON array at the top level, got {type(data).__name__}"
        )

    lines = []
    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            raise TypeError(
                f"Item at index {idx} is not a JSON object (dict), "
                f"got {type(item).__name__}"
            )
        # separators=(', ', ': ') gives spaces after commas and colons,
        # matching the style { "key": "value", ... }
        compact = json.dumps(item, ensure_ascii=False, separators=(", ", ": "))
        lines.append("    " + compact)          # 4-space indent for array items

    if lines:
        output = "[\n" + ",\n".join(lines) + "\n]\n"
    else:
        output = "[]\n"
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output)
    except OSError as exc:
        raise IOError(f"Cannot write to '{output_path}': {exc}") from exc

    return len(data)


def main() -> None:
    if len(sys.argv) != 3:
        prog = os.path.basename(sys.argv[0])
        print(f"Usage: {prog} <input.json> <output.json>", file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        count = format_json_array(input_file, output_file)
        print(f"Success: formatted {count} object(s) → '{output_file}'")
    except Exception as exc:
        # Catch everything and print a clean error message
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()