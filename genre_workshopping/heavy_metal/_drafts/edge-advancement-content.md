# Heavy Metal — Edge / Advancement / Pact Push Content Drafts

**Status:** Drafts ready for Dev consumption. Not yet wired — these YAML blocks live here until ADR-078 stories land in Dev, at which point they get lifted verbatim into the live files.

**Source ADR:** [ADR-078](../../../../docs/adr/078-edge-composure-advancement-rituals.md)
**Source plan:** `~/.claude/plans/ticklish-spinning-reef.md`
**Author:** GM (Hawkeye Pierce, MASH theme), 2026-04-15

## Story → block consumption map

| Epic-Edge story | What lands in heavy_metal | Source block in this draft |
|---|---|---|
| 3 (HP purge + edge_config) | Strip HP fields from `rules.yaml`; add `edge_config` block | §1 |
| 5 (advancement engine) | Add `mechanical_effects` to each affinity tier in `progression.yaml` | §2 — **see Margaret deviation note** |
| 6 (pact push currencies) | Add three `resources` to `rules.yaml`; extend `pact_working` beats | §3 + §4 |
| 8 (acceptance playtest) | Rewrite `confrontations[type=combat]` beats; author sample pacts | §5 + §6 |

## ✓ Architect Ruling — ADR-078 Amended

**Resolved 2026-04-15.** Margaret ruled on the location question in ADR-078 §5 and the "Architect Rulings on GM Draft" section. The deviation is now ratified:

- **Effects host on existing progression structures wherever those exist.** Heavy_metal slots `mechanical_effects:` arrays into existing affinity tiers in `progression.yaml`. Genres without an affinity scaffold use a standalone `{genre}/advancements.yaml`. The loader supports both locations from day one.
- **Story 5 includes a per-genre audit pass** to determine which genres host effects in `progression.yaml` and which need a new file. Content task, not engine task.
- **`AdvancementEffect` enum extended in v1:** `LoreRevealBonus { scope: LoreRevealScope }` is in. `BeatDiscount` gained `resource_mod: Option<HashMap<String, i32>>` so Pact-affinity tiers can discount push-currency costs.
- **`RecoveryTrigger::OnBeatSuccess` extended in v1:** `while_strained: bool` is in. Precise definition: `current <= max / 4` (matches UI Cracked state).
- **Four extended variants deferred to ADR-082+:** `AllyBeatDiscount`, `BetweenConfrontationsAction`, `AllyEdgeGrant`, `EdgeThresholdDelay`. Heavy_metal Craft and Lore tiers 2-3 carry explicit `mechanical_effects: []  # TODO ADR-082+` stubs in this draft. Tier 1 of both ships with `LoreRevealBonus`.
- **`read_the_opponent` patience beat endorsed** as story 8 content.
- **Voice/Flesh/Ledger no auto-refill endorsed** — narrative recovery only.
- **Combat `edge_delta` numbers** are first-pass; story 4 smoke playtest is the tuning gate.

See ADR-078 §"Architect Rulings on GM Draft" for the full ruling text.

---

## §1 — `edge_config` block (story 3, lands in `rules.yaml`)

Replaces the deleted `hp_formula`, `class_hp_bases`, `default_hp`, `default_ac`, and the `stat_display_fields: [hp, max_hp, ac]` block. Heavy_metal-flavored: classes that get hit a lot start with more Edge because they've been *practicing being hit*, not because they're meatier.

