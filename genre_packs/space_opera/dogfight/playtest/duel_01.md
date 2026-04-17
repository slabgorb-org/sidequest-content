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

## Debrief

*Fill this in AFTER the third turn. Take 5 minutes. Don't rush it — this is
the whole reason the playtest exists.*

### Cells exercised

| Turn | Pair used | Cell name |
|------|-----------|-----------|
| 1    |           |           |
| 2    |           |           |
| 3    |           |           |

### Per-cell calibration tags

*For each cell you used, tag it with one of: `exciting` / `calibrated` /
`lopsided` / `confusing` / `dull`. Brief notes on why.*

- **Turn 1 cell:** tag = __________  notes:
- **Turn 2 cell:** tag = __________  notes:
- **Turn 3 cell:** tag = __________  notes:

### Pacing

- Was there a "mutual kill risk" moment? Did it feel earned?
- Did any pilot ever feel they had **no** good option? (That's a design flaw.)
- Did any pilot ever feel they had **one obvious** option? (Also a design flaw.)
- Did energy management matter? Did anyone run low?

### Narration

- Did the 2-3-sentence-per-cockpit narration from the hints feel natural,
  or did it read like table text?
- Did you catch the GM making up anything NOT in the descriptor? (If yes,
  that's the SOUL violation we're trying to prevent — write down exactly
  what the GM invented.)

### Mechanics

- Did the energy pool feel like a resource, or was it a footnote?
- Did the d6 mutual-kill tiebreaker feel right, or should it be dice-less?
- Any cell you'd rewrite?

### Go / no-go

- **Ready to expand to 8 maneuvers?** (yes / no / not yet)
  - If "not yet," what needs to change first?
- **Ready to promote to wireframe HUD prototype?** (yes / no / not yet)
- **Ready to reskin to another genre?** (yes / no / not yet)

### Session log

| Field         | Value   |
|---------------|---------|
| Playtest date |         |
| Red pilot     |         |
| Blue pilot    |         |
| GM            |         |
| Duration      |         |
| Winner        |         |

### Free-form notes

>
