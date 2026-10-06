import os
import re
import time

from downloader import Downloader
from resolver import Resolver


class Rule(object):
    def __init__(self, name, url):
        self.Name = name
        self.FileName = self.Name.replace(' ', '_') + '.txt'
        self.URL = url
        self.Downloader = Downloader(os.getcwd() + '/rules/' + self.FileName, self.URL)

    def Update(self):
        if self.Downloader.Download():
            return True
        return False

def GetRuleList(fileName):
    ruleList = []
    with open(fileName, "r", encoding='utf-8') as f:
        for line in f:
            line = line.replace('\r', '').replace('\n', '')
            if line.find('|')==0 and line.rfind('|')==len(line)-1:
                rule = list(map(lambda x: x.strip(), line[1:].split('|')))
                # 规则源表格特征：第 3 列含 URL 括号，第 4 列是更新日期（yyyy/mm/dd）
                # 该判断可防止"订阅链接"等其它表格被误识别为规则源
                if len(rule) < 5:
                    continue
                if not re.match(r'^\d{4}/\d{1,2}/\d{1,2}$', rule[4]):
                    continue
                if rule[2].find('(') > 0 and rule[2].find(')') > 0:
                    url = rule[2][rule[2].find('(')+1:rule[2].find(')')]
                    matchObj1 = re.match(r'(http|https)://[\w\-_]+(\.[\w\-_]+)+([\w\-.,@?^=%&:/~+#]*[\w\-@?^=%&/~+#])?', url)
                    if matchObj1:
                        ruleList.append([rule[0], rule[1], url, rule[4]])
    return ruleList