```yaml
# ── Edge / Composure ──────────────────────────────────────────
# Replaces HP. Edge is the deflection currency — your footing,
# your nerve, your read on the room. When it's gone, the next
# thing that happens is the thing that was always going to happen.
edge_config:
  # Per-class base Edge capacity. Heavy_metal classes sort by
  # *how much pressure their training accustomed them to*, not
  # by hit-die size. The Fighter has carried a shield through
  # a winter siege; the Wizard has read in a room where the
  # candles kept blowing out; both took *damage*, just different
  # damage.
  base_max_by_class:
    Fighter:   6   # the doomed-prince baseline
    Barbarian: 7   # nothing to lose, everything to spend
    Paladin:   6   # oath as armour
    Ranger:    5   # the long quiet of the road
    Monk:      6   # one breath, then the next
    Cleric:    5   # the litany as anchor
    Druid:     5   # something else holds you up
    Bard:      5   # composure is the trade
    Rogue:     5   # the half-second nobody else has
    Warlock:   4   # the thing that watches you is not steady
    Wizard:    4   # the room is too loud for the work
    Sorcerer:  4   # the gift is also the wound

  # Default recovery. Heavy_metal is gritty: Edge refills between
  # confrontations, but only if the practitioner *had a moment*.
  # If the next confrontation begins before the breath is taken,
  # the player carries whatever they have.
  recovery_defaults:
    on_resolution: full       # full refill at confrontation close
    on_long_rest: full        # always full at long rest
    between_back_to_back: 0   # zero refill if no breath was taken

  # The composure-break threshold. When Edge hits zero, this
  # narrator_hint goes into the LoreStore as a high-priority
  # KnownFact. The narrator is *required* to honour it on the
  # next exchange — the prose at zero-Edge is not freelance.
  thresholds:
    - at: 1
      event_id: edge_strained
      narrator_hint: |
        The character is one exchange from breaking. Their breath
        is wrong; their stance has shortened by half a foot. The
        opponent has noticed. Describe the loss of bearing — the
        glance toward the exit, the grip that re-seats itself one
        beat too late.
      direction: crossing_down
    - at: 0
      event_id: composure_break
      narrator_hint: |
        The ledger turns. Whatever was being deflected now lands.
        The narrator must carry the genuine consequence on the
        next exchange — a wound that does not close, a yield that
        is heard, a name spoken that cannot be unspoken, a death
        that the room makes room for. This is not the time for
        deflection prose. The price is paid in this beat.
      direction: crossing_down

  # Display fields for the character sheet. The UI reads this
  # list declaratively — composure_state is derived by the
  # frontend from current/max ratio (Fresh / Strained / Cracked /
  # Broken).
  display_fields:
    - edge
    - max_edge
    - composure_state
```

**HP fields to delete from `rules.yaml` when this lands:**

```yaml
# DELETE these lines from heavy_metal/rules.yaml:
hp_formula: "class_base * level"             # phantom — never wired
default_hp: 10                                # phantom
default_ac: 10                                # phantom
class_hp_bases:                               # phantom — entire block
  Fighter: 10
  …
stat_display_fields:                          # replaced by edge_config.display_fields
  - hp
  - max_hp
  - ac
```

---

## §2 — Affinity `mechanical_effects` (story 5, lands in `progression.yaml`)

**Adds `mechanical_effects:` arrays to each existing affinity tier.** Does not replace any existing fields. The `tier_thresholds: [6, 14, 28]` line stays — what's new is *what each tier buys mechanically* in addition to the existing narrative reward.

Each affinity gets three tiers' worth of mechanical effects, themed to its existing flavor. Iron and Pact carry combat/ritual weight. Court covers social-confrontation Edge. Ruin owns recovery. Craft and Lore stay non-combat but get their own mechanical reveals so they don't feel like dead branches for combat-leaning characters.

