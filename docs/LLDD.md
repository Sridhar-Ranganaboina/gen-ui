# Low-Level Design Document (LLDD)

## Sprint-wise Implementation Plan and Codex Development Backlog

### 1. Delivery Assumptions

| Item | Recommendation |
| --- | --- |
| Sprint duration | 2 weeks |
| MVP duration | 8 sprints / 16 weeks |
| Team model | Platform backend, SDK/frontend, data engineering, ML/LLM, DevOps, QA |
| First production target | One web application, one GenUI slot, rule-based + memory-backed personalization |
| Initial SDK target | React SDK + plain JavaScript SDK |
| Deferred to later | Full Flutter SDK, Teams/Outlook adapter, advanced ML ranking, multi-agent workflows |

### 2. Sprint Roadmap Summary

| Sprint | Theme | Main Outcome |
| --- | --- | --- |
| Sprint 0 | Foundation & Planning | Repo, architecture decisions, contracts, environment setup |
| Sprint 1 | Contracts & Core API Skeleton | Decision API, Event API, UI Manifest schema |
| Sprint 2 | GenUI SDK Foundation | React SDK, Web SDK, GenUI slot rendering |
| Sprint 3 | Orchestrator & Rule Engine | Request orchestration, eligibility rules, fallback path |
| Sprint 4 | Memory Model & Event Pipeline | Employee memory, interaction events, memory updates |
| Sprint 5 | GenUI Runtime & Admin Registry | Component catalog, app/surface/slot registry |
| Sprint 6 | LLM Composer & Governance | Structured UI/content generation with policy validation |
| Sprint 7 | Experimentation, Observability & Audit | A/B testing, telemetry, audit dashboards |
| Sprint 8 | Hardening & Pilot Rollout | Security, performance, onboarding guide, pilot app integration |

### 3. Sprint 0: Foundation & Planning

#### Objective
Set up the engineering foundation so Codex and developers can start building safely with clear boundaries.

#### Deliverables

| Task ID | Task | Description | Owner |
| --- | --- | --- | --- |
| S0-T1 | Create mono-repo structure | Create /contracts, /services, /sdks, /apps, /infra, /docs folders | Tech Lead |
| S0-T2 | Define architecture decision records | Add ADRs for SDK approach, schema-driven rendering, event model, LLM constraints | Architect |
| S0-T3 | Define initial MVP scope | Confirm first channel, first app, first surface, first GenUI slot | Product + Architect |
| S0-T4 | Create local dev environment | Docker Compose for API, Redis, Postgres, Kafka/mock queue | Backend |
| S0-T5 | Setup CI pipeline | Lint, test, build, contract validation | DevOps |
| S0-T6 | Define coding standards | TypeScript, Java/Python, naming conventions, logging standards | Tech Lead |
| S0-T7 | Define security baseline | Auth assumptions, token propagation, PII handling rules | Security |

#### Acceptance Criteria
- Repo structure is created.
- CI pipeline runs on pull request.
- Local developer setup works.
- ADRs are available in /docs/adrs.
- MVP scope is finalized.

### 4. Sprint 1: Contracts & Core API Skeleton

#### Objective
Build contract-first foundation for all future development.

#### Deliverables

| Task ID | Task | Description | Owner |
| --- | --- | --- | --- |
| S1-T1 | Create DecisionRequest schema | Define canonical request from app/SDK to platform | Backend |
| S1-T2 | Create DecisionResponse schema | Define response containing decision, UI manifest, audit metadata | Backend |
| S1-T3 | Create UI Manifest schema | Define JSON schema for card, banner, CTA, form, table, carousel | Frontend |
| S1-T4 | Create SignalEvent schema | Define interaction events: impression, click, dismiss, submit, error | Data |
| S1-T5 | Create OpenAPI spec | APIs for /v1/decisions/evaluate, /v1/events/interactions | Backend |
| S1-T6 | Generate API clients | Generate TypeScript client from OpenAPI | Backend |
| S1-T7 | Build API skeleton | Create empty endpoints with validation and mock responses | Backend |
| S1-T8 | Add contract tests | Validate sample payloads against schema | QA |

