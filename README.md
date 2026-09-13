# adblock-hosts

面向广告拦截的订阅源仓库，按**目标工具/格式**分目录管理。覆盖 AdAway/BindHosts（hosts 格式）、AdGuardHome（adblock 规则）、通用纯域名工具，**dae / daed / v2ray / xray**（V2Ray 二进制 geosite `.dat`），以及 **sing-box / SagerNet 系**（二进制 rule-set `.srs`）。

Generated/updated: 2026-09-05

## 目录结构 / Layout
```
├── README.md
├── hosts/      hosts-format（每行 `0.0.0.0 域名`）→ AdAway / BindHosts
│   └── hosts.txt
├── adguard/    Adblock 语法 `||域名^` / `@@||域名^` → AdGuard Home
│   ├── adguard_blacklist.txt
│   └── adguard_whitelist.txt
├── domain/     纯域名（每行一个域名）→ 按内容解析的通用工具
│   ├── blacklist.txt
│   └── whitelist.txt
├── geodata/    V2Ray geosite 二进制 `.dat`(含 tag) → dae/daed/v2ray/xray 的 `ext:` 引用
│   └── Lhl.dat
└── singbox/    sing-box 二进制 rule-set `.srs` → sing-box / SagerNet 系 `rule_set`
    ├── Lhl-blacklist.srs
    └── Lhl-whitelist.srs
```

## 订阅连接 / Subscription links（按工具选用）

### 1) AdAway / BindHosts（hosts 格式）
- hosts : https://raw.githubusercontent.com/LianghaiLi-root/adblock-hosts/main/hosts/hosts.txt

### 2) AdGuard Home（adblock 语法）
- 黑名单(拦截) : https://raw.githubusercontent.com/LianghaiLi-root/adblock-hosts/main/adguard/adguard_blacklist.txt （每行 `||domain^`）
- 白名单(例外) : https://raw.githubusercontent.com/LianghaiLi-root/adblock-hosts/main/adguard/adguard_whitelist.txt （每行 `@@||domain^`）

### 3) 纯域名（供按内容解析的通用工具）
- blacklist : https://raw.githubusercontent.com/LianghaiLi-root/adblock-hosts/main/domain/blacklist.txt （157 条）
- whitelist : https://raw.githubusercontent.com/LianghaiLi-root/adblock-hosts/main/domain/whitelist.txt （16 条）

### 4) dae / daed / v2ray / xray（二进制 geosite `.dat`）
- geodata : https://raw.githubusercontent.com/LianghaiLi-root/adblock-hosts/main/geodata/Lhl.dat

`.dat` 为 **V2Ray asset 二进制格式**（非纯文本），内部含两个 tag，使用 `ext:` 按标签引用：
- `ext:"Lhl.dat:blacklist"` —— 广告黑名单（161 条，`full` 精确匹配）
- `ext:"Lhl.dat:whitelist"` —— 白名单（16 条，`full` 精确匹配）
- xray/v2ray 例：`domain(ext:Lhl.dat:blacklist) -> block`
- dae/daed routing 例：`domain(ext:"Lhl.dat:blacklist") -> block`

> 说明：本仓库不随带官方 `geoip.dat`/`geosite.dat`。此 `Lhl.dat` 仅含本仓库自维护的广告黑白名单两个 tag，供需要精确域名拦截的自定义 dat 场景使用（如 daed 的 `ext:` 引用）。

### 5) sing-box（二进制 rule-set `.srs`）
- 黑名单(拦截) : https://raw.githubusercontent.com/LianghaiLi-root/adblock-hosts/main/singbox/Lhl-blacklist.srs
- 白名单(例外) : https://raw.githubusercontent.com/LianghaiLi-root/adblock-hosts/main/singbox/Lhl-whitelist.srs

`.srs` 为 **sing-box rule-set 二进制格式**（`format: binary`），供 sing-box / SagerNet 系用 `rule_set` 引用。匹配语义为 `domain`（**等值**，仅精确命中该完整域名，不含子域名），与 `geodata/Lhl.dat` 的 `full` 一致。

> sing-box 的 `rule_set` **没有 tag 概念**（同一 `.srs` 内多条规则是「或」关系），因此黑白名单拆成两个文件；白名单要在黑名单规则**之前**放行。

route 配置示例（白名单先豁免、黑名单再拦截）：
```json
{
  "route": {
    "rule_set": [
      { "type": "remote", "tag": "lhl-white", "format": "binary",
        "url": "https://raw.githubusercontent.com/LianghaiLi-root/adblock-hosts/main/singbox/Lhl-whitelist.srs",
        "update_interval": "24h" },
      { "type": "remote", "tag": "lhl-black", "format": "binary",
        "url": "https://raw.githubusercontent.com/LianghaiLi-root/adblock-hosts/main/singbox/Lhl-blacklist.srs",
        "update_interval": "24h" }
    ],
    "rules": [
      { "rule_set": "lhl-white", "action": "route", "outbound": "direct" },
      { "rule_set": "lhl-black", "action": "reject" }
    ]
  }
}
```

本地重新生成（**无需 CI**，`.srs` 是二进制，只能由 sing-box 官方二进制编译）：
```sh
python3 .github/scripts/build_srs.py --sing-box /path/to/sing-box
# 或指定环境变量：
SING_BOX_BIN=/path/to/sing-box python3 .github/scripts/build_srs.py
# 只生成源 JSON（不编译）：
python3 .github/scripts/build_srs.py --dump-json
```

## 规则说明 / Rules
- 广告黑名单（blacklist）：157 个广告域名，匹配方式为 `full` / `domain`（仅精确命中该完整域名，不含其子域名）——符合“精准域名”语义。
- 白名单（whitelist）：16 个真实放行域名（已剔除 10.0.2.2 / localhost 等非 DNS 项及加密 DoH/DoT 服务器域名，如 dns.alidns.com / doh.360.cn / doh.pub），同样为 `full` / `domain` 精确匹配。
- 各格式文件（hosts / adguard / domain / geodata / singbox）均由同一份权威域名清单（`domain/*.txt`）派生，内容一致，仅面向工具不同。