```yaml
# ── Iron — martial bearing ────────────────────────────────────
- name: "Iron"
  description: "Martial bearing — the sword-work of doomed princes…"
  triggers: [...]   # unchanged
  tier_thresholds: [6, 14, 28]
  mechanical_effects:
    - tier: 1
      label: "Standing Wound"
      narration_hint: "The character has learned to fight with a body that already hurts. They start each confrontation with one more breath than they should."
      effects:
        - { type: edge_max_bonus, amount: 1 }
    - tier: 2
      label: "Holding the Line"
      narration_hint: "Defensive postures cost the character less. The brace that used to drain them now restores them."
      effects:
        - { type: beat_discount, beat_id: brace, edge_delta_mod: -1 }
        - { type: edge_max_bonus, amount: 1 }
    - tier: 3
      label: "The Sword-Work of Doomed Princes"
      narration_hint: "When the character commits, the opponent's footing breaks faster than it should. There is something in the swing the opponent has seen before in old stories."
      effects:
        - { type: leverage_bonus, beat_id: committed_blow, target_edge_delta_mod: -1 }
        - { type: edge_max_bonus, amount: 2 }

# ── Pact — bargained magic ───────────────────────────────────
- name: "Pact"
  description: "Bargained magic — the practitioner's hand in the working…"
  triggers: [...]
  tier_thresholds: [5, 12, 25]
  mechanical_effects:
    - tier: 1
      label: "First Reading"
      narration_hint: "The practitioner has spoken the terms aloud often enough that the words do not cost what they used to."
      effects:
        - { type: beat_discount, beat_id: invoke, resource_mod: { voice: 1 } }
    - tier: 2
      label: "Hand on the Ledger"
      narration_hint: "The practitioner has paid in body and in book often enough that the second cost has become familiar. The flesh holds steadier; the ledger entries write themselves shorter."
      effects:
        - { type: beat_discount, beat_id: commit_cost, resource_mod: { flesh: 1 } }
        - { type: edge_max_bonus, amount: 1 }
    - tier: 3
      label: "The Working Knows You"
      narration_hint: "The practitioner has run the rite enough that the rite *anticipates* — power answers a half-beat early, and the closing comes at less cost than the practitioner remembers it costing the first time."
      effects:
        - { type: edge_recovery, trigger: { type: on_beat_success, beat_id: close_the_book }, amount: 2 }
        - { type: beat_discount, beat_id: force_completion, resource_mod: { ledger: 1 } }

# ── Court — political maneuvering ────────────────────────────
- name: "Court"
  description: "Political maneuvering in collapsing halls…"
  triggers: [...]
  tier_thresholds: [5, 12, 25]
  mechanical_effects:
    - tier: 1
      label: "Reading the Room"
      narration_hint: "The character notices the small things — who is angled toward whom, whose hand is on whose shoulder, who has not spoken. The room costs them less to be in."
      effects:
        - { type: edge_max_bonus, amount: 1 }   # composure carries to debt_collection too
        - { type: beat_discount, beat_id: acknowledge, edge_delta_mod: -1 }
    - tier: 2
      label: "The Right Knife"
      narration_hint: "The character can tell which precedent the collector is building toward and reach for it first. Reassignments land more often; refusals cost less."
      effects:
        - { type: leverage_bonus, beat_id: reassign, target_edge_delta_mod: -1 }
    - tier: 3
      label: "Heard at the High Table"
      narration_hint: "The character has the kind of standing where a refusal in the hall is *remembered*. The collector flinches before the player has finished speaking."
      effects:
        - { type: leverage_bonus, beat_id: refuse, target_edge_delta_mod: -2 }
        - { type: edge_max_bonus, amount: 1 }

# ── Ruin — the expertise of having already lost ──────────────
- name: "Ruin"
  description: "The particular expertise of having already lost…"
  triggers: [...]
  tier_thresholds: [7, 16, 30]
  mechanical_effects:
    - tier: 1
      label: "Walking Out"
      narration_hint: "The character has walked out of one catastrophe already. The next one does not surprise them."
      effects:
        - { type: edge_recovery, trigger: { type: on_resolution }, amount: 0 }   # baseline
        - { type: edge_max_bonus, amount: 1 }
    - tier: 2
      label: "Strength from Grief"
      narration_hint: "When the character is at the edge of breaking, something in them refuses. They find a breath nobody else would have found."
      effects:
        # The killer effect: when Edge drops to 1, the next successful
        # beat refunds 2 Edge. Lets the player stand once after they
        # should have fallen.
        - { type: edge_recovery, trigger: { type: on_beat_success, while_strained: true }, amount: 2 }
    - tier: 3
      label: "The Decay Heard First"
      narration_hint: "The character can hear the end of a fight before it arrives. They start each confrontation already braced for the consequence."
      effects:
        - { type: edge_max_bonus, amount: 2 }
        - { type: edge_recovery, trigger: { type: on_resolution }, amount: 0 }   # full default

# ── Craft — guild-laborer's art (non-combat hooks) ───────────
- name: "Craft"
  description: "The guild-laborer's art…"
  triggers: [...]
  tier_thresholds: [5, 12, 25]
  mechanical_effects:
    - tier: 1
      label: "Hand-Memory"
      narration_hint: "The character can identify the maker of a thing by its flaws — and through that recognition, can sometimes predict what the thing will do under stress."
      effects:
        - { type: lore_reveal_bonus, scope: object_provenance }   # NON-EDGE: Craft narrator-side hook
    - tier: 2
      label: "Working the Material"
      narration_hint: "The character can repair under fire — a snapped strap, a fouled lock, a guttering torch. Quick fixes between exchanges, not in them."
      effects: []   # TODO ADR-082+ — needs BetweenConfrontationsAction variant (new game-state slot)
    - tier: 3
      label: "The Apprentice's Hand"
      narration_hint: "The character has trained others. In a confrontation where they are giving instruction — to an ally, a child, a panicked soldier — the ally's beats cost less."
      effects: []   # TODO ADR-082+ — needs AllyBeatDiscount variant (party-aware resolved_beat_for)

# ── Lore — forbidden and half-forbidden knowledge (non-combat) ─
- name: "Lore"
  description: "Forbidden and half-forbidden knowledge…"
  triggers: [...]
  tier_thresholds: [6, 14, 28]
  mechanical_effects:
    - tier: 1
      label: "The Quiet Recognition"
      narration_hint: "When something supernatural enters the scene, the character knows what it is before anyone else. The narrator must reveal one true fact about it on first sight."
      effects:
        - { type: lore_reveal_bonus, scope: supernatural_entity }
    - tier: 2
      label: "The Half-Forbidden Page"
      narration_hint: "The character can name the rite, the genealogy, or the heresy at the critical moment. When this happens, all allies in the scene get one Edge."
      effects: []   # TODO ADR-082+ — needs AllyEdgeGrant variant (scene-scope ally lookup)
    - tier: 3
      label: "The Sign Read in Time"
      narration_hint: "The character can identify a daemon, spirit, or working *before* it acts. Composure breaks that involve supernatural opponents do not happen on the same exchange — the character gets one extra breath."
      effects: []   # TODO ADR-082+ — needs EdgeThresholdDelay variant (conditional threshold firing)
```

