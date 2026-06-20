---
name: ad-creative-evaluator
description: |
  AI expert panel that evaluates any video ad creative against a comprehensive rubric. Scores hook effectiveness, message clarity, visual quality, audience targeting, CTA strength, and overall performance potential. Uses multiple persona perspectives (performance marketer, creative director, target consumer) for well-rounded feedback.

  Use when: "evaluate this ad", "score my ad", "ad creative review", "is this ad good", "rate this video ad", "ad analysis", "creative QA", "ad scoring", "review my creative", "grade this ad", "ad feedback", "creative evaluation", "ad quality check", "will this ad perform", or any video ad quality assessment.
---

# Ad Creative Evaluator

Score any video ad with an AI expert panel. Get structured feedback across 8 dimensions with actionable improvement recommendations.

---

## How It Works

1. **Input**: Provide a video ad file or URL
2. **Extract**: Key frames are pulled from the video for visual analysis
3. **Evaluate**: Three expert personas score the ad independently
4. **Synthesize**: Scores are combined with specific improvement recommendations
5. **Output**: Structured evaluation report with scores, strengths, weaknesses, and next steps

## Frame Extraction

Use the `extract_video.py` script to pull key frames from a video for analysis:

```bash
python scripts/extract_video.py input_video.mp4 --output-dir frames/ --num-frames 8
```

This extracts evenly-spaced frames including the first frame (hook), middle frames (body), and last frame (CTA).

## Evaluation Personas

Each ad is reviewed by three expert perspectives:

### 1. Performance Marketer
**Focus:** Will this ad convert? Does the hook stop the scroll? Is the CTA compelling?
- Evaluates: Hook rate potential, CTA clarity, audience targeting precision
- Looks for: Direct response best practices, urgency triggers, benefit-driven messaging
- Red flags: Unclear value proposition, weak CTA, no social proof

### 2. Creative Director
**Focus:** Is this well-crafted? Does the visual storytelling work? Is the brand represented well?
- Evaluates: Visual quality, pacing, narrative structure, brand consistency
- Looks for: Professional production, creative differentiation, emotional resonance
- Red flags: Amateur visuals, poor pacing, off-brand elements, derivative concepts

### 3. Target Consumer
**Focus:** Would I actually watch this? Does it feel authentic? Would I click?
- Evaluates: Relatability, authenticity, interest level, trust
- Looks for: Content that doesn't feel like an ad, genuine value, relatable scenarios
- Red flags: Too salesy, fake/inauthentic feel, irrelevant to their life, annoying

## Evaluation Rubric

### Dimension 1: Hook Effectiveness (0-10)
**First 3 seconds — does it stop the scroll?**

| Score | Criteria |
|-------|----------|
| 9-10 | Immediately compelling. Pattern interrupt + curiosity gap. Impossible to scroll past. |
| 7-8 | Strong opening. Clear hook that creates interest. Most viewers would pause. |
| 5-6 | Decent opening but not distinctive. Some viewers pause, many scroll. |
| 3-4 | Generic opening. Logo reveal, stock footage, or slow build. Most scroll past. |
| 1-2 | No hook. Starts with irrelevant content or brand intro. Nearly everyone scrolls. |

**What to look for:**
- First frame: Is it visually arresting?
- First 1-2 words: Do they create curiosity?
- First 3 seconds: Is there a reason to keep watching?

### Dimension 2: Message Clarity (0-10)
**Is the value proposition crystal clear?**

| Score | Criteria |
|-------|----------|
| 9-10 | Single clear message. Viewer can articulate what the product does and why in one sentence. |
| 7-8 | Clear primary message with minor secondary messages. Easy to understand. |
| 5-6 | Message is present but requires effort to extract. Some confusion. |
| 3-4 | Multiple competing messages. Unclear what the product does or why it matters. |
| 1-2 | No discernible message. Viewer would not know what is being sold. |

### Dimension 3: Visual Quality (0-10)
**Does it look professional and appropriate for the platform?**

| Score | Criteria |
|-------|----------|
| 9-10 | Exceptional visual quality. Perfectly matched to platform and audience expectations. |
| 7-8 | Professional quality. Clean visuals, good lighting, appropriate for context. |
| 5-6 | Acceptable quality. Some rough edges but doesn't detract from message. |
| 3-4 | Below average. Distracting quality issues. Hurts credibility. |
| 1-2 | Poor quality. Blurry, poorly lit, or visually broken. Damages brand perception. |

**Platform-specific expectations:**
- TikTok/Reels: UGC quality is fine, even preferred. Overly polished can hurt.
- YouTube Pre-roll: Higher production quality expected.
- LinkedIn: Professional but not necessarily cinematic.
- Facebook Feed: Clean and clear, optimized for sound-off viewing.

