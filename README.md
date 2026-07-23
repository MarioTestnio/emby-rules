# Emby 分流规则

基于 [justdoiting/emby-rules](https://github.com/justdoiting/emby-rules) 整理，适配 Clash / Mihomo / Surge / Egern。

## 文件说明

| 文件 | 适用工具 | 格式 |
|------|---------|------|
| `clash/emby.yaml` | Clash Party / Mihomo / Clash for Windows | YAML |
| `surge/emby.list` | Egern / Surge / Shadowrocket | Surge List |

## 远端引用

把 `<你的用户名>` 替换为你的 GitHub 用户名，仓库名统一为 `emby-rules`。

### jsDelivr（推荐）

```yaml
# Clash / Mihomo
rule-providers:
  emby:
    type: http
    url: "https://cdn.jsdelivr.net/gh/<你的用户名>/emby-rules@main/clash/emby.yaml"
    interval: 86400
    path: ./rules/emby.yaml
```

```yaml
# Egern / Surge
[Rule]
RULE-SET,https://cdn.jsdelivr.net/gh/<你的用户名>/emby-rules@main/surge/emby.list,Emby
```

### GitHub Raw

```yaml
# Clash / Mihomo
url: "https://raw.githubusercontent.com/<你的用户名>/emby-rules/main/clash/emby.yaml"
```

```yaml
# Egern / Surge
RULE-SET,https://raw.githubusercontent.com/<你的用户名>/emby-rules/main/surge/emby.list,Emby
```

## 本地更新

```bash
cd emby-rules
git add .
git commit -m "update: 更新 Emby 规则"
git push
```

## 规则来源

- justdoiting/emby-rules
- blackmatrix7/ios_rule_script (参考)
