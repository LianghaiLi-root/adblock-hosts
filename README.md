# adblock-hosts

面向广告拦截的订阅源仓库，按**目标工具/格式**分目录管理。覆盖 AdAway/BindHosts（hosts 格式）、AdGuardHome（adblock 规则）、通用纯域名工具，以及 **dae / daed / v2ray / xray**（V2Ray 二进制 geosite `.dat`）。

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
└── geodata/    V2Ray geosite 二进制 `.dat`(含 tag) → dae/daed/v2ray/xray 的 `ext:` 引用
    └── blacklist_geosite.dat
```

## 订阅连接 / Subscription links（按工具选用）

### 1) AdAway / BindHosts（hosts 格式）
- hosts : https://raw.githubusercontent.com/LianghaiLi-root/adblock-hosts/main/hosts/hosts.txt

### 2) AdGuard Home（adblock 语法）
- 黑名单(拦截) : https://raw.githubusercontent.com/LianghaiLi-root/adblock-hosts/main/adguard/adguard_blacklist.txt （每行 `||domain^`）
- 白名单(例外) : https://raw.githubusercontent.com/LianghaiLi-root/adblock-hosts/main/adguard/adguard_whitelist.txt （每行 `@@||domain^`）

### 3) 纯域名（供按内容解析的通用工具）
- blacklist : https://raw.githubusercontent.com/LianghaiLi-root/adblock-hosts/main/domain/blacklist.txt （113 条）
- whitelist : https://raw.githubusercontent.com/LianghaiLi-root/adblock-hosts/main/domain/whitelist.txt （19 条）

### 4) dae / daed / v2ray / xray（二进制 geosite `.dat`）
- geodata : https://raw.githubusercontent.com/LianghaiLi-root/adblock-hosts/main/geodata/blacklist_geosite.dat

`.dat` 为 **V2Ray asset 二进制格式**（非纯文本），内部含两个 tag，使用 `ext:` 按标签引用：
- `ext:"blacklist_geosite.dat:blacklist"` —— 广告黑名单（113 条，`full` 精确匹配）
- `ext:"blacklist_geosite.dat:whitelist"` —— 白名单（19 条，`full` 精确匹配）
- xray/v2ray 例：`domain(ext:blacklist_geosite.dat:blacklist) -> block`
- dae/daed routing 例：`domain(ext:"blacklist_geosite.dat:blacklist") -> block`

> 说明：本仓库不随带官方 `geoip.dat`/`geosite.dat`。此 `blacklist_geosite.dat` 仅含本仓库自维护的广告黑白名单两个 tag，供需要精确域名拦截的自定义 dat 场景使用（如 daed 的 `ext:` 引用）。

## 规则说明 / Rules
- 广告黑名单（blacklist）：113 个广告域名，匹配方式为 `full`（仅精确命中该完整域名，不含其子域名）——符合“精准域名”语义。
- 白名单（whitelist）：19 个真实放行域名（已剔除 10.0.2.2 / localhost 等非 DNS 项），同样为 `full` 精确匹配。
- 各格式文件（hosts / adguard / domain / geodata）均由同一份权威域名清单派生，内容一致，仅面向工具不同。
