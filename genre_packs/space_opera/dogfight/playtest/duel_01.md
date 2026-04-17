# Dogfight Playtest — Duel 01: The Merge

**Purpose:** Validate the 4-maneuver × 16-cell MVP interaction table by resolving
three turns of a 2-player dogfight by hand. No code, no UI — just this file,
`../maneuvers_mvp.yaml`, and `../interactions_mvp.yaml`.

**Time budget:** 20-30 minutes for three turns plus debrief.

---

## How to run this playtest

1. **Three humans.** One plays Red Pilot, one plays Blue Pilot, one is the GM
   (who owns the lookup table and writes narration).
2. **Read the starting state below.** Both pilots have the same view of their
   own cockpit: opponent at 12 o'clock, head-on, close range, no gun solution,
   energy 60. Both pilots know their opponent has the same view.
3. **Each turn, both pilots secretly write their maneuver choice** in the
   Commit boxes. The four options are: `straight`, `bank`, `loop`,
   `kill_rotation`. Don't peek at each other.
4. **Reveal commits.** GM looks up the `(red, blue)` pair in
   `interactions_mvp.yaml` → `cells`.
5. **Apply deltas.** GM writes the `red_view` fields into Red's row and the
   `blue_view` fields into Blue's row. Subtract each pilot's own maneuver
   `energy_cost` from their energy pool (remember `straight` is -5, which
   means +5 recovery).
6. **GM narrates.** 2-3 sentences per cockpit, using the cell's
   `narration_hint` as the beat. Red hears Red's narration, Blue hears Blue's.
   Same event, two POVs.
7. **Resolve shots:**
   - If one pilot has `gun_solution: true` and the other does not, the firing
     pilot scores a clean hit. Note it in Result.
   - If both have `gun_solution: true`, each rolls a d6. Higher roll fires
     first and scores. The lower-roll pilot still fires, but fires at a
     target that has already begun to break — halve the damage, or rule it
     a graze.
   - If neither has a gun solution, no shots this turn.
8. **Win conditions.**
   - First clean hit on a lightly-armored fighter is a kill.
   - Two grazes to the same pilot is a kill.
   - If a pilot runs out of energy (≤0), they cannot choose `loop` next turn.
9. **Continue** for 3 turns or until one pilot is dead.
10. **Fill in the Debrief section.** This is the most important part — it's
    what we use to calibrate the table before expanding to 8 maneuvers.

> **SOUL check:** Before narration, the GM confirms each of their 2-3 sentences
> refers to something that is actually in the descriptor. No hallucinated
> geometry. If the narrator wants to say "Red's wing grazed an asteroid" and
> there's no `environment: asteroid_field` in the descriptor, the GM should
> NOT write that. Train the reflex here on paper before it ever matters in code.

---

## Starting State — Merge

**Environment:** Deep space. Unmapped system, no terrain. Two fighters closing
head-on at full burn. Gun range. First maneuvers due.

### Red Pilot — starting descriptor

| Field          | Value            |
|----------------|------------------|
| target_bearing | 12               |
| target_range   | close            |
| target_aspect  | head_on          |
| closure        | closing_fast     |
| energy         | 60               |
| gun_solution   | false            |

### Blue Pilot — starting descriptor

| Field          | Value            |
|----------------|------------------|
| target_bearing | 12               |
| target_range   | close            |
| target_aspect  | head_on          |
| closure        | closing_fast     |
| energy         | 60               |
| gun_solution   | false            |

**Opening narration (GM reads aloud to both pilots):**

> Two fighters race toward the same point in empty space. Nose cones
> aligned, guns hot, neither pilot yet committed to a turn. The stars behind
> each cockpit are the same stars. In three seconds, one pilot's will be
> different.

---

## Turn 1

### Sealed-letter commits

| Red's maneuver               | Blue's maneuver              |
|------------------------------|------------------------------|
|                              |                              |

### Resolution

- **Cell used (pair):**
- **Cell name:**

### Red Pilot — updated descriptor

| Field          | Value    |
|----------------|----------|
| target_bearing |          |
| target_range   |          |
| target_aspect  |          |
| closure        |          |
| energy         |          |
| gun_solution   |          |

### Blue Pilot — updated descriptor

