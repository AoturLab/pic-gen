# pic-gen

**AI 图片生成与提示词优化工具** — 一个 Skill，支持通义万相、Banana (Flux)、DALL-E 3 多模型。

## 功能

- ✨ **提示词优化**：输入简单描述，自动生成各平台最优提示词
- 🎨 **多模型支持**：通义万相、Banana/Flux、DALL-E 3，一个 Skill 搞定
- 🔑 **密钥管理**：对话中直接发送 API Key，自动写入配置
- 💬 **对话式交互**：像和产品经理对话一样，一步一步引导生成
- 📋 **格式覆盖**：Midjourney / Stable Diffusion / Flux / DALL-E / 通义万相

## 支持平台

| 模型 | 平台 | 说明 |
|---|---|---|
| 通义万相 | `qwen` | 阿里云 DashScope API，默认模型 |
| Banana / Flux | `banana` | 开源 Flux 模型 |
| DALL-E 3 | `dalle` | OpenAI API |

## 快速开始

### 1. 安装 Skill

```bash
clawhub install pic-gen
```

### 2. 配置 API Key

**方式 A**：手动编辑 `config/models.yaml`：

```yaml
default: qwen
models:
  qwen:
    enabled: true
    api_key: "your-dashscope-key"
    model: "qwen-image-2.0-pro"
```

**方式 B**：在对话中直接发送 API Key，Bot 自动写入配置。

### 3. 开始使用

在支持 OpenClaw 的聊天界面（如 Discord），直接说：

```
画一只在月球上弹吉他的猫
```

Bot 会：
1. 优化提示词（多平台版本展示）
2. 询问用哪个模型（或使用默认）
3. 生成图片

## 命令示例

```
# 直接生成（用默认模型）
画一个赛博朋克城市

# 指定模型
用 banana 生成 梵高风格的向日葵

# 优化已有提示词
优化这个提示词：a beautiful sunset

# 切换默认模型
设置默认模型为 dalle

# 更新 API Key
更新通义 key 为 sk-xxxxx
```

## 目录结构

```
pic-gen/
├── SKILL.md                  # Skill 定义文件（AI 读取）
├── config/
│   └── models.yaml           # 模型配置（API Key 在此）
├── scripts/
│   ├── optimize.py           # 提示词优化核心
│   ├── generate_qwen.py      # 通义万相生成器
│   ├── generate_banana.py    # Banana/Flux 生成器
│   ├── generate_dalle.py     # DALL-E 生成器
│   └── update_config.py      # 配置管理工具
└── references/
    ├── midjourney.md         # MJ 格式参考
    ├── stable-diffusion.md   # SD 格式参考
    ├── flux.md               # Flux 格式参考
    └── dalle.md              # DALL-E 格式参考
```

## 提示词优化原理

输入简单描述后，Skill 自动补全以下维度：

| 维度 | 示例 |
|---|---|
| 主体细节 | 「猫」→「橘猫，坐姿，眯眼打盹」 |
| 场景背景 | 「在户外」→「京都寺庙庭院，春日午后」 |
| 风格 | 「好看」→「宫崎骏动画风格」 |
| 光影 | 「亮」→「逆光，金色边缘光」 |
| 构图 | 「拍猫」→「低角度平视，浅景深」 |
| 技术参数 | 平台专属参数 |

## 开发

```bash
# 优化提示词（本地测试）
python3 pic-gen/scripts/optimize.py -i "一只猫" -p all

# 生成图片
python3 pic-gen/scripts/generate_qwen.py -p "一只猫" --download -o ./output

# 配置管理
python3 pic-gen/scripts/update_config.py show
python3 pic-gen/scripts/update_config.py set-key qwen your-key
```

## 发布到 ClawHub

```bash
clawhub publish ./pic-gen --slug pic-gen --name "pic-gen" --version 1.0.0
```

## License

MIT
