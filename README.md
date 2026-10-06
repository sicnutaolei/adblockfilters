# AdBlock DNS Filters

[![Update Filters](https://github.com/sicnutaolei/adblockfilters/actions/workflows/downloader.yml/badge.svg)](https://github.com/sicnutaolei/adblockfilters/actions/workflows/downloader.yml)
[![Generate Blacklist](https://github.com/sicnutaolei/adblockfilters/actions/workflows/blacklist.yml/badge.svg)](https://github.com/sicnutaolei/adblockfilters/actions/workflows/blacklist.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)

适用于 AdGuard / AdGuard Home 等去广告服务的**合并规则库**，每 8 小时自动更新一次。

个人收藏了不少广告过滤规则，但每次往新设备添加时很头疼，于是写了这个项目：定时从各上游规则源拉取更新，合并、去重、剔除失效域名，生成开箱即用的规则订阅文件。

> 本项目 fork 自 [217heidai/adblockfilters](https://github.com/217heidai/adblockfilters)，在此基础上按自己的使用习惯做了定制（详见 [与上游的差异](#与上游的差异)）。

## 特性

| 特性 | 说明 |
|:-|:-|
| ⏱️ 自动更新 | GitHub Actions 每 8 小时（`0 */8 * * *`）自动拉取上游规则并合并提交 |
| 🧹 合并去重 | 汇总 20+ 上游规则源，跨源去重、按域名层级归并（二级域名已拦截则不再保留其子域名） |
| 🩺 失效域名剔除 | 通过 SmartDNS 对拦截域名做解析探测，移除已无法解析的域名 |
| 🎯 精准拦截 | 保留 AdGuard 通配语法（`||example.com^`、`@@||example.com^`） |
| 🧩 双规则输出 | `adblockdns.txt`（DNS 拦截，全量）+ `adblockfilters.txt`（浏览器插件补充） |
| ⚙️ 可定制 | 通过 `rules/white.txt` 全局放行，`rules/black.txt` 强制拦截 |

## 说明

1. 定时从上游各规则源获取更新，合并去重。
2. 使用国内、国外多组 DNS 服务，分别对上游各规则源拦截的域名进行解析，**去除已无法解析的域名**（上游规则源中存在大量失效域名，无需加入拦截规则）。
3. 本项目**仅对上游规则做合并、去重、去除无效域名，不做任何内容修改**。如发现误拦截，可临时添加放行规则（如 `@@||www.example.com^$important`），并向上游规则源反馈。
4. GitHub Actions 每天额外跑一次黑名单生成任务（`blacklist.py`），将探测到的失效域名沉淀到 `rules/black.txt`，避免每次全量重复解析。

## 订阅链接

1. **规则 1**：AdGuard Home、AdGuard 等 **DNS 拦截服务**使用。
2. **规则 2**：AdGuard 等**浏览器插件**使用，为规则 1 的补充（仅含 filter 规则，不含纯域名）。
3. 推荐 **规则 1 + 规则 2** 组合使用，覆盖面最全。
4. 加速链接基于 `gh-proxy.com`，国内网络可直连；如失效可换用其他 GitHub 加速服务。

| 规则 | 说明 | 原始链接 | 加速链接 |
|:-|:-|:-|:-|
| 规则1：DNS 拦截 | 全量域名拦截规则 | `https://raw.githubusercontent.com/sicnutaolei/adblockfilters/main/rules/adblockdns.txt` | `https://gh-proxy.com/https://raw.githubusercontent.com/sicnutaolei/adblockfilters/main/rules/adblockdns.txt` |
| 规则2：插件拦截 | 浏览器插件补充规则 | `https://raw.githubusercontent.com/sicnutaolei/adblockfilters/main/rules/adblockfilters.txt` | `https://gh-proxy.com/https://raw.githubusercontent.com/sicnutaolei/adblockfilters/main/rules/adblockfilters.txt` |

> **当前规则规模**（以最近一次生成为准）：
> - `adblockdns.txt`：约 **30 万条**拦截域名 + 100 余条放行域名
> - `adblockfilters.txt`：约 **12 万条**过滤器规则

## 上游规则源

1. 感谢各位广告过滤规则维护者的辛苦付出。
2. 不再引用 [anti-AD](https://anti-ad.net/adguard.txt)、[yhosts](https://raw.githubusercontent.com/VeleSila/yhosts/master/hosts.txt)，具体原因见 [Mosney/anti-anti-AD](https://github.com/Mosney/anti-anti-AD)。
3. 已移除 [Notracking blocklist](https://raw.githubusercontent.com/notracking/hosts-blocklists/master/adblock/adblock.txt)（原项目[已停止维护](https://github.com/notracking/hosts-blocklists/issues/900)）。
4. 已移除 [ADgk](https://raw.githubusercontent.com/banbendalao/ADgk/master/ADgk.txt)（项目超过 1 年未更新）。

| 规则 | 类型 | 原始链接 | 本项目产物 | 更新日期 |
|:-|:-|:-|:-|:-|
| AdGuard Base filter | filter | [原始链接](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_2_Base/filter.txt) | [rules/AdGuard_Base_filter.txt](./rules/AdGuard_Base_filter.txt) | 2026/10/07 |
| AdGuard Chinese filter | filter | [原始链接](https://raw.githubusercontent.com/AdguardTeam/FiltersRegistry/master/filters/filter_224_Chinese/filter.txt) | [rules/AdGuard_Chinese_filter.txt](./rules/AdGuard_Chinese_filter.txt) | 2026/10/07 |
| AdGuard DNS filter | filter | [原始链接](https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt) | [rules/AdGuard_DNS_filter.txt](./rules/AdGuard_DNS_filter.txt) | 2026/10/07 |
| CJX's Annoyance List | filter | [原始链接](https://raw.githubusercontent.com/cjx82630/cjxlist/master/cjx-annoyance.txt) | [rules/CJX's_Annoyance_List.txt](./rules/CJX's_Annoyance_List.txt) | 2026/10/01 |
| EasyList | filter | [原始链接](https://easylist-downloads.adblockplus.org/easylist.txt) | [rules/EasyList.txt](./rules/EasyList.txt) | 2026/10/07 |
| EasyList China | filter | [原始链接](https://easylist-downloads.adblockplus.org/easylistchina.txt) | [rules/EasyList_China.txt](./rules/EasyList_China.txt) | 2026/10/07 |
| EasyPrivacy | filter | [原始链接](https://easylist-downloads.adblockplus.org/easyprivacy.txt) | [rules/EasyPrivacy.txt](./rules/EasyPrivacy.txt) | 2026/10/07 |
| xinggsf mv | filter | [原始链接](https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/mv.txt) | [rules/xinggsf_mv.txt](./rules/xinggsf_mv.txt) | 2025/12/25 |
| xinggsf rule | filter | [原始链接](https://raw.githubusercontent.com/xinggsf/Adblock-Plus-Rule/master/rule.txt) | [rules/xinggsf_rule.txt](./rules/xinggsf_rule.txt) | 2025/09/09 |
| jiekouAD | filter | [原始链接](https://raw.githubusercontent.com/damengzhu/banad/main/jiekouAD.txt) | [rules/jiekouAD.txt](./rules/jiekouAD.txt) | 2026/10/01 |
| 1Hosts (Lite) | dns | [原始链接](https://raw.githubusercontent.com/badmojr/1Hosts/master/Lite/adblock.txt) | [rules/1Hosts_(Lite).txt](./rules/1Hosts_(Lite).txt) | 2026/09/03 |
| Anti AD | dns | [原始链接](https://anti-ad.net/easylist.txt) | [rules/Anti_AD.txt](./rules/Anti_AD.txt) | 2026/10/05 |
| AdRules DNS List | dns | [原始链接](https://raw.githubusercontent.com/Cats-Team/AdRules/main/dns.txt) | [rules/AdRules_DNS_List.txt](./rules/AdRules_DNS_List.txt) | 2026/10/06 |
| AWAvenue Ads Rule | dns | [原始链接](https://raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt) | [rules/AWAvenue_Ads_Rule.txt](./rules/AWAvenue_Ads_Rule.txt) | 2026/09/21 |
| Hblock | dns | [原始链接](https://hblock.molinero.dev/hosts_adblock.txt) | [rules/Hblock.txt](./rules/Hblock.txt) | 2026/10/06 |
| NEO DEV HOST | dns | [原始链接](https://raw.githubusercontent.com/neodevpro/neodevhost/master/lite_adblocker) | [rules/NEO_DEV_HOST.txt](./rules/NEO_DEV_HOST.txt) | 2025/02/18 |
| OISD Basic | dns | [原始链接](https://abp.oisd.nl/basic/) | [rules/OISD_Basic.txt](./rules/OISD_Basic.txt) | 2026/10/07 |
| SmartTV Blocklist | dns | [原始链接](https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/SmartTV-AGH.txt) | [rules/SmartTV_Blocklist.txt](./rules/SmartTV_Blocklist.txt) | 2026/09/08 |
| 1024 hosts | host | [原始链接](https://raw.githubusercontent.com/Goooler/1024_hosts/master/hosts) | [rules/1024_hosts.txt](./rules/1024_hosts.txt) | 2025/09/09 |
| ad-wars hosts | host | [原始链接](https://raw.githubusercontent.com/jdlingyu/ad-wars/master/hosts) | [rules/ad-wars_hosts.txt](./rules/ad-wars_hosts.txt) | 2023/11/17 |
| StevenBlack hosts | host | [原始链接](https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts) | [rules/StevenBlack_hosts.txt](./rules/StevenBlack_hosts.txt) | 2026/10/03 |

> ⚠️ 部分上游源已长期未更新或失效（如 `NEO DEV HOST`、`ad-wars hosts`、`1024 hosts`），规则文件可能是历史快照。它们仍会被合并，但贡献的增量有限。

## 放行 / 强制拦截

在 `rules/` 目录下有两个手工维护的清单，脚本每次生成都会读取：

| 文件 | 作用 | 格式 |
|:-|:-|:-|
| `rules/white.txt` | **全局放行**。命中的域名不会被写入拦截规则 | 每行一个域名，`#` 开头为注释 |
| `rules/black.txt` | **强制拦截 / 失效域名记录**。由 `blacklist.py` 自动生成，也可手工追加 | 每行一个域名 |

`black.txt` 会剔除那些被上游误标、但实际已无法解析的域名，从而缩小误杀面。

## 工作流程

项目由两个 GitHub Actions 工作流驱动：

| 工作流 | 触发时机 | 执行脚本 | 作用 |
|:-|:-|:-|:-|
| `downloader.yml`（Update Filters） | 每 8 小时 + 手动 | `abblockfilters.py` | 下载上游规则 → 合并去重 → 生成 `adblockdns.txt` / `adblockfilters.txt` → 刷新 README |
| `blacklist.yml`（Generate Blacklist） | 每天 01:00 + 手动 | `blacklist.py` | 启动 SmartDNS → 探测域名有效性 → 生成 `rules/black.txt` |

也可以本地手动触发：

```bash
# 安装依赖
pip install -U requests tld tcping IPy dnspython

# 拉取上游规则并生成合并规则（同时会重写 README.md）
python abblockfilters.py

# 生成失效域名黑名单（需要本地 SmartDNS 监听 127.0.0.1:5053）
python blacklist.py
```

### 目录结构

```
adblockfilters/
├── .github/workflows/
│   ├── downloader.yml        # 每 8 小时更新规则
│   └── blacklist.yml         # 每天生成失效域名黑名单
├── rules/
│   ├── adblockdns.txt        # 生成的 DNS 拦截规则（规则1）
│   ├── adblockfilters.txt    # 生成的插件过滤规则（规则2）
│   ├── adblockdns.backup     # 合并前的全量域名备份（用于有效性探测）
│   ├── black.txt             # 失效域名黑名单
│   ├── white.txt             # 手工放行清单
│   └── *.txt                 # 各上游规则源的本地快照
├── abblockfilters.py         # 主流程：下载 → 合并 → 生成规则 → 更新 README
├── resolver.py               # 规则解析：将 host/dns/filter 语法解析为域名
├── downloader.py             # 下载器：SHA256 比对，仅在内容变化时更新
├── blacklist.py              # 失效域名探测，生成 black.txt
└── smartdns.conf             # 探测用 SmartDNS 配置
```

## 与上游的差异

本 fork 保留了上游早期（v1）的单文件实现，并做了针对性定制：

| 项目 | 上游（217heidai） | 本 fork |
|:-|:-|:-|
| 代码结构 | 多模块（`adblock.py` / `filter.py` / `readme.py` / `updater.py`）+ SQLite 存储 | 保持早期单文件结构（`abblockfilters.py` / `downloader.py` / `resolver.py` / `blacklist.py`） |
| 输出格式 | 17+ 种（Clash / sing-box / mosdns / v2ray / hosts / dnsmasq …） | 2 种：`adblockdns.txt` + `adblockfilters.txt` |
| 加速链接 | jsDelivr、boki.moe、ghfast.top 三路 | `gh-proxy.com` 单路 |
| SmartDNS 配置 | 带 EDNS 子网（上海电信定向优化） | 已移除 EDNS 子网，新增 Cloudflare 上游 |

**其他定制**：

- `smartdns.conf` 增加了 `server-tls 1.1.1.1:853`（Cloudflare）上游，可靠性更高。
- 移除了上游配置中针对上海电信的 `-subnet 222.66.251.8/32` 参数，避免非该网络环境下解析异常。

> 由于上游已完成重构，本 fork 的代码不再与上游保持同步。若需上游的最新特性（多格式输出、Lite 规则等），建议直接使用 [上游仓库](https://github.com/217heidai/adblockfilters)。

## FAQ

**Q：规则文件多久更新一次？**
A：GitHub Actions 每 8 小时拉取一次。你可以在仓库的 Actions 页面查看最近一次运行状态。

**Q：误拦截了某个域名怎么办？**
A：在 `rules/white.txt` 中添加该域名（每行一个）并提交，下一轮生成时会自动放行；也可在 AdGuard 中临时添加 `@@||域名^$important` 放行。

**Q：为什么规则文件里有些已废弃的域名还在？**
A：失效域名的剔除依赖 SmartDNS 解析探测，探测失败可能有超时或 DNS 缓存等偶发因素。多次运行后会逐步收敛。

**Q：加速链接打不开？**
A：`gh-proxy.com` 为第三方加速服务，可能临时不可用。可自行替换为其他 GitHub 加速前缀，或使用原始链接。

**Q：可以只订阅其中一条规则吗？**
A：可以。仅用 DNS 拦截服务时订阅规则 1 即可；浏览器插件场景建议规则 1 + 规则 2。

## 致谢

- 上游项目：[217heidai/adblockfilters](https://github.com/217heidai/adblockfilters)
- 所有规则源维护者（AdGuard、EasyList、AdRules、1Hosts、OISD、Hblock 等）

## License

[MIT](./LICENSE)
