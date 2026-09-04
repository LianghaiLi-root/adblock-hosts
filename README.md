# adblock-hosts
Ad blocking subscription for Anime Republic (com.shizi.tool.p3), serving **AdAway/BindHosts** (hosts-format) and **AdGuardHome** (DNS adblock rules).
Generated from Aliyun server v2 lists (2026-09-03 / auto).

## 订阅连接 / Subscription links

适用于两类工具，请按需选用对应连接：

### 1) AdAway / BindHosts（hosts 格式）— 供 AdAway、BindHosts 等 hosts 源工具导入
- hosts.txt : https://raw.githubusercontent.com/LianghaiLi-root/adblock-hosts/main/hosts.txt
- blacklist.txt : https://raw.githubusercontent.com/LianghaiLi-root/adblock-hosts/main/blacklist.txt (纯域名)

### 2) AdGuardHome（adblock 语法，DNS 级）— 供 AdGuardHome 的“DNS拦截清单 / 允许清单”导入
- **黑名单(拦截)**: https://raw.githubusercontent.com/LianghaiLi-root/adblock-hosts/main/adguard_blacklist.txt  （每行 `||domain^`）
- **白名单(例外放行)**: https://raw.githubusercontent.com/LianghaiLi-root/adblock-hosts/main/adguard_whitelist.txt （每行 `@@||domain^`）

> 旧订阅连接（hosts.txt / blacklist.txt / whitelist.txt）保持不变，继续可用。

## File / 文件说明
### AdAway / BindHosts 用途
- hosts.txt : AdAway hosts-format, 113 ad domains (`0.0.0.0 domain`)。Add as an AdAway / BindHosts hosts source.
- blacklist.txt : same 113 ad domains in pure-domain form (one per line).
- whitelist.txt : merged whitelist (含 whitelist_v2 + whitelist_custom) for allow-listing.
### AdGuardHome 用途
- adguard_blacklist.txt : DNS 广告拦截规则，adblock 格式 `||domain^`，113 条。AdGuardHome 导入路径：过滤器 -> DNS拦截清单 -> 添加过滤器列表 -> 填入上面 raw 连接。
- adguard_whitelist.txt : 例外/放行规则，adblock allowlist 格式 `@@||domain^`，19 条真实域名(已剔除 10.0.2.2 / localhost 等非 DNS 项)。AdGuardHome 导入路径：过滤器 -> DNS允许清单 -> 添加过滤器列表。

## 数据源 / Source
阿里云权威名单：blacklist_v2.txt (113 条)、whitelist_v2.txt、whitelist_custom_v2.txt。
