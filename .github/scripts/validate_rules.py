#!/usr/bin/env python3
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("missing dependency: pyyaml")
    sys.exit(1)

RULE_TYPES = {"DOMAIN", "DOMAIN-KEYWORD", "DOMAIN-SUFFIX", "IP-CIDR", "PROCESS-NAME"}
ERRORS = []


def check_yaml_file(path: Path):
    text = path.read_text(encoding='utf-8')
    if 'payload:' not in text:
        ERRORS.append(f"{path}: missing payload section")
        return
    data = yaml.safe_load(text)
    if not isinstance(data, dict) or 'payload' not in data:
        ERRORS.append(f"{path}: payload section is not a list")
        return
    payload = data['payload']
    if not isinstance(payload, list):
        ERRORS.append(f"{path}: payload section is not a list")
        return
    seen = set()
    for idx, item in enumerate(payload, start=1):
        if not isinstance(item, str):
            ERRORS.append(f"{path}: payload[{idx}] is not a string")
            continue
        if 'DOMAIN-KEYWORD' in item:
            continue
        if ',' not in item:
            ERRORS.append(f"{path}: payload[{idx}] missing comma: {item}")
            continue
        rule_type, rest = item.split(',', 1)
        rule_type = rule_type.strip()
        if rule_type not in RULE_TYPES:
            ERRORS.append(f"{path}: payload[{idx}] unknown rule type: {item}")
            continue
        if ',' not in rest:
            ERRORS.append(f"{path}: payload[{idx}] missing value: {item}")
            continue
        value = rest.split(',', 1)[0].strip()
        if not value:
            ERRORS.append(f"{path}: payload[{idx}] empty value: {item}")
            continue
        key = (rule_type, value)
        if rule_type in {'DOMAIN-KEYWORD', 'DOMAIN-SUFFIX'} and value in seen:
            ERRORS.append(f"{path}: payload[{idx}] duplicate domain value: {value}")
        seen.add(key)


def check_list_file(path: Path):
    seen = set()
    for lineno, raw in enumerate(path.read_text(encoding='utf-8').splitlines(), start=1):
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
            ERRORS.append(f"{path}:{lineno}: unknown rule type: {line}")
        if ',' not in rest:
            ERRORS.append(f"{path}:{lineno}: missing value after rule type: {line}")
            continue
        value = rest.split(',', 1)[0].strip()
        if not value:
            ERRORS.append(f"{path}:{lineno}: empty value for rule: {line}")
            continue
        key = (rule_type, value)
        if rule_type in {'DOMAIN-KEYWORD', 'DOMAIN-SUFFIX'} and value in seen:
            ERRORS.append(f"{path}:{lineno}: duplicate domain value: {value}")
        seen.add(key)


def main():
    root = Path(__file__).resolve().parent.parent.parent
    files = [
        (root / 'clash' / 'emby.yaml', 'yaml'),
        (root / 'surge' / 'emby.list', 'list'),
        (root / 'egern' / 'emby.yaml', 'yaml'),
        (root / 'mihomo' / 'emby.yaml', 'yaml'),
        (root / 'mihomo' / 'personal-direct.yaml', 'yaml'),
        (root / 'clash' / 'personal-direct.yaml', 'yaml'),
        (root / 'egern' / 'personal-direct.yaml', 'yaml'),
        (root / 'surge' / 'personal-direct.list', 'list'),
    ]
    for path, kind in files:
        if not path.exists():
            ERRORS.append(f"missing file: {path}")
            continue
        if kind == 'yaml':
            check_yaml_file(path)
        else:
            check_list_file(path)

    if ERRORS:
        print("Validation failed:")
        for err in ERRORS:
            print(f"- {err}")
        sys.exit(1)
    print("Validation passed.")


if __name__ == '__main__':
    main()
