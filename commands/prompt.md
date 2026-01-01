# /prompt - AI 프롬프트 생성기

> **Version**: 1.8.0 | **Updated**: 2026-01-01
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

## 🔍 명시적 요소 확장 규칙 (Explicit Element Expansion)

**원칙**: 사용자 입력이 간략해도, AI가 누락된 요소를 추론하여 **명시적으로 상세하게** 채웁니다.

### 확장 프로세스

1. **사용자 입력 분석**: 제공된 키워드/문장에서 핵심 의도 파악
2. **누락 요소 식별**: 아래 체크리스트 기준으로 빈 항목 확인
3. **추론 및 확장**: 문맥에 맞게 **구체적인 값**으로 채움
4. **명시적 출력**: 모든 요소를 프롬프트에 **상세히** 기술

### 목적별 확장 체크리스트

| 목적 | 필수 확장 요소 | 예시 (입력 → 확장) |
|------|--------------|------------------|
| **이미지** | 피사체, 표정, 동작, 배경, 조명, 색상, 구도, 분위기 | "밝은 모습" → "자연스러운 미소, 카메라 응시, 골든아워 조명, 부드러운 보케 배경" |
| **동영상** | 피사체, 동작(시작→진행→종료), 카메라워크, 오디오, 페이스 | "걷는 장면" → "좌→우로 걸음, 트래킹샷, 발소리+환경음" |
| **코딩** | 언어, 프레임워크, 아키텍처, 에러처리, 테스트 | "API" → "FastAPI, RESTful, try-except, pytest 포함" |
| **글쓰기** | 톤, 대상, 길이, 구조, 핵심메시지 | "블로그" → "친근한 톤, 개발자 대상, 1500자, 서론-3단락-결론" |
| **분석** | 범위, 기간, 비교대상, 평가기준, 출력형식 | "시장 분석" → "국내 SaaS, 2024-2025, 3사 비교, 표+차트" |
| **에이전트** | 역할, 도구, 권한, 제약, 출력형식 | "자동화해줘" → "데이터수집 에이전트, 웹검색+파일저장, 읽기전용, JSON 출력" |

### 확장 원칙

1. **암묵적 → 명시적**: "좋은 느낌"같은 모호한 표현을 구체적 속성으로 변환
2. **단일 → 다중**: 하나의 키워드를 여러 관련 요소로 분해
3. **추상 → 구체**: 개념적 설명을 실행 가능한 상세 사항으로 변환

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
| **Text-to-Video** | Veo 3.1 | Sora 2 | Sora 2 Pro |
| **Image-to-Video** | Veo 3.1 | Wan 2.5 | Kling 2.6 Pro |

### 동영상 생성 모델 상세 (생성 길이 비교)

> **기본 길이** = 확장/스토리보드 기능 미사용 시
> **최대 길이** = 확장/스토리보드/Flow 사용 시

| 모델 | 기본 길이 | 최대 길이 | 해상도 | 비고 |
|------|----------|----------|--------|------|
| **Veo 3.1** | 4-8초 | 60초 (~148초) | 1080p | 네이티브 오디오, 7초씩 확장 가능 |
| **Sora 2** | 10초 | 15초 | 720p | ChatGPT Plus 이상 |
| **Sora 2 Pro** | 20초 | 25초 | 1080p | ChatGPT Pro ($200/월) |

---

| 목적 | 1순위 | 2순위 | 3순위 |
|------|-------|-------|-------|
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

#### 🖼️ 이미지 생성 시 질문 (4가지)

