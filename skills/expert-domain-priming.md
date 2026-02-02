---
name: expert-domain-priming
description: 전문가 도메인 프라이밍 가이드. 실제 전문가 지명과 전문 용어로 AI의 잠재 공간을 활성화하는 방법론.
references:
  - prompt-engineering-guide
  - context-engineering-collection
version: 1.0.0
created: 2026-02-02
author: Claude Code
source_credits:
  - name: 최승준 소장
    context: "Master Class - 원리를 생각하는 프롬프팅"
  - name: 공냥이(@specal1849)
    context: "프롬프트 쿠튀르: 전문가의 AI 활용법"
  - name: erucipe (Notion A-Z)
    url: https://erucipe.notion.site/A-Z-2e3d5c9e7e5980c4a593f1994582f1ab
---

# 전문가 도메인 프라이밍 가이드

> **"act as an expert" 대신 실제 전문가를 지명하고, 그들의 전문 용어를 사용하라"**
>
> 프롬프트 안의 단어는 AI가 탐색하는 잠재 공간(Latent Space)의 좌표다.
> 전문 용어는 그 좌표를 정확히 찍어, 모델 내부의 전문가 영역을 활성화한다.

---

## 1. 핵심 원칙

### 1.1 왜 전문가 지명이 효과적인가

LLM은 Mixture of Experts(MoE) 아키텍처를 사용한다. 수많은 '전문가 모듈' 중 요청에 맞는 일부만 활성화된다.

```
일반 프롬프트: "마케팅에 대해 알려줘"
  → 넓은 들판에서 평균적인 답변 (일반 상식 영역)

전문가 프롬프트: "Philip Kotler의 STP 프레임워크에 입각한 B2B SaaS 포지셔닝 전략"
  → 좁은 문제 공간에서 정확한 답변 (전문가 잠재 공간 활성화)
```

**메커니즘:**
- **적확한 토큰(Appropriate Tokens)** = 전문가 이름 + 전문 용어 + 프레임워크명
- 이 토큰들이 **라우팅 시그널(Routing Signal)** 역할을 수행
- 모델 내부의 해당 전문 영역 모듈이 활성화됨
- 결과: 문제 공간(Problem Space)이 축소 → 정확도 상승

### 1.2 프롬프트 단어의 5가지 역할

모든 프롬프트의 단어는 다음 5가지 중 하나의 역할을 수행한다:

| # | 역할 | 영문 | 핵심 질문 | 효과 |
|---|------|------|-----------|------|
| 1 | **범위 지정** | Target Scope | 어디서 찾을까? | 문제 공간 축소 |
| 2 | **목적 고정** | Goal | 무엇을 달성할까? | 방향성 확보 |
| 3 | **형식 강제** | Format | 어떻게 출력할까? | 구조화된 결과 |
| 4 | **오류 금지** | No-Go | 무엇을 피할까? | 품질 하한선 |
| 5 | **행동 지정** | Behavior | 어떻게 작업할까? | 과정 품질 |

### 1.3 금지어 6개 (Style Faux Pas)

다음 표현은 AI의 문제 공간을 넓혀 품질을 저하시킨다:

| 금지어 | 문제점 | 대안 |
|--------|--------|------|
| **알아서 잘** | 목표 부재 → AI가 임의로 채움 | 구체적 성공 조건 명시 |
| **깔끔하게** | 기준 모호 → 평균적 톤 | 형식과 구조 지정 (표, 리스트, 3단 구조 등) |
| **대충** | 품질 하한선 붕괴 → 토큰 절약 | 최소 품질 기준 명시 |
| **자세히** | 범위 불명확 → 장황한 출력 | 대상 독자와 깊이 수준 지정 |
| **완벽하게** | 기준 없음 → 과잉 생성 | 체크리스트 형태로 기준 제시 |
| **적당히** | 양적 기준 없음 → 임의 분량 | 수량, 길이, 항목 수 명시 |

> **핵심**: 미사여구를 고치지 말고, **조건을 추가**해야 한다.

---

## 2. 도메인 프라이밍 5단계 적용법

### Step 1: 도메인 식별

사용자의 요청에서 해당 분야를 식별한다.

```
예시: "마케팅 전략 보고서를 써줘"
  → 도메인: 마케팅/브랜딩
  → 세부 분야: 전략 수립, 포지셔닝
```

### Step 2: 실제 전문가 2-3명 조회

아래 전문가 데이터베이스에서 해당 도메인의 전문가를 찾는다.

```
마케팅 도메인 → Philip Kotler, Seth Godin, David Aaker
  → 선택: Kotler (전략 중심), Godin (혁신 마케팅)
```