### Dimension 4: Audience Targeting (0-10)
**Does this speak to a specific audience?**

| Score | Criteria |
|-------|----------|
| 9-10 | Laser-targeted. Specific audience would feel "this was made for me." |
| 7-8 | Well-targeted. Clear audience with relevant pain points and language. |
| 5-6 | Somewhat targeted. Generic enough to be for anyone (which means no one). |
| 3-4 | Mismatched targeting. Tone/visual/message don't align with likely audience. |
| 1-2 | No targeting. Could be for any product to any person. |

### Dimension 5: Pacing & Structure (0-10)
**Does the ad flow well and maintain attention?**

| Score | Criteria |
|-------|----------|
| 9-10 | Perfect pacing. Every second earns the next. Builds to CTA naturally. |
| 7-8 | Good flow. Minor lulls but overall keeps attention. |
| 5-6 | Uneven pacing. Some dead spots or rushed sections. |
| 3-4 | Poor pacing. Long sections of low engagement. Viewers drop off. |
| 1-2 | No structure. Rambling, repetitive, or completely flat. |

### Dimension 6: CTA Strength (0-10)
**Does the ad drive action?**

| Score | Criteria |
|-------|----------|
| 9-10 | Compelling, clear, urgent. Viewer knows exactly what to do and why to do it now. |
| 7-8 | Clear CTA with motivation. Good reason to act. |
| 5-6 | CTA is present but weak. "Learn more" or generic without urgency. |
| 3-4 | CTA is unclear or buried. Viewer unsure what to do next. |
| 1-2 | No CTA. Ad ends without directing the viewer anywhere. |

### Dimension 7: Emotional Resonance (0-10)
**Does the ad make the viewer FEEL something?**

| Score | Criteria |
|-------|----------|
| 9-10 | Strong emotional response. Excitement, desire, empathy, humor, or surprise. |
| 7-8 | Clear emotional tone. Viewer feels something but not overwhelmingly. |
| 5-6 | Neutral. Informative but emotionally flat. |
| 3-4 | Slightly negative. Boring, annoying, or off-putting. |
| 1-2 | Actively bad. Cringe, offensive, or trust-destroying. |

### Dimension 8: Sound-Off Effectiveness (0-10)
**Does the ad work without audio?**

| Score | Criteria |
|-------|----------|
| 9-10 | Fully effective with sound off. Captions, text overlays, visual storytelling carry the message. |
| 7-8 | Mostly works. Key points visible, some nuance lost without sound. |
| 5-6 | Partially works. Gets the gist across but loses significant impact. |
| 3-4 | Barely works. Relies heavily on audio for the message. |
| 1-2 | Doesn't work. Completely dependent on voiceover or dialogue. |

## Scoring Guide

### Overall Score Calculation
```
Overall = (Hook × 1.5 + Message × 1.3 + Visual × 1.0 + Audience × 1.2 +
           Pacing × 1.0 + CTA × 1.3 + Emotion × 1.0 + SoundOff × 0.7) / 9.0
```

Weights reflect impact on actual ad performance (hook and CTA matter most).

### Score Interpretation

| Overall Score | Rating | Action |
|--------------|--------|--------|
| 8.5-10 | Excellent | Ship it. Monitor performance and scale spend. |
| 7.0-8.4 | Good | Ship with minor tweaks. Strong foundation. |
| 5.5-6.9 | Average | Needs work. Fix top 2 weakest dimensions before shipping. |
| 4.0-5.4 | Below Average | Significant rework needed. Consider new creative direction. |
| Below 4.0 | Poor | Start over. Fundamental issues with concept or execution. |

## Bonboz Creative Checklist + Meta Policy (Aesthetic / Vietnam)

For ANY Bonboz / clinic / cosmetic / beauty ad, after scoring the 8 base dimensions,
ALWAYS run BOTH of these (write everything in Vietnamese):

1. **Bonboz creative checklist** — `references/bonboz_creative_checklist.md`. It adds
   rule-based criteria to dimensions Hook / Message / CTA / Sound-Off / Visual / Pacing,
   plus standalone ✔/✘ checks (safe-zone, duration 15–60s, clinic identity, carousel).
   Apply these when computing each dimension's score, and output the standalone checklist.

