# Dogfight Playtest — Duel 02: The Tail Chase

**Purpose:** Validate the 4-maneuver x 16-cell tail-chase interaction table by
resolving three turns of a 2-player dogfight by hand. Proves the sealed-letter
system generalizes beyond the merge starting state.

**Time budget:** 20-30 minutes for three turns plus debrief.

---

## How to run this playtest

1. **Three humans.** One plays Red Pilot (pursuer), one plays Blue Pilot
   (evader), one is the GM (who owns the lookup table and writes narration).
2. **Read the starting state below.** Red starts behind Blue — Red sees Blue's
   tail at 12 o'clock, Blue sees Red's nose at 6 o'clock. Both have energy 60.
   Neither has a gun solution yet (close but not locked).
3. **Each turn, both pilots secretly write their maneuver choice** in the
   Commit boxes. The four options are: `straight`, `bank`, `loop`,
   `kill_rotation`. Don't peek at each other.
4. **Reveal commits.** GM looks up the `(red, blue)` pair in
   `interactions_tail_chase.yaml` > `cells`.
5. **Apply deltas.** GM writes the `red_view` fields into Red's row and the
   `blue_view` fields into Blue's row. Subtract each pilot's own maneuver
   `energy_cost` from their energy pool.
6. **GM narrates.** 2-3 sentences per cockpit, using the cell's
   `narration_hint` as the beat. Red hears Red's narration, Blue hears Blue's.
   Same event, two POVs.
7. **Resolve shots:**
   - If one pilot has `gun_solution: true` and the other does not, the firing
     pilot scores a hit. Check `hit_severity` for damage level.
   - If both have `gun_solution: true`, each rolls a d6. Higher roll fires
     first and scores. The lower-roll pilot still fires, but at a damaged
     target — halve the damage.
   - If neither has a gun solution, no shots this turn.
8. **Win conditions.**
   - Hull damage per severity: graze = 5, clean = 15, devastating = 30.
   - Starting hull: 10 (light fighter). Two grazes = kill.
   - If a pilot runs out of energy (<=0), they cannot choose `loop` next turn.
9. **Extend-and-return rule:** After any turn where no hit landed AND at least
   one pilot's closure is `opening_fast`, both pilots reset to the tail-chase
   starting state with current energy preserved.
10. **Continue** for 3 turns or until one pilot is dead.
11. **Fill in the Debrief section.**

> **SOUL check:** Before narration, the GM confirms each of their 2-3 sentences
> refers to something that is actually in the descriptor. No hallucinated
> geometry. Red is the PURSUER — narration hints frame the action from behind.
> Blue is the EVADER — narration hints frame the action from ahead.

---

## Starting State — Tail Chase

**Environment:** Deep space. One fighter trailing the other in a stern pursuit.
Red has positional advantage. Blue must evade or reverse to fight.

### Red Pilot (Pursuer) — starting descriptor

| Field          | Value            |
|----------------|------------------|
| target_bearing | 12               |
| target_range   | close            |
| target_aspect  | tail_on          |
| closure        | closing          |
| energy         | 60               |
| gun_solution   | false            |

### Blue Pilot (Evader) — starting descriptor

| Field          | Value            |
|----------------|------------------|
| target_bearing | 06               |
| target_range   | close            |
| target_aspect  | head_on          |
| closure        | closing          |
| energy         | 60               |
| gun_solution   | false            |

**Opening narration (GM reads aloud to both pilots):**

> A lone fighter screams through the void, engines at full burn. Behind it,
> barely a ship-length back, a second fighter matches every jink and weave.
> The pursuer's gun cone is close — not locked, but close. The evader knows
> the guns are there. Both pilots reach for their maneuver commit.

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
- Hit severity:
- Hull damage:
- Notes:

---

## Turn 2

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
- Hit severity:
- Hull damage:
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
- Hit severity:
- Hull damage:
- Notes:

---

## Debrief

*Fill this in AFTER the third turn. Take 5 minutes.*

### Cells exercised

| Turn | Pair used | Cell name |
|------|-----------|-----------|
| 1    |           |           |
| 2    |           |           |
| 3    |           |           |

### Per-cell calibration tags

- **Turn 1 cell:** tag = __________  notes:
- **Turn 2 cell:** tag = __________  notes:
- **Turn 3 cell:** tag = __________  notes:

### Tail-chase specific questions

- Did the asymmetry feel right? Did Red feel like the pursuer and Blue like
  the evader?
- Did the evader have viable escape options, or did every choice feel hopeless?
- Did the pursuer's advantage feel earned or automatic?
- Did any reversal (kill_rotation by Blue) feel dramatically satisfying?

### Pacing

- Was there a "mutual kill risk" moment? Did it feel earned?
- Did energy management matter?
- Did the extend-and-return rule fire? Did it feel natural?

### Go / no-go

- **Ready to expand to 8 maneuvers?** (yes / no / not yet)
- **Ready to promote to wireframe HUD prototype?** (yes / no / not yet)
- **Tail-chase geometry validates the system?** (yes / no / not yet)
  - If "not yet," what feels different from merge that needs attention?

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
