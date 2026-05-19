---
name: prompt-sync-obsidian
description: Use when needing 프롬프트 동기화 (Obsidian). 프롬프트 생성기 결과물을 Obsidian vault에 저장.
---

# Obsidian 동기화 전용 스킬

GitHub의 GPTs/Gems 최신본을 Obsidian vault에 동기화합니다.

> **Version**: 1.1.0 | **Updated**: 2025-12-28

## 동기화 대상

| GitHub 원본 | Obsidian 대상 |
|------------|--------------|
| `instructions/GPTs-Prompt-Generator.md` | `Prompt-Engineering/GPTs-Prompt-Generator-Instructions.md` |
| `instructions/Gems-Prompt-Generator.md` | `Prompt-Engineering/Gems-Prompt-Generator-Instructions.md` |

## 워크플로우

1. **GitHub 최신본 읽기**: Read 도구로 원본 파일 읽기
2. **Obsidian 기존본 읽기**: Obsidian CLI read → MCP fallback → Read 도구 fallback
3. **변경 사항 식별**: 버전, 섹션별 차이점 파악
4. **업데이트 적용**: MCP update_note (surgical edit) → CLI read-modify-overwrite → Write 도구 fallback

### Obsidian 도구 우선순위 (3-Tier Fallback)

```bash
OBSIDIAN_CLI="/mnt/c/Program Files/Obsidian/Obsidian.com"
```

| 작업 | Tier 1: CLI | Tier 2: MCP | Tier 3: Raw |
|------|------------|-------------|-------------|
| 읽기 | `"$OBSIDIAN_CLI" read path="{path}"` | `mcp__obsidian__read_note` | `Read(file_path)` |
| Surgical edit | MCP 우선 (아래 참조) | `mcp__obsidian__update_note` | `Edit(file_path)` |
| 전체 교체 | `"$OBSIDIAN_CLI" create path="{path}" content="{new}"` | MCP update_note (전체 oldText→newText) | `Write(file_path)` |

> **Note**: `update_note`의 surgical text replacement(oldText→newText)는 MCP가 1순위입니다. CLI는 read-modify-overwrite 패턴으로 우회해야 하므로 이 경우 MCP를 먼저 사용합니다.

## 동기화 패턴 (CRITICAL)

### Surgical Edit: MCP update_note 방식 (1순위)

노트 히스토리 보존을 위해 `update_note`로 변경 사항만 적용합니다.
Surgical text replacement는 MCP가 가장 적합합니다.

```javascript
// 부분 업데이트 (권장)
mcp__obsidian__update_note({
  path: "Prompt-Engineering/GPTs-Prompt-Generator-Instructions.md",
  edits: [
    {
      oldText: "> **Version**: 3.8.1",
      newText: "> **Version**: 4.0.0"
    },
    {
      oldText: "이전 섹션 내용",
      newText: "새로운 섹션 내용"
    }
  ]
})
```

### MCP 실패 시: CLI read-modify-overwrite 패턴 (2순위)

```bash
OBSIDIAN_CLI="/mnt/c/Program Files/Obsidian/Obsidian.com"

# 1. CLI로 현재 내용 읽기
"$OBSIDIAN_CLI" read path="Prompt-Engineering/GPTs-Prompt-Generator-Instructions.md"

# 2. 내용을 수정하여 CLI create로 덮어쓰기
"$OBSIDIAN_CLI" create path="Prompt-Engineering/GPTs-Prompt-Generator-Instructions.md" content="[수정된 전체 내용]"
```

### CLI도 실패 시: Edit/Write 도구 fallback (3순위)

```
# 부분 수정
Edit(file_path="<wsl-home>/Documents/Obsidian/Second_Brain/Prompt-Engineering/GPTs-Prompt-Generator-Instructions.md",
     old_string="...", new_string="...")

# 전체 교체
Write(file_path="<wsl-home>/Documents/Obsidian/Second_Brain/Prompt-Engineering/GPTs-Prompt-Generator-Instructions.md",
      content="[새로운 전체 내용]")
```

### 전체 교체가 필요한 경우

구조가 크게 변경되어 부분 업데이트가 어려운 경우:

**방법 1: MCP 전체 내용을 oldText/newText로 지정**
```javascript
mcp__obsidian__update_note({
  path: "Prompt-Engineering/GPTs-Prompt-Generator-Instructions.md",
  edits: [
    {
      oldText: "[기존 전체 내용]",
      newText: "[새로운 전체 내용]"
    }
  ]
})
```

**방법 2: CLI create로 덮어쓰기**
```bash
"$OBSIDIAN_CLI" create path="Prompt-Engineering/GPTs-Prompt-Generator-Instructions.md" content="[새로운 전체 내용]"
```

**방법 3: 섹션별 순차 업데이트**
- 헤더 기준으로 섹션 분리
- 각 섹션을 개별 edit으로 적용

### dryRun으로 테스트 (MCP 사용 시)

매칭이 불확실할 때 먼저 테스트:
```javascript
mcp__obsidian__update_note({
  path: "...",
  edits: [...],
  dryRun: true  // 실제 적용 없이 미리보기
})
```

## 주의사항

### oldText 매칭 규칙
- **정확히 일치**해야 함 (공백, 줄바꿈 포함)
- 줄바꿈은 `\n`으로 표현
- 탭/스페이스 차이 주의

### 대규모 변경 시 전략
1. 버전 번호 먼저 업데이트
2. 주요 섹션 헤더 변경
3. 섹션 내용 순차 업데이트
4. Changelog 추가

## Obsidian Vault 경로 규칙 (CRITICAL)

**Vault root = `Second_Brain` 폴더**

```
✅ 올바른 경로:
   Prompt-Engineering/GPTs-Prompt-Generator-Instructions.md

❌ 잘못된 경로:
   Second_Brain/Prompt-Engineering/...  (중첩 폴더 생성됨!)
```

## 동기화 옵션

- **전체**: GPTs + Gems 모두 동기화
- **GPTs만**: GPTs-Prompt-Generator만 동기화
- **Gems만**: Gems-Prompt-Generator만 동기화

---

## Metadata

- **Version**: 1.1.0
- **Changes v1.1.0**:
  - delete→create 패턴에서 update_note 방식으로 전환
  - dryRun 테스트 방법 추가
  - oldText 매칭 규칙 및 주의사항 추가
