# pic-gen

**AI Image Generation & Prompt Optimizer** — An OpenClaw Skill that supports multiple image generation models including Qwen Wanxiang (通义万相), Banana (Flux), and DALL-E 3.

## Features

- ✨ **Prompt Optimization**: Convert simple descriptions into professional-grade prompts for any platform
- 🎨 **Multi-Model Support**: Qwen Wanxiang, Banana/Flux, DALL-E 3 — one Skill to rule them all
- 🔑 **API Key Management**: Send API keys directly in chat, auto-saved to config
- 💬 **Conversational Interface**: Step-by-step guidance like talking to a product manager
- 📋 **Format Coverage**: Midjourney / Stable Diffusion / Flux / DALL-E / Qwen Wanxiang

## Supported Platforms

| Model | ID | Description |
|---|---|---|
| Qwen Wanxiang | `qwen` | Alibaba Cloud DashScope API, default |
| Banana / Flux | `banana` | Open-source Flux models |
| DALL-E 3 | `dalle` | OpenAI API |

## Quick Start

### 1. Install

```bash
clawhub install pic-gen
```

### 2. Configure API Key

**Option A**: Edit `pic-gen/config/models.yaml` manually:

```yaml
default: qwen
models:
  qwen:
    enabled: true
    api_key: "your-dashscope-key"
    model: "qwen-image-2.0-pro"
```

**Option B**: Send the key directly in chat — the Bot writes it to config automatically.

**Option C**: Use environment variables (recommended — keeps keys out of config files):

```bash
export DASHSCOPE_API_KEY="sk-xxxxxxxx"
export BANANA_API_KEY="your-banana-key"
export OPENAI_API_KEY="sk-xxxxxxxx"
```

### 3. Start Using

In any OpenClaw-enabled chat (Discord, etc.):

```
Draw a cat on the moon
```

Bot will:
1. Optimize the prompt (multi-platform versions shown)
2. Ask which model to use (or use default)
3. Generate and return the image

## Project Structure

```
pic-gen/
├── SKILL.md                  # Skill definition (AI reads this)
├── config/
│   └── models.yaml           # Model config (API keys here)
├── scripts/
│   ├── optimize.py           # Core prompt optimizer
│   ├── generate_qwen.py      # Qwen Wanxiang generator
│   ├── generate_banana.py   # Banana/Flux generator
│   ├── generate_dalle.py    # DALL-E generator
│   └── update_config.py      # Config management tool
└── references/
    ├── midjourney.md         # MJ format guide
    ├── stable-diffusion.md   # SD format guide
    ├── flux.md              # Flux format guide
    └── dalle.md            # DALL-E format guide
```

## Prompt Optimization Strategy

### Scene-Aware Lighting

Automatically matches lighting/mood to your scene:

| Scene | Qwen Wanxiang | Midjourney |
|---|---|---|
| Rainy night | rain beams, wet texture, neon reflections | neon reflections on wet streets |
| Cyberpunk | neon lights, cyber effects, cold tones | neon + cyberpunk atmosphere |
| Night / stars | moonlight, starburst, deep night sky | neon + night atmosphere |
| Sunrise / sunset | golden hour, warm tones, soft backlight | golden hour + warm tones |
| Forest / nature | natural light, dappled light, fresh vibe | natural sunlight + dappled |
| Cafe / interior | natural + soft light, cozy | warm interior + cozy |

### Artist Style Detection

| Style | Qwen Wanxiang Boost | Midjourney Boost |
|---|---|---|
| Van Gogh / oil painting | bold colors, brushstroke texture | Van Gogh inspired, bold brushstrokes |
| Ghibli / anime | anime style, soft tones, Ghibli lighting | Studio Ghibli, dreamy atmosphere |
| Pixar / 3D cartoon | 3D animation, Pixar texture | Pixar 3D animation style |

### Example Output

**Input**: "Van Gogh-style sunflower field"

```
🎨 Midjourney:
"Van Gogh-style sunflower field, cinematic photography, shot on Canon EOS R5,
post-impressionist art style, Van Gogh inspired, bold colors,
visible brushstrokes, --ar 16:9 --s 400 --v 6"

🖼️ DALL-E 3:
"Van Gogh 风格的向日葵花田, vivid colors, high detail,
professional photography, highly detailed, perfect composition"

⚡ Qwen Wanxiang:
"梵高风格的向日葵花田，细节丰富，高品质，浓烈色彩，笔触感，后印象派风格，厚涂感"
```

## ⚠️ API Key Security

- **Never** share config files containing real API keys on GitHub, Discord, or any public channel
- `config/models.yaml` is gitignored — make sure api_key fields are empty before committing
- If a key is leaked, regenerate it immediately in the platform console

## Dev Commands

```bash
# Optimize prompt (local test)
python3 pic-gen/scripts/optimize.py -i "a cat" -p all

# Generate image
python3 pic-gen/scripts/generate_qwen.py -p "a cat" --download -o ./output

# Config management
python3 pic-gen/scripts/update_config.py show
python3 pic-gen/scripts/update_config.py set-key qwen your-key
```

## Publish to ClawHub

```bash
clawhub publish ./pic-gen --slug pic-gen --name "pic-gen" --version 1.0.0
```

## Links

- **GitHub**: https://github.com/AoturLab/pic-gen
- **ClawHub**: https://clawhub.com/skills/pic-gen

## License

MIT