```
AskUserQuestion 호출 (questions 배열에 4개 질문):
[
  {
    "question": "이미지 스타일을 선택해주세요",
    "header": "스타일",
    "multiSelect": false,
    "options": [
      {"label": "사진풍 (Recommended)", "description": "실제 사진처럼 사실적인 이미지"},
      {"label": "일러스트", "description": "만화/애니메이션 스타일"},
      {"label": "3D 렌더링", "description": "3D 그래픽 스타일"},
      {"label": "수채화/유화", "description": "전통 회화 스타일"}
    ]
  },
  {
    "question": "이미지 비율을 선택해주세요",
    "header": "비율",
    "multiSelect": false,
    "options": [
      {"label": "1:1 (Recommended)", "description": "정사각형 - SNS, 프로필"},
      {"label": "16:9", "description": "와이드 - 유튜브, 배너"},
      {"label": "9:16", "description": "세로 - 스토리, 릴스"},
      {"label": "4:3", "description": "표준 - PPT, 사진"}
    ]
  },
  {
    "question": "조명 스타일을 선택해주세요",
    "header": "조명",
    "multiSelect": false,
    "options": [
      {"label": "자연광 (Recommended)", "description": "자연스러운 햇빛/실내광"},
      {"label": "스튜디오", "description": "전문 촬영 조명"},
      {"label": "골든아워", "description": "황금빛 일출/일몰"},
      {"label": "네온/드라마틱", "description": "강렬한 색상 조명"}
    ]
  },
  {
    "question": "분위기를 선택해주세요",
    "header": "분위기",
    "multiSelect": false,
    "options": [
      {"label": "밝은/활기찬 (Recommended)", "description": "따뜻하고 긍정적인 느낌"},
      {"label": "어두운/신비로운", "description": "미스터리하고 분위기 있는"},
      {"label": "몽환적/판타지", "description": "꿈결같은 초현실적 분위기"},
      {"label": "역동적/강렬한", "description": "에너지 넘치는 액션 느낌"}
    ]
  }
]
```

> **참고**: 구도(클로즈업/와이드샷 등)는 "기타" 옵션에서 추가 지정 가능

#### 🎬 동영상 생성 시 질문 (5가지)

```
AskUserQuestion 호출 (questions 배열에 최대 4개씩, 2번에 나눠 호출):

[첫 번째 호출 - 모델/스타일]
[
  {
    "question": "동영상 생성 모델을 선택해주세요",
    "header": "모델",
    "multiSelect": false,
    "options": [
      {"label": "Veo 3.1 (Recommended)", "description": "기본 8초 (최대 60초), 네이티브 오디오, 1080p"},
      {"label": "Sora 2", "description": "기본 10초 (최대 15초), 720p"},
      {"label": "Sora 2 Pro", "description": "기본 20초 (최대 25초), 1080p, ChatGPT Pro 필요"}
    ]
  },
  {
    "question": "동영상 스타일을 선택해주세요",
    "header": "스타일",
    "multiSelect": false,
    "options": [
      {"label": "시네마틱 (Recommended)", "description": "영화같은 고퀄리티 영상"},
      {"label": "다큐멘터리", "description": "현실적인 다큐 스타일"},
      {"label": "애니메이션", "description": "만화/애니 스타일"},
      {"label": "뮤직비디오", "description": "빠른 컷, 역동적"}
    ]
  },
  {
    "question": "동영상 길이를 선택해주세요 (모델별 기본 옵션)",
    "header": "길이",
    "multiSelect": false,
    "options": [
      {"label": "기본 (Recommended)", "description": "Veo: 8초 / Sora 2: 10초 / Sora 2 Pro: 20초"},
      {"label": "짧게", "description": "Veo: 4초 / Sora 2: 5초 / Sora 2 Pro: 10초"},
      {"label": "길게 (확장 필요)", "description": "Veo: 30-60초 / Sora 2: 15초 / Sora 2 Pro: 25초"}
    ]
  },
  {
    "question": "카메라 워크를 선택해주세요",
    "header": "카메라",
    "multiSelect": false,
    "options": [
      {"label": "고정샷 (Recommended)", "description": "안정적인 고정 촬영"},
      {"label": "패닝", "description": "좌우로 천천히 이동"},
      {"label": "줌인/줌아웃", "description": "확대/축소 효과"},
      {"label": "트래킹샷", "description": "피사체 따라 이동"}
    ]
  }
]

[두 번째 호출 - 오디오 (Veo 선택 시에만)]
[
  {
    "question": "오디오 구성을 선택해주세요",
    "header": "오디오",
    "multiSelect": false,
    "options": [
      {"label": "환경음만 (Recommended)", "description": "자연스러운 배경 사운드"},
      {"label": "대화 포함", "description": "캐릭터 대사 있음"},
      {"label": "배경음악", "description": "BGM 추가"},
      {"label": "무음", "description": "소리 없이 영상만"}
    ]
  }
]
```

