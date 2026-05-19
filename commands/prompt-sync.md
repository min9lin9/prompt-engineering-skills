# /prompt-sync - 프롬프트 생성기 단일 스킬 동기화 에이전트

프롬프트 생성기 시스템을 `skills/prompt-engineering-guide.md` 단일 스킬 기준으로 동기화합니다.

> **Version**: 4.0.0 | **Updated**: 2026-05-12  
> **부모 Repo**: `treylom/obsidian-ai-vault`  
> **배포 Repo**: `treylom/prompt-engineering-skills`  
> **원칙**: 프롬프트 스킬은 하나만 유지합니다.

$ARGUMENTS

---

## 실제 저장소 구조

```text
<workspace>/                              # 부모 repo 권원
|-- prompt-engineering-skills/              # 수정 대상 원본
|   |-- commands/{prompt.md,prompt-sync.md}
|   |-- instructions/{GPTs,Gems}-Prompt-Generator.md
|   |-- skills/prompt-engineering-guide.md  # 단일 스킬
|   |-- examples/*.md
|   |-- README.md
|   `-- LICENSE
|-- .claude/commands/                       # 로컬 명령 사본
|-- .claude/skills/prompt-engineering-guide.md
`-- AI_Second_Brain/050-Prompt-Engineering/prompt-engineering-skills/
```

배포 저장소 `treylom/prompt-engineering-skills`는 위 원본의 미러입니다.

## 동기화 대상

| # | 위치 | 방식 |
|---|------|------|
| 1 | `~/.claude/commands/` | `prompt.md`, `prompt-sync.md` 복사 |
| 2 | `~/.claude/skills/` | `prompt-engineering-guide.md` 복사, 이전 분리 스킬 제거 |
| 3 | `<vault-repo>/050-Prompt-Engineering/prompt-engineering-skills/` | 전체 미러 |
| 4 | `<wsl-vault>/AI_Second_Brain/050-Prompt-Engineering/prompt-engineering-skills/` | 전체 미러 |
| 5 | `<wsl-vault>/prompt-engineering-skills/` | 전체 미러 |
| 6 | `<wsl-home>/OneDrive/Desktop/AI/prompt-engineering-skills/` | 전체 미러, 있으면 수행 |
| 7 | `/tmp/pes-deploy/prompt-engineering-skills/` | 배포 repo 미러 + commit/push |

## 1-Shot Bash

```bash
SRC=<workspace>/prompt-engineering-skills
WIN_OBS=<wsl-vault>

# 1) 전체 미러
for T in   "<vault-repo>/050-Prompt-Engineering/prompt-engineering-skills/"   "$WIN_OBS/AI_Second_Brain/050-Prompt-Engineering/prompt-engineering-skills/"   "$WIN_OBS/prompt-engineering-skills/"   "<wsl-home>/OneDrive/Desktop/AI/prompt-engineering-skills/" ; do
  [ -d "$(dirname "$T")" ] && rsync -a --delete --exclude='.git/' --exclude='.gitmodules' "$SRC/" "$T"
done

# 2) Claude Code 로컬 사본
mkdir -p ~/.claude/commands ~/.claude/skills
cp "$SRC/commands/prompt.md" ~/.claude/commands/prompt.md
cp "$SRC/commands/prompt-sync.md" ~/.claude/commands/prompt-sync.md
cp "$SRC/skills/prompt-engineering-guide.md" ~/.claude/skills/prompt-engineering-guide.md

# 3) 이전 분리 프롬프트 스킬 제거
rm -f   ~/.claude/skills/gpt-5.5-prompt-enhancement.md   ~/.claude/skills/claude-4.7-prompt-strategies.md   ~/.claude/skills/claude-4.6-prompt-strategies.md   ~/.claude/skills/gemini-3.1-prompt-strategies.md   ~/.claude/skills/image-prompt-guide.md   ~/.claude/skills/research-prompt-guide.md   ~/.claude/skills/expert-domain-priming.md   ~/.claude/skills/slide-prompt-guide.md   ~/.claude/skills/context-engineering-collection.md
rm -rf   ~/.claude/skills/claude-4.6-prompt-strategies   ~/.claude/skills/gemini-3.1-prompt-strategies   ~/.claude/skills/image-prompt-guide   ~/.claude/skills/research-prompt-guide   ~/.claude/skills/expert-domain-priming

# 4) GPTs/Gems instructions 보조 사본
mkdir -p <vault-repo>/050-Prompt-Engineering "$WIN_OBS/AI_Second_Brain/050-Prompt-Engineering" "$WIN_OBS/Library/Prompt-Engineering"
cp "$SRC/instructions/GPTs-Prompt-Generator.md" <vault-repo>/050-Prompt-Engineering/GPTs-Prompt-Generator-Instructions.md
cp "$SRC/instructions/Gems-Prompt-Generator.md" <vault-repo>/050-Prompt-Engineering/Gems-Prompt-Generator-Instructions.md
cp "$SRC/instructions/GPTs-Prompt-Generator.md" "$WIN_OBS/AI_Second_Brain/050-Prompt-Engineering/GPTs-Prompt-Generator-Instructions.md"
cp "$SRC/instructions/Gems-Prompt-Generator.md" "$WIN_OBS/AI_Second_Brain/050-Prompt-Engineering/Gems-Prompt-Generator-Instructions.md"
cp "$SRC/instructions/GPTs-Prompt-Generator.md" "$WIN_OBS/Library/Prompt-Engineering/GPTs-Prompt-Generator-Instructions.md"
cp "$SRC/instructions/Gems-Prompt-Generator.md" "$WIN_OBS/Library/Prompt-Engineering/Gems-Prompt-Generator-Instructions.md"

# 5) 배포 repo 미러
DEPLOY=/tmp/pes-deploy/prompt-engineering-skills
if [ ! -d "$DEPLOY/.git" ]; then
  mkdir -p /tmp/pes-deploy
  git clone https://github.com/treylom/prompt-engineering-skills.git "$DEPLOY"
fi
( cd "$DEPLOY" && git fetch origin master && git checkout master && git reset --hard origin/master )
rsync -a --delete --exclude='.git/' --exclude='.gitmodules' "$SRC/" "$DEPLOY/"
```

## 검증

```bash
find <repo>/skills -maxdepth 1 -type f -printf '%f
'
node -e "const fs=require('fs'); const c=fs.readFileSync('<repo>/instructions/GPTs-Prompt-Generator.md','utf8'); console.log(c.length, c.length <= 8000)"
git -C <workspace> status --short -- prompt-engineering-skills .claude/commands/prompt.md .claude/commands/prompt-sync.md .claude/skills/prompt-engineering-guide.md AI_Second_Brain/050-Prompt-Engineering/prompt-engineering-skills
```

## 완료 기준

- `skills/`에는 `prompt-engineering-guide.md` 하나만 존재합니다.
- README, `/prompt`, GPTs/Gems 지침은 단일 스킬 업로드/참조를 안내합니다.
- 미러 경로와 배포 repo가 같은 파일 구조를 갖습니다.
- GPTs instructions는 8000자 이하입니다.