**Status of extended `AdvancementEffect` variants (Margaret ruled 2026-04-15):**
- ✓ **`lore_reveal_bonus`** — IN day-1 enum. Craft tier 1 and Lore tier 1 ship with this in v1. Single field, no plumbing change.
- ⏳ **`ally_beat_discount`, `between_confrontations_action`, `ally_edge_grant`, `edge_threshold_delay`** — DEFERRED to ADR-082+. Each requires substantial new context plumbing (party-aware `resolved_beat_for`, new game-state slots, scene-scope queries, conditional threshold firing). Craft tier 2-3 and Lore tier 2-3 ship in v1 with `effects: []  # TODO ADR-082+` stubs — labels and narration_hints preserved as authored content, ready to wire when ADR-082+ lands. ADR-082+ is filed after story 8's playtest acceptance gate clears.

---

## §3 — Three new push-currency `resources` (story 6, lands in `rules.yaml`)

```yaml
# ── Push currencies for pact_working ──────────────────────────
# Three voluntary resource pools that the practitioner spends
# to push pact-working beats. They do not refill on rest —
# they refill only through the slow, narrative-driven recovery
# that heavy_metal demands (see triggers below). A practitioner
# who has spent all three has been *changed* by the working.
resources:
  - name: voice
    label: "Voice"
    min: 0
    max: 10
    starting: 10
    voluntary: true
    decay_per_turn: 0
    thresholds:
      - at: 3
        event_id: voice_thinning
        narrator_hint: "The practitioner's voice has begun to thin. Not from disuse — from the weight of true names spoken into the working."
        direction: crossing_down
      - at: 1
        event_id: voice_almost_spent
        narrator_hint: "The practitioner has one true name left to spend. Anything beyond it will have to be paid in another currency."
        direction: crossing_down
      - at: 0
        event_id: voice_spent
        narrator_hint: "The practitioner cannot speak the terms aloud anymore. Future invocations must be written, signed in ink that costs flesh, or carried by a proxy who does not yet know what they are agreeing to."
        direction: crossing_down

  - name: flesh
    label: "Flesh"
    min: 0
    max: 10
    starting: 10
    voluntary: true
    decay_per_turn: 0
    thresholds:
      - at: 5
        event_id: flesh_marked
        narrator_hint: "The practitioner is *visibly* marked now — a streak of white in the hair, a hand that no longer warms, a tremor at the wrist. The court has noticed."
        direction: crossing_down
      - at: 2
        event_id: flesh_failing
        narrator_hint: "The practitioner's body is keeping score in a way the practitioner cannot any longer ignore. Stairs are difficult. Cold is difficult. The mirror is difficult."
        direction: crossing_down
      - at: 0
        event_id: flesh_spent
        narrator_hint: "The practitioner has paid all the body has to pay. The next working must be carried by someone else's flesh, or by the ledger alone, or not at all."
        direction: crossing_down

  - name: ledger
    label: "Ledger"
    min: 0
    max: 10
    starting: 10
    voluntary: true
    decay_per_turn: 0
    thresholds:
      - at: 6
        event_id: ledger_seen
        narrator_hint: "The practitioner's name has begun to appear in places it was not written. A clerk in a chancery the practitioner has never visited has the practitioner's full birth-name copied in a margin."
        direction: crossing_down
      - at: 3
        event_id: ledger_pursued
        narrator_hint: "Collectors are asking after the practitioner now — politely, with appointments. A house-of-the-ledger has filed a formal interest."
        direction: crossing_down
      - at: 0
        event_id: ledger_due
        narrator_hint: "The practitioner's account has come up for collection. Until the debt is settled, every door the practitioner walks through is being watched. This is not the working talking. This is the bureaucracy of the working talking."
        direction: crossing_down
```