### Step 3: 핵심 용어/프레임워크 추출

선택한 전문가의 대표 용어와 프레임워크를 프롬프트에 삽입한다.

```
Kotler → STP(Segmentation-Targeting-Positioning), Marketing Mix(4P→7P), CLV
Godin → Purple Cow, Permission Marketing, Tribe
```

### Step 4: 프롬프트에 전문가명 + 용어 삽입

```markdown
❌ Before: "마케팅 전략 보고서를 잘 써줘"

✅ After:
"Philip Kotler의 STP 프레임워크와 David Aaker의 Brand Equity 모델에 입각하여
B2B SaaS 시장의 포지셔닝 전략 보고서를 작성하라.

- 세그멘테이션: TAM/SAM/SOM 기준
- 타겟팅: ICP(Ideal Customer Profile) 정의
- 포지셔닝: 경쟁사 대비 차별화 맵
- 출력: 요약(200자)-본문(3섹션)-결론-액션아이템"
```

### Step 5: 5가지 역할 체크리스트 점검

작성한 프롬프트를 5가지 역할로 점검한다:

```
□ 범위 지정: "B2B SaaS 시장" ✅
□ 목적 고정: "포지셔닝 전략 보고서" ✅
□ 형식 강제: "요약-본문-결론-액션아이템" ✅
□ 오류 금지: (필요시 추가) "추측성 정보 사용 금지" 등
□ 행동 지정: "STP 프레임워크에 입각하여" ✅
```

---

## 3. 품질 수렴 루프

한 번에 완성하려는 태도가 가장 비싼 습관이다. 프롬프트는 반복적으로 수렴시킨다.

```
(1) 프롬프트 작성 후 생성
        ↓
(2) 기준 미달이면 새 세션에서 수정 후 재생성
        ↓
(3) 결과를 비교해 부족한 조건을 추가
        ↓
(4) 검토 지시로 결함을 찾음
        ↓
(5) 수정 지시로 재생성
        ↓
    (반복 → 수렴)
```

**루프 안에서 해야 할 것:**
1. **단어의 효과 관찰**: 어떤 키워드가 결과를 바꾸는지 파악
2. **적정선 판단**: 품질이 충분한 지점에서 사용
3. **결과물 미리 구상**: 어떤 출력을 원하는지 먼저 생각

---

## 4. 전문가 데이터베이스 (12개 도메인)

### 4.1 기술/AI/소프트웨어

| 전문가 | 전문 분야 | 핵심 용어/프레임워크 |
|--------|----------|---------------------|
| **Martin Fowler** | 소프트웨어 아키텍처 | Refactoring, Microservices, Domain-Driven Design, Event Sourcing |
| **Robert C. Martin** | 클린 코드 | SOLID Principles, Clean Architecture, TDD, Dependency Inversion |
| **Kent Beck** | 소프트웨어 설계 | Extreme Programming, Test-Driven Development, Design Patterns |
| **Geoffrey Hinton** | 딥러닝/신경망 | Backpropagation, Representation Learning, Capsule Networks |
| **Andrej Karpathy** | AI/신경망 교육 | Neural Network training, Tokenization, nanoGPT, Software 2.0 |
| **Chris Olah / Catherine Olsson** | 해석가능 AI | Transformer Circuits, Feature Visualization, Mechanistic Interpretability |

### 4.2 비즈니스/경영/전략

| 전문가 | 전문 분야 | 핵심 용어/프레임워크 |
|--------|----------|---------------------|
| **Michael Porter** | 경쟁 전략 | Five Forces, Value Chain, Competitive Advantage, Generic Strategies |
| **Clayton Christensen** | 혁신 전략 | Disruptive Innovation, Jobs-to-be-Done, Innovator's Dilemma |
| **Peter Drucker** | 경영 일반 | Management by Objectives, Knowledge Worker, Effectiveness |
| **Jim Collins** | 기업 성과 | Good to Great, BHAG, Hedgehog Concept, Level 5 Leadership |
| **Herbert Simon** | 의사결정 | Bounded Rationality, Satisficing, Administrative Behavior |

### 4.3 마케팅/브랜딩

| 전문가 | 전문 분야 | 핵심 용어/프레임워크 |
|--------|----------|---------------------|
| **Philip Kotler** | 마케팅 전략 | STP, Marketing Mix(4P→7P), CLV, Holistic Marketing |
| **Seth Godin** | 혁신 마케팅 | Purple Cow, Permission Marketing, Tribes, The Dip |
| **David Aaker** | 브랜드 전략 | Brand Equity Model, Brand Architecture, Brand Identity |
| **Al Ries / Jack Trout** | 포지셔닝 | Positioning, 22 Laws of Marketing, Mind Share |
| **Byron Sharp** | 마케팅 사이언스 | How Brands Grow, Mental Availability, Physical Availability |

