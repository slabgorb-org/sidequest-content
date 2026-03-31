# Star Chamber — Behavior Specs (BDD)

Behavioral scenarios for the Star Chamber genre pack. These validate that
the Confrontation Engine (Epic 16) correctly supports tribunal mechanics,
suspicion tracking, and testimony-as-evidence.

---

## Feature: Suspicion Resource

Suspicion is an involuntary ResourcePool that accumulates based on player
actions and NPC testimony. The player never sees a number — only narrative
signals driven by threshold events.

### Scenario: Suspicion increases from risky action

```gherkin
Given a star_chamber session with suspicion at 2
When the player visits the banned printer at night
And the narrator patch includes resource delta suspicion +2
Then suspicion should be 4
And a KnownFact should be minted with event_id "suspicion_noticed"
And the narrator_hint "Someone is asking about you" should appear in the next prompt context
```

### Scenario: Suspicion decays when laying low

```gherkin
Given a star_chamber session with suspicion at 5
When 3 turns pass without suspicion-raising actions
Then suspicion should decay to 4.7
And no new suspicion threshold should fire
```

### Scenario: Suspicion threshold triggers arrest

```gherkin
Given a star_chamber session with suspicion at 9
When the narrator patch includes resource delta suspicion +1
Then suspicion should be 10
And a KnownFact should be minted with event_id "suspicion_arrest"
And the narrator_hint should include "Guards at the door"
And a tribunal encounter should be eligible to start
```

### Scenario: Suspicion thresholds are idempotent across save/load

```gherkin
Given a star_chamber session where "suspicion_noticed" has already fired
When the session is saved and reloaded
Then "suspicion_noticed" should be in fired_thresholds
And crossing suspicion 3 again should not mint a duplicate KnownFact
```

---

## Feature: Tribunal Encounter

The tribunal is a StructuredEncounter with conviction as its metric. The
player sits before judges and responds to testimony. Every prior action
in the game feeds the evidence dossier.

### Scenario: Tribunal starts with evidence-based conviction

```gherkin
Given a star_chamber session where 3 testimony KnownFacts exist against the player
When a tribunal encounter begins
Then the encounter type should be "inquisition"
And the metric name should be "conviction"
And conviction starting value should reflect accumulated evidence weight
And the narrator prompt should include all testimony KnownFacts
```

### Scenario: Cross-examination reduces conviction

```gherkin
Given an active tribunal encounter with conviction at 6
When the player chooses the "cross_examine" beat
And the rhetoric check succeeds
Then conviction should decrease by the beat's metric_delta
And a narrator_hint should note the witness's credibility is damaged
```

### Scenario: Failed cross-examination backfires

```gherkin
Given an active tribunal encounter with conviction at 6
When the player chooses the "cross_examine" beat
And the rhetoric check fails
Then conviction should increase by 2 (the risk penalty)
And a narrator_hint should note the tribunal's displeasure
```

### Scenario: Confession resolves the tribunal

```gherkin
Given an active tribunal encounter
When the player chooses the "confess" beat
Then the encounter should resolve
And the outcome should be determined by the world's confession rules
And the game should transition to the confession aftermath
```

### Scenario: Conviction threshold condemns

```gherkin
Given an active tribunal encounter with conviction at 9
When testimony adds conviction past threshold_high (10)
Then the encounter should resolve with outcome "condemned"
And the narrator should describe the sentencing
```

### Scenario: Acquittal through negative conviction

```gherkin
Given an active tribunal encounter with conviction at -3
When the player successfully cross-examines, pushing conviction to -5
Then the encounter should resolve with outcome "acquitted"
And the narrator should describe the tribunal's grudging release
```

---

## Feature: Interrogation Encounter

Interrogation is a StructuredEncounter where the player (or the tribunal)
extracts testimony from an NPC. Cooperation is the metric.

### Scenario: Threatening a witness raises suspicion

```gherkin
Given an interrogation encounter with an NPC witness
When the player chooses the "threaten" beat
Then cooperation should increase by 3
But suspicion should also increase by 1
And a KnownFact should record the player's use of threats
```

### Scenario: Befriending a witness costs nothing

```gherkin
Given an interrogation encounter with an NPC witness
When the player chooses the "befriend" beat
And the charm check succeeds
Then cooperation should increase by 1
And suspicion should not change
```

### Scenario: Broken witness yields testimony KnownFact

```gherkin
Given an interrogation encounter with cooperation at 7
When cooperation crosses threshold_high (8)
Then the encounter should resolve
And a KnownFact should be minted with the NPC's testimony content
And the testimony should become available as evidence in future tribunal encounters
```

---

## Feature: Satire Axis

The satire axis controls narrator tone without changing mechanics. At
grave, the tribunal is terrifying. At farcical, it's absurd. The
conviction meter, the beats, the resolution — all identical.

### Scenario: Same tribunal, different tone

```gherkin
Given a star_chamber session with satire axis at 0.1 (grave)
When a tribunal encounter begins
Then the narrator_hints should include the grave modifier text
And the narrator tone should be "meticulous institutional horror"

Given a star_chamber session with satire axis at 0.9 (farcical)
When a tribunal encounter begins
Then the narrator_hints should include the farcical modifier text
And the narrator tone should be "absurd institutional farce"
And the encounter mechanics should be identical to the grave version
```

### Scenario: Satire affects accusation content

```gherkin
Given a star_chamber session with satire axis at 0.9
When the tribunal reads charges
Then the charges should be petty, contradictory, or transparently personal
And the delivery should be completely deadpan
And the mechanical consequence should be identical to grave-mode charges
```

---

## Feature: Informant Assignment

The assignment matrix randomizes which NPCs are informants each playthrough.
Players cannot determine this from archetype alone.

### Scenario: Informant identity varies per playthrough

```gherkin
Given two star_chamber sessions with the same world and seed
When session A assigns informants with seed 12345
And session B assigns informants with seed 67890
Then the informant NPC set should differ between sessions
And at least one NPC who was friendly in session A should be an informant in session B
```

### Scenario: Informant reports raise suspicion

```gherkin
Given a star_chamber session where the baker NPC is an assigned informant
When the player tells the baker about visiting the printer
Then after the NPC's autonomous action phase
The narrator should have access to a testimony KnownFact from the baker
And suspicion should increase
```

---

## Feature: Testimony as Persistent Evidence

Testimony from NPCs (whether from interrogation, informant reports, or
voluntary witness statements) persists as KnownFacts in LoreStore and
feeds the tribunal's evidence dossier.

### Scenario: Testimony accumulates across the game

```gherkin
Given a star_chamber session in act 1
When NPC_A testifies that the player visited the printer
And NPC_B testifies that the player spoke against the bishop
Then both KnownFacts should persist in LoreStore
And when a tribunal encounter begins in act 3
Then both testimonies should appear in the narrator's evidence context
```

### Scenario: Contradictory testimony creates opportunity

```gherkin
Given a tribunal encounter where NPC_A says the player was at the printer
And NPC_B says the player was at the tavern at the same time
Then the narrator should recognize the contradiction
And the "cross_examine" beat should be available with a bonus
```