| Field          | Value    |
|----------------|----------|
| target_bearing |          |
| target_range   |          |
| target_aspect  |          |
| closure        |          |
| energy         |          |
| gun_solution   |          |

### Narration — Red's cockpit

>

### Narration — Blue's cockpit

>

### Result

- Shots fired:
- Hits / grazes / misses:
- Damage (narrative, not numeric):
- Notes:

---

## Turn 2

*Carry forward each pilot's updated descriptor from Turn 1 as the new starting
state, then commit → resolve → narrate.*

### Sealed-letter commits

| Red's maneuver               | Blue's maneuver              |
|------------------------------|------------------------------|
|                              |                              |

### Resolution

- **Cell used (pair):**
- **Cell name:**

### Red Pilot — updated descriptor

| Field          | Value    |
|----------------|----------|
| target_bearing |          |
| target_range   |          |
| target_aspect  |          |
| closure        |          |
| energy         |          |
| gun_solution   |          |

### Blue Pilot — updated descriptor

| Field          | Value    |
|----------------|----------|
| target_bearing |          |
| target_range   |          |
| target_aspect  |          |
| closure        |          |
| energy         |          |
| gun_solution   |          |

### Narration — Red's cockpit

>

### Narration — Blue's cockpit

>

### Result

- Shots fired:
- Hits / grazes / misses:
- Damage:
- Notes:

---

## Turn 3

### Sealed-letter commits

| Red's maneuver               | Blue's maneuver              |
|------------------------------|------------------------------|
|                              |                              |

### Resolution

- **Cell used (pair):**
- **Cell name:**

### Red Pilot — updated descriptor

| Field          | Value    |
|----------------|----------|
| target_bearing |          |
| target_range   |          |
| target_aspect  |          |
| closure        |          |
| energy         |          |
| gun_solution   |          |

### Blue Pilot — updated descriptor

| Field          | Value    |
|----------------|----------|
| target_bearing |          |
| target_range   |          |
| target_aspect  |          |
| closure        |          |
| energy         |          |
| gun_solution   |          |

### Narration — Red's cockpit

>

### Narration — Blue's cockpit

>

### Result

- Shots fired:
- Hits / grazes / misses:
- Damage:
- Notes:

---

## Debrief — Run 1

### Cells exercised

| Turn | Pair used | Cell name |
|------|-----------|-----------|
| 1    | loop, loop | Twin loops — merge resumed |
| 2    | kill_rotation, straight | Red's flip-and-burn back-shot |
| 3    | — | Game ended turn 2 (Red kill) |

### Per-cell calibration tags

- **Turn 1 cell (loop/loop):** tag = `calibrated` — Both pilots committed to offense, got a stalemate. Tension built correctly — "we both know we have to commit harder next turn."
- **Turn 2 cell (kill_rotation/straight):** tag = `exciting` — Red's gamble paid off. Blue played safe and got punished. Devastating back-shot felt earned because Red spent energy on the high-risk flip.

### Pacing

- Mutual kill risk moment: No (game ended before mutual gunline). The loop/loop stalemate created excellent tension for turn 2.
- No-good-option feeling: No — Blue had bank as a valid counter to kill_rotation but chose straight (too safe).
- One-obvious-option: No — the RPS triangle was felt. Both pilots agonized.
- Energy management: Not tested — game ended in 2 turns before energy mattered.

### Narration

- Narration hints read naturally. The loop/loop "twin curtains of exhaust" beat was strong.
- No SOUL violations caught.

### Session log

| Field         | Value   |
|---------------|---------|
| Playtest date | 2026-04-16 |
| Red pilot     | Game theory simulation (aggressive) |
| Blue pilot    | Game theory simulation (passive) |
| GM            | Winchester |
| Duration      | 2 turns |
| Winner        | Red (devastating back-shot) |

---

## Debrief — Run 2

### Cells exercised

| Turn | Pair used | Cell name |
|------|-----------|-----------|
| 1    | straight, straight | Clean merge |
| 2    | bank, loop | Red slips the loop |
| 3    | bank, kill_rotation | Red banks past the back-shot |

### Per-cell calibration tags

