# Perseus Cloud — Campaign Notes & Import Provenance

> **Source:** imported from Jade & Sebastien's *Master Lore* Obsidian vault
> (`~/Downloads/Master Lore`), 2026-05-28. This world is a **draft skeleton**
> (`world.yaml: draft: true`). The lore, factions, systems, and cultures were
> transcribed faithfully from the vault. Where the vault was **silent**, the
> import does **not** fabricate canon — gaps are flagged below for the table
> to fill, because (per Jade) most blanks are *curse-of-knowledge*: table
> canon so obvious to the players that nobody wrote it down.

## Sector frame (vault canon)

- **Perseus Cloud** — a Sectors Without Number sector, sealed off from the
  rest of the galaxy by the **Great Hyperspace Explosion (GHE)**, the
  Scream-analog that ended the **Persean Praetorium** and severed the jump
  lanes out.
- SWN map: <https://sectorswithoutnumber.com/sector/jKE1v8y9c4ykSx3YWYXH>
- Five contesting powers: **Regency of Thar**, **Southeastern Confederacy**,
  **Nimian Authority**, **Church of Recreation**, **House Akkad**. (The
  **Yulan Governance Conglomerate** is the corporate power on Yula — imported
  as a distinct faction, not one of the five houses.)

## Season 1 campaign skeleton (vault canon — titles only, beats are the table's)

The vault records the *structure* of the Season 1 campaign but not its prose.
Captured here verbatim so it is preserved, **not** invented into openings:

- **Season 1 Party:** Thorin Rist, Cyprien Coulombart, Gabriel — "massively
  important historical figures in the recent development of the sector's
  history."
- **Session 1 — The Jailbreak** → branches into **Session 2**, drawn by three
  hook NPCs:
  - **Barial Fen** (Church of Recreation, "Hassam" branch) → Session 2 — Hassam
  - **Eritrea Velmar** ("Halgerd" branch) → Session 2 — Halgerd
  - **Felra Amberton** ("Victory" branch) → Session 2 — Victory
- **The Princess and the Poisoner** — a scenario with central NPCs **Restra
  Velmont** and **Aliya Dad** (an Admiral in the Thari Navy exerting a
  regressive cultural force).
- **The Haven Propaganda Crisis** — downstream of the New Kowloon Dust delivery
  from the Yulan Broadcast Company to the Church of Recreation.

> These are **not** wired into `openings.yaml` — that file uses a neutral
> sector-arrival so the world plays cold or drops into Season 1. When Jade &
> Sebastien want the campaign live, author the Jailbreak as its own opening.

## Curse-of-knowledge gaps — TABLE CANON TO CAPTURE (not to invent)

The vault left these blank because they're obvious at the table. They are
**stubbed** in the YAML (`[STUB — Jade to author]`) and should be filled by
**interview**, not by the engine guessing:

| Gap | Where stubbed | What to capture |
|-----|---------------|-----------------|
| **Southeastern Confederacy** | `lore.yaml` factions | What is it? Holdings, goals, who runs it, disposition toward the others. |
| **Nimian Authority** | `lore.yaml` factions | Same — identity, territory, what it wants. |
| **House Akkad** | `lore.yaml` factions | Same — a noble house? a corp? its holdings and angle. |
| **Spacers** | `cultures/spacer.yaml` | Are they a faction, a culture, an underclass, or all three? Their relationship to Yula/Glitter and the lanes. |
| **Hyperspace / the GHE** | `lore.yaml` history | What actually *happened*? Is hyperspace travel still possible in-sector? What are **Shadows**? |
| **Dust** | `lore.yaml` cosmology | The parent of Lazarus Dust — what is Dust, where does it come from, what does corruption do generally? |
| **Psychics** | `lore.yaml` cosmology | Praetorium-legacy discipline — how common, how regarded, mechanically (SWN psionics?). |
| **Naming conventions** | `cultures/*.yaml` slots | All three culture naming slots are **provisional** best-fits. Capture the table's actual convention per culture. |
| **NPCs** | (not yet authored) | Restra Velmont, Aliya Dad, the three hook NPCs — only role-tags exist. Need disposition, voice, OCEAN, faction ties for an `npcs.yaml`. |

## Import file manifest

```
perseus_cloud/
├── world.yaml          # draft skeleton, starts on Yula
├── lore.yaml           # GHE, Praetorium, 5 factions (+Yulan), Dust/Pretech/Psychics
├── cartography.yaml    # 10 systems: thar coelitha lazzaro occum yula regula scrina zira terma ceron
├── history.yaml        # 4 maturity tiers + POIs (location entities)
├── cultures/           # thari, yulan, spacer (naming provisional)
├── openings.yaml       # solo + MP, sector-situated (NOT Season 1)
└── CAMPAIGN_NOTES.md   # this file
```

Inherits pack-level char_creation, archetypes, visual_style, and tropes from
`space_opera` (which binds the **SWN** ruleset — the reason this sector slots
in cleanly: the Cloud was built on SWN bones).