def CreatReadme(ruleList, fileName):
    if os.path.exists(fileName):
        os.remove(fileName)

    repo = 'sicnutaolei/adblockfilters'
    raw = 'https://raw.githubusercontent.com/%s/main/rules/' % (repo)

    def rawLink(name):
        return raw + name.replace(' ', '_') + '.txt'

    def accel(url):
        return 'https://gh-proxy.com/' + url

    with open(fileName, 'a', encoding='utf-8') as f:
        f.write("# AdBlock DNS Filters\n\n")
        f.write("[![Update Filters](https://github.com/%s/actions/workflows/downloader.yml/badge.svg)]"
                "(https://github.com/%s/actions/workflows/downloader.yml)\n" % (repo, repo))
        f.write("[![Generate Blacklist](https://github.com/%s/actions/workflows/blacklist.yml/badge.svg)]"
                "(https://github.com/%s/actions/workflows/blacklist.yml)\n" % (repo, repo))
        f.write("[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)\n\n")
        f.write("适用于 AdGuard / AdGuard Home 等去广告服务的**合并规则库**，每 8 小时自动更新一次。\n\n")
        f.write("个人收藏了不少广告过滤规则，但每次往新设备添加时很头疼，于是写了这个项目："
                "定时从各上游规则源拉取更新，合并、去重、剔除失效域名，生成开箱即用的规则订阅文件。\n\n")
        f.write("> 本项目 fork 自 [217heidai/adblockfilters](https://github.com/217heidai/adblockfilters)，"
                "在此基础上按自己的使用习惯做了定制（详见 [与上游的差异](#与上游的差异)）。\n\n")

        f.write("## 特性\n\n")
        f.write("| 特性 | 说明 |\n|:-|:-|\n")
        f.write("| ⏱️ 自动更新 | GitHub Actions 每 8 小时（`0 */8 * * *`）自动拉取上游规则并合并提交 |\n")
        f.write("| 🧹 合并去重 | 汇总 20+ 上游规则源，跨源去重、按域名层级归并（二级域名已拦截则不再保留其子域名） |\n")
        f.write("| 🩺 失效域名剔除 | 通过 SmartDNS 对拦截域名做解析探测，移除已无法解析的域名 |\n")
        f.write("| 🎯 精准拦截 | 保留 AdGuard 通配语法（`||example.com^`、`@@||example.com^`） |\n")
        f.write("| 🧩 双规则输出 | `adblockdns.txt`（DNS 拦截，全量）+ `adblockfilters.txt`（浏览器插件补充） |\n")
        f.write("| ⚙️ 可定制 | 通过 `rules/white.txt` 全局放行，`rules/black.txt` 强制拦截 |\n\n")

        f.write("## 说明\n\n")
        f.write("1. 定时从上游各规则源获取更新，合并去重。\n")
        f.write("2. 使用国内、国外多组 DNS 服务，分别对上游各规则源拦截的域名进行解析，**去除已无法解析的域名**"
                "（上游规则源中存在大量失效域名，无需加入拦截规则）。\n")
        f.write("3. 本项目**仅对上游规则做合并、去重、去除无效域名，不做任何内容修改**。"
                "如发现误拦截，可临时添加放行规则（如 `@@||www.example.com^$important`），并向上游规则源反馈。\n")
        f.write("4. GitHub Actions 每天额外跑一次黑名单生成任务（`blacklist.py`），"
                "将探测到的失效域名沉淀到 `rules/black.txt`，避免每次全量重复解析。\n\n")

        f.write("## 订阅链接\n\n")
        f.write("1. **规则 1**：AdGuard Home、AdGuard 等 **DNS 拦截服务**使用。\n")
        f.write("2. **规则 2**：AdGuard 等**浏览器插件**使用，为规则 1 的补充（仅含 filter 规则，不含纯域名）。\n")
        f.write("3. 推荐 **规则 1 + 规则 2** 组合使用，覆盖面最全。\n")
        f.write("4. 加速链接基于 `gh-proxy.com`，国内网络可直连；如失效可换用其他 GitHub 加速服务。\n\n")
        f.write("| 规则 | 说明 | 原始链接 | 加速链接 |\n|:-|:-|:-|:-|\n")
        f.write("| 规则1：DNS 拦截 | 全量域名拦截规则 | `%s` | `%s` |\n"
                % (rawLink('adblockdns'), accel(rawLink('adblockdns'))))
        f.write("| 规则2：插件拦截 | 浏览器插件补充规则 | `%s` | `%s` |\n\n"
                % (rawLink('adblockfilters'), accel(rawLink('adblockfilters'))))
        f.write("> **当前规则规模**（以最近一次生成为准）：\n"
                "> - `adblockdns.txt`：约 **30 万条**拦截域名 + 100 余条放行域名\n"
                "> - `adblockfilters.txt`：约 **12 万条**过滤器规则\n\n")

        f.write("## 上游规则源\n\n")
        f.write("1. 感谢各位广告过滤规则维护者的辛苦付出。\n")
        f.write("2. 不再引用 [anti-AD](https://anti-ad.net/adguard.txt)、"
                "[yhosts](https://raw.githubusercontent.com/VeleSila/yhosts/master/hosts.txt)，"
                "具体原因见 [Mosney/anti-anti-AD](https://github.com/Mosney/anti-anti-AD)。\n")
        f.write("3. 已移除 [Notracking blocklist](https://raw.githubusercontent.com/notracking/hosts-blocklists/master/adblock/adblock.txt)"
                "（原项目[已停止维护](https://github.com/notracking/hosts-blocklists/issues/900)）。\n")
        f.write("4. 已移除 [ADgk](https://raw.githubusercontent.com/banbendalao/ADgk/master/ADgk.txt)（项目超过 1 年未更新）。\n\n")
        f.write("| 规则 | 类型 | 原始链接 | 本项目产物 | 更新日期 |\n")
        f.write("|:-|:-|:-|:-|:-|\n")
        for rule in ruleList:
            name = rule[0].replace(' ', '_')
            f.write("| %s | %s | [原始链接](%s) | [rules/%s.txt](./rules/%s.txt) | %s |\n"
                    % (rule[0], rule[1], rule[2], name, name, rule[3]))
        f.write("\n> ⚠️ 部分上游源已长期未更新或失效（如 `NEO DEV HOST`、`ad-wars hosts`、`1024 hosts`），"
                "规则文件可能是历史快照。它们仍会被合并，但贡献的增量有限。\n\n")

        f.write("## 放行 / 强制拦截\n\n")
        f.write("在 `rules/` 目录下有两个手工维护的清单，脚本每次生成都会读取：\n\n")
        f.write("| 文件 | 作用 | 格式 |\n|:-|:-|:-|\n")
        f.write("| `rules/white.txt` | **全局放行**。命中的域名不会被写入拦截规则 | 每行一个域名，`#` 开头为注释 |\n")
        f.write("| `rules/black.txt` | **强制拦截 / 失效域名记录**。由 `blacklist.py` 自动生成，也可手工追加 | 每行一个域名 |\n\n")
        f.write("`black.txt` 会剔除那些被上游误标、但实际已无法解析的域名，从而缩小误杀面。\n\n")

        f.write("## 工作流程\n\n")
        f.write("项目由两个 GitHub Actions 工作流驱动：\n\n")
        f.write("| 工作流 | 触发时机 | 执行脚本 | 作用 |\n|:-|:-|:-|:-|\n")
        f.write("| `downloader.yml`（Update Filters） | 每 8 小时 + 手动 | `abblockfilters.py` | "
                "下载上游规则 → 合并去重 → 生成 `adblockdns.txt` / `adblockfilters.txt` → 刷新 README |\n")
        f.write("| `blacklist.yml`（Generate Blacklist） | 每天 01:00 + 手动 | `blacklist.py` | "
                "启动 SmartDNS → 探测域名有效性 → 生成 `rules/black.txt` |\n\n")
        f.write("也可以本地手动触发：\n\n")
        f.write("```bash\n")
        f.write("# 安装依赖\npip install -U requests tld tcping IPy dnspython\n\n")
        f.write("# 拉取上游规则并生成合并规则（同时会重写 README.md）\npython abblockfilters.py\n\n")
        f.write("# 生成失效域名黑名单（需要本地 SmartDNS 监听 127.0.0.1:5053）\npython blacklist.py\n")
        f.write("```\n\n")

        f.write("### 目录结构\n\n")
        f.write("```\n")
        f.write("adblockfilters/\n")
        f.write("├── .github/workflows/\n")
        f.write("│   ├── downloader.yml        # 每 8 小时更新规则\n")
        f.write("│   └── blacklist.yml         # 每天生成失效域名黑名单\n")
        f.write("├── rules/\n")
        f.write("│   ├── adblockdns.txt        # 生成的 DNS 拦截规则（规则1）\n")
        f.write("│   ├── adblockfilters.txt    # 生成的插件过滤规则（规则2）\n")
        f.write("│   ├── adblockdns.backup     # 合并前的全量域名备份（用于有效性探测）\n")
        f.write("│   ├── black.txt             # 失效域名黑名单\n")
        f.write("│   ├── white.txt             # 手工放行清单\n")
        f.write("│   └── *.txt                 # 各上游规则源的本地快照\n")
        f.write("├── abblockfilters.py         # 主流程：下载 → 合并 → 生成规则 → 更新 README\n")
        f.write("├── resolver.py               # 规则解析：将 host/dns/filter 语法解析为域名\n")
        f.write("├── downloader.py             # 下载器：SHA256 比对，仅在内容变化时更新\n")
        f.write("├── blacklist.py              # 失效域名探测，生成 black.txt\n")
        f.write("└── smartdns.conf             # 探测用 SmartDNS 配置\n")
        f.write("```\n\n")

        f.write("## 与上游的差异\n\n")
        f.write("本 fork 保留了上游早期（v1）的单文件实现，并做了针对性定制：\n\n")
        f.write("| 项目 | 上游（217heidai） | 本 fork |\n|:-|:-|:-|\n")
        f.write("| 代码结构 | 多模块（`adblock.py` / `filter.py` / `readme.py` / `updater.py`）+ SQLite 存储 | "
                "保持早期单文件结构（`abblockfilters.py` / `downloader.py` / `resolver.py` / `blacklist.py`） |\n")
        f.write("| 输出格式 | 17+ 种（Clash / sing-box / mosdns / v2ray / hosts / dnsmasq …） | "
                "2 种：`adblockdns.txt` + `adblockfilters.txt` |\n")
        f.write("| 加速链接 | jsDelivr、boki.moe、ghfast.top 三路 | `gh-proxy.com` 单路 |\n")
        f.write("| SmartDNS 配置 | 带 EDNS 子网（上海电信定向优化） | 已移除 EDNS 子网，新增 Cloudflare 上游 |\n\n")
        f.write("**其他定制**：\n\n")
        f.write("- `smartdns.conf` 增加了 `server-tls 1.1.1.1:853`（Cloudflare）上游，可靠性更高。\n")
        f.write("- 移除了上游配置中针对上海电信的 `-subnet 222.66.251.8/32` 参数，避免非该网络环境下解析异常。\n\n")
        f.write("> 由于上游已完成重构，本 fork 的代码不再与上游保持同步。"
                "若需上游的最新特性（多格式输出、Lite 规则等），建议直接使用 "
                "[上游仓库](https://github.com/217heidai/adblockfilters)。\n\n")

        f.write("## FAQ\n\n")
        f.write("**Q：规则文件多久更新一次？**\n"
                "A：GitHub Actions 每 8 小时拉取一次。你可以在仓库的 Actions 页面查看最近一次运行状态。\n\n")
        f.write("**Q：误拦截了某个域名怎么办？**\n"
                "A：在 `rules/white.txt` 中添加该域名（每行一个）并提交，下一轮生成时会自动放行；"
                "也可在 AdGuard 中临时添加 `@@||域名^$important` 放行。\n\n")
        f.write("**Q：为什么规则文件里有些已废弃的域名还在？**\n"
                "A：失效域名的剔除依赖 SmartDNS 解析探测，探测失败可能有超时或 DNS 缓存等偶发因素。"
                "多次运行后会逐步收敛。\n\n")
        f.write("**Q：加速链接打不开？**\n"
                "A：`gh-proxy.com` 为第三方加速服务，可能临时不可用。"
                "可自行替换为其他 GitHub 加速前缀，或使用原始链接。\n\n")
        f.write("**Q：可以只订阅其中一条规则吗？**\n"
                "A：可以。仅用 DNS 拦截服务时订阅规则 1 即可；浏览器插件场景建议规则 1 + 规则 2。\n\n")

        f.write("## 致谢\n\n")
        f.write("- 上游项目：[217heidai/adblockfilters](https://github.com/217heidai/adblockfilters)\n")
        f.write("- 所有规则源维护者（AdGuard、EasyList、AdRules、1Hosts、OISD、Hblock 等）\n\n")

        f.write("## License\n\n")
        f.write("[MIT](./LICENSE)\n")