> **참고**: 분위기(평화로운/긴장감 등)는 "기타" 옵션에서 추가 지정 가능
> **참고**: 확장/스토리보드 요청 시 해당 모델의 최대 길이까지 유동적으로 대응

#### 💻 코딩/개발 시 질문 (4가지)

```
AskUserQuestion 호출 (questions 배열에 4개 질문):
[
  {
    "question": "타겟 AI 모델을 선택해주세요",
    "header": "AI 모델",
    "multiSelect": false,
    "options": [
      {"label": "Claude Opus 4.5 (Recommended)", "description": "코딩 1위, 에이전트 최적"},
      {"label": "GPT-5.2", "description": "수학/논리 강점"},
      {"label": "Gemini 3 Pro", "description": "멀티모달 강점"}
    ]
  },
  {
    "question": "프롬프트 상세도를 선택해주세요",
    "header": "상세도",
    "multiSelect": false,
    "options": [
      {"label": "상세 (Recommended)", "description": "구조화된 XML 프롬프트"},
      {"label": "보통", "description": "1-2문단 수준"},
      {"label": "간결", "description": "3-5문장 핵심만"}
    ]
  },
  {
    "question": "코드 아키텍처 수준을 선택해주세요",
    "header": "아키텍처",
    "multiSelect": false,
    "options": [
      {"label": "함수/모듈 단위 (Recommended)", "description": "재사용 가능한 함수로 구성"},
      {"label": "클래스 기반", "description": "OOP 패턴 적용"},
      {"label": "전체 시스템", "description": "디렉토리 구조 포함"},
      {"label": "단일 스크립트", "description": "간단한 1파일 코드"}
    ]
  },
  {
    "question": "에러 처리 수준을 선택해주세요",
    "header": "에러처리",
    "multiSelect": false,
    "options": [
      {"label": "기본 try-except (Recommended)", "description": "핵심 에러만 처리"},
      {"label": "상세 에러 처리", "description": "모든 예외 상황 처리"},
      {"label": "로깅 포함", "description": "에러 + 로그 시스템"},
      {"label": "없음", "description": "에러 처리 생략"}
    ]
  }
]
```

> **참고**: 테스트 옵션(유닛테스트/TDD 등)은 "기타" 옵션에서 추가 지정 가능

#### ✍️ 글쓰기/창작 시 질문 (5가지)

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
    - label: "설명적/교육적"
      description: "튜토리얼, 가이드용"

- question: "글 분량을 선택해주세요"
  header: "분량"
  options:
    - label: "중간 (Recommended)"
      description: "1-2문단, 500자 내외"
    - label: "짧은"
      description: "3-5문장"
    - label: "긴"
      description: "여러 문단, 1000자+"
    - label: "시리즈"
      description: "여러 파트로 나눔"

- question: "대상 독자를 선택해주세요"
  header: "대상"
  options:
    - label: "일반 대중 (Recommended)"
      description: "전문 지식 없는 독자"
    - label: "전문가/업계 종사자"
      description: "해당 분야 전문가"
    - label: "초보자/입문자"
      description: "처음 접하는 독자"
    - label: "내부 팀/동료"
      description: "회사/조직 내부용"

- question: "글의 구조를 선택해주세요"
  header: "구조"
  options:
    - label: "서론-본론-결론 (Recommended)"
      description: "전통적인 3단 구성"
    - label: "문제-해결"
      description: "문제 제시 후 해결책"
    - label: "리스트형"
      description: "번호/글머리 나열"
    - label: "스토리텔링"
      description: "내러티브 흐름"

- question: "핵심 메시지/목적을 선택해주세요"
  header: "목적"
  options:
    - label: "정보 전달 (Recommended)"
      description: "객관적 정보 제공"
    - label: "설득/행동 유도"
      description: "독자의 행동 변화 유도"
    - label: "엔터테인먼트"
      description: "재미와 흥미 제공"
    - label: "감정 전달"
      description: "감동, 공감 유발"