---

## §4 — Extended `pact_working` beats (story 6, replaces existing block in `rules.yaml`)

Each existing beat gains a `resource_deltas` field. Narrator hints are *unchanged* — they already say exactly what is being spent. We're making the cost typed.

```yaml
- type: pact_working
  label: "Working the Rite"
  category: ritual                   # CHANGED from "social" — enables ritual prompt section
  metric:
    name: rite_progress
    direction: ascending
    starting: 0
    threshold_high: 10
    threshold_low: 0
  beats:
    - id: invoke
      label: "Invoke the Terms"
      metric_delta: 2
      stat_check: INT
      resource_deltas: { voice: -1 }
      effect: "The rite advances one step; the working's terms are laid down"
      narrator_hint: "The practitioner names the debt, the creditor, and the price. The ritual formally opens. The air, if one is paying attention, becomes measurable."
    - id: commit_cost
      label: "Commit the Cost"
      metric_delta: 3
      stat_check: CON
      resource_deltas: { flesh: -2 }
      risk: "The cost can be mis-paid — if the check fails, the rite advances but the debt is assigned to a wrong account; consequences may ripple for days or weeks"
      effect: "The working draws forward; the caster feels the withdrawal"
      narrator_hint: "Describe the commitment in concrete terms — an hour of life, a memory, a name, a year. Whatever is spent, it leaves."
    - id: steady_the_rite
      label: "Steady the Rite"
      metric_delta: 1
      stat_check: WIS
      resource_deltas: { voice: -1 }
      effect: "The rite stabilises; interference is held at bay"
      narrator_hint: "The practitioner holds the working's shape against whatever is pressing back against it. This is the work of mastery, done quietly."
    - id: force_completion
      label: "Force Completion"
      metric_delta: 4
      stat_check: CHA
      resource_deltas: { ledger: -3, flesh: -1 }
      risk: "If the check fails, the rite collapses — the debt is still owed, and is now owed with a penalty that is never small"
      effect: "The rite lurches to its end"
      narrator_hint: "The practitioner stops pretending the rite is easy. Force is applied. Whatever happens next will be legible to anyone nearby with the sensitivity to feel it."
    - id: close_the_book
      label: "Close the Book"
      metric_delta: 0
      stat_check: WIS
      resource_deltas: { ledger: -1 }
      resolution: true
      consequence: "The rite is complete — or is formally broken off with a lesser consequence than forcing it would carry"
      narrator_hint: "The practitioner closes the working deliberately — successful or not. The room feels it. The ledger either balances, or does not, and everyone in the room knows which."
  mood: ritual
```

