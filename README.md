# Bonboz Evaluation Creative

> Skill chấm creative (ảnh/video) ads Meta TRƯỚC khi chạy — rubric 8 chiều + bộ rule riêng của Bonboz Clinic (16 cờ policy thẩm mỹ + checklist).

**Bonboz tuỳ biến** từ [creatify-ai/ad-creative-evaluator](https://github.com/creatify-ai/ad-creative-evaluator) (MIT). Bổ sung:
- `references/meta_policy_aesthetic.md` — 16 cờ policy theo BỘ RULE Bonboz (19/06/2026). KHÔNG cờ: before/after, 18+, hình bác sĩ, fake UI.
- `references/bonboz_creative_checklist.md` — gắn rule vào rubric 8 chiều + check safe-zone/duration/định danh.

> Score any video ad with an AI expert panel — performance marketer, creative director, and target consumer.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Skill](https://img.shields.io/badge/Claude-Agent_Skill-blueviolet)](https://docs.anthropic.com)

## What This Does

Get structured, actionable feedback on any video ad creative. Three AI expert personas evaluate your ad across 8 weighted dimensions and produce a detailed report with scores, strengths, weaknesses, and specific improvement recommendations.

## Quick Install

```bash
# Clone into your Claude skills directory
git clone https://github.com/Creatify-AI/ad-creative-evaluator.git ~/.claude/skills/ad-creative-evaluator
```

## What's Inside

| Feature | Description |
|---------|-------------|
| 3 Expert Personas | Performance Marketer, Creative Director, Target Consumer |
| 8-Dimension Rubric | Hook, Message, Visual, Audience, Pacing, CTA, Emotion, Sound-Off |
| Weighted Scoring | Hook and CTA weighted highest (they matter most for performance) |
| Frame Extraction Script | Python script to pull key frames from video files |
| Evaluation Template | Structured output format with persona disagreement analysis |
| Improvement Workflow | Links evaluation findings to specific next-step tools |

## Standalone Features

### Expert Panel Evaluation
Every ad is reviewed from three perspectives — a performance marketer asking "will this convert?", a creative director asking "is this well-crafted?", and a target consumer asking "would I actually watch this?". When these personas disagree, it reveals the most actionable insights.

### 8-Dimension Rubric
Comprehensive scoring across Hook Effectiveness, Message Clarity, Visual Quality, Audience Targeting, Pacing & Structure, CTA Strength, Emotional Resonance, and Sound-Off Effectiveness. Each dimension has clear 1-10 criteria.

### Frame Extraction
Python script (`scripts/extract_video.py`) extracts key frames from any video file — first frame (hook), evenly-spaced body frames, and last frame (CTA) — for visual analysis.

## API Automation

After evaluation, automate the improvement cycle:

- Low hook score? Generate 5 hook variants with URL-to-Video
- Wrong avatar? Test new personas with AI Avatar API
- Need better visuals? Use Asset Generator for higher-quality B-roll
- Clone a better competitor ad? Use Ad Clone with your product

### 🔑 Getting Your API Key

Getting set up takes less than 2 minutes:

1. Create a free account at [creatify.ai](https://creatify.ai)
2. Head to [Settings → API](https://app.creatify.ai/settings/organization/api)
3. Copy your **API ID** and **API Key**
4. You're ready to go — the other skills in this series include full code examples

New accounts include free credits so you can try everything out before committing.

## File Structure

```
ad-creative-evaluator/
├── SKILL.md                         # Main skill (install this)
├── scripts/
│   └── extract_video.py             # Frame extraction utility
├── references/
│   ├── personas.md                  # Expert persona definitions
│   ├── rubric.md                    # Scoring rubric quick reference
│   └── evaluation_template.md       # Structured output template
├── README.md
└── LICENSE
```

## See Also

- [video-ad-generator](https://github.com/Creatify-AI/video-ad-generator) — Product URL → video ad pipeline
- [ai-avatar-video](https://github.com/Creatify-AI/ai-avatar-video) — AI talking-head videos with 1,500+ personas
- [ai-ad-prompt-guide](https://github.com/Creatify-AI/ai-ad-prompt-guide) — Battle-tested prompting for AI ad creative
- [video-ad-reverse-engineer](https://github.com/Creatify-AI/video-ad-reverse-engineer) — Reverse-engineer competitor ads
- [static-ad-concept-generator](https://github.com/Creatify-AI/static-ad-concept-generator) — 320+ proven ad concept templates

## Contributing

PRs welcome! Please open an issue first to discuss changes.

## License

MIT