def GetBlackList():
    blackList = []
    fileName = os.getcwd() + "/rules/black.txt"
    if os.path.exists(fileName):
        with open(fileName, 'r') as f:
            blackList = f.readlines()
            blackList = list(map(lambda x: x.replace("\n", ""), blackList))
    return blackList

def GetWhiteList():
    whiteList = []
    fileName = os.getcwd() + "/rules/white.txt"
    if os.path.exists(fileName):
        with open(fileName, 'r') as f:
            for line in f.readlines():
                if not line.startswith("#") and len(line.replace("\n", "")) > 4:
                    whiteList.append(line.replace("\n", ""))
    return whiteList

# 去重、排序
def sort(domainDict, isBlock, blackList, whiteList):
    def repetition(l):
        tmp = []
        for i in l:
            for j in l:
                if len(i) > len(j) and i.rfind("." + j) == len(i) - len(j) - 1:
                    tmp.append(i)
                    break
        return list(set(l)-set(tmp))
    blockList = []
    blockList_all = []
    fldList = []
    for item in domainDict:
        fldList.append(item)
    fldList.sort() # 排序
    for fld in fldList:
        subdomainList = list(set(domainDict[fld])) # 去重
        if '' in subdomainList and fld not in whiteList: # 二级域名已被拦截，则干掉所有子域名
            subdomainList = ['']
        subdomainList = list(filter(None, subdomainList)) # 去空
        if len(subdomainList) > 0:
            if len(subdomainList) > 2:
                subdomainList = repetition(subdomainList) # 短域名已被拦截，则干掉所有长域名。如'a.example'、'b.example'、'example'，则只保留'example'
            subdomainList.sort() # 排序
            for subdomain in subdomainList:
                item = "%s.%s"%(subdomain, fld)
                if isBlock:
                    blockList_all.append("||%s^"%(item))
                else:
                    blockList_all.append("@@||%s^"%(item))
                
                if item not in blackList and item not in whiteList:
                    if isBlock:
                        blockList.append("||%s^"%(item))
                    else:
                        blockList.append("@@||%s^"%(item))
        else:
            item = "%s"%(fld)
            if isBlock:
                blockList_all.append("||%s^"%(item))
            else:
                blockList_all.append("@@||%s^"%(item))
            
            if item not in blackList and item not in whiteList:
                if isBlock:
                    blockList.append("||%s^"%(item))
                else:
                    blockList.append("@@||%s^"%(item))
    
    return blockList,blockList_all