#### Core APIs
- `POST /v1/decisions/evaluate`
- `POST /v1/events/interactions`
- `GET /v1/ui-manifests/{manifestId}`

#### Acceptance Criteria
- OpenAPI contract is available.
- JSON schemas validate successfully.
- Mock Decision API returns valid DecisionResponse.
- Event API accepts SignalEvent payload.
- TypeScript API client is generated.

### 5. Sprint 2: GenUI SDK Foundation

#### Objective
Create the first SDK that AD teams can easily integrate into existing applications.

#### Deliverables

| Task ID | Task | Description | Owner |
| --- | --- | --- | --- |
| S2-T1 | Create SDK core package | @jpmc/genui-core with API client, config, context builder | SDK Team |
| S2-T2 | Create React SDK package | @jpmc/genui-react with Provider and Slot components | SDK Team |
| S2-T3 | Create Web SDK package | @jpmc/genui-web for legacy apps using script tag and data attributes | SDK Team |
| S2-T4 | Implement GenUIProvider | Initializes app ID, user context, channel, session | SDK Team |
| S2-T5 | Implement GenUISlot | Calls Decision API and renders returned UI manifest | SDK Team |
| S2-T6 | Add fallback support | Show default fallback component when GenUI fails | SDK Team |
| S2-T7 | Add SDK telemetry | Track render success, failure, latency, impression | SDK Team |
| S2-T8 | Build sample app | React demo app with dashboard slot and fallback UI | Frontend |

#### React Integration Example
```tsx
<GenUIProvider
  appId="employee-portal"
  channel="web"
  contextProvider={getUserContext}
>
  <GenUISlot
    name="dashboard-hero"
    fallback={<DefaultDashboardHero />}
  />
</GenUIProvider>
```

#### Legacy Web Integration Example
```html
<div data-genui-slot="dashboard-hero"></div>
<script
  src="/genui-web-sdk.js"
  data-app-id="employee-portal">
</script>
```

#### Acceptance Criteria
- React app can render GenUI slot.
- Legacy web page can render GenUI slot using script-based SDK.
- SDK sends DecisionRequest to backend.
- SDK handles failure with fallback.
- SDK emits impression and render telemetry events.

### 6. Sprint 3: Orchestrator & Rule Engine

#### Objective
Build the first real personalization path without ML/LLM dependency.

#### Deliverables

| Task ID | Task | Description | Owner |
| --- | --- | --- | --- |
| S3-T1 | Build Orchestrator service | Normalize request, enrich context, call rule engine | Backend |
| S3-T2 | Build Rules Engine service | Evaluate eligibility, suppression, role-based rules | Backend |
| S3-T3 | Define rule DSL | JSON/YAML rule definition format | Backend |
| S3-T4 | Implement candidate selection | Select static/personalized candidates based on rules | Backend |
| S3-T5 | Implement priority resolver | Resolve conflicts across multiple eligible candidates | Backend |
| S3-T6 | Add fallback chain | Default content if no rule matches | Backend |
| S3-T7 | Add rule explainability | Return reason codes and rule hits in response | Backend |
| S3-T8 | Add golden rule tests | Unit tests for each rule scenario | QA |

#### Rule Example
```json
{
  "ruleId": "show-manager-action-card",
  "surface": "dashboard-hero",
  "conditions": [
    {
      "field": "roleContext.isManager",
      "operator": "equals",
      "value": true
    }
  ],
  "action": {
    "candidateId": "manager-pending-approvals-card",
    "priority": 90
  }
}
```

#### Acceptance Criteria
- Orchestrator receives DecisionRequest.
- Rule Engine returns eligible candidates.
- DecisionResponse contains selected candidate and reason codes.
- Fallback content is returned if no rule matches.
- Rule tests pass for manager, non-manager, restricted user, and fallback scenarios.

### 7. Sprint 4: Employee Memory Model & Event Pipeline

#### Objective
Enable real-time personalization based on employee behavior and journey state.

#### Deliverables