```

#### 🔍 분석/리서치 시 질문 (5가지)

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
    - label: "트렌드 분석"
      description: "시간에 따른 변화"

- question: "출력 형식을 선택해주세요"
  header: "형식"
  options:
    - label: "표/테이블 (Recommended)"
      description: "데이터 정리에 최적"
    - label: "글머리 목록"
      description: "항목별 나열"
    - label: "서술형"
      description: "문장으로 설명"
    - label: "차트/그래프 제안"
      description: "시각화 방향 포함"

- question: "분석 범위를 선택해주세요"
  header: "범위"
  options:
    - label: "특정 주제 집중 (Recommended)"
      description: "좁고 깊게 분석"
    - label: "넓은 개요"
      description: "여러 주제 넓게"
    - label: "경쟁사/시장 비교"
      description: "외부 비교 포함"
    - label: "내부 데이터 분석"
      description: "자체 데이터 중심"

- question: "분석 기간을 선택해주세요"
  header: "기간"
  options:
    - label: "최근 1년 (Recommended)"
      description: "최신 데이터 기준"
    - label: "전체 기간"
      description: "역사적 관점"
    - label: "최근 분기"
      description: "단기 트렌드"
    - label: "미래 전망"
      description: "예측 포함"

- question: "평가 기준을 선택해주세요"
  header: "기준"
  options:
    - label: "정량적 지표 (Recommended)"
      description: "수치, 통계 중심"
    - label: "정성적 평가"
      description: "품질, 의견 중심"
    - label: "혼합 평가"
      description: "정량+정성 모두"
    - label: "벤치마크 비교"
      description: "업계 표준 대비"
```

#### 🤖 에이전트/자동화 시 질문 (5가지)

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
    - label: "계층적"
      description: "오케스트레이터 + 워커"

- question: "도구 사용 범위를 선택해주세요"
  header: "도구"
  options:
    - label: "기본 도구 (Recommended)"
      description: "파일, 검색, 코드 실행"
    - label: "확장 도구"
      description: "MCP, API 연동"
    - label: "최소 도구"
      description: "텍스트 처리만"
    - label: "커스텀 도구"
      description: "맞춤 도구 정의"

- question: "에이전트 권한 수준을 선택해주세요"
  header: "권한"
  options:
    - label: "읽기 전용 (Recommended)"
      description: "조회만 가능, 안전"
    - label: "읽기+쓰기"
      description: "파일 생성/수정 가능"
    - label: "전체 권한"
      description: "시스템 명령 포함"
    - label: "샌드박스"
      description: "격리된 환경에서만"

- question: "자동화 범위를 선택해주세요"
  header: "범위"
  options:
    - label: "단일 작업 (Recommended)"
      description: "한 가지 목표만 수행"
    - label: "반복 작업"
      description: "루프/배치 처리"
    - label: "조건부 분기"
      description: "상황별 다른 처리"
    - label: "전체 워크플로우"
      description: "시작-끝 자동화"

- question: "출력 형식을 선택해주세요"
  header: "출력"
  options:
    - label: "구조화 JSON (Recommended)"
      description: "파싱 용이한 형식"
    - label: "Markdown 리포트"
      description: "사람이 읽기 좋은 형식"
    - label: "로그/스트림"
      description: "실시간 진행 상황"
    - label: "파일 저장"
      description: "결과를 파일로 출력"
```

---

### Step 1.7: 중간 구조화 (조건부 실행)

목적에 따라 프롬프트 생성 전 **중간 구조화 단계**를 수행합니다.

#### 🎬 동영상: 스토리보드 생성

**트리거**: 목적 = 동영상생성

**자동 수행:**
1. 사용자 요청을 분석하여 스토리보드 생성
2. 시간순으로 장면 구성 (오프닝 → 전개 → 클라이막스)
3. 각 장면별: 설명, 카메라 워크, 오디오 정의

**스토리보드 출력 형식:**

```markdown
## 📋 스토리보드

| 시간 | 장면 | 설명 | 카메라 | 오디오 |
|------|------|------|--------|--------|
| 0-3초 | 오프닝 | [장면 설명] | [카메라 워크] | [오디오] |
| 3-6초 | 전개 | [장면 설명] | [카메라 워크] | [오디오] |
| 6-10초 | 클라이막스 | [장면 설명] | [카메라 워크] | [오디오] |

