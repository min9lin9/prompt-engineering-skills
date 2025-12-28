# 프롬프트 엔지니어링 스킬

> **모델 순위**: [LMArena Leaderboard](https://lmarena.ai) 기반 (2025년 12월 기준)

Claude Code, ChatGPT GPTs, Gemini Gems를 위한 종합 AI 프롬프트 엔지니어링 스킬 모음입니다.

---

## 바로 사용하기

설정 없이 바로 사용할 수 있는 링크입니다:

| 플랫폼 | 링크 |
|--------|------|
| **ChatGPT GPTs** | [두부경 종합 프롬프트 생성기](https://chatgpt.com/g/g-694feb6bf18481918acd876e3c3eed37-tofukyung-jonghab-peurompeuteu-saengseonggi) |
| **Gemini Gems** | [프롬프트 생성기 Gem](https://gemini.google.com/gem/1yY760AO5nQsnBs4kGTdxAJXdQRAIDdOD?usp=sharing) |

---

## 개요

이 저장소는 다음 모델에 최적화된 프롬프트 엔지니어링 자료를 제공합니다:

| 모델 | 커버리지 |
|------|----------|
| **GPT-5.2 / GPT-5.2-Codex** | XML 패턴, reasoning_effort, Compaction |
| **Claude 4.5 (Opus/Sonnet/Haiku)** | 명시적 지시, Extended Thinking |
| **Gemini 3** | Constraints First, 멀티모달 컨텍스트 |
| **Veo 3.1** | 오디오 포함 동영상 생성 |
| **Gemini Image** | 이미지 생성 |

### 목적별 추천 모델 (LMArena 기준)

> 출처: [LMArena Leaderboard](https://lmarena.ai) - 사용자 투표 기반 순위

| 목적 | 1순위 | 2순위 | 3순위 |
|------|-------|-------|-------|
| **코딩/개발** | Claude Opus 4.5 | GPT-5.2 | Gemini 3 Pro |
| **수학/논리** | GPT-5.2 | Gemini 3 Flash | Claude Opus 4.5 |
| **글쓰기/창작** | Gemini 3 Pro | Gemini 3 Flash | Claude Opus 4.5 |
| **이미지 생성** | GPT Image 1.5 | Gemini 3 Pro Image | Flux 2 Max |
| **동영상 생성** | Veo 3.1 | Sora 2 Pro | Veo 3 |
| **웹 검색/리서치** | Gemini 3 Pro Grounding | GPT-5.2 Search | GPT-5.1 Search |
| **팩트체크** | **GPT-5.2 Thinking** | Gemini 3 Pro Grounding | Perplexity Sonar Pro |

---

## 저장소 구조

```
prompt-engineering-skills/
├── README.md                           # 이 파일
├── LICENSE                             # MIT 라이선스
│
├── skills/                             # 핵심 스킬 파일
│   ├── prompt-engineering-guide.md     # 모델별 프롬프트 전략
│   ├── image-prompt-guide.md           # 이미지 생성 가이드
│   ├── gpt-5.2-prompt-enhancement.md   # GPT-5.2 전용 패턴
│   ├── claude-4.5-prompt-strategies.md # Claude 4.5 전용 전략
│   ├── gemini-prompt-strategies.md     # Gemini/Veo/Nano Banana 전략
│   └── context-engineering-collection.md  # CE 원칙
│
├── commands/                           # Claude Code 커맨드
│   └── prompt.md                       # /prompt 커맨드
│
├── instructions/                       # GPTs/Gems 시스템 프롬프트
│   ├── GPTs-Prompt-Generator.md        # ChatGPT GPTs용
│   └── Gems-Prompt-Generator.md        # Gemini Gems용
│
└── examples/                           # 사용 예시
    ├── gpt-5.2-examples.md
    ├── claude-4.5-examples.md
    └── image-generation-examples.md
```

---

## 직접 설정하기

### Claude Code 사용자

스킬 파일을 `.claude/skills/` 디렉토리에 복사:

```bash
cp skills/*.md ~/.claude/skills/
cp commands/*.md ~/.claude/commands/
```

그 후 Claude Code에서 `/prompt` 커맨드 사용.

### ChatGPT GPTs 직접 만들기

1. [GPT Editor](https://chat.openai.com/gpts/editor) 접속
2. `skills/` 폴더의 파일을 **Knowledge**에 업로드
3. `instructions/GPTs-Prompt-Generator.md` 내용을 **Instructions**에 붙여넣기

### Gemini Gems 직접 만들기

1. [Gems 설정](https://gemini.google.com/gems) 접속
2. `skills/` 폴더의 파일을 **지식 파일**에 업로드
3. `instructions/Gems-Prompt-Generator.md` 내용을 **지침**에 붙여넣기

---

## 핵심 스킬

### prompt-engineering-guide.md

메인 스킬 파일:
- 모델별 프롬프트 전략
- 각 모델의 필수 XML 블록
- Context Engineering 원칙
- 목적별 템플릿
- 품질 체크리스트

### image-prompt-guide.md

공냥이(@specal1849)님의 자료를 기반으로 한 종합 이미지 생성 가이드:
- 시그널(Signal)과 신뢰도(Faithful) 개념
- 프롬프트 형식 비교 (JSON/XML/Markdown/자연어)
- 스타일별 템플릿 (제품/푸드/패션/캐릭터 등)
- 조명 및 카메라 기법
- 인포그래픽 제작 가이드

### context-engineering-collection.md

[Agent Skills for Context Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering)을 기반으로 한 Context Engineering 원칙:
- Attention Budget 관리
- 컨텍스트 저하 방지
- 멀티 에이전트 패턴
- 도구 설계 원칙

---

## 지원 모델

### GPT-5.2 / GPT-5.2-Codex

| 기능 | 패턴 |
|------|------|
| 장황함 제어 | `<output_verbosity_spec>` |
| 범위 제약 | `<design_and_scope_constraints>` |
| 불확실성 처리 | `<uncertainty_and_ambiguity>` |
| 도구 사용 | `<tool_usage_rules>` |

**Codex 핵심 원칙**: "Less is More" - 최소한의 프롬프팅이 최적

### Claude 4.5

| 기능 | 패턴 |
|------|------|
| 기본 행동 | `<default_to_action>` |
| 명시적 지시 | 모든 행동에 필수 |
| Extended Thinking | 복잡한 추론 시 활성화 |
| 병렬 도구 호출 | `<use_parallel_tool_calls>` |

### Gemini 3 / Veo 3.1 / Gemini Image

| 기능 | 패턴 |
|------|------|
| Constraints First | 제약 조건을 최상단에 배치 |
| Temperature | 1.0 권장 |
| 멀티모달 | 이미지/오디오 컨텍스트 네이티브 지원 |
| Veo 오디오 | 대화, 음향효과, 배경음 |

---

## 크레딧

### 이미지 프롬프트 가이드

[공냥이 (@specal1849)](https://threads.net/@specal1849)님의 자료 기반:
- [Image Prompt 101 슬라이드](https://docs.google.com/presentation/d/1rPQVnbu1INJyUAqCvMA7dkO2WzJpD4Q9q_UXq9RH2GU/edit)
- [PRO Image Prompt Notion](https://fascinated-alley-b43.notion.site/PRO-2b1861d1faaf80b8bf7ef4093827f59b)

### 컨텍스트 엔지니어링

Muratcan Koylan의 [Agent Skills for Context Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) 기반

### 모델 문서

OpenAI, Anthropic, Google 공식 문서 참조

---

## 라이선스

MIT License - [LICENSE](./LICENSE) 참조

---

## 기여

기여를 환영합니다! PR 제출 전 기여 가이드라인을 확인해 주세요.

---

## 버전

- **현재**: 1.3.0
- **최종 업데이트**: 2025-12-28
- **변경사항 v1.3.0**:
  - 검색/리서치 모델 추천 추가 (Search Arena 기준)
  - 팩트체크: GPT-5.2 Thinking 고정 추천
  - research-prompt-guide.md 스킬 파일 추가
- **변경사항 v1.2.0**:
  - 빠른 프리셋 제거 → LMArena 기반 목적별 추천으로 대체
  - 모든 문서에 LMArena 출처 명시

---

---

# Prompt Engineering Skills

> **Model Rankings**: Based on [LMArena Leaderboard](https://lmarena.ai) (December 2025)

A comprehensive collection of AI prompt engineering skills for Claude Code, ChatGPT GPTs, and Gemini Gems.

---

## Use Instantly

Use these links without any setup:

| Platform | Link |
|----------|------|
| **ChatGPT GPTs** | [Tofukyung Comprehensive Prompt Generator](https://chatgpt.com/g/g-694feb6bf18481918acd876e3c3eed37-tofukyung-jonghab-peurompeuteu-saengseonggi) |
| **Gemini Gems** | [Prompt Generator Gem](https://gemini.google.com/gem/1yY760AO5nQsnBs4kGTdxAJXdQRAIDdOD?usp=sharing) |

---

## Overview

This repository provides production-ready prompt engineering resources optimized for:

| Model | Coverage |
|-------|----------|
| **GPT-5.2 / GPT-5.2-Codex** | XML patterns, reasoning_effort, Compaction |
| **Claude 4.5 (Opus/Sonnet/Haiku)** | Explicit instructions, Extended Thinking |
| **Gemini 3** | Constraints First, multimodal context |
| **Veo 3.1** | Video generation with audio |
| **Gemini Image** | Image generation |

### Recommended Models by Purpose (LMArena)

> Source: [LMArena Leaderboard](https://lmarena.ai) - User voting based rankings

| Purpose | 1st | 2nd | 3rd |
|---------|-----|-----|-----|
| **Coding/Dev** | Claude Opus 4.5 | GPT-5.2 | Gemini 3 Pro |
| **Math/Logic** | GPT-5.2 | Gemini 3 Flash | Claude Opus 4.5 |
| **Writing/Creative** | Gemini 3 Pro | Gemini 3 Flash | Claude Opus 4.5 |
| **Image Generation** | GPT Image 1.5 | Gemini 3 Pro Image | Flux 2 Max |
| **Video Generation** | Veo 3.1 | Sora 2 Pro | Veo 3 |
| **Web Search/Research** | Gemini 3 Pro Grounding | GPT-5.2 Search | GPT-5.1 Search |
| **Fact-Check** | **GPT-5.2 Thinking** | Gemini 3 Pro Grounding | Perplexity Sonar Pro |

---

## Repository Structure

```
prompt-engineering-skills/
├── README.md                           # This file
├── LICENSE                             # MIT License
│
├── skills/                             # Core skill files
│   ├── prompt-engineering-guide.md     # Multi-model prompt strategies
│   ├── image-prompt-guide.md           # Image generation guide
│   ├── gpt-5.2-prompt-enhancement.md   # GPT-5.2 specific patterns
│   ├── claude-4.5-prompt-strategies.md # Claude 4.5 specific strategies
│   ├── gemini-prompt-strategies.md     # Gemini/Veo/Nano Banana strategies
│   └── context-engineering-collection.md  # CE principles
│
├── commands/                           # Claude Code commands
│   └── prompt.md                       # /prompt command
│
├── instructions/                       # GPTs/Gems system prompts
│   ├── GPTs-Prompt-Generator.md        # For ChatGPT GPTs
│   └── Gems-Prompt-Generator.md        # For Gemini Gems
│
└── examples/                           # Usage examples
    ├── gpt-5.2-examples.md
    ├── claude-4.5-examples.md
    └── image-generation-examples.md
```

---

## Setup Your Own

### For Claude Code Users

Copy skill files to your `.claude/skills/` directory:

```bash
cp skills/*.md ~/.claude/skills/
cp commands/*.md ~/.claude/commands/
```

Then use the `/prompt` command in Claude Code.

### Create Your Own ChatGPT GPTs

1. Go to [GPT Editor](https://chat.openai.com/gpts/editor)
2. Upload files from `skills/` to **Knowledge**
3. Paste `instructions/GPTs-Prompt-Generator.md` into **Instructions**

### Create Your Own Gemini Gems

1. Go to [Gems Settings](https://gemini.google.com/gems)
2. Upload files from `skills/` to **Knowledge files**
3. Paste `instructions/Gems-Prompt-Generator.md` into **Instructions**

---

## Core Skills

### prompt-engineering-guide.md

The main skill file covering:
- Model-specific prompt strategies
- Required XML blocks for each model
- Context Engineering principles
- Purpose-specific templates
- Quality checklists

### image-prompt-guide.md

Comprehensive image generation guide based on [@specal1849](https://threads.net/@specal1849)'s work:
- Signal and Faithful concepts
- Prompt format comparison (JSON/XML/Markdown/Natural language)
- Style templates (Product, Food, Fashion, Character, etc.)
- Lighting and camera techniques
- Infographic creation guide

### context-engineering-collection.md

Context Engineering principles based on [Agent Skills for Context Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering):
- Attention budget management
- Context degradation prevention
- Multi-agent patterns
- Tool design principles

---

## Supported Models

### GPT-5.2 / GPT-5.2-Codex

| Feature | Pattern |
|---------|---------|
| Verbosity Control | `<output_verbosity_spec>` |
| Scope Constraints | `<design_and_scope_constraints>` |
| Uncertainty Handling | `<uncertainty_and_ambiguity>` |
| Tool Usage | `<tool_usage_rules>` |

**Codex Key Principle**: "Less is More" - minimal prompting works best

### Claude 4.5

| Feature | Pattern |
|---------|---------|
| Action by Default | `<default_to_action>` |
| Explicit Instructions | Required for all behaviors |
| Extended Thinking | Enable for complex reasoning |
| Parallel Tool Calls | `<use_parallel_tool_calls>` |

### Gemini 3 / Veo 3.1 / Gemini Image

| Feature | Pattern |
|---------|---------|
| Constraints First | Place constraints at the top |
| Temperature | 1.0 recommended |
| Multimodal | Native image/audio context |
| Veo Audio | Dialogue, sound effects, ambient |

---

## Credits

### Image Prompt Guide

Based on materials by [공냥이 (@specal1849)](https://threads.net/@specal1849):
- [Image Prompt 101 Slides](https://docs.google.com/presentation/d/1rPQVnbu1INJyUAqCvMA7dkO2WzJpD4Q9q_UXq9RH2GU/edit)
- [PRO Image Prompt Notion](https://fascinated-alley-b43.notion.site/PRO-2b1861d1faaf80b8bf7ef4093827f59b)

### Context Engineering

Based on [Agent Skills for Context Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering) by Muratcan Koylan.

### Model Documentation

Official docs from OpenAI, Anthropic, Google

---

## License

MIT License - see [LICENSE](./LICENSE)

---

## Contributing

Contributions welcome! Please read the contributing guidelines before submitting PRs.

---

## Version

- **Current**: 1.3.0
- **Last Updated**: 2025-12-28
- **Changes v1.3.0**:
  - Added search/research model recommendations (Search Arena)
  - Fact-check: GPT-5.2 Thinking fixed recommendation
  - Added research-prompt-guide.md skill file
- **Changes v1.2.0**:
  - Removed fast presets → Replaced with LMArena-based recommendations
  - Added LMArena source attribution to all documentation
