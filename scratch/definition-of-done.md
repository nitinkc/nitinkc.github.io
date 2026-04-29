# Definition of Done (DoD)

> **Spirit of DoD:** Can anything prevent us from shipping this work? All items below must be satisfied before a story is considered complete and ready for deployment.

---

## Story Level DoD

### AI-Assisted Development (GitHub Copilot)

- [ ] Code generated with GitHub Copilot has been **reviewed and understood** by the developer — no unreviewed AI-generated code is merged
- [ ] Copilot suggestions have been validated against acceptance criteria and team coding standards
- [ ] AI-generated unit tests have been reviewed and confirmed to cover intended scenarios

### Code Quality

- [ ] Development ("doing") is complete
- [ ] Code reviewed by **at least two peers** before merge
- [ ] Code merged into main branch
- [ ] Coding style guidelines followed
- [ ] Unit test coverage for new code is **≥ 80%**
- [ ] Accumulative unit tests written and passing
- [ ] No new unresolved defects — all testable tests executed

### Documentation

- [ ] Technical / support documentation updated (design documents, README, inline comments)
- [ ] CTF story files approved by the PO (where applicable)
- [ ] Deployment plan complete for all environments, including release version added to story

### Testing

- [ ] Developer has **reviewed and tested their own work** before peer review
- [ ] Manual testing completed by developer
- [ ] QA tested (where applicable)
- [ ] Integration tested (where applicable)
- [ ] Regression testing completed (where applicable)
- [ ] Locally tested — feature verified in local environment before raising for review

### Approval

- [ ] **Lead approval sought** — lead has reviewed and signed off before merging
- [ ] Acceptance criteria reviewed and met
- [ ] Story reviewed and **accepted by Product Owner (PO)**
- [ ] Demo completed (where applicable, per CTF guidelines)

### Closure

- [ ] All sub-tasks and sprint bugs associated with the story are closed (marked Done)

---

## Sprint Level DoD

All story-level DoD items are met, plus:

- [ ] All sub-tasks and sprint bugs resolved and closed
- [ ] Manual testing completed at a minimum; QA involvement where applicable
- [ ] Story accepted as done by Product Owner

---

## Release Level DoD

All sprint-level DoD items are met, plus:

- [ ] All bugs tested by DEV, demoed, and signed off by QA in all lower environments
- [ ] Regression testing completed and signed off by QA
- [ ] UAT completed and signed off
- [ ] All Pen test and Static Analysis issues addressed before release
- [ ] All stories and bugs deployed to production and E2E tested in production
- [ ] QA signs off on production testing
- [ ] **PO signs off on the deployment** after QA completes testing
- [ ] Align to style guide (font, colour, usage, filter availability and location)

---

## Quick Reference Checklist

| # | Check | Owner |
|---|-------|-------|
| 1 | Copilot-generated code reviewed & understood | Developer |
| 2 | Code review by 2+ peers & merged | Developer |
| 3 | Unit tests written, passing, ≥ 80% coverage | Developer |
| 4 | Docs updated (design doc, README, support docs) | Developer |
| 5 | Locally tested | Developer |
| 6 | QA tested | QA / Developer |
| 7 | Lead approval sought & received | Developer / Lead |
| 8 | Acceptance criteria met | Developer |
| 9 | PO sign-off | PO |
| 10 | All sub-tasks closed | Developer |
| 11 | Deployment plan complete | Developer |