---

✅ 이 스토리보드로 프롬프트를 생성할까요? (Y/수정 요청)
```

**사용자 확인 후 → Step 2: 시간초별 프롬프트 생성**

#### ✍️ 글쓰기/리서치: 개요 생성

**트리거**: 목적 = 글쓰기/창작 OR 분석/리서치

**자동 수행:**
1. 사용자 요청을 분석하여 개요(아웃라인) 생성
2. 논리적 구조로 섹션 구성
3. 각 섹션별: 목표, 핵심 포인트 정의

**개요 출력 형식:**

```markdown
## 📋 개요

### 글 구조

1. **서론** - [핵심 메시지]
   - 도입부 훅
   - 배경 설명

2. **본론 1** - [첫 번째 논점]
   - 주요 내용
   - 예시/근거

3. **본론 2** - [두 번째 논점]
   - 주요 내용
   - 예시/근거

4. **결론** - [정리 및 Call-to-Action]
   - 요약
   - 다음 단계 제안

---

✅ 이 개요로 프롬프트를 생성할까요? (Y/수정 요청)
```

**사용자 확인 후 → Step 2: 섹션별 프롬프트 생성**

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

**🖼️ 이미지/동영상 프롬프트 출력 형식 (CRITICAL)**

이미지 또는 동영상 프롬프트 생성 시:
1. **반드시 JSON 구조로 출력** (자연어 출력 금지)
2. 본 파일의 "이미지 프롬프트 JSON 구조" 또는 "동영상 프롬프트 JSON 구조" 섹션 템플릿 사용
3. `details` 필드만 자연어로 유연하게 작성

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
5️⃣ **에이전트 모드** - AI와 대화하며 프롬프트를 단계별로 완성 (최적의 결과물 도출)

💬 **선택하세요** (예: "1", "2", "3", "4", "5")
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
- **모델별 기본 길이 (확장 미사용)**:
  - Veo 3.1: 4초 / 6초 / 8초 (기본)
  - Sora 2: 5초 / 10초 (기본)
  - Sora 2 Pro: 10초 / 15초 / 20초 (기본)
- **확장/스토리보드 시**: 모델별 최대 길이까지 유동 대응
- 오디오: 대화 / 배경음악 / 효과음 (Veo만 네이티브 지원)
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
다시 5가지 선택지 제시 (Step 3으로 복귀)
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
5️⃣ **에이전트 모드** - AI와 대화하며 프롬프트를 단계별로 완성
```

---

### Step 5: 에이전트 모드 (5번 선택 시)

AI와 대화하며 프롬프트를 단계별로 최적화합니다.

**에이전트 모드 시작 출력:**

```markdown
🤖 **에이전트 모드 진입**

현재 프롬프트를 분석했습니다. 다음 영역을 개선할 수 있습니다:

1. **[영역1]**: [현재 상태] → [개선 가능한 방향]
2. **[영역2]**: [현재 상태] → [개선 가능한 방향]
3. **[영역3]**: [현재 상태] → [개선 가능한 방향]

💬 어느 영역을 먼저 개선할까요? (번호 또는 질문을 입력하세요)
```

**에이전트 모드 워크플로우:**

```
사용자: 5번 선택
   ↓
AI: 현재 프롬프트 분석 + 개선 가능 영역 3-5개 제시
   ↓
사용자: 영역 선택 또는 질문
   ↓
AI: 해당 영역에 대한 세부 옵션 제시 또는 질문 응답
   ↓
(반복 - 사용자가 만족할 때까지)
   ↓
사용자: "완료" 또는 "이걸로 실행"
   ↓
AI: 최종 프롬프트 출력 + 5가지 선택지 (Step 3으로 복귀)
```

**에이전트 모드 개선 영역 예시:**