**Note:** The `category` field changes from `social` to `ritual`. This is the trigger for the new conditional prompt section in the unified narrator (ADR-067 pattern). All *other* heavy_metal confrontations (combat, chase, debt_collection, negotiation) keep their existing categories.

---

## §5 — Rewritten combat ConfrontationDef (story 8, replaces existing block in `rules.yaml`)

The `momentum` metric stays as the encounter clock for narration's sake (it tells the narrator who's pressing whom in the scene), but Edge debits on `CreatureCore` are what *actually decide* the fight. Beats now carry `edge_delta` (cost to the actor) and `target_edge_delta` (pressure stripped from the opponent).

```yaml
- type: combat
  label: Blade-work
  category: combat
  # Momentum stays as the narrative clock — describes who is
  # pressing whom in the scene. Edge on CreatureCore is the
  # mechanical truth. Both update; the narrator reads momentum,
  # the engine resolves on Edge.
  metric:
    name: momentum
    direction: bidirectional
    starting: 0
    threshold_high: 10
    threshold_low: -10
  beats:
    - id: strike
      label: Strike
      metric_delta: 2
      stat_check: STR
      edge_delta: 0           # the actor doesn't lose composure on a clean swing
      target_edge_delta: 2    # the opponent gives ground
      narrator_hint: "Describe the blow with specificity — which grip, which angle, what gave way. Heavy Metal combat is not choreography; it is plumbing."
    - id: brace
      label: Brace
      metric_delta: 1
      stat_check: CON
      edge_delta: -1          # bracing RECOVERS one Edge — recentering, finding the breath
      target_edge_delta: 0
      narrator_hint: "The character sets their weight, takes the impact, pays for it later. The breath returns."
    - id: committed_blow
      label: "Committed Blow"
      metric_delta: 4
      stat_check: STR
      edge_delta: 3           # all-in costs composure
      target_edge_delta: 4    # but it costs the opponent more
      risk: "Overcommits — lose 3 momentum and take a counter on failure. On a fail, the character also loses an additional 2 Edge."
      narrator_hint: "An all-in swing; the character is not planning a follow-up. Describe the violence as expensive — to the one making it, as well as the one receiving it."
    - id: read_the_opponent
      label: "Read the Opponent"
      metric_delta: 1
      stat_check: WIS
      edge_delta: -2          # patience refills composure substantially
      target_edge_delta: 0
      effect: "Next strike beat from this character costs 1 less Edge."
      narrator_hint: "The character pauses, watches, declines to commit. The opponent is forced to choose first. Heavy Metal rewards the patience that costs nothing visible."
    - id: break_contact
      label: "Break Contact"
      metric_delta: 0
      stat_check: DEX
      edge_delta: 0
      target_edge_delta: 0
      resolution: true
      consequence: "Combat ends — the character withdraws, or the enemy lets them go"
      narrator_hint: "Disengagement is a mercy in Heavy Metal. Describe it as such."
  mood: combat
```

**New beat: `read_the_opponent`.** Adding this beat — not in the original combat ConfrontationDef — gives the player a way to *recover Edge mid-fight* through patience. Without it, every combat beat costs Edge or is neutral, and the only way to refill is to win or break contact. That makes long fights a war of attrition the player can't escape, which is wrong for the deflection-until-break feel. Patience as a beat is the genre-true counter to attrition. **Flag for Margaret:** is this an in-scope content addition or does it need its own ADR note?

