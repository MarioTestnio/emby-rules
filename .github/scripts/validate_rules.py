#!/usr/bin/env python3
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("missing dependency: pyyaml")
    sys.exit(1)

RULE_TYPES = {"DOMAIN", "DOMAIN-KEYWORD", "DOMAIN-SUFFIX", "IP-CIDR", "PROCESS-NAME"}
ERRORS = []


def _normalize_rule_type(rule_type: str) -> str:
    return rule_type.strip().upper()


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
        item = item.strip()
        if not item:
            ERRORS.append(f"{path}: payload[{idx}] empty line")
            continue
        if item.startswith('#'):
            continue
        if ',' in item:
            rule_type, rest = item.split(',', 1)
            rule_type = _normalize_rule_type(rule_type)
            if rule_type not in RULE_TYPES:
                ERRORS.append(f"{path}: payload[{idx}] unknown rule type: {item}")
                continue
            value = rest.split(',', 1)[0].strip()
        else:
            rule_type = 'DOMAIN'
            value = item
        if not value:
            ERRORS.append(f"{path}: payload[{idx}] empty value: {item}")
            continue
        key = (rule_type, value)
        if key in seen:
            ERRORS.append(f"{path}: payload[{idx}] duplicate domain value: {value}")
        seen.add(key)


def check_list_file(path: Path):
    seen = set()
    for lineno, raw in enumerate(path.read_text(encoding='utf-8').splitlines(), start=1):
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if ',' in line:
            rule_type, rest = line.split(',', 1)
            rule_type = _normalize_rule_type(rule_type)
            if rule_type not in RULE_TYPES:
                ERRORS.append(f"{path}:{lineno}: unknown rule type: {line}")
            value = rest.split(',', 1)[0].strip()
        else:
            rule_type = 'DOMAIN'
            value = line
        if not value:
            ERRORS.append(f"{path}:{lineno}: empty value for rule: {line}")
            continue
        key = (rule_type, value)
        if key in seen:
            ERRORS.append(f"{path}:{lineno}: duplicate domain value: {value}")
        seen.add(key)


def check_json_file(path: Path):
    text = path.read_text(encoding='utf-8')
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        ERRORS.append(f"{path}: invalid json: {e}")
        return
    if not isinstance(data, dict):
        ERRORS.append(f"{path}: root is not a json object")
        return
    if data.get('version') not in (2, 3, 4, 5):
        ERRORS.append(f"{path}: missing or invalid version")
    rules = data.get('rules')
    if not isinstance(rules, list):
        ERRORS.append(f"{path}: rules is not a list")
        return
    seen = set()
    for idx, item in enumerate(rules, start=1):
        if not isinstance(item, dict):
            ERRORS.append(f"{path}: rules[{idx}] is not an object")
            continue
        domain_items = []
        if 'domain_suffix' in item:
            domain_items = item['domain_suffix']
        elif 'domain_keyword' in item:
            domain_items = item['domain_keyword']
        elif 'domain' in item:
            domain_items = item['domain']
        elif 'domain_regex' in item:
            domain_items = item['domain_regex']
        else:
            ERRORS.append(f"{path}: rules[{idx}] missing supported domain field")
            continue
        if not isinstance(domain_items, list):
            ERRORS.append(f"{path}: rules[{idx}] domain field is not a list")
            continue
        for value in domain_items:
            if not isinstance(value, str) or not value.strip():
                ERRORS.append(f"{path}: rules[{idx}] empty domain value")
                continue
            key = (item.get('domain_suffix') and 'DOMAIN-SUFFIX' or item.get('domain_keyword') and 'DOMAIN-KEYWORD' or 'DOMAIN', value)
            if key in seen:
                ERRORS.append(f"{path}: rules[{idx}] duplicate domain value: {value}")
            seen.add(key)


def main():
    root = Path(__file__).resolve().parent.parent.parent
    files = [
        (root / 'clash' / 'emby.yaml', 'yaml'),
        (root / 'surge' / 'emby.list', 'list'),
        (root / 'mihomo' / 'emby.yaml', 'yaml'),
        (root / 'mihomo' / 'personal-direct.yaml', 'yaml'),
        (root / 'clash' / 'personal-direct.yaml', 'yaml'),
        (root / 'egern' / 'emby.json', 'json'),
        (root / 'egern' / 'personal-direct.json', 'json'),
        (root / 'surge' / 'personal-direct.list', 'list'),
    ]
    for path, kind in files:
        if not path.exists():
            ERRORS.append(f"missing file: {path}")
            continue
        if kind == 'yaml':
            check_yaml_file(path)
        elif kind == 'list':
            check_list_file(path)
        elif kind == 'json':
            check_json_file(path)
        else:
            ERRORS.append(f"unsupported file kind: {path} ({kind})")

    if ERRORS:
        print("Validation failed:")
        for err in ERRORS:
            print(f"- {err}")
        sys.exit(1)
    print("Validation passed.")


if __name__ == '__main__':
    main()
