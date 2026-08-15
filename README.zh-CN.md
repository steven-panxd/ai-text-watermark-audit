# AI 文本水印审计

一个本地运行的 AI 文本水印审计工具。首个研究对象是 Claude，扫描器本身不绑定任何模型厂商。

[English](README.md) · [Claude 水印说明](docs/claude-watermark.md) · [方法论](docs/methodology.md) · [常见问题](docs/faq.md)

## 它解决什么问题

Anthropic 表示，受支持的 Claude 模型会在生成文本中嵌入肉眼不可见的水印。但截至目前，Anthropic 尚未公布可用于验证该统计信号的技术检测器。

因此，本项目严格区分两个问题：

1. 文档中是否存在可以直接观察到的 Unicode 或格式信号？
2. 厂商官方检测器是否验证了模型水印？

`textmark` 目前能够回答第一个问题。对于 Claude 的模型级水印，它会展示公开证据和 `not-publicly-documented` 状态，而不是猜测检测结果。

## 安装

需要 Python 3.10 或更高版本。

```bash
pipx install git+https://github.com/steven-panxd/ai-text-watermark-audit.git
```

## 使用

扫描 UTF-8 文本：

```bash
textmark scan draft.txt
```

输出 JSON，并在发现 warning 时返回非零状态码：

```bash
textmark scan draft.txt --json --fail-on warning
```

比较编辑前后的两个版本：

```bash
textmark compare original.txt edited.txt --json
```

查看带来源的厂商声明：

```bash
textmark claims
```

当前能够识别：

- 零宽字符及格式控制字符；
- 双向文本控制符；
- Unicode tag 字符；
- 非常规空格和变体选择符；
- 混合拉丁、西里尔或希腊字母的可疑单词；
- 精确位置、Unicode 名称、转义值和 SHA-256 摘要。

工具没有运行时依赖，不会上传被扫描的文本。

## 如何理解扫描结果

发现隐藏字符不代表文字由 AI 生成。排版、emoji 和部分语言本来就会合理使用不可见字符。同样，没有发现也不能证明文字由人类创作，更不能排除统计水印。

扫描结果是取证线索，不是作者身份判定。

## Claude 水印的当前状态

截至 2026 年 8 月 14 日：

- Anthropic 表示，2026 年 8 月 2 日及以后发布的 Claude 模型会在发布时支持机器可读标记；
- 更早发布的模型正在逐步加入支持；
- 受支持模型的标记全球生效；
- 面向第三方的检测技术文档尚未发布。

主要来源：[How Claude marks AI-generated content](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content)。

## 许可

[MIT](LICENSE)。本项目独立开发，与 Anthropic 或其他模型厂商不存在隶属关系。