| Task ID | Task | Description | Owner |
| --- | --- | --- | --- |
| S4-T1 | Create memory schema | EmployeeMemorySnapshot, IntentState, JourneyState | Data + Backend |
| S4-T2 | Implement Memory Service | APIs for get/update memory snapshot | Backend |
| S4-T3 | Create Redis/Postgres storage | Redis for hot memory, Postgres for durable memory | Backend |
| S4-T4 | Implement Event API persistence | Store incoming SDK events | Backend |
| S4-T5 | Create event processor | Consume interaction events and update memory | Data |
| S4-T6 | Track recent interactions | Store recent clicks, dismissals, impressions | Data |
| S4-T7 | Track journey state | Maintain journey step and completion status | Data |
| S4-T8 | Add memory-based rules | Suppress dismissed cards, continue active journey | Backend |

#### Memory Snapshot Example
```json
{
  "employeeId": "E12345",
  "memoryVersion": 12,
  "roleContext": {
    "isManager": true,
    "department": "Technology",
    "location": "India"
  },
  "behavioralMemory": {
    "recentDismissedCards": ["training-reminder"],
    "recentClickedActions": ["pending-approval-card"]
  },
  "journeyState": {
    "activeJourneyId": "manager-productivity-journey",
    "currentStep": "review-pending-approvals"
  }
}
```

#### Acceptance Criteria
- SDK events are received and stored.
- Memory service returns snapshot under target latency.
- Interaction events update memory.
- Rule engine can use memory fields.
- Recently dismissed cards are suppressed.

### 8. Sprint 5: GenUI Runtime, Component Catalog & Admin Registry

#### Objective
Create controlled UI rendering using approved enterprise components.

#### Deliverables

| Task ID | Task | Description | Owner |
| --- | --- | --- | --- |
| S5-T1 | Build component catalog | Define approved components: card, banner, CTA, form, table | Frontend |
| S5-T2 | Build manifest renderer | Convert UI Manifest JSON to React components | Frontend |
| S5-T3 | Add manifest validation | Validate component type, props, action type | Frontend |
| S5-T4 | Create App Registry | Register appId, owner, allowed channels | Backend |
| S5-T5 | Create Surface Registry | Register surfaces like dashboard, profile, workflow page | Backend |
| S5-T6 | Create Slot Registry | Register allowed GenUI slots per app/surface | Backend |
| S5-T7 | Create Action Registry | Register allowed actions: open link, modal, create task, dismiss | Backend |
| S5-T8 | Add admin seed scripts | Seed sample app/surface/slot/config | Backend |

#### UI Manifest Example
```json
{
  "schemaVersion": "1.0.0",
  "surface": "employee-dashboard",
  "slot": "dashboard-hero",
  "components": [
    {
      "type": "summary_card",
      "id": "pending-approvals-card",
      "props": {
        "title": "You have pending approvals",
        "body": "3 approvals are waiting for your review.",
        "cta": {
          "label": "Review now",
          "action": "open_link",
          "target": "/approvals"
        }
      }
    }
  ]
}
```

#### Acceptance Criteria
- Only approved components can render.
- Invalid UI manifest is rejected.
- App/surface/slot registry is available.
- Decision API validates requested slot against registry.
- React SDK renders manifest from component catalog.

### 9. Sprint 6: LLM Composer & Governance

#### Objective
Add controlled GenAI capability for content and UI composition without allowing the LLM to bypass rules or policy.

#### Deliverables

| Task ID | Task | Description | Owner |
| --- | --- | --- | --- |
| S6-T1 | Build LLM Composer service | Compose title/body/summary/UI props using approved context | GenAI Team |
| S6-T2 | Add structured output schema | Force LLM output into approved UI Manifest schema | GenAI Team |
| S6-T3 | Add prompt templates | Create prompts for summary card, action card, email block | GenAI Team |
| S6-T4 | Add policy validator | Validate PII, tone, forbidden claims, unsupported actions | Security + GenAI |
| S6-T5 | Add hallucination guardrails | LLM can only use facts provided by orchestrator | GenAI Team |
| S6-T6 | Add timeout fallback | Return static content if LLM fails or times out | Backend |
| S6-T7 | Add LLM audit fields | Store prompt version, model version, schema validation status | Backend |
| S6-T8 | Add GenAI test fixtures | Golden tests for valid/invalid LLM outputs | QA |

