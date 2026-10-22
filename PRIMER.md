# PRIMER: Environmental-Message Persona System (handoff for a new model)

Written 2026-10-16. Root folder: `Research-Agenda/` (inside `identity-simulation-main-main/`).
Goal: embed theory-grounded LLM personas in a UI where users (a) ask personas questions and (b) test environmental
messages, to learn how different U.S. ideological groups would react and how to tailor messages to them.
Read this file first. Open the referenced files only when a task needs them.

---

## 1. User preferences (follow these)
- **Efficiency/energy matters.** Conflict order: correctness > verified correctness in few iterations > runtime
  efficiency > token/tool-call efficiency. See `Green Coding System Prompt.docx`. If that file is locked, copy it first.
  Practical rules:
  - keep responses short
  - batch tool calls and API calls; use batch APIs where latency allows
  - use smaller models (e.g., Sonnet/Haiku) for routine subtasks
  - classify hot vs. cold code paths before optimizing
- **Keep folders clean.** Analysis outputs go in `Segmentation/`.
- **Group and persona names are ideological, never party-based.**
- **Prompts never reveal which persona is "main" vs. "variant"** (see §4). The user may add that later.

## 2. File map

| Path | What it is | Read when |
|---|---|---|
| `Behavioral Layers.txt` (v2.2) | Theory: the 4-layer model, parameters/rules with stable IDs, message-response protocol | Building logic for updates, judging, or new personas |
| `Persona System.txt` (v1.2) | How persona prompts are written, run, and validated | Building the runtime, judge, or validation |
| `Behavioral Layers - original draft.txt` | The user's original 4-layer sketch | Rarely |
| `Personas NEW/*.txt` (18) | **Individual personas**: named people, 2nd person, ~1,100 words | Loaded as system prompts |
| `Personas Generic/*.txt` (18) | **Segment profiles**: 3rd person, layer by layer, plus a researcher context section | Loaded as system prompts |
| `Segmentation/` | Data pipeline: scripts, outputs, specs, writing briefs | Re-running or extending the data work |
| `Survey Data/` | WVS-US 2017, Pew ATP W158 (2024), VCSI (2026) with codebooks/questionnaires | Only for new analysis |
| Corpus PDFs | Schwartz; Stern et al. (VBN, NEP, moral norms, Stern 2000); Dunlap NEP; Tarrant & Cordell; Kahan ×3; Dake | Only to verify theory |

Exclude `Stern 2000 Psychology and the Science...pdf`: its publisher restricts AI use. The pre-existing
`identity-simulation-main-main/personas/` folder was NOT created in this work.

## 3. Theory in one page
Full detail is in `Behavioral Layers.txt`. Cite rules by ID (e.g., L3.R8); IDs are append-only.

- **L1 Core values (Schwartz)**: stable; trade-offs define a person. Environmental concern comes from
  self-transcendence/universalism, and in-group benevolence ≠ environmentalism (L1.R5). §2.
- **L2 Worldview**: two parts.
  - Nature: the NEP, a "folk ecological theory."
  - Society: Kahan's cultural cognition, with two axes, hierarchy-egalitarianism and individualism-communitarianism.
    Hierarchical individualists discount environmental risk through *identity-protective cognition*. Worldview ≠ party
    (L2.R12).
  - Also part of L2: political identity (L2.P9) and source trust (L2.P8). §3.
- **L3 Norm activation (Stern VBN)**: the chain runs awareness of consequences (to self/others/biosphere), then
  ascription of responsibility (self/industry/government), then personal norm. Values filter evidence. Costly asks
  trigger neutralization (L3.R8). §4.
- **L4 Behavior**: channels are consumer, policy approval, sacrifice/willingness to pay, citizenship, activism, and
  (optionally) organizational. Stern 2000's ABC model: attitudes matter most when context is neutral; habit,
  capability, and cost explain gaps (L4.R12-R14). §5.