def CreatDNS(blockDict, unblockDict, fileName):
    blackList = GetBlackList()
    whiteList = GetWhiteList()
    blockList,blockList_all = sort(blockDict, True, blackList, whiteList)
    unblockList,unblockList_all = sort(unblockDict, False, blackList, whiteList)

    # 备份全量域名，用于检查域名有效性生成黑名单
    backupName = fileName[:-len("txt")] + "backup"
    if os.path.exists(backupName):
        os.remove(backupName)
    with open(backupName, 'a') as f:
        for fiter in blockList_all:
            f.write("%s\n"%(fiter))
        for fiter in unblockList_all:
            f.write("%s\n"%(fiter))

    # 生成规则文件
    if os.path.exists(fileName):
        os.remove(fileName)    
    with open(fileName, 'a') as f:
        f.write("!\n")
        f.write("! Title: AdBlock DNS\n")
        f.write("! Description: 适用于AdGuard的去广告合并规则，每8个小时更新一次。规则源：1Hosts (Lite)、AdGuard Base filter、AdGuard Base filter、AdGuard DNS filter、AdRules DNS List、Hblock、NEO DEV HOST、OISD Basic、1024 hosts、ad-wars hosts、StevenBlack hosts、xinggsf、EasyList、Easylist China、EasyPrivacy、CJX's Annoyance List、SmartTV Blocklist、AWAvenue Ads Rule、jiekouAD\n")
        f.write("! Homepage: https://github.com/sicnutaolei/adblockfilters\n")
        f.write("! Source: https://raw.githubusercontent.com/sicnutaolei/adblockfilters/main/rules/adblockdns.txt\n")
        f.write("! Version: %s\n"%(time.strftime("%Y%m%d%H%M%S", time.localtime())))
        f.write("! Last modified: %s\n"%(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())))
        f.write("! Blocked domains: %s\n"%(len(blockList)))
        f.write("! unBlocked domains: %s\n"%(len(unblockList)))
        f.write("!\n")
        for fiter in blockList:
            f.write("%s\n"%(fiter))
        for fiter in unblockList:
            f.write("%s\n"%(fiter))