#### LLM Usage Rule
- The LLM must not decide what action to show.
- The LLM only composes approved content for an already selected candidate.

#### LLM Composer Flow
- Orchestrator
  - Rule Engine selects eligible candidate
  - Decision Engine ranks candidate
  - LLM Composer generates title/body/UI props
  - Schema Validator validates output
  - Policy Validator approves output
  - DecisionResponse returned to SDK

#### Acceptance Criteria
- LLM output always matches UI Manifest schema.
- Invalid LLM output is blocked.
- Policy failures trigger fallback content.
- Prompt version and model version are stored in audit log.
- LLM is not allowed to create unsupported actions.

### 10. Sprint 7: Experimentation, Observability & Audit

#### Objective
Make the platform measurable, auditable, and production-operable.

#### Deliverables

| Task ID | Task | Description | Owner |
| --- | --- | --- | --- |
| S7-T1 | Add experiment assignment | Deterministic bucket assignment by employee/app/surface | Backend |
| S7-T2 | Add A/B variant support | Variant A/B mapping in decision response | Backend |
| S7-T3 | Add exposure event | Emit experiment exposure event from SDK | SDK Team |
| S7-T4 | Add OpenTelemetry tracing | Trace request across SDK, API, orchestrator, rules, memory, LLM | DevOps |
| S7-T5 | Add metrics dashboards | Latency, error rate, render success, fallback rate, policy block rate | DevOps |
| S7-T6 | Add decision audit log | Store selected action, rule hits, model/LLM metadata, reason codes | Backend |
| S7-T7 | Build basic audit viewer | Search decision by decisionId/user/app/surface | Frontend |
| S7-T8 | Add alerting rules | SLO alerts for Decision API, Event API, SDK render failure | DevOps |

#### Key Metrics

| Metric | Target |
| --- | --- |
| Decision API availability | 99.9% MVP |
| Decision API p95 latency | < 700 ms without LLM |
| SDK render success | > 99% |
| Event ingestion success | > 99.5% |
| Schema validation pass rate | 100% for final response |
| Fallback rate | Monitored, should reduce over time |
| Policy block rate | Monitored by app/surface |

#### Acceptance Criteria
- Every decision has audit record.
- Every rendered GenUI experience emits exposure/impression.
- Traces are correlated using requestId and decisionId.
- Dashboards are available.
- Experiment assignment is deterministic.

### 11. Sprint 8: Hardening, Pilot Rollout & AD Team Onboarding

#### Objective
Prepare platform for first controlled application integration.

#### Deliverables

| Task ID | Task | Description | Owner |
| --- | --- | --- | --- |
| S8-T1 | Security review | Threat model, auth review, PII review, LLM safety review | Security |
| S8-T2 | Performance testing | Load test Decision API, Event API, Memory Service | QA |
| S8-T3 | Chaos testing | Test failure of LLM, Memory, Rule Engine, Event Pipeline | QA |
| S8-T4 | SDK documentation | Integration guide for React and legacy web apps | SDK Team |
| S8-T5 | AD onboarding checklist | App registration, slot creation, context provider, fallback UI | Product |
| S8-T6 | Pilot app integration | Integrate one real internal app with one GenUI slot | App Team + Platform |
| S8-T7 | Production readiness review | Runbook, support model, dashboards, rollback plan | DevOps |
| S8-T8 | Controlled rollout | Enable for small pilot user group | Product + Platform |

#### AD Team Onboarding Checklist
1. Register appId.
2. Register surface name.
3. Register GenUI slot name.
4. Install SDK.
5. Add GenUIProvider.
6. Add GenUISlot.
7. Provide user/context provider.
8. Add fallback UI.
9. Validate events in dashboard.
10. Complete production readiness checklist.

#### Acceptance Criteria
- One pilot app integrated successfully.
- One GenUI slot live for pilot users.
- Fallback works.
- Audit logs are generated.
- Dashboards are active.
- Rollback plan is tested.

### 12. Sprint-wise Codex Task Breakdown