- **CX and RS**: demographics modulate, never determine (§6). Survey response style is §7.
- **Message effects (§4.6, §9)**, important for message testing:
  - A solution frame that fits the audience's worldview increases belief in the *facts*; an offensive one decreases it.
  - Messenger cultural affinity matters; unexpected allies and plural messengers reduce polarization.
  - Balanced information can polarize.
  - Lectures and moralizing cause hardening.
  - Realistic shifts are small: at most 1 band per message, 2 if the issue is unfamiliar. Values never move.
- **Calibration (§10)**: real people are *imperfectly* coherent. §10.5 lists realistic tensions (T1-T15) and §10.6
  lists implausible patterns (X1-X10).

## 4. Segmentation summary
Details: `Segmentation/wvs_segmentation_report.txt`, `bridge_report.txt`, `persona_specs.txt`.

**Method**
1. Weighted k-means on 14 theory-grounded composites from WVS-US 2017 (N=2,586). Values, both worldview axes, and
   trust were inputs; party and ideology only describe the groups.
2. k=6 was chosen for stability (bootstrap ARI 0.68) and breadth.
3. Groups are regions of a continuum (silhouette ≈0.10), not hard types.

**Validation**: support for "environment over growth" (held out of clustering) falls monotonically from 86% to 24%
across the groups.

**The six groups** (left → right; share of the WVS sample)
1. **Secular Progressive Egalitarian** (15%): secular, egalitarian-communitarian, pro-science and pro-media, distrusts
   police, military, churches, and business.
2. **Institutional Civic Moderate** (17%): moderately religious; highest social and institutional trust; responds to
   expert messengers.
3. **Disaffected Distruster** (16%): low trust in people, institutions, and science; fatalist-like; suspicious of every
   messenger; partisanship mixed.
4. **Secular Market Nationalist** (17%): secular, market-individualist, nationalist, fairly science-optimistic; open to
   innovation and market framing; resists mandates.
5. **Religious Communitarian Traditionalist** (19%): religious and traditional but skeptical of markets; stewardship and
   community framing; mixed party.
6. **Religious Free-Market Conservative** (17%): hierarchical-individualist; most religious and most pro-market;
   strongest identity-protective dismissal of climate risk.

**Bridge to present-day data**: the surveys share no respondents, so present-day respondents were assigned to groups
probabilistically using a logistic model on shared variables.
- ATP 2024: 60% accuracy; trust items help most.
- VCSI 2026: 41% (weak link).
- Weakest-identified groups: Secular Market Nationalist and Religious Communitarian Traditionalist.
- Because assignment rests on shared variables only, between-group gaps are probably understated.
- ATP gradient check: "human activity contributes a great deal" falls from 81% to 12% left to right.

**Subgroups (3 per group)**: within each group, members were ranked by ideology+party and split into weighted
terciles. File suffixes:
- `_1` = middle third (intended "main")
- `_2` = more conservative third
- `_3` = more progressive third

This mapping lives ONLY in filenames and in `Segmentation/`. Do not surface it in prompts. You may show it in a
researcher view of the UI if the user wants.

## 5. The two persona formats

| | `Personas NEW` (individual) | `Personas Generic` (segment) |
|---|---|---|
| Voice | 2nd person; first-person replies as a named person | 3rd-person analyst ("Most members would...") |
| Structure | Operator preamble + S1-S10 (Persona System Part III) | A: use instructions; B: profile under 8 layer headers; C: "Behind-the-scenes context" |
| Best for | Conversational realism, quotes, focus-group feel | Predictions with typical response + within-segment range |
| Notes | 18 fictional people, diverse; some counter-stereotypical | Section C uses theory terms and says it must not affect answers. If it leaks into outputs, strip everything from the line "BEHIND-THE-SCENES CONTEXT" onward before loading |

Load each file verbatim as the **system prompt**; the user's question or message is the user turn. Both formats are
set to **October 2026, present-day U.S.**

## 6. UI / runtime design (recommended)

**Core flows**
1. **Ask a persona**: pick a group (or persona), ask a question, get the answer.
2. **Test a message**: the user enters a message and optional messenger/source. Run it against all selected personas;
   show reactions side by side.