---

## §6 — Three sample pacts for story 8 playtest

Each pact is a fully-formed scenario fragment Keith can drop into a heavy_metal session as a pre-authored fixture. They exist to test (a) push-currency debit flow, (b) `composure_break` firing on the practitioner when Edge is also spent during a high-stakes ritual, (c) the narrator's adherence to threshold KnownFacts on `voice_almost_spent` / `flesh_failing` / `ledger_pursued`.

### Pact A — *The Frost-Letter*

**Setup.** A young noblewoman has been cursed by a dying rival to die on her wedding day. The practitioner is hired to break the curse. They have one night.

**Working description.** The curse is a written debt — the dying rival entered the noblewoman's name in a frost-ledger before death. Breaking it requires *removing the entry*, which can only be done by another entry that costs the practitioner more than the original entry cost the rival.

**Push pattern to test.**
- `invoke` ×1 (Voice -1)
- `commit_cost` ×2 (Flesh -4) — the practitioner gives up two fingers' worth of grip strength, permanent
- `force_completion` ×1 (Ledger -3, Flesh -1) — the practitioner's name now appears in the same frost-ledger
- `close_the_book` ×1 (Ledger -1)

**Total spend.** Voice -1, Flesh -5, Ledger -4. The practitioner walks out of the working *changed*. Threshold expectation: `flesh_marked` (at=5) fires, narrator must honour it on next scene.

**Acceptance test.** GM panel must show all three resource pool decrements. `creature.edge_delta` must show practitioner Edge cost from the difficulty checks (not from the resource_deltas — those are *extra*). Narrator must mention the practitioner's hand on the next exchange after the working closes.

### Pact B — *The Borrowed Year*

**Setup.** The practitioner needs to know what their dead mentor knew about a particular daemon. The mentor is in no fit state to tell them. The mentor's apprentice — the practitioner — must borrow a year of the mentor's *post-mortem time* and read it.

**Working description.** A pact_working against the boundary of the dead. The metric advances quickly because the mentor is not resisting; the cost is high because what is being borrowed is *time the mentor cannot have back*.

**Push pattern.**
- `invoke` ×1 (Voice -1) — naming the mentor's full name, including the name the mentor was given as a child
- `commit_cost` ×1 (Flesh -2) — the practitioner ages a year visibly during the working
- `steady_the_rite` ×3 (Voice -3) — the boundary is *thin* and keeps trying to close
- `close_the_book` ×1 (Ledger -1)

**Total spend.** Voice -4, Flesh -2, Ledger -1. Modest in body, expensive in voice. Threshold expectation: `voice_thinning` (at=3) fires.

**Acceptance test.** Voice ResourcePool must drop to 6 (from 10). `voice_thinning` LoreFragment must mint at the crossing. Narrator must reference the practitioner's voice in the next dialogue scene — hoarseness, a half-cough, a sentence trailed off.

### Pact C — *The Ledger Refused*

**Setup.** A collector has come for the practitioner's grandfather's debt — a debt the practitioner cannot in conscience pay because paying it would condemn their grandfather's surviving servants to indenture. The practitioner must *refuse* the pact while standing inside it.

**Working description.** This is an inverted pact_working. The practitioner is not creating a working — they are *refusing to ratify one that already exists*. The push cost is in *Ledger* primarily, because what is being spent is the practitioner's standing-in-account.

**Push pattern.**
- `invoke` ×1 (Voice -1) — naming the grandfather aloud, in the collector's hearing
- `force_completion` ×2 (Ledger -6, Flesh -2) — the practitioner enters their *own* name in the ledger as the new debtor, then strikes through the entire account
- `close_the_book` ×1 (Ledger -1)

**Total spend.** Voice -1, Flesh -2, Ledger -7. The practitioner has just made themselves a *prominent* mark for every debt-collector in the region. Threshold expectation: `ledger_seen` (at=6) AND `ledger_pursued` (at=3) both fire, in that order.