#### Epic 1: Contracts
- S1-T1: Create decision-request.schema.json
- S1-T2: Create decision-response.schema.json
- S1-T3: Create ui-manifest.schema.json
- S1-T4: Create signal-event.schema.json
- S1-T5: Create decisions.openapi.yaml
- S1-T6: Create events.openapi.yaml
- S1-T7: Add schema validation tests
- S1-T8: Add mock payload fixtures

#### Epic 2: Backend Services
- S1-T9: Create Decision API service skeleton
- S1-T10: Create Event API service skeleton
- S3-T1: Create Orchestrator service
- S3-T2: Create Rule Engine service
- S4-T1: Create Memory Service
- S5-T1: Create Registry Service
- S6-T1: Create LLM Composer service
- S7-T1: Create Audit Service

#### Epic 3: SDKs
- S2-T1: Create @jpmc/genui-core package
- S2-T2: Create @jpmc/genui-react package
- S2-T3: Create @jpmc/genui-web package
- S2-T4: Implement GenUIProvider
- S2-T5: Implement GenUISlot
- S2-T6: Implement useGenUI hook
- S2-T7: Implement event tracking client
- S2-T8: Implement fallback rendering

#### Epic 4: UI Runtime
- S5-T1: Create component catalog
- S5-T2: Implement summary_card renderer
- S5-T3: Implement banner renderer
- S5-T4: Implement action_card renderer
- S5-T5: Implement form renderer
- S5-T6: Implement table renderer
- S5-T7: Implement UI manifest validator
- S5-T8: Implement action handler registry

#### Epic 5: Memory & Events
- S4-T1: Create memory database tables
- S4-T2: Implement GetMemorySnapshot API
- S4-T3: Implement UpdateMemorySnapshot API
- S4-T4: Implement event ingestion persistence
- S4-T5: Implement event processor
- S4-T6: Update memory from impression event
- S4-T7: Update memory from click event
- S4-T8: Update memory from dismiss event

#### Epic 6: Governance & Audit
- S6-T1: Implement schema validation gate
- S6-T2: Implement policy validation gate
- S6-T3: Implement LLM output sanitizer
- S6-T4: Implement prompt version registry
- S7-T1: Implement decision audit log
- S7-T2: Implement audit search API
- S7-T3: Implement audit viewer screen
- S7-T4: Add rule hit explanation
- S7-T5: Add policy outcome explanation

### 13. Recommended MVP Scope

#### MVP Should Include
- React SDK
- Plain JavaScript Web SDK
- Decision API
- Event API
- Orchestrator
- Rule Engine
- Memory Service
- Component Catalog
- UI Manifest Renderer
- Audit Log
- Basic LLM Composer
- One pilot app
- One GenUI slot

#### MVP Should Not Include Initially
- Full Flutter SDK
- Teams/Outlook adapter
- Advanced ML ranking
- Multi-agent orchestration
- Full admin console
- Cross-LOB enterprise rollout
- Autonomous UI generation without schema validation

### 14. Definition of Done
A task is complete only when:
- Code is implemented.
- Unit tests are added.
- Contract tests pass.
- Logs and metrics are added.
- Error handling is implemented.
- Security validation is done where applicable.
- Documentation is updated.
- Sample request/response is available.
- Code review is completed.

### 15. Final Implementation Sequence for Codex
1. Create repository structure.
2. Create JSON schemas.
3. Create OpenAPI specs.
4. Generate TypeScript API client.
5. Build Decision API mock.
6. Build Event API mock.
7. Build React SDK.
8. Build GenUISlot renderer.
9. Build Rule Engine.
10. Build Orchestrator.
11. Build Memory Service.
12. Build Event Processor.
13. Build Component Catalog.
14. Build LLM Composer.
15. Build Audit Service.
16. Build sample pilot app.
17. Add tests, telemetry, and hardening.

### Best LLDD Addition Summary
Add this section after API Contracts, Data Model, and Component Design.

Most important design decision:
AD teams should integrate using SDK and slots. The GenUI platform owns orchestration, personalization, memory, policy, audit, and GenAI composition. This keeps individual application-team effort low and allows enterprise-scale adoption.