### 4.4 UX/디자인

| 전문가 | 전문 분야 | 핵심 용어/프레임워크 |
|--------|----------|---------------------|
| **Don Norman** | 인지 디자인 | Affordance, Gulf of Execution/Evaluation, Human-Centered Design |
| **Jakob Nielsen** | 사용성 공학 | 10 Heuristics, Usability Testing, Nielsen's Law |
| **Jef Raskin** | 인터페이스 디자인 | The Humane Interface, Cognitive Load, Modeless UI |
| **Edward Tufte** | 정보 시각화 | Data-Ink Ratio, Sparklines, Small Multiples, Chartjunk |
| **Steve Krug** | 웹 사용성 | Don't Make Me Think, Trunk Test, Usability Walk-through |

### 4.5 데이터/분석

| 전문가 | 전문 분야 | 핵심 용어/프레임워크 |
|--------|----------|---------------------|
| **Nate Silver** | 통계적 예측 | Signal vs Noise, Bayesian Thinking, Probabilistic Forecasting |
| **Edward Tufte** | 데이터 시각화 | Data-Ink Ratio, Sparklines, Analytical Design Principles |
| **Hans Rosling** | 데이터 커뮤니케이션 | Factfulness, Gap Instinct, Dollar Street, Animated Charts |
| **Hadley Wickham** | 데이터 과학/R | Tidy Data, Grammar of Graphics (ggplot2), Tidyverse |
| **DJ Patil** | 데이터 전략 | Data Products, Data-Driven Decision Making |

### 4.6 교육/학습과학

| 전문가 | 전문 분야 | 핵심 용어/프레임워크 |
|--------|----------|---------------------|
| **Seymour Papert** | 구성주의 학습 | Constructionism, Mindstorms, Objects to Think With, Logo |
| **Lev Vygotsky** | 사회적 학습 | ZPD(Zone of Proximal Development), Scaffolding, Mediation |
| **Benjamin Bloom** | 교육 평가 | Bloom's Taxonomy, Mastery Learning |
| **K. Anders Ericsson** | 전문성 연구 | Deliberate Practice, 10000 Hour Rule, Expert Performance |
| **John Hattie** | 메타분석 | Visible Learning, Effect Size, Feedback |

### 4.7 심리학/행동과학

| 전문가 | 전문 분야 | 핵심 용어/프레임워크 |
|--------|----------|---------------------|
| **Daniel Kahneman** | 행동경제학 | System 1/2, Heuristics & Biases, Prospect Theory, Anchoring |
| **Gary Klein** | 자연적 의사결정 | RPD(Recognition-Primed Decision), Premortem, NDM |
| **Mihaly Csikszentmihalyi** | 몰입 | Flow State, Optimal Experience, Autotelic Personality |
| **Robert Cialdini** | 설득 심리학 | 6 Principles of Influence, Pre-suasion, Social Proof |
| **Angela Duckworth** | 그릿/끈기 | Grit, Deliberate Practice, Passion + Perseverance |

### 4.8 의학/건강과학

| 전문가 | 전문 분야 | 핵심 용어/프레임워크 |
|--------|----------|---------------------|
| **Atul Gawande** | 의료 품질/체크리스트 | Checklist Manifesto, Positive Deviance, Coaching in Medicine |
| **Siddhartha Mukherjee** | 종양학/유전학 | Emperor of All Maladies, Gene, Cancer Biology |
| **John Ioannidis** | 메타연구/근거중심의학 | "Why Most Published Research Findings Are False", Meta-analysis |
| **Ben Goldacre** | 근거중심의학 비판 | Bad Science, Bad Pharma, Systematic Review, P-hacking |
| **Eric Topol** | 디지털 의료 | Deep Medicine, AI in Healthcare, Patient Empowerment |

### 4.9 법률/규제

| 전문가 | 전문 분야 | 핵심 용어/프레임워크 |
|--------|----------|---------------------|
| **Lawrence Lessig** | 사이버법 | Code is Law, Creative Commons, Four Regulators |
| **Cass Sunstein** | 행동 규제 | Nudge, Cost-Benefit Analysis, Libertarian Paternalism |
| **Tim Wu** | 기술/독점 규제 | The Master Switch, Net Neutrality, Attention Merchants |
| **Ryan Calo** | AI 법학 | Algorithmic Accountability, Robot Law, Digital Intermediaries |

