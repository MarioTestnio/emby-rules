#!/usr/bin/env python3
import re
import sys
from pathlib import Path

RULE_TYPES = {"DOMAIN", "DOMAIN-KEYWORD", "DOMAIN-SUFFIX", "IP-CIDR", "PROCESS-NAME"}
ERRORS = []

def check_yaml_text(text: str, path: Path):
    if 'payload:' not in text:
        ERRORS.append(f"{path}: missing payload section")

def check_list_text(text: str, path: Path):
    seen = set()
    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if 'DOMAIN-KEYWORD' in line:
            continue
        if ',' not in line:
            ERRORS.append(f"{path}:{lineno}: missing comma in line: {raw}")
            continue
        rule_type, rest = line.split(',', 1)
        rule_type = rule_type.strip()
        if rule_type not in RULE_TYPES:
            ERRORS.append(f"{path}:{lineno}: unknown rule type: {rule_type}")
        if ',' not in rest:
            ERRORS.append(f"{path}:{lineno}: missing value after rule type: {raw}")
            continue
        value = rest.split(',', 1)[0].strip()
        if not value:
            ERRORS.append(f"{path}:{lineno}: empty value for rule: {raw}")
        else:
            key = (rule_type, value)
            if rule_type in {'DOMAIN-KEYWORD', 'DOMAIN-SUFFIX'} and value in seen:
                ERRORS.append(f"{path}:{lineno}: duplicate domain value: {value}")
            seen.add(key)

def main():
    root = Path(__file__).resolve().parent.parent
    files = [
        root / 'clash' / 'emby.yaml',
        root / 'surge' / 'emby.list',
        root / 'egern' / 'emby.yaml',
    ]
    for path in files:
        if not path.exists():
            ERRORS.append(f"missing file: {path}")
            continue
        text = path.read_text(encoding='utf-8')
        if path.suffix == '.yaml':
            check_yaml_text(text, path)
        else:
            check_list_text(text, path)
        check_list_text(text, path)

    if ERRORS:
        print("Validation failed:")
        for err in ERRORS:
            print(f"- {err}")
        sys.exit(1)
    print("Validation passed.")

if __name__ == '__main__':
    main()