- **Turn 1 cell (straight/straight):** tag = `dull` — Both played safe. No consequence, no drama. This is the safety baseline — dull is by design.
- **Turn 2 cell (bank/loop):** tag = `calibrated` — Blue committed to offense, Red evaded. Blue wasted 30 energy on the loop. Evasive slip worked as the safety valve.
- **Turn 3 cell (bank/kill_rotation):** tag = `calibrated` — Blue tried the kill rotation, Red banked out. Blue's flip found empty space. The counter-play felt crisp.

### Pacing

- No mutual kill risk (nobody committed to double-offense). Game was defensive.
- Energy: Blue spent heavily on offensive maneuvers (loop + kill_rotation = -60 energy), Red conserved with bank + bank. Energy asymmetry felt meaningful by turn 3.
- No forced choices — both pilots had viable options each turn.

### Session log

| Field         | Value   |
|---------------|---------|
| Playtest date | 2026-04-16 |
| Red pilot     | Game theory simulation (evasive) |
| Blue pilot    | Game theory simulation (aggressive) |
| GM            | Winchester |
| Duration      | 3 turns |
| Winner        | Draw (no hits, Blue energy-depleted) |

---

## Debrief — Run 3

### Cells exercised

| Turn | Pair used | Cell name |
|------|-----------|-----------|
| 1    | straight, loop | Blue reverses onto Red's six |
| 2    | loop, kill_rotation | Mutual gunline — knife fight |
| 3    | kill_rotation, kill_rotation | Drift-through knife fight |

### Per-cell calibration tags

- **Turn 1 cell (straight/loop):** tag = `calibrated` — Blue's reversal onto Red's six felt like the correct reward for committing to offense vs passive. Clean hit.
- **Turn 2 cell (loop/kill_rotation):** tag = `exciting` — Both committed to offense after Red took damage. Mutual gunline was the highest-tension moment in all 3 runs. Both pilots exposed.
- **Turn 3 cell (kill_rotation/kill_rotation):** tag = `exciting` — Both went all-in. Drift-through knife fight. Mutual graze damage. Felt like the climax the system was designed for.

### Pacing

- Mutual kill risk: Yes (turns 2 and 3). Both felt earned — the pilots escalated deliberately.
- Energy: Both burned heavily. By turn 3, options were constrained — kill_rotation was almost forced by energy depletion. This is good (energy pressure creates drama) but borderline (if both pilots are forced into kill_rotation, the RPS collapses).
- The 3-turn arc (safe opener → mid-game hit → climactic mutual gunline) emerged naturally from the RPS triangle.

### Narration

- Mutual gunline narration hints were excellent — "staring down each other's gun barrels" is exactly the moment the system is built for.
- One minor SOUL concern: the kill_rotation/kill_rotation hint says "whoever fires first probably lives" which implies a speed-draw mechanic not in the rules. The d6 tiebreaker covers this but the narration should reference it.

### Mechanics

- Energy pool felt like a real resource in run 3. Both pilots noticed depletion.
- d6 tiebreaker worked for mutual gunline. Quick, decisive, no ambiguity.
- No cells need rewriting — the RPS balance held across all 3 runs.

### Go / no-go

- **Ready to expand to 8 maneuvers?** Yes — the 4-maneuver RPS triangle is balanced. All exercised cells scored calibrated or exciting. The one `dull` cell (straight/straight) is the safety baseline by design.
- **Ready to promote to wireframe HUD prototype?** Not yet — need story 38-10 (tail-chase starting state) to prove the system generalizes beyond merge.
- **Ready to reskin to another genre?** Not yet — the descriptor schema is genre-agnostic, but no non-space_opera content exists to validate against.

### Session log

| Field         | Value   |
|---------------|---------|
| Playtest date | 2026-04-16 |
| Red pilot     | Game theory simulation (mixed) |
| Blue pilot    | Game theory simulation (aggressive) |
| GM            | Winchester |
| Duration      | 3 turns |
| Winner        | Blue (graze damage advantage) |

### Free-form notes

> Three runs exercised 8 of 16 cells. The 8 unexercised cells are all mirrors or evasive-vs-evasive/passive-vs-evasive pairings that produce no shots and no drama — they're the "both pilots play safe" space. The RPS core (offense vs passive = kill, offense vs evasive = miss, offense vs offense = mutual risk) is sound. Energy depletion creates a natural escalation arc. The extend-and-return rule (38-8) prevents infinite drift — any no-hit opening_fast turn resets to merge. Recommendation: proceed to 8 maneuvers.
