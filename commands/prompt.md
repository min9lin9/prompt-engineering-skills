# /prompt - AI 프롬프트 생성기

> **Version**: 1.5.2 | **Updated**: 2026-01-01
> **Model Rankings**: [LMArena Leaderboard](https://lmarena.ai) (2025년 12월 기준)

AI 모델별로 최적화된 프롬프트를 생성합니다.

$ARGUMENTS

---

## ⛔ CRITICAL RULES (최상단 배치)

**이 커맨드는 "프롬프트 생성" 전용입니다.**

### 절대 금지 사항
- ❌ 프롬프트 출력 없이 이미지/동영상 바로 생성 금지
- ❌ 1번 선택 전 작업 실행 금지
- ❌ 수정 시(2번/3번) 바로 실행 금지 → 프롬프트만 출력

### 실행 트리거 (ONLY THESE)
- "1번" 또는 "바로 실행" → 작업 실행
- "이 프롬프트로 만들어줘" → 작업 실행

---

## 목적별 추천 모델 (LMArena 기준)

> 출처: [LMArena Leaderboard](https://lmarena.ai) - 2025년 12월 기준 사용자 투표 순위

| 목적 | 1순위 | 2순위 | 3순위 |
|------|-------|-------|-------|
| **코딩/개발** | Claude Opus 4.5 | GPT-5.2 | Gemini 3 Pro |
| **수학/논리** | GPT-5.2 | Gemini 3 Flash | Claude Opus 4.5 |
| **글쓰기/창작** | Gemini 3 Pro | Gemini 3 Flash | Claude Opus 4.5 |
| **종합/분석** | Gemini 3 Pro | Grok 4.1 | Claude Opus 4.5 |
| **Hard Prompts** | Claude Opus 4.5 | Gemini 3 Pro | Grok 4.1 |
| **비전/멀티모달** | Gemini 3 Pro | Gemini 3 Flash | GPT-5.1 |
| **이미지 생성** | gpt-image (GPT Image 1.5) | Gemini 3 Pro Image | Flux 2 Max |
| **이미지 편집** | gpt-image (ChatGPT) | Gemini 3 Pro Image | Seedream 4.5 |
| **Text-to-Video** | Veo 3.1 | Sora 2 Pro | Veo 3 |
| **Image-to-Video** | Veo 3.1 | Wan 2.5 | Kling 2.6 Pro |
| **웹 검색/리서치** | Gemini 3 Pro Grounding | GPT-5.2 Search | GPT-5.1 Search |
| **팩트체크** | **GPT-5.2 Thinking** | Gemini 3 Pro Grounding | Perplexity Sonar Pro |

---

## 워크플로우

### Step 1: 목적 감지 + 옵션 선택 (AskUserQuestion 활용)

**$ARGUMENTS 처리 규칙:**

- `$ARGUMENTS`가 **비어있거나 너무 짧으면** → 대화형 모드로 전환:
  ```
  💬 어떤 프롬프트를 생성할까요?
  예: "이미지 생성", "코딩", "블로그 글 작성"
  ```
- `$ARGUMENTS`가 **너무 길면** (200자 초과) → 핵심만 추출:
  ```
  📋 요청이 길어서 핵심만 추출했습니다: [핵심 요약]
  ```

**목적 자동 감지 테이블:**

| 키워드/패턴 | 자동 선택 목적 | 권장 출력 형식 |
|------------|---------------|---------------|
| 이미지, 그림, 사진, 그려줘 | 이미지생성 | **JSON 구조 기본** |
| 영상, 동영상, 비디오, 클립 | 동영상생성 | **JSON 구조 기본** |
| 코드, 코딩, 개발, 프로그램 | 코딩/개발 | XML |
| 글, 작성, 블로그, 기사 | 글쓰기/창작 | Markdown + 자연어 |
| 분석, 데이터, 통계, 비교 | 분석/리서치 | XML |
| 에이전트, 자동화, 워크플로우 | 에이전트 | XML |
| 팩트체크, 사실 확인, 검증 | 팩트체크 | XML |
| 조사, 리서치, 찾아줘 | 리서치/조사 | XML |
| 수학, 계산, 풀이, 증명 | 수학/논리 | Markdown + 자연어 |

---

### Step 1.5: 🎯 AskUserQuestion으로 옵션 수집 (Claude Code 전용)

**CRITICAL: Claude Code에서는 반드시 `AskUserQuestion` 도구를 사용하여 사용자에게 옵션을 물어봅니다.**

목적이 감지되면, 해당 목적에 맞는 옵션을 `AskUserQuestion` 도구로 질문합니다.

#### 🖼️ 이미지 생성 시 질문

```
AskUserQuestion 호출:
- question: "이미지 스타일을 선택해주세요"
  header: "스타일"
  options:
    - label: "사진풍 (Recommended)"
      description: "실제 사진처럼 사실적인 이미지"
    - label: "일러스트"
      description: "만화/애니메이션 스타일"
    - label: "3D 렌더링"
      description: "3D 그래픽 스타일"
    - label: "수채화/유화"
      description: "전통 회화 스타일"

- question: "이미지 비율을 선택해주세요"
  header: "비율"
  options:
    - label: "1:1 (Recommended)"
      description: "정사각형 - SNS, 프로필"
    - label: "16:9"
      description: "와이드 - 유튜브, 배너"
    - label: "9:16"
      description: "세로 - 스토리, 릴스"
    - label: "4:3"
      description: "표준 - PPT, 사진"

- question: "조명 스타일을 선택해주세요"
  header: "조명"
  options:
    - label: "자연광 (Recommended)"
      description: "자연스러운 햇빛/실내광"
    - label: "스튜디오"
      description: "전문 촬영 조명"
    - label: "골든아워"
      description: "황금빛 일출/일몰"
    - label: "네온/드라마틱"
      description: "강렬한 색상 조명"
```

#### 🎬 동영상 생성 시 질문

```
AskUserQuestion 호출:
- question: "동영상 스타일을 선택해주세요"
  header: "스타일"
  options:
    - label: "시네마틱 (Recommended)"
      description: "영화같은 고퀄리티 영상"
    - label: "다큐멘터리"
      description: "현실적인 다큐 스타일"
    - label: "애니메이션"
      description: "만화/애니 스타일"
    - label: "뮤직비디오"
      description: "빠른 컷, 역동적"

- question: "동영상 길이를 선택해주세요"
  header: "길이"
  options:
    - label: "5초 (Recommended)"
      description: "짧은 클립, SNS용"
    - label: "10초"
      description: "중간 길이"
    - label: "30초"
      description: "긴 영상"

- question: "카메라 워크를 선택해주세요"
  header: "카메라"
  options:
    - label: "고정샷 (Recommended)"
      description: "안정적인 고정 촬영"
    - label: "패닝"
      description: "좌우로 천천히 이동"
    - label: "줌인/줌아웃"
      description: "확대/축소 효과"
    - label: "트래킹샷"
      description: "피사체 따라 이동"
```

#### 💻 코딩/개발 시 질문

```
AskUserQuestion 호출:
- question: "타겟 AI 모델을 선택해주세요"
  header: "AI 모델"
  options:
    - label: "Claude Opus 4.5 (Recommended)"
      description: "코딩 1위, 에이전트 최적"
    - label: "GPT-5.2"
      description: "수학/논리 강점"
    - label: "Gemini 3 Pro"
      description: "멀티모달 강점"

- question: "프롬프트 상세도를 선택해주세요"
  header: "상세도"
  options:
    - label: "상세 (Recommended)"
      description: "구조화된 XML 프롬프트"
    - label: "보통"
      description: "1-2문단 수준"
    - label: "간결"
      description: "3-5문장 핵심만"
```

#### ✍️ 글쓰기/창작 시 질문

```
AskUserQuestion 호출:
- question: "글쓰기 스타일을 선택해주세요"
  header: "스타일"
  options:
    - label: "전문적/공식적 (Recommended)"
      description: "비즈니스, 리포트용"
    - label: "친근한/대화체"
      description: "블로그, SNS용"
    - label: "창의적/문학적"
      description: "스토리, 에세이용"

- question: "글 분량을 선택해주세요"
  header: "분량"
  options:
    - label: "중간 (Recommended)"
      description: "1-2문단, 500자 내외"
    - label: "짧은"
      description: "3-5문장"
    - label: "긴"
      description: "여러 문단, 1000자+"
```

#### 🔍 분석/리서치 시 질문

```
AskUserQuestion 호출:
- question: "분석 깊이를 선택해주세요"
  header: "깊이"
  options:
    - label: "심층 분석 (Recommended)"
      description: "상세한 데이터 분석"
    - label: "요약 분석"
      description: "핵심만 빠르게"
    - label: "비교 분석"
      description: "여러 항목 비교"

- question: "출력 형식을 선택해주세요"
  header: "형식"
  options:
    - label: "표/테이블 (Recommended)"
      description: "데이터 정리에 최적"
    - label: "글머리 목록"
      description: "항목별 나열"
    - label: "서술형"
      description: "문장으로 설명"
```

#### 🤖 에이전트/자동화 시 질문

```
AskUserQuestion 호출:
- question: "에이전트 복잡도를 선택해주세요"
  header: "복잡도"
  options:
    - label: "단일 에이전트 (Recommended)"
      description: "하나의 작업에 집중"
    - label: "멀티 에이전트"
      description: "여러 에이전트 협업"
    - label: "파이프라인"
      description: "순차적 작업 흐름"

- question: "도구 사용 범위를 선택해주세요"
  header: "도구"
  options:
    - label: "기본 도구 (Recommended)"
      description: "파일, 검색, 코드 실행"
    - label: "확장 도구"
      description: "MCP, API 연동"
    - label: "최소 도구"
      description: "텍스트 처리만"
```

---

### Step 2: 프롬프트 생성 (진행 상황 표시)

**🔄 진행 상황 표시 (필수)**

프롬프트 생성 중 **반드시 아래 상태 메시지를 순서대로 출력**합니다:

```
🔍 요청 분석 중... → ✅ 목적: [감지된 목적], 형식: [출력 형식]
🧠 전문가 토론 진행 중... (약 5-10초)
✅ 프롬프트 생성 완료!
```

**CE 체크리스트 (자동 적용)**

| 원칙 | 적용 방법 |
|------|----------|
| **U자형 배치** | 시작: Critical Rules / 끝: Final Reminder |
| **Lost-in-Middle 방지** | 핵심 규칙 시작+끝 반복 |
| **Signal-to-Noise** | 장황한 설명 → 표/글머리 |

**모델별 필수 블록**

| 모델 | 필수 블록 |
|------|----------|
| GPT-5.2 | `<output_verbosity_spec>` |
| Claude Opus 4.5 | `<default_to_action>` |
| Gemini 3 | Constraints 최상단 |
| 이미지/동영상 | 주제/스타일/분위기 |

**전문가 3인 토론 (간략 진행)**

> 내부 토론 후 **핵심 결정만 1줄로 표시**: "💡 [적용된 주요 개선점]"

| 역할 | 검토 초점 |
|------|----------|
| Expert 1 | CE 원칙, 토큰 효율 |
| Expert 2 | 내용 정확성, 완전성 |
| Expert 3 | 최종 결정, 조율 |

---

### Step 3: 프롬프트 출력 + 개선 옵션 제시

**출력 형식 (프롬프트는 반드시 코드블록으로 출력):**

```markdown
## ✅ 프롬프트 생성 완료

```
[생성된 프롬프트 - 반드시 코드블록 안에 출력]
```

---

📋 **전문가 검토 완료** | CE 체크리스트 ✅ | 모델 최적화 ✅

---

## 어떻게 하시겠습니까?

1️⃣ **바로 실행** - 해당 프롬프트로 작업 바로 실행
2️⃣ **자동 개선** - AI가 자동으로 프롬프트 강화 → 수정된 프롬프트 출력 (실행 ❌)
3️⃣ **직접 개선** - 제시되는 옵션 중 선택하여 수정 → 수정된 프롬프트 출력 (실행 ❌)
4️⃣ **기타** - 다른 요청 또는 질문

💬 **선택하세요** (예: "1", "2", "3", "4")
```

**🎨 개선 옵션 (3번 선택 시에만 아래 옵션 표시)**

```markdown
### 🎨 개선 옵션

**공통:**
- 상세도 조절: 간결(3-5문장) / 보통(1-2문단) / 상세(구조화)
- 예시 추가 (입출력 샘플)
- 제약조건 추가 (하지 말아야 할 것)
- 출력형식 변경 (JSON, 표, 글머리 등)
- 역할 강화 (전문가 페르소나)
- 단계별 사고 추가 (Chain of Thought)

**🖼️ 이미지 전용:**
- 비율: 1:1 / 16:9 / 9:16 / 4:3
- 스타일: 사진풍 / 일러스트 / 3D / 수채화 / 사이버펑크
- 조명: 자연광 / 스튜디오 / 골든아워 / 네온
- 앵글: 클로즈업 / 와이드샷 / 버드아이뷰 / 로우앵글

**🎬 동영상 전용:**
- 길이: 5초 / 10초 / 30초
- 오디오: 대화 / 배경음악 / 효과음
- 카메라: 패닝 / 줌인 / 트래킹샷
- 부정 프롬프트: 제외할 요소

💬 **선택하세요** (예: "비율 16:9, 스타일 사이버펑크")
```

---

### Step 4: 프롬프트 수정 워크플로우 (2번/3번 선택 시)

**CRITICAL: 수정 시에는 프롬프트만 출력, 바로 실행 금지**

```
수정 요청 (2번 또는 3번)
   ↓
수정된 프롬프트 생성 (전문가 토론 백그라운드 실행)
   ↓
수정된 프롬프트 출력
   ↓
다시 4가지 선택지 제시 (Step 3으로 복귀)
```

**수정 후 출력 형식:**

```markdown
## ✅ 프롬프트 수정 완료

**수정 사항:** [적용된 변경 내용]

[수정된 프롬프트 코드블록]

---

📋 **전문가 검토 완료** | CE 체크리스트 ✅ | 모델 최적화 ✅

---

## 어떻게 하시겠습니까?

1️⃣ **바로 실행** - 해당 프롬프트로 작업 바로 실행
2️⃣ **자동 개선** - AI가 자동으로 프롬프트 강화
3️⃣ **직접 개선** - 옵션 선택하여 추가 수정
4️⃣ **기타** - 다른 요청 또는 질문
```

---

## 이미지 프롬프트 JSON 구조 (기본 형식)

**단일 이미지:**
```json
{
  "subject": "주제 - 핵심 피사체 설명",
  "style": "스타일 - 사진풍/일러스트/3D/수채화 등",
  "mood": "분위기 - 색조, 감정, 톤",
  "composition": "구도 - 앵글, 프레이밍",
  "lighting": "조명 - 자연광/스튜디오/골든아워 등",
  "details": "세부사항 - 추가 디테일 (자연어로 유연하게)",
  "aspect_ratio": "16:9"
}
```

**다중 이미지:**
```json
{
  "shared_style": {
    "art_style": "공통 스타일",
    "color_palette": "공통 색상",
    "aspect_ratio": "16:9"
  },
  "images": [
    { "sequence": 1, "description": "첫 번째 이미지 설명" },
    { "sequence": 2, "description": "두 번째 이미지 설명" }
  ]
}
```

---

## 동영상 프롬프트 JSON 구조 (기본 형식)

**단일 동영상:**
```json
{
  "subject": "주제 - 핵심 피사체/장면 설명",
  "action": "동작 - 움직임, 행동, 변화",
  "style": "스타일 - 시네마틱/다큐멘터리/애니메이션 등",
  "camera": "카메라 워크 - 패닝/줌인/트래킹샷 등",
  "audio": {
    "dialogue": "대화 (따옴표로 표기)",
    "sfx": "음향효과",
    "music": "배경음악/환경음"
  },
  "duration": "5초/10초/30초",
  "details": "세부사항 - 추가 디테일 (자연어로 유연하게)",
  "negative": "제외할 요소 (wall, frame 등)"
}
```

**다중 장면:**
```json
{
  "shared_style": {
    "visual_style": "공통 비주얼 스타일",
    "color_grade": "색보정 톤",
    "aspect_ratio": "16:9"
  },
  "scenes": [
    { "sequence": 1, "duration": "5초", "description": "첫 번째 장면 설명", "audio": "..." },
    { "sequence": 2, "duration": "5초", "description": "두 번째 장면 설명", "audio": "..." }
  ]
}
```

**오디오 표기법:**
- 대화: '따옴표' 사용 (예: 'Hello, how are you?')
- 음향효과: 명시적 설명 (예: door creaking, footsteps on gravel)
- 배경음: 환경 설명 (예: ambient city noise, gentle rain)

---

## 이미지 비율 가이드

| 비율 | 용도 | 권장 상황 |
|------|------|----------|
| **1:1** (기본값) | 정사각형 | SNS 프로필, 아이콘, 일반 이미지 |
| **16:9** | 와이드 | 유튜브 썸네일, 프레젠테이션, 배너 |
| **9:16** | 세로 | 스마트폰 배경, 스토리, 릴스 |
| **4:3** | 표준 | 프레젠테이션, 사진 |
| **3:4** | 세로 표준 | 포트레이트, 인물 사진 |

---

## 참조 스킬

| # | 파일명 | 용도 | 필수 여부 |
|---|--------|------|----------|
| 1 | `prompt-engineering-guide.md` | 모델별 프롬프트 전략 총괄 | ✅ 필수 |
| 2 | `context-engineering-collection.md` | CE 원칙 | ✅ 권장 |
| 3 | `gpt-5.2-prompt-enhancement.md` | GPT-5.2 전용 XML 패턴 | GPT 시 |
| 4 | `claude-4.5-prompt-strategies.md` | Claude 4.5 에이전트/코딩 전략 | Claude 시 |
| 5 | `gemini-prompt-strategies.md` | Gemini 3, Flash, Veo, Nano Banana 전략 | Gemini 시 |
| 6 | `image-prompt-guide.md` | 이미지/동영상 생성 가이드 (공냥이 @specal1849) | 이미지/동영상 시 |
| 7 | `research-prompt-guide.md` | 리서치/팩트체크 가이드 (두부 @tofukyung) | 팩트체크/리서치 시 |

---

## 사용 예시

```
/prompt
→ $ARGUMENTS 분석 후 즉시 프롬프트 생성 + 개선 옵션 제시

/prompt Claude로 블로그 글 작성용 프롬프트 만들어줘
→ Claude Opus 4.5 + 글쓰기 목적으로 즉시 생성 + 개선 옵션 제시

/prompt 코딩용 프롬프트 만들어줘
→ LMArena 순위 기반 최적 모델로 즉시 생성 + 개선 옵션 제시
```

---

## Metadata

- **Version**: 1.5.2
- **Updated**: 2026-01-01
- **Changes v1.5.2**:
  - **[MAJOR] AskUserQuestion 옵션 수집 복원**: 모든 프롬프트 생성 시 사용자에게 옵션을 클릭해서 선택하도록 Step 1.5 추가
  - **목적별 맞춤 질문**: 이미지, 동영상, 코딩, 글쓰기, 분석, 에이전트 각각에 최적화된 질문 세트 정의
- **Changes v1.5.1**:
  - **이미지/동영상 JSON 구조 템플릿 추가**: command 파일에 JSON 구조 예시 직접 포함 (동영상 JSON 출력 누락 버그 수정)
- **Changes v1.5.0**:
  - **[MAJOR] 동영상 프롬프트 JSON 구조화**: 이미지와 동일하게 JSON+자연어 형식 통일
  - **gpt-image 모델명 통일**: GPT Image 1.5/ChatGPT Image → gpt-image로 명칭 통일
  - **출력 형식 테이블 간소화**: 이미지/동영상 모두 JSON 구조 기본으로 통합
  - **버전 체계 리셋**: 모든 채널 1.5.0으로 통일
- **Changes v4.2.0**:
  - **research-prompt-guide.md 크레딧 추가**: 두부 @tofukyung 크레딧 추가
  - **image-prompt-guide.md 크레딧 추가**: 공냥이 @specal1849 크레딧 추가
- **Changes v4.1.0**:
  - **금지사항 강화**: 이미지/동영상 바로 생성 방지 규칙 최상단 배치
  - **개선 옵션 UI**: 3번 선택 시에만 세부 옵션 표시
  - **프롬프트 코드블록 출력**: 모든 프롬프트를 코드블록으로 출력
  - **이미지 JSON 구조 기본화**: 자연어 대신 JSON 구조 기본, 유연한 부분만 자연어
- **Changes v4.0.0**:
  - **[MAJOR] 워크플로우 전면 개편**: 입력 폼 제거 → 즉시 프롬프트 생성
  - **개선 옵션 4가지 UI**: 프롬프트 출력 후 선택지 제시
  - **출력 형식 자동 라우팅**: 목적별 최적 형식 자동 선택 (이미지=JSON, 보고서=XML)
  - **전문가 토론 백그라운드 필수화**: skip 불가, 출력 간소화
  - **수정 워크플로우 추가**: 2번/3번 선택 시 프롬프트만 출력 (실행 금지)
  - **이미지/동영상 옵션**: 개선 단계(3번)로 이동
- **Changes v3.3.0**:
  - **자동/필수 입력 분리**: 목적별 필수 입력 필드 구분
- **Changes v3.0.0**:
  - **[MAJOR] 전문가 3인 토론 필수화**: 모든 프롬프트 생성에 자동 적용
