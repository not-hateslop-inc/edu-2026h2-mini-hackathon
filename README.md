# edu-2026h2-mini-hackathon

2026 하반기 11회차 **LLM Agent 미니 해커톤** (EDU-2026-H2-11, 2026-11-19) 저장소입니다. 환경: Python 3.12, Conda 환경 `hs-2026h2`

운영안은 2025 하반기(EDU-2025-H2-14), 2026 상반기(EDU-2026-H1-10)를 다시 썼고, 필수 요건과 평가 방식만 바꿨습니다.

## 시작

```bash
cp -r template teams/{팀명}
cd teams/{팀명}
python agent.py
python eval/run_eval.py
```

## 필수 요건

- [ ] 최대 실행 단계(`recursion_limit`)와 초과 시 안내 문장
- [ ] Tool 오류 재시도 제한
- [ ] 쓰기·보내기 동작에 `interrupt` 승인
- [ ] Trace JSONL 저장 (`traces/`)
- [ ] 평가 세트 10개(`eval/cases.jsonl`)와 `run_eval.py` 결과
- [ ] MCP 서버를 붙였다면 7회차 보안 점검표
- [ ] README: 문제, 사용자, 구조도, 실행 방법, 한계

## 평가 (10회차 기준)

| 항목 | 비중 |
| --- | --- |
| 평가 세트 통과율 (팀 10개 + 운영진 비공개 5개) | 30% |
| 종료 조건·실패 처리·승인 | 25% |
| Trace로 동작 설명 | 20% |
| 문제 정의와 사용자 가치 | 15% |
| 발표 | 10% |

행사용 API Key는 정기 교육용과 다른 키입니다. 팀별 하루 상한이 있고, 행사 후 폐기합니다. 발표 화면에 `.env`가 보이지 않게 해 주세요.

결과는 `RESULTS.md`를 확인해 주세요.
