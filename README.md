# OiiOii Product Architecture

基于可见页面证据完成的 OiiOii 产品架构逆向分析，覆盖用户操作、专业 Agent 协作、工具与模型调用、全局上下文、媒资、状态、计费、安全和基础设施。

## 在线报告

直接访问：<https://w93139.github.io/oiioii-product-architecture/>

报告是静态网页，不需要登录或安装。页面包含响应式布局、证据图片链接以及 Mermaid 架构图。

## 结论边界

报告严格区分四类结论：

- `【已确认】`：页面、官方材料或可复现结果直接支持。
- `【合理推断】`：多项事实支持，但后台实现不可见。
- `【建议设计】`：面向未来的设计建议，不代表当前产品实现。
- `【未知】`：现有证据不足或存在冲突。

本仓库不是 OiiOii 官方项目，也不声称获得其私有源码、系统提示词、隐藏思维链或后台实现。

## 本地查看

克隆仓库后，可以直接打开 `index.html`。为了获得与 GitHub Pages 更接近的行为，也可以在仓库根目录启动本地静态服务器：

```bash
python3 -m http.server 8000
```

然后访问 <http://localhost:8000/>。

Mermaid 图通过外部 CDN 加载，因此首次渲染需要网络连接；报告正文和证据图片保存在仓库内。

## 校验

仓库提供只读校验脚本，用于检查 HTML 基本结构、目录锚点、证据文件和 Mermaid 源码是否齐全：

```bash
python3 scripts/validate_site.py
```

GitHub Actions 会在提交和拉取请求中运行同一检查。现有 Pages 发布流程保持不变。

## 目录

```text
oiioii-product-architecture/
├── .github/workflows/
├── OiiOii-拆解图片汇总/
├── LICENSE
├── README.md
├── THIRD_PARTY_NOTICES.md
├── index.html
└── scripts/
    └── validate_site.py
```

## 开源许可与第三方内容

本仓库中由维护者原创的报告文本和源代码采用 [MIT License](LICENSE)。证据截图可能包含第三方产品界面、商标、名称或生成资产，这些内容的权利仍归各自权利人所有，不因本仓库的 MIT License 自动获得再许可。详见 [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md)。
