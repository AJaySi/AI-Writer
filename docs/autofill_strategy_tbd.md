### Autofill: Learning, Personalization, and Explainability

This document outlines next-step enhancements for Content Strategy Autofill focusing on: learning from user acceptances, industry presets, constraint-aware generation, explainability, and RAG-lite context. It also captures the trade-offs for sectioned generation vs single-call generation.

## Goals
- Increase accuracy, personalization, and trust without increasing UI complexity.
- Keep costs predictable while reducing timeouts and retries.
- Preserve user control: never overwrite locked/accepted fields without consent.

## Single-call vs Sectioned Generation
- Single-call (current):
  - Pros: 1 AI request, simpler orchestration.
  - Cons: Larger prompt, higher timeout risk, brittle for structured JSON, hard to pinpoint failures.
- Sectioned (per category):
  - Pros: Shorter prompts, better accuracy, quicker partial results, granular retries; lower latency per section; easier streaming (“Category X complete”).
  - Cons: More calls; must cap/parallelize and cache to control cost.
- Recommendation: Hybrid
  - Default: single-call for fast baseline; fallback/option: sectioned generation for users with large sites or when single-call fails/times out.
  - Implement a server flag `mode=hybrid|single|sectioned` and a per-user policy (feature flag).

## Learning from Acceptances
- Data we already persist: `content_strategy_autofill_insights` (accepted fields + sources/meta).
- Learning policy:
  - Build a per-user profile vector of “accepted values” and “field tendencies” (e.g., formats: video, cadence: weekly; brand voice: authoritative).
  - During refresh:
    - Use these as soft priors in prompt (“Bias toward previously accepted values unless contradictory to new constraints”).
    - Prefer stable fields to remain unchanged unless explicitly unconstrained.
- Storage additions:
  - Add fields to `content_strategy_autofill_insights` meta: `industry`, `company_size`, `accepted_at`.
  - Maintain a compact, cached user profile (derived) for prompt injection.
- Safety:
  - Respect locked fields (frontend lock) → never modified by refresh.

## Industry Presets
- Purpose: Cold-start quality boost.
- Source: curated presets per industry, company size, and region.
- Shape:
  - Minimal key set aligned to core inputs (e.g., `preferred_formats`, `content_frequency`, `brand_voice`, `editorial_guidelines` template).
- Retrieval:
  - Endpoint: GET `/autofill/presets?industry=...&size=...&region=...` (cached).
- Merge policy:
  - Apply only to empty fields; AI may override if constraints request.

## Constraint-Aware Generation
- User constraints: budget ceiling, cadence/frequency, format allowlist, timeline bounds.
- UI:
  - “Constraints” panel (chip-set) accessible from header/Progress area.
- Backend:
  - Accept constraints in refresh request (query/body).
  - Inject constraints into prompt header and soft-validate outputs.
- Validation:
  - Enforce with server-side validators; warn if AI violates, and auto-correct when safe.

## Explain This Suggestion (Mini-modal)
- Trigger: info icon next to each field.
- Content:
  - Short justification text (one or two sentences), sources (onboarding/RAG docs), confidence.
  - No raw chain-of-thought; ask model for a concise rationale summary that’s safe to expose.
- Backend payload additions:
  - For each field: `meta[field] = { rationale: string, sources: string[] }` (optional).
- Caution: redact sensitive content; keep rationale brief and non-speculative.

## RAG-lite: Retrievable Context for Refresh
- Context sources:
  - Latest website crawl snippets (top pages, headings, meta), recent analytics top pages (if connected), competitor headlines if available.
- Ingestion:
  - Lightweight index (in-memory/SQLite) with page URL, title, summary; refresh on demand with TTL.
- Prompt strategy:
  - Provide 3–5 top relevant snippets per category; keep token budget small.
- Controls:
  - User toggle “Use live site signals” in refresh.

## API Additions
- Refresh
  - GET `/autofill/refresh/stream?ai_only=true&constraints=...&mode=hybrid&use_rag=true`
  - Non-stream POST variant mirrors params.
- Presets
  - GET `/autofill/presets?industry=...&size=...&region=...` → returns compact preset payload.
- Acceptances (existing)
  - POST `/{strategy_id}/autofill/accept` → persist accepted fields with transparency/meta.

## UI Enhancements
- Per-field lock and regenerate
  - Lock prevents overwrite; Regenerate calls sectioned refresh for that field’s category.
- Diff view on refresh
  - Show before → after per field with accept/revert quick actions.
- Constraints chips
  - Visible summary in header; edit inline.
- “Explain” modal
  - Shows rationale and sources for the current value.

## Observability & Metrics
- Track per-field fill-rate, violation corrections, latency (per section), AI cost per refresh.
- Alert on sudden drops in non-null field count or spike in violations/timeouts.

## Rollout Plan
1) Phase 1 (Low risk): presets + constraints + per-field lock, no sectioning.
2) Phase 2: sectioned generation behind a feature flag; per-field regenerate.
3) Phase 3: RAG-lite snippets and explain modal; start learning from acceptances in prompts.
4) Phase 4: tune/fine-grain priors and add advanced validation rules per industry.

## References
- Gemini structured output: https://ai.google.dev/gemini-api/docs/structured-output 