# Emby 分流规则

基于 [justdoiting/emby-rules](https://github.com/justdoiting/emby-rules) 与 [MetaCubeX/meta-rules-dat](https://github.com/MetaCubeX/meta-rules-dat) 整理，适配 Clash / Mihomo / Surge / Egern。

## 文件结构

```
emby-rules/
├── clash/
│   ├── personal-direct.yaml   # Clash 格式：直连规则集
│   └── emby.yaml              # Clash 格式：Emby 代理规则集
├── mihomo/
│   ├── personal-direct.yaml   # Mihomo 格式：直连规则集
│   └── emby.yaml              # Mihomo 格式：Emby 代理规则集
├── surge/
│   ├── personal-direct.list   # Surge 格式：直连规则集
│   └── emby.list              # Surge 格式：Emby 代理规则集
├── egern/
│   ├── personal-direct.yaml   # Egern 格式：直连规则集
│   └── emby.yaml              # Egern 格式：Emby 代理规则集
└── README.md
```

## 规则组成

### PersonalDirect（直连规则集）
- OneSmartPro Emby 直连规则：`media.emby.pro`、`sfcj.org`、`emos.club` 等 8 条
- OneSmartPro 基础直连规则：`taotu.ink`、`vidhub`、`onedrive`、`microsoft.com` 等 12 条

### Emby（代理规则集）
- OneSmartPro Emby 策略组规则（非直连部分）
- MetaCubeX/meta-rules-dat `category-emby` 新增规则

## 使用方式

### Mihomo / Clash Party

```yaml
rule-providers:
  PersonalDirect:
    type: http
    url: https://cdn.jsdelivr.net/gh/MarioTestnio/emby-rules@main/mihomo/personal-direct.yaml
    interval: 86400
    path: ./ruleset/personal-direct.yaml

  Emby:
    type: http
    url: https://cdn.jsdelivr.net/gh/MarioTestnio/emby-rules@main/mihomo/emby.yaml
    interval: 86400
    path: ./ruleset/emby.yaml

rules:
  - RULE-SET,PersonalDirect,国内直连
  - RULE-SET,Emby,Emby
```

### Surge / Egern

```yaml
[Rule]
RULE-SET,https://cdn.jsdelivr.net/gh/MarioTestnio/emby-rules@main/surge/personal-direct.list,国内直连
RULE-SET,https://cdn.jsdelivr.net/gh/MarioTestnio/emby-rules@main/surge/emby.list,Emby
```

或使用 Egern YAML 格式：

```yaml
rule-providers:
  PersonalDirect:
    type: http
    url: https://cdn.jsdelivr.net/gh/MarioTestnio/emby-rules@main/egern/personal-direct.yaml
    interval: 86400

  Emby:
    type: http
    url: https://cdn.jsdelivr.net/gh/MarioTestnio/emby-rules@main/egern/emby.yaml
    interval: 86400

[Rule]
RULE-SET,PersonalDirect,国内直连
RULE-SET,Emby,Emby
```

## 更新日志

- 2025-07-23：初始版本，拆分直连/代理规则集，托管到 GitHub + jsDelivr