| 목적 | 제안 영역 |
|------|----------|
| **이미지** | 피사체 디테일, 스타일 일관성, 조명/분위기, 구도 최적화, 네거티브 프롬프트 |
| **동영상** | 동작 시퀀스, 카메라 워크, 오디오 레이어, 장면 전환, 타이밍 조절 |
| **코딩** | 에러 핸들링, 성능 최적화, 테스트 케이스, 문서화, 확장성 |
| **글쓰기** | 톤 조절, 구조 강화, 예시 추가, 청중 맞춤, 핵심 메시지 |
| **분석** | 데이터 범위, 비교 기준, 시각화, 인사이트 깊이, 액션 아이템 |
| **에이전트** | 도구 구성, 권한 설정, 에러 복구, 출력 형식, 체크포인트 |

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
  "model": "Veo 3.1 | Sora 2 | Sora 2 Pro",
  "subject": "주제 - 핵심 피사체/장면 설명",
  "action": "동작 - 움직임, 행동, 변화",
  "style": "스타일 - 시네마틱/다큐멘터리/애니메이션 등",
  "camera": "카메라 워크 - 패닝/줌인/트래킹샷 등",
  "audio": {
    "dialogue": "대화 (따옴표로 표기)",
    "sfx": "음향효과",
    "music": "배경음악/환경음"
  },
  "duration": "모델별 기본: Veo 8초 / Sora 2 10초 / Sora 2 Pro 20초",
  "details": "세부사항 - 추가 디테일 (자연어로 유연하게)",
  "negative": "제외할 요소 (wall, frame 등)"
}
```

**다중 장면 (스토리보드 기반):**
```json
{
  "shared_style": {
    "visual_style": "공통 비주얼 스타일",
    "color_grade": "색보정 톤",
    "aspect_ratio": "16:9"
  },
  "scenes": [
    { "sequence": 1, "time_range": "0-3초", "duration": "3초", "description": "오프닝 장면 설명", "camera": "와이드샷", "audio": "환경음" },
    { "sequence": 2, "time_range": "3-6초", "duration": "3초", "description": "전개 장면 설명", "camera": "패닝", "audio": "대화 포함" },
    { "sequence": 3, "time_range": "6-10초", "duration": "4초", "description": "클라이막스 장면 설명", "camera": "클로즈업", "audio": "배경음악" }
  ],
  "total_duration": "10초"
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

- **Version**: 1.8.0
- **Updated**: 2026-01-01
- **Changes v1.8.0**:
  - **[MAJOR] 동영상 모델 선택 기능 추가**: Veo 3.1, Sora 2, Sora 2 Pro 중 선택 (AskQuestion 첫 번째 질문)
  - **동영상 모델별 생성 길이 비교 테이블 추가**: 기본 길이(확장 미사용), 최대 길이(확장 사용), 해상도 정보
  - **동영상 길이 옵션 이원화**: 기본 옵션(확장 미사용) + 확장/스토리보드 사용 시 유동적 대응
  - **동영상 JSON 구조에 model 필드 추가**: 선택한 모델 정보 포함
- **Changes v1.7.0**:
  - **[MAJOR] 동영상 스토리보드 워크플로우 추가**: 동영상 생성 시 시간순 스토리보드 먼저 생성 후 프롬프트 생성
  - **[MAJOR] 글쓰기/리서치 개요 워크플로우 추가**: 글쓰기/리서치 시 개요(아웃라인) 먼저 생성 후 섹션별 프롬프트 생성
  - **Step 1.7 "중간 구조화" 단계 신설**: 목적별 구조화 단계 조건부 실행
  - **동영상 JSON에 time_range, camera 필드 추가**: 시간초별 장면 관리
- **Changes v1.6.0**:
  - **[MAJOR] 명시적 요소 확장 규칙 추가**: 사용자 입력이 간략해도 AI가 누락된 요소를 상세하게 채움
  - **[MAJOR] 에이전트 모드 옵션 추가**: 5번 옵션으로 AI와 대화하며 프롬프트를 단계별로 최적화
  - **[MAJOR] AskUserQuestion 5가지 확대**: 모든 목적에서 최소 5가지 질문으로 확장
  - **5가지 옵션 UI**: 기존 4가지에서 에이전트 모드 추가
  - **에이전트 모드 워크플로우 섹션 추가**: Step 5로 에이전트 모드 상세 가이드
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
