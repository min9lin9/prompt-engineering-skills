# 프롬프트 엔지니어링 통합 스킬

Claude Code, ChatGPT GPTs, Gemini Gems에서 함께 쓰는 단일 프롬프트 엔지니어링 스킬 저장소입니다.

> **현재 구조**: `skills/prompt-engineering-guide.md` 하나만 유지합니다. 기존 모델별/목적별 프롬프트 스킬은 모두 이 파일의 본문과 통합 부록으로 병합되었습니다.

## 바로 사용하기

| 플랫폼 | 링크 |
|--------|------|
| ChatGPT GPTs | [두부경 종합 프롬프트 생성기](https://chatgpt.com/g/g-694feb6bf18481918acd876e3c3eed37-tofukyung-jonghab-peurompeuteu-saengseonggi) |
| Gemini Gems | [프롬프트 생성기 Gem](https://gemini.google.com/gem/1ZV9S3vNOwExi4_yLHRJKFtpNpATPDI5d?usp=sharing) |

## 커버리지

`prompt-engineering-guide.md` 안에 다음 영역을 모두 포함합니다.

| 영역 | 포함 내용 |
|------|----------|
| GPT 5.x | GPT-5.5 outcome-first markdown, GPT-5.2/5.4 legacy XML, Codex 프롬프팅 |
| Claude 4.x | Opus 4.7 adaptive thinking, Opus 4.6 fallback, Sonnet/Haiku 패턴, XML 블록 |
| Gemini / Veo | Gemini 3.1, Gemini Flash, Veo 3.1, Nano Banana/NB2 이미지 전략 |
| 이미지 / 동영상 | JSON 구조, 시그널/신뢰도, 카메라/조명/구도, 비영어 대사 stage direction |
| 리서치 / 팩트체크 | IFCN 원칙, LoopFactChecker, QuickFactCheck, StructuredResearch 워크플로우 |
| 슬라이드 / PPT | Outline-first, 27개 비주얼 스타일, STYLE_INSTRUCTIONS, 이미지 JSON |
| 전문가 프라이밍 | 실존 전문가 지명, 도메인별 전문가 DB, 품질 수렴 루프 |
| Context Engineering | Attention budget, lost-in-middle 방지, context compression, tool design 원칙 |

## 저장소 구조

```text
prompt-engineering-skills/
|-- README.md
|-- LICENSE
|-- commands/
|   |-- prompt.md
|   `-- prompt-sync.md
|-- instructions/
|   |-- GPTs-Prompt-Generator.md
|   `-- Gems-Prompt-Generator.md
|-- skills/
|   `-- prompt-engineering-guide.md
`-- examples/
    |-- claude-4.5-examples.md
    |-- gpt-5.4-examples.md
    `-- image-generation-examples.md
```

## 설치

### Claude Code 글로벌 설치

```bash
git clone https://github.com/treylom/prompt-engineering-skills.git /tmp/pes && mkdir -p ~/.claude/skills ~/.claude/commands && cp /tmp/pes/skills/prompt-engineering-guide.md ~/.claude/skills/ && cp /tmp/pes/commands/*.md ~/.claude/commands/ && rm -rf /tmp/pes
```

### Windows PowerShell

```powershell
git clone https://github.com/treylom/prompt-engineering-skills.git $env:TEMP\pes; `
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.claude\skills", "$env:USERPROFILE\.claude\commands" | Out-Null; `
Copy-Item "$env:TEMP\pes\skills\prompt-engineering-guide.md" "$env:USERPROFILE\.claude\skills"; `
Copy-Item "$env:TEMP\pes\commands\*.md" "$env:USERPROFILE\.claude\commands"; `
Remove-Item -Recurse -Force "$env:TEMP\pes"
```

### GPTs / Gems

- Knowledge / 지식 파일: `skills/prompt-engineering-guide.md` 하나만 업로드합니다.
- Instructions / 지침: `instructions/GPTs-Prompt-Generator.md` 또는 `instructions/Gems-Prompt-Generator.md`를 사용합니다.

## 운영 규칙

- 새 프롬프트 스킬 파일을 추가하지 않습니다.
- 모델별 업데이트, 이미지/동영상, 리서치, 슬라이드, 전문가 프라이밍, Context Engineering 업데이트는 모두 `skills/prompt-engineering-guide.md`에 병합합니다.
- `/prompt-sync`는 권원 파일을 미러 경로와 배포 저장소로 동기화하는 용도로만 사용합니다.

## English Summary

This repository now ships one canonical prompt engineering skill: `skills/prompt-engineering-guide.md`. All previous model-specific and workflow-specific prompt skills have been consolidated into that single file. Upload only that one knowledge file to GPTs/Gems, and install only that one skill file for Claude Code.

## License

MIT License. See [LICENSE](./LICENSE).