def CreatFiter(filterList, fileName):
    # 去重、排序
    def sort(L, whiteList):
        L = list(set(L)-set(whiteList))
        L.sort()
        return L

    whiteList = GetWhiteList()
    filterList = sort(filterList, whiteList)

    if os.path.exists(fileName):
        os.remove(fileName)
    
    with open(fileName, 'a') as f:
        f.write("!\n")
        f.write("! Title: AdBlock Filter\n")
        f.write("! Description: 适用于AdGuard的去广告合并规则，每8个小时更新一次。规则源：1Hosts (Lite)、AdGuard Base filter、AdGuard Base filter、AdGuard DNS filter、AdRules DNS List、Hblock、NEO DEV HOST、OISD Basic、1024 hosts、ad-wars hosts、StevenBlack hosts、xinggsf、EasyList、Easylist China、EasyPrivacy、CJX's Annoyance List、SmartTV Blocklist、AWAvenue Ads Rule、jiekouAD\n")
        f.write("! Homepage: https://github.com/sicnutaolei/adblockfilters\n")
        f.write("! Source: https://raw.githubusercontent.com/sicnutaolei/adblockfilters/main/rules/adblockfilters.txt\n")
        f.write("! Version: %s\n"%(time.strftime("%Y%m%d%H%M%S", time.localtime())))
        f.write("! Last modified: %s\n"%(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())))
        f.write("! Blocked Filters: %s\n"%(len(filterList)))
        f.write("!\n")
        for fiter in filterList:
            f.write("%s\n"%(fiter))

def Entry():
    def dictadd(d1, d2):
        d3 = dict()
        for item in d1:
            d3[item] = d1[item]
            if item in d2:
                d3[item] += d2[item]
        for item in d2:
            if item not in d1:
                d3[item] = d2[item]
        return d3
    pwd = os.getcwd()
    ruleFile = pwd + '/README.md'

    ruleList = GetRuleList(ruleFile)

    isUpdate = False
    lastUpdate = time.strftime("%Y/%m/%d", time.localtime())
    for i in range(0, len(ruleList)):
        rule = Rule(ruleList[i][0], ruleList[i][2])
        if rule.Update():
            isUpdate = True
            ruleList[i][3] = lastUpdate
    
    if isUpdate:
        blockDict = dict()
        unblockDict = dict()
        filterList = []
        for i in range(0, len(ruleList)):
            resolver = Resolver(os.getcwd() + '/rules/' + ruleList[i][0].replace(' ', '_') + '.txt')
            d1, d2, l3 = resolver.Resolve(ruleList[i][1])
            print('%s: block[%s],unblock[%s],filter[%s]'%(ruleList[i][0], len(d1), len(d2), len(l3)))
            blockDict = dictadd(blockDict, d1)
            unblockDict = dictadd(unblockDict, d2)
            filterList += l3

        # 生成合并规则
        CreatDNS(blockDict, unblockDict, pwd + '/rules/adblockdns.txt')
        CreatFiter(filterList, pwd + '/rules/adblockfilters.txt')

        # 更新README.md
    CreatReadme(ruleList, pwd + '/README.md')

if __name__ == '__main__':
    Entry()
