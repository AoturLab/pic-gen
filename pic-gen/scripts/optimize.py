#!/usr/bin/env python3
"""
pic-gen: 提示词优化脚本
将用户简单描述转化为各平台最优提示词
"""

import argparse
import sys
import os
import yaml

# 当前文件所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
CONFIG_PATH = os.path.join(SKILL_DIR, "config", "models.yaml")
REF_DIR = os.path.join(SKILL_DIR, "references")


def load_ref(platform: str) -> str:
    """加载平台参考文档"""
    ref_file = os.path.join(REF_DIR, f"{platform}.md")
    if os.path.exists(ref_file):
        with open(ref_file, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def optimize_for_qwen(prompt: str) -> str:
    """优化通义万相提示词"""
    ref = load_ref("stable-diffusion")  # 参考 SD 格式（qwen 和 SD 格式相近）
    # 通义万相支持中英文，直接优化输入
    optimized = prompt.strip()
    # 检查是否缺少数质量词
    if "细节" not in optimized and "detail" not in optimized.lower():
        optimized = f"{optimized}，细节丰富，高品质"
    return optimized


def optimize_for_midjourney(prompt: str) -> str:
    """优化 Midjourney 提示词"""
    ref = load_ref("midjourney")
    optimized = prompt.strip()
    # 检查是否包含参数
    if "--ar" not in optimized:
        optimized = f"{optimized}, --ar 16:9"
    if "--s" not in optimized:
        optimized = f"{optimized} --s 250"
    return optimized


def optimize_for_stable_diffusion(prompt: str) -> str:
    """优化 Stable Diffusion 提示词"""
    ref = load_ref("stable-diffusion")
    parts = []

    # 质量标签
    quality_tags = "masterpiece, best quality, high quality, official art, extremely detailed CG unity 8k wallpaper"

    # 负面提示词
    negative_prompt = ("low quality, worst quality, normal quality, blurry, "
                       "watermark, text, signature, deformed, bad anatomy, "
                       "extra limbs, malformed limbs, bad hands, missing fingers")

    # 组装
    optimized = f"{quality_tags}, {prompt.strip()}"
    return optimized, negative_prompt


def optimize_for_flux(prompt: str) -> str:
    """优化 Flux 提示词"""
    ref = load_ref("flux")
    # Flux 偏好自然语言，不需要标签堆叠
    optimized = prompt.strip()
    # 确保有风格描述
    if "cinematic" not in optimized.lower() and "photorealistic" not in optimized.lower():
        optimized = f"{optimized}, cinematic, photorealistic"
    return optimized


def optimize_for_dalle(prompt: str) -> str:
    """优化 DALL-E 3 提示词（翻译成英文）"""
    ref = load_ref("dalle")
    # 通义万相：中英双语，保留原意并补全
    # 简单检查是否有英文，没有则加
    prompt_lower = prompt.lower()
    has_english = any(c.isascii() for c in prompt if c not in " \t\n")

    if not has_english:
        # 简单翻译（实际使用时 LLM 会做更好的翻译）
        prompt = f"{prompt}, vivid, detailed, high quality"

    optimized = prompt.strip()
    return optimized


def optimize(prompt: str, platform: str = "all") -> dict:
    """
    主优化函数

    Args:
        prompt: 用户原始描述
        platform: 目标平台 ["qwen", "midjourney", "stable_diffusion", "flux", "dalle", "all"]

    Returns:
        dict: 各平台优化结果
    """
    platforms_map = {
        "qwen": ("通义万相版", optimize_for_qwen, "⚡"),
        "midjourney": ("Midjourney 版", optimize_for_midjourney, "🎨"),
        "stable_diffusion": ("Stable Diffusion 版", optimize_for_stable_diffusion, "🖌️"),
        "flux": ("Flux 版", optimize_for_flux, "🌊"),
        "dalle": ("DALL-E 3 版", optimize_for_dalle, "🖼️"),
    }

    if platform == "all":
        results = {}
        for key, (label, func, emoji) in platforms_map.items():
            try:
                result = func(prompt)
                if isinstance(result, tuple):
                    results[key] = {"label": label, "emoji": emoji, "prompt": result[0], "negative": result[1]}
                else:
                    results[key] = {"label": label, "emoji": emoji, "prompt": result}
            except Exception as e:
                results[key] = {"label": label, "emoji": emoji, "error": str(e)}
        return results
    elif platform in platforms_map:
        label, func, emoji = platforms_map[platform]
        result = func(prompt)
        if isinstance(result, tuple):
            return {"label": label, "emoji": emoji, "prompt": result[0], "negative": result[1]}
        else:
            return {"label": label, "emoji": emoji, "prompt": result}
    else:
        return {"error": f"Unknown platform: {platform}"}


def format_output(results: dict) -> str:
    """格式化输出为可读文本"""
    lines = []
    for key, data in results.items():
        if "error" in data:
            lines.append(f"{data['emoji']} {data['label']}: 错误 - {data['error']}")
            continue
        lines.append(f"{data['emoji']} **{data['label']}**：")
        lines.append(f"「{data['prompt']}」")
        if "negative" in data:
            lines.append(f"   负面词：{data['negative']}")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="pic-gen 提示词优化器")
    parser.add_argument("--input", "-i", required=True, help="用户原始描述")
    parser.add_argument("--platform", "-p", default="all",
                        choices=["qwen", "midjourney", "stable_diffusion", "flux", "dalle", "all"],
                        help="目标平台（默认 all）")
    parser.add_argument("--format", "-f", default="text", choices=["text", "yaml", "json"],
                        help="输出格式")
    args = parser.parse_args()

    results = optimize(args.input, args.platform)

    if args.format == "text":
        print(format_output(results))
    elif args.format == "yaml":
        print(yaml.dump(results, allow_unicode=True, default_flow_style=False))
    elif args.format == "json":
        import json
        print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