**Acceptance test.** Two threshold KnownFacts must mint in sequence. The next two scenes after this working *must* feature collectors asking after the practitioner — that's the narrator obeying the threshold facts. If they don't, the LoreStore→prompt injection is broken.

---

## §7 — Resolved questions (Margaret rulings, 2026-04-15)

All six questions are now resolved. Listed in original order with the ruling inline:

1. ✓ **`mechanical_effects` location for non-heavy_metal genres.** **Ruled: ADR-078 §5 amended.** Effects host on existing progression structures wherever those exist; standalone `advancements.yaml` is the fallback for genres with no scaffold. Story 5 includes a per-genre audit pass. Heavy_metal uses its existing `progression.yaml` affinity tiers as authored in §2 above.
2. ✓ **Extended `AdvancementEffect` variants.** **Ruled: split decision.** `LoreRevealBonus` is IN the day-1 enum (Craft tier 1, Lore tier 1 use it). The other four (`AllyBeatDiscount`, `BetweenConfrontationsAction`, `AllyEdgeGrant`, `EdgeThresholdDelay`) are deferred to ADR-082+ — each requires substantial new plumbing. Craft tier 2-3 and Lore tier 2-3 ship in v1 with documented `effects: []  # TODO ADR-082+` stubs (see §2 above — labels and narration_hints preserved as authored content). ADR-082+ is filed after story 8's playtest acceptance gate clears.
3. ✓ **`while_strained` recovery trigger condition.** **Ruled: added to `RecoveryTrigger::OnBeatSuccess` in v1.** Precise definition: `current <= max / 4`, matching the UI Cracked composure_state. Honors Ruin tier 2's thematic core ("stand once after you should have fallen").
4. ✓ **`read_the_opponent` patience beat in combat ConfrontationDef.** **Ruled: endorsed as story 8 content.** The criterion is "every combat ConfrontationDef must include at least one beat with `edge_delta < 0`" — `read_the_opponent` satisfies it for heavy_metal. Other genres can author their own equivalent. Not a precedent for content scope creep.
5. ✓ **Resource recovery cadence for Voice/Flesh/Ledger.** **Ruled: endorsed as drafted.** No auto-refill. Narrative recovery only — silent meditation, bed-rest, debt forgiveness. Engine-side this is `decay_per_turn: 0` and no `recovery_per_rest` auto-trigger; the existing `ResourcePool` schema supports this with no code change. Genre-truth call.
6. ✓ **Combat ConfrontationDef edge_delta tuning.** **Ruled: not architectural.** Story 4's smoke playtest is the tuning gate. First-pass numbers in §5 above; adjust based on playtest feel.

Bonus addition Margaret made unprompted that affects this draft:

7. ✓ **`BeatDiscount.resource_mod: Option<HashMap<String, i32>>` added to the day-1 enum.** Required for Pact tier 1 / tier 2 / tier 3 effects in §2 above (which discount push-currency costs on `pact_working` beats). Without this field, those effects wouldn't load. Margaret caught it during the architect rulings pass.

See ADR-078 §"Architect Rulings on GM Draft" for the full ruling text. Stories 3, 5, 6, and 8 are unblocked from a content-spec perspective.

---

## Status

**Fully aligned with ADR-078 as of 2026-04-15.** All blocks are draft-ready, self-consistent, and architecturally ratified. Stories 3, 5, 6, and 8 can lift their relevant sections directly when Dev (Winchester) reaches them.

**Next GM action when stories begin landing:**
- During story 4's smoke playtest gate: return to §5 to tune `edge_delta` numbers based on what felt right or wrong.
- After story 8 acceptance: file the parallel content drafts for the other 9 genres (one ADR follow-up per genre — lower priority than heavy_metal acceptance, will need a per-genre audit to determine effects-host location per the ADR-078 §5 amendment).
- After ADR-082+ lands: revisit the four deferred Craft/Lore tier-2/tier-3 stubs and wire them with the new variants.

— Hawkeye Pierce, Heavy Metal field hospital, 2026-04-15