3. **"Appellate" mode** (user's idea): per group, one persona gives the "majority opinion" and the other two give
   "concurring/dissenting opinions" saying where they'd differ. A red-team variant lets the personas challenge each
   other's reasoning.
   - Default: treat all three as equals.
   - Optionally use `_1` as the majority.

**Implementation**
- **Calls**: one LLM call per persona per turn, using that persona's file as the system prompt.
  - Message testing: 6 groups × 3 = 18 calls per message. Batch them with the provider's batch API or parallel
    requests.
  - Appellate dissents: a second call per minority persona, giving it the majority text and asking where it disagrees
    and why, in character.
- **Settings** (Persona System 5.6):
  - provider default temperature (~1.0), never 0
  - k≥3 samples per persona for anything quantitative; report the modal answer and spread
  - for closed items, constrain the output to an option label
- **Multi-turn state** (Persona System 5.4; BL §9). Don't let the model drift freely.
  - A small, cheap **judge** call codes each message:
    - values invoked
    - messenger trust/affinity
    - whether the solution frame is congenial
    - whether the message is forceful/moralizing
    - whether it implies a personal cost
  - The orchestrator applies step limits in code and injects a one-line in-character state note before the next turn.
  - Keep a per-persona state ledger (JSON) of the DYNAMIC parameters (BL Appendix A).
- **Output for message tests**: per persona, show:
  - the reaction
  - believability of the facts (↑/↓)
  - felt obligation
  - stated intention
  - likely backfire
  - which frame or messenger would work better

  Aggregate by group and highlight disagreements within groups (the appellate view).
- **Never** inject study hypotheses, construct names, or "be consistent/realistic" instructions into prompts
  (Persona System 6.2).

**Validation before release**
- Run the probe battery (Persona System 7.2, P1-P10) on each persona in fresh sessions, judged with ±1 band tolerance.
  The battery has **not been run yet**.
- Also check that the predicted group gradients match `bridge_report.txt` (e.g., belief in human causation falls left
  → right).

## 7. Caveats to show users
- Personas are **synthetic predictions**, not evidence. Validate important message decisions with real respondents or
  published experiments.
- Message-response magnitudes are design defaults, not calibrated against experiments (BL gap G14).
- Values come from 2017 data; present-day views come from probabilistic links to 2024/2026 surveys.
- VCSI is an opt-in sample.
- Inferred elements are tagged (I) in BL and in each generic file's section C.
- Ethics (Persona System Part X): label outputs as simulated; no real people; do not let personas converse with real
  members of the public without disclosure and approval.

## 8. Open items / next steps
1. Run the probe battery on all 36 prompts and fix failures; at most 2 revision cycles per prompt.
2. Build the judge/orchestrator and state ledger (§6).
3. Calibrate message effects against framing/messenger experiments if the user supplies them.
4. Optional: obtain the full VCSI codebook to use the unlabeled grids (Q_Q*, D_enviromentx*, D_media*).
5. Optional: a survey containing Schwartz values, Kahan scales, and environmental items for the same respondents. This
   would remove the weak-bridge problem.

## 9. Reproducing / extending the data work
Run in order from `Segmentation/` (plain `python`; needs pandas, numpy, scikit-learn, openpyxl):
1. `wvs_segmentation.py` → `wvs_segments.csv`, `wvs_segment_profiles.csv`, report. Seed 20261015; selected column
   `group_k6`.
2. `bridge_model.py` → `bridge_atp_probs.csv`, `bridge_vcsi_probs.csv`, report.
3. `persona_specs.py` → `persona_specs.csv/.txt`.

Persona text was written by subagents from `persona_writing_brief.txt` (individual) and `generic_writing_brief.txt`
(generic). Reuse those briefs to regenerate or add personas.

**Data quirks**
- WVS: negative missing codes; IDs and dates were lost in the CSV and are not needed.
- ATP: read with `usecols` to skip stray pasted columns; 99 = missing.
- VCSI: every other spreadsheet row is blank (use `dropna(how="all")`); use age bands, never date of birth.