### 4.10 금융/투자

| 전문가 | 전문 분야 | 핵심 용어/프레임워크 |
|--------|----------|---------------------|
| **Benjamin Graham** | 가치 투자 | Margin of Safety, Mr. Market, Intrinsic Value |
| **Warren Buffett** | 투자 철학 | Moat, Circle of Competence, Owner's Earnings |
| **Ray Dalio** | 매크로/원칙 | Principles, All Weather Portfolio, Machine Economy |
| **Aswath Damodaran** | 기업 가치평가 | DCF, Narrative + Numbers, Valuation |
| **Nassim Taleb** | 리스크/불확실성 | Black Swan, Antifragile, Skin in the Game, Fat Tails |

### 4.11 글쓰기/저널리즘/콘텐츠

| 전문가 | 전문 분야 | 핵심 용어/프레임워크 |
|--------|----------|---------------------|
| **William Zinsser** | 논픽션 글쓰기 | On Writing Well, Clarity, Simplicity, Clutter-Free |
| **Stephen King** | 창작 글쓰기 | On Writing, Show Don't Tell, Kill Your Darlings |
| **Ann Handley** | 콘텐츠 마케팅 | Everybody Writes, Content Rules, Brand Journalism |
| **Joseph Campbell** | 내러티브 구조 | Hero's Journey, Monomyth, Archetypes |
| **Robert McKee** | 스토리 구조 | Story, Inciting Incident, Climax, Arc |

### 4.12 인지과학/확장된 마음 (Deep-Cut)

> 아래는 연구자 레벨의 전문가로, 깊은 분석이 필요할 때 활용한다.

| 전문가 | 전문 분야 | 핵심 용어/프레임워크 |
|--------|----------|---------------------|
| **Andy Clark** | 확장된 마음 | Extended Mind, Cognitive Extension, Predictive Processing |
| **Edwin Hutchins** | 분산 인지 | Distributed Cognition, Cognition in the Wild |
| **Lucy Suchman** | 상황적 행동 | Plans and Situated Actions, Human-Machine Interaction |
| **Karl Weick** | 센스메이킹 | Sensemaking, Enactment, Organizational Resilience |
| **Donald Schön** | 반성적 실천 | Reflective Practitioner, Reflection-in-Action |
| **Alison Gopnik** | 아동 탐색/가설생성 | Theory Theory, Bayesian Children, Exploration vs Exploitation |
| **Peter Gärdenfors** | 개념 공간 | Conceptual Spaces, Geometric Cognition |
| **Francisco Varela** | 체화 인지 | Enactivism, Autopoiesis, Embodied Mind |
| **Virginia Satir** | 시스템 치료 | Self-Other-Context, Communication Stances, Congruence |
| **W. Timothy Gallwey** | 이너 게임 | Self 1/Self 2, Non-judgmental Awareness, Performance Coaching |

---

## 5. 전문가 없을 때 폴백 메커니즘

데이터베이스에 해당 분야 전문가가 없을 경우:

### 방법 1: AI에게 전문가 탐색 요청

```markdown
"[특정 분야]의 가장 영향력 있는 연구자/실무가 3명을 추천하라.
각각의 대표 저서, 핵심 프레임워크, 주요 용어 3-5개를 포함할 것."
```

### 방법 2: 웹 검색 활용

```
1. 해당 분야 + "influential researchers" 또는 "seminal works" 검색
2. Top 3 전문가 식별
3. 그들의 핵심 프레임워크/용어 추출
4. 프롬프트에 삽입
```

### 방법 3: 메타프롬프팅

> AI에게 해당 분야 프롬프트를 먼저 작성하게 하면, 업계 개념/정의/관행/평가 기준이 자동 포함된다.

```markdown
"당신은 [분야] 전문가입니다. 이 분야에서 [작업]을 수행하는 최적의 프롬프트를 작성하라.
업계에서 사용하는 전문 용어, 관행적인 산출물 구조, 좋은 결과를 가르는 평가 기준을 반드시 포함할 것."
```

---

## 6. 도메인 프라이밍 적용 예시 (Before/After)

### 예시 1: 소프트웨어 아키텍트

