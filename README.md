# Emby 分流规则

基于 [justdoiting/emby-rules](https://github.com/justdoiting/emby-rules) 与 [MetaCubeX/meta-rules-dat](https://github.com/MetaCubeX/meta-rules-dat) 整理，适配 Clash / Mihomo / Surge / Egern。

## 文件说明

| 文件 | 适用工具 | 格式 |
|------|---------|------|
| `clash/emby.yaml` | Clash Party / Mihomo / Clash for Windows | YAML |
| `surge/emby.list` | Egern / Surge / Shadowrocket | Surge List |
| `egern/emby.yaml` | Egern | Egern YAML |

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

```yaml
# Egern YAML
rule-providers:
  emby:
    type: http
    url: "https://cdn.jsdelivr.net/gh/<你的用户名>/emby-rules@main/egern/emby.yaml"
    interval: 86400
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
- MetaCubeX/meta-rules-dat (category-emby)
- OneSmartPro 本地规则集