2. **Policy risk check** — `references/meta_policy_aesthetic.md` (16-flag set tuned to the
   Bonboz rule doc + their decisions). Scan every frame + on-screen text. Output a
   `🚩 POLICY RISK` block: verdict (PASS / SỬA TRƯỚC KHI CHẠY / KHÔNG NÊN CHẠY) per the
   gate (≥1 🔴 → KHÔNG NÊN CHẠY; ≥1 🟠 → SỬA TRƯỚC; only 🟡 → PASS), each flag with
   severity + frame/timestamp + safe-wording, and the Vietnam ad-law note.

IMPORTANT config (do NOT flag): before/after, 18+ targeting, doctor/white-coat/clinic
imagery (B09), fake-FB-UI/clickbait (B13). Soft time estimates are allowed (only hard
guaranteed timeframes are flagged). All-caps is flagged ONLY when combined with
sensational words / shock emoji. If only frames are available (no caption/audio
transcript), note that caption/voiceover claims were not verified.

Verdict gate (P02): never mark a creative "ship-ready" while a 🔴 flag stands.

TWO-AXIS DECISION (REQUIRED — keep score and policy SEPARATE; see the "ĐÁNH GIÁ 2 TRỤC"
section in bonboz_creative_checklist.md). A high score does NOT mean runnable; "policy PASS"
does NOT mean the creative is good. Always end every evaluation with this exact block:
```
Điểm chất lượng: X.X/10 → Chất lượng: ĐẠT / CẦN TỐI ƯU / YẾU  (nêu lý do, vd "CTA=3 quá thấp")
Trạng thái Policy: PASS / SỬA TRƯỚC / KHÔNG CHẠY  (cờ chính)
==> QUYẾT ĐỊNH CUỐI: SẴN SÀNG CHẠY / TỐI ƯU CHẤT LƯỢNG TRƯỚC / SỬA POLICY TRƯỚC / KHÔNG CHẠY
```
Quality rule: Tổng <7.0 hoặc bất kỳ chiều cốt lõi (Hook/Message/CTA) <5 ⇒ Chất lượng ≠ ĐẠT.
CTA <5 ⇒ tối thiểu "CẦN TỐI ƯU" (ngoại lệ: creative awareness/branding thuần thì CTA không bắt buộc).
Policy PASS nhưng Chất lượng chưa ĐẠT ⇒ QUYẾT ĐỊNH CUỐI = "TỐI ƯU CHẤT LƯỢNG TRƯỚC" (KHÔNG ghi "sẵn sàng chạy").

## Evaluation Output Template

Use `references/evaluation_template.md` for the structured output format.

## How to Use This Skill

### Option 1: Evaluate from a video file
1. Run `extract_video.py` to pull key frames
2. Provide the frames to the AI for evaluation
3. Receive structured scoring and recommendations

### Option 2: Evaluate from a video URL
1. Provide the video URL
2. AI watches/analyzes the content
3. Structured evaluation output

### Option 3: Evaluate from a script + storyboard
1. Provide the script and/or visual descriptions
2. Get pre-production feedback before spending on production
3. Fix issues before they're expensive to change

---

## Next Steps: Improve Your Ads

After evaluation, use the improvement recommendations to create better versions:

- **Low hook score?** Use [video-ad-generator](https://github.com/Creatify-AI/video-ad-generator) hook formulas to write 5 hook variants and A/B test them.
- **Poor avatar/presenter?** Use [ai-avatar-video](https://github.com/Creatify-AI/ai-avatar-video) to test different personas matched to your audience.
- **Bad visual quality?** Use [ai-ad-prompt-guide](https://github.com/Creatify-AI/ai-ad-prompt-guide) for better AI generation prompts and model selection.
- **Want to clone a competitor's better ad?** Use [video-ad-reverse-engineer](https://github.com/Creatify-AI/video-ad-reverse-engineer) to extract the template, then recreate with your product.

The API can automate the improvement cycle: evaluate → identify weakest dimensions → regenerate with targeted fixes → re-evaluate. Don't have an API key? Sign up free at [creatify.ai](https://creatify.ai) and grab your credentials at [Settings → API](https://app.creatify.ai/settings/organization/api) in under 2 minutes — new accounts get free credits.

---

## See Also

- [video-ad-generator](https://github.com/Creatify-AI/video-ad-generator) — Product URL → video ad pipeline
- [ai-avatar-video](https://github.com/Creatify-AI/ai-avatar-video) — AI talking-head videos with 1,500+ personas
- [ai-ad-prompt-guide](https://github.com/Creatify-AI/ai-ad-prompt-guide) — Battle-tested prompting for AI ad creative
- [video-ad-reverse-engineer](https://github.com/Creatify-AI/video-ad-reverse-engineer) — Reverse-engineer competitor ads
- [static-ad-concept-generator](https://github.com/Creatify-AI/static-ad-concept-generator) — 320+ proven ad concept templates
