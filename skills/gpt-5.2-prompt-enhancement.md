# GPT-5.2 프롬프트 향상 스킬

> GPT-5.2 최적화 프롬프트 패턴 적용

## 개요

이 스킬은 사용자가 GPT-5.2용 프롬프트 생성을 요청할 때 OpenAI의 공식 프롬프팅 가이드에 기반한 최적화 패턴을 자동으로 적용합니다.

## 트리거 조건

다음 상황에서 이 스킬을 활성화:
- 사용자가 "GPT-5.2용 프롬프트" 생성 요청
- 사용자가 "ChatGPT 프롬프트" 작성 요청 후 GPT-5.2 확인됨
- 사용자가 프롬프트에 "5.2" 또는 "GPT-5.2" 언급

## 필수 적용 패턴

### 1. 장황함 제어 (output_verbosity_spec)

모든 GPT-5.2 프롬프트에 포함:

```xml
<output_verbosity_spec>
- 기본: 3-6문장 또는 글머리 5개 이하
- 예/아니오 질문: 2문장 이하
- 복잡한 작업: 개요 1문단 + 글머리 5개
- 긴 서술 문단 금지, 짧은 글머리 선호
- 사용자 요청 재진술 금지
</output_verbosity_spec>
```

### 2. 범위 제약 (design_and_scope_constraints)

코딩/디자인 작업 시 포함:

```xml
<design_and_scope_constraints>
- 요청한 것만 정확히 구현
- 추가 기능/컴포넌트/UX 개선 금지
- 모호하면 가장 단순한 해석 선택
</design_and_scope_constraints>
```

### 3. 불확실성 처리 (uncertainty_and_ambiguity)

정보 검색/분석 작업 시 포함:

```xml
<uncertainty_and_ambiguity>
- 모호하면 명확화 질문 1-3개 또는 2-3개 해석 제시
- 불확실하면 정확한 수치 조작 금지
- "제공된 맥락에 따르면..." 표현 사용
</uncertainty_and_ambiguity>
```

### 4. 도구 사용 규칙 (tool_usage_rules)

에이전트/도구 기반 작업 시 포함:

```xml
<tool_usage_rules>
- 내부 지식보다 도구 우선
- 독립적 읽기 작업은 병렬화
- 쓰기/업데이트 후 변경 사항 재진술
</tool_usage_rules>
```

### 5. 구조화된 추출 (extraction_spec)

데이터 추출 작업 시 포함:

```xml
<extraction_spec>
- 스키마 정확히 따르기 (추가 필드 금지)
- 소스에 없으면 null (추측 금지)
- 반환 전 누락 필드 재스캔
</extraction_spec>
```

## 프롬프트 생성 워크플로우

1. **작업 유형 파악**: 코딩, 분석, 리서치, 추출 중 식별
2. **필수 패턴 선택**: 작업 유형에 맞는 XML 블록 선택
3. **프롬프트 구조화**:
   - 역할/페르소나 정의
   - 핵심 지시사항
   - 적용 가능한 XML 제약 블록
   - 출력 형식 지정
4. **검증**: 범위 표류 방지, 장황함 제어 포함 확인

## 예시: 웹 리서치 에이전트 프롬프트

```xml
<web_research_agent>
  <role>전문가 연구 보조자</role>

  <core_mission>
    - 사용자 질문에 완전하고 도움되게 답변
    - 사실 조작 금지, 검증 불가 시 명확히 진술
    - 기본값은 상세하고 유용하게
  </core_mission>

  <output_verbosity_spec>
    - 기본: 3-6문장 또는 글머리 5개 이하
    - 복잡한 질문: 개요 1문단 + 핵심 글머리
  </output_verbosity_spec>

  <uncertainty_and_ambiguity>
    - 불확실하면 웹 검색 선호
    - 모든 웹 정보에 인용 포함
    - 명확화 질문 금지, 모든 의도 포괄
  </uncertainty_and_ambiguity>
</web_research_agent>
```

## 참고 자료

- [[GPT-5.2-Prompting-Complete-Guide]]
- [[GPT-5.2-XML-프롬프트-모음]]
- [OpenAI Cookbook - GPT-5.2 Prompting Guide](https://cookbook.openai.com/examples/gpt-5/gpt-5-2_prompting_guide)
