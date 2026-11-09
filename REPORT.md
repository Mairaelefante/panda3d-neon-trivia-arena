# Neon Trivia Arena: Technical Review and Proposed Development Roadmap

**Repository:** https://github.com/Mairaelefante/panda3d-neon-trivia-arena  
**Report date:** 2026-11-09  
**Status:** Python/Panda3D interactive game prototype. Code inspected, not executed or gameplay-tested.

## Overview

Neon Trivia Arena is a neon-themed 3D trivia arena prototype written in Python using Panda3D. The inspected `main.py` defines a main menu, an arena scene, lighting, four visually represented player podiums, a question UI, and controls for highlighting an answer and cycling questions.

This is **not yet a working scored trivia game**. The current interface explicitly describes question handling and scoring as placeholders.

## Implemented functionality observed in source

- Panda3D `ShowBase` application with window configuration and a menu.
- A scene generated from `CardMaker` cards, colored floor strips, labels and four podiums.
- Ambient light and two colored point lights.
- UI with `OnscreenText` and `DirectButton`; click to highlight a response.
- Keyboard controls: `1` through `4` highlight answers; `Space` advances; `Escape` returns to the menu.
- Question navigation with wraparound after the last question, dependent on a separately imported question collection.
- `.gitignore` for Python cache and common editor files.

## Problems and limitations identified

### Missing question module (blocking)
The script imports `from data.question import QUESTIONS`, but the inspected public repository root contains only `.gitignore`, `README.md`, `cover.svg`, and `main.py`. No `data/question.py` is present in that listing. Thus a clean checkout appears **unable to launch as-is**, unless additional files exist outside the checked repository. This should be remedied by adding a lawful, original sample question bank and documenting the expected schema.

### Scoring and validation are placeholders
`load_question()` displays an explicit placeholder message; `highlight_answer()` changes the UI color but does not check correctness. The score label is static and no round-completion logic is implemented.

### Scene lifecycle / UI cleanup
`enter_arena()` attaches new roots; `clear_scene()` removes those roots but the `answer_panels` list is not reset. Re-entering the arena may leave stale Python references and append new buttons. Verify with a repeated menu/arena smoke test, then reset the list and clean up resource lifetime.

### Data and robustness
There is no documented question validation, graceful handling of an empty question bank, persistence, accessibility validation, or automated regression testing.

### Documentation
The current README gives generic setup language including an unrelated `main.lua` entry point. Document Panda3D/Python prerequisites, exact launch command, controls, known limits, and the missing-module issue. Add dependency pinning as appropriate.

## Proposed roadmap (future work, not implemented yet)

| Workstream | Intended work | Estimated effort |
| --- | --- | ---: |
| Runnable prototype | Add original sample question bank, dependency manifest, setup instructions and smoke test | 4 h |
| Core game loop | Correct answer validation, score updates, rounds, progression and restart | 7 h |
| UX and input | Answer feedback, timer, navigation consistency and keyboard/UI accessibility | 5 h |
| Scene robustness | Fix UI node/button lifecycle, repeated arena transitions, cleanup and edge cases | 4 h |
| Content system | Question-bank schema validation, categories, randomized sequences and local data format | 5 h |
| Testing and documentation | Logic-focused automated tests, manual test matrix, README and release notes | 4 h |
| **Total proposed** | | **29 h** |

These hours are only **provisional estimates**. They are not worked hours, billable hours, user activity, or a guarantee that the work will happen. The owner should confirm that this is work they genuinely plan to do independently before referencing the plan in a BYOP submission.

## Suggested acceptance criteria

1. A fresh clone starts with documented commands on a supported Python/Panda3D installation.
2. Test questions have an explicit schema and valid correct-answer indices.
3. Answer selection produces correct/incorrect feedback and consistent score updates.
4. Reopening the arena repeatedly does not accumulate button references or corrupt game state.
5. The end of a round is handled, with visible result and restart controls.
6. Pure-Python question/scoring logic has automated tests, and GUI interactions have a documented manual test checklist.
7. No third-party confidential game content, employer/client IP, private user data or secrets are committed.

## BYOP eligibility checks to resolve before submission

- **Ownership and provenance:** The repo is in a personal GitHub account, but this does **not** establish that the work was created outside an employer, client, or university engagement. The owner must confirm the legal rights to the code and assets, especially given the possibility of professional game-development work.
- **License:** MIT license added at root. Check rights to any third-party assets or question content before redistribution.
- **Commit history:** Preserve original commits unchanged; do not fabricate or reconstruct development history.
- **Future work:** Proposed 29-hour development plan recorded above, subject to owner's genuine intent.
- **Secrets and regulated data:** No complete commit-history secret scan has been performed.
- **Execution:** The repository has not been installed or launched in this review, and missing `data.question` is a source-inspection concern rather than an observed traceback.

## Recommended next engineering action

Restore or author an original `data/question` module with a small synthetic question bank, document installation and launch, and verify menu/arena transitions. After it runs, extract testable scoring logic and implement a minimal complete single-player round. Make those changes in ordinary development commits.