```markdown
❌ Before:
"API 설계를 리뷰해줘. 잘 되어있는지 확인해줘."

✅ After:
"Martin Fowler의 Richardson Maturity Model과 Robert C. Martin의 SOLID 원칙에 입각하여
아래 REST API 설계를 리뷰하라.

평가 기준:
1. Richardson Level 3 (HATEOAS) 준수 여부
2. Single Responsibility Principle 적용 여부
3. API Versioning 전략 (URI vs Header)
4. 에러 응답 표준화 (RFC 7807 준수)

출력: 항목별 점수(1-5) + 개선 제안 + 리팩토링 우선순위"
```

### 예시 2: 마케팅 전략가

```markdown
❌ Before:
"브랜드 포지셔닝 전략을 세워줘. 좋은 전략으로."

✅ After:
"David Aaker의 Brand Equity Model과 Al Ries의 Positioning 법칙에 입각하여
[브랜드명]의 B2C 시장 포지셔닝 전략을 수립하라.

분석 프레임:
1. Aaker의 Brand Identity Prism: 물리적 특성, 개성, 문화, 관계, 반영, 자기이미지
2. Ries의 Law of Focus: 하나의 단어/개념 선점 전략
3. Byron Sharp의 Mental Availability: 브랜드 연상 구축 전략

출력: 포지셔닝 맵 + 타겟 세그먼트 프로필 + 차별화 메시지 3가지 + 실행 로드맵"
```

### 예시 3: 데이터 분석가

```markdown
❌ Before:
"데이터 시각화를 자세히 해줘."

✅ After:
"Edward Tufte의 Analytical Design 원칙과 Stephen Few의 Dashboard Design에 입각하여
아래 매출 데이터의 시각화 전략을 제안하라.

적용 원칙:
1. Tufte의 Data-Ink Ratio 최대화
2. Few의 Information Dashboard Design: 핵심 지표 우선 배치
3. Nate Silver의 Signal vs Noise 접근: 의미 있는 트렌드만 부각

금지사항:
- 3D 차트, 불필요한 장식(Chartjunk) 사용 금지
- 이중 축(Dual Axis) 차트 지양
- 색상 7개 초과 사용 금지

출력: 차트 유형 선택 근거 + 대시보드 레이아웃 + Sparkline 적용 구간"
```

---

## 7. 프롬프트 작성 최종 체크리스트

프롬프트 작성 전 자문:

```
□ 전문가 지명: 해당 분야 실제 전문가 1-3명을 지명했는가?
□ 전문 용어: 전문가의 프레임워크/이론/용어를 사용했는가?
□ 범위 지정: 탐색 범위가 명확한가? (도메인, 세부 분야)
□ 목적 고정: 성공 조건이 정의되어 있는가?
□ 형식 강제: 출력 구조가 지정되어 있는가?
□ 오류 금지: 하지 말아야 할 것이 명시되어 있는가?
□ 행동 지정: 작업 방식이 지시되어 있는가?
□ 금지어 제거: 알아서잘/깔끔하게/대충/자세히/완벽하게/적당히 제거했는가?
□ 결과물 구상: 원하는 출력의 모습을 미리 구상했는가?
```

---

## 8. 참조 원칙 요약

### 프롬프트 쿠튀르 핵심

> "같은 AI를 쓰는데 왜 전문가가 더 잘 쓸까?"

| 일반 사용자 | 전문가 |
|------------|--------|
| "자세히 설명해줘" | 업계 용어로 범위 지정 |
| 넓은 들판에서 평균적 답변 | 좁은 문제 공간에서 정확한 답변 |
| 완연한 문장 + 부사 | 명확한 키워드 조합 |
| 한 번에 완성하려 함 | 생성→검토→수정 루프 |

### Master Class 핵심

> "프롬프트 엔지니어링은 LLM의 잠재 공간을 정확한 토큰으로 타격하여 원하는 지능을 꺼내 쓰는 아키텍처링 행위"

**3대 원칙:**
1. **Skill Architecture**: 프롬프트를 재사용 가능한 스킬 단위로 모듈화
2. **Domain Priming**: 적확한 토큰으로 전문가 영역 활성화
3. **Human-AI Loop**: 인간이 방향을 설정하고, AI가 지식을 펼치고, 인간이 평가하는 반복

---

## Metadata

- **Version**: 1.0.0
- **Created**: 2026-02-02
- **Changes v1.0.0**: 초기 생성
  - 핵심 원칙 (잠재 공간 활성화, 5가지 역할, 금지어 6개)
  - 도메인 프라이밍 5단계 적용법
  - 품질 수렴 루프
  - 전문가 데이터베이스 12개 도메인 (60+ 전문가)
  - 폴백 메커니즘 (전문가 탐색, 웹 검색, 메타프롬프팅)
  - Before/After 적용 예시 3개
  - 프롬프트 작성 최종 체크리스트
