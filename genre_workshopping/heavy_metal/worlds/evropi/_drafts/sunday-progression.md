# Evropi — Sunday GM-Fiat Progression Sheet

**Status:** Pre-Epic-39. The Edge/Composure engine and typed `AdvancementEffect` enum are not yet wired. This sheet is **narrator-facing prose guidance** — the GM (Keith) and the narrator LLM honor these milestones through storytelling, not dice modifiers. Use it at the table this weekend.

**Author:** GM (Hawkeye), 2026-04-18
**Audience:** Keith (running the session), the narrator LLM (injecting this as a persistent KnownFact per character), the party
**Lifespan:** Until Epic 39 ships — at which point these become real mechanical effects in each character's `character-progression/{slug}.yaml` (see sibling folder).

---

## How to use this sheet

1. At session start, load each character's **Trunk** entry as a persistent narrator hint (KnownFact priority: high). The narrator must honor it from the opening scene.
2. When a character hits a **milestone trigger**, announce it at the table ("Rux, you just earned *Kept the Master's Books*"). Add the milestone's narration_hint to that character's KnownFact stack.
3. Three milestones per character per level (matches `progression.yaml: milestones_per_level: 3`). At L2 and L3, pick any three from the path sheet below — triggered by play, not pre-selected.
4. **Do not** require dice modifiers. The milestones manifest as *what the narrator does*, not *what the numbers say*. That's genre-true for heavy_metal and it lets the session run this Sunday.
5. When Epic 39 lands, the typed YAML in `character-progression/` becomes canonical; this sheet retires.

---

## Party composition note

Five of the six characters share the hook *reach_a_buried_place* (Rux, Prot'Thokk, Hant, Pumblestone, Th`rook). Pumblestone carries *unpaid_teacher* alone. The Zbóźny mines are the gravity well. Progression should cash in when they arrive — every character should have one milestone that *only fires at the buried place*, reserving a payoff for the arc destination.

---

## Rux — Kobold Rogue, 12,000-year servant-line

**Trunk — *The Dog That Listens*** (persistent)
> When an NPC has addressed Rux as an animal within the last exchange, the narrator gives Rux one concrete piece of information the NPC didn't mean to reveal — a glanced-at door, a mispronounced name, a ledger left open. Rux's indignation is *attentive*. He has not stopped explaining, and the world has not stopped correcting him for it.

**Silent Servant** (stealth/knowledge)
- *Kept the Master's Books* — once per scene, Rux recognizes a sigil, script, or heraldry from archive-memory; narrator reveals one true fact about any written object he touches.
- *The Room Before the Scholar* — when entering an archive, court, or record-chamber, Rux arrives first; the first infiltration obstacle does not resolve against him.
- *Twelve Thousand Years of Listening* — **1/arc.** Rux declares he knows something only a Tismenni servant would know. The narrator must make it true and must make it *matter* within the same scene.

**Defender of the Master** (DPS)
- *Low Line* — Rux's strikes land where scholars taught his line to strike. The narrator describes precision, not force. Damage language is *scholar-killer*, not duelist.
- *Between the Words* — when an enemy is mid-speech, Rux's attack resolves *inside* the sentence. Once per scene, the enemy's own words are the last thing they say.
- *The Master Is Still Protected* — **1/arc.** Rux declares a ward on one named companion. The next blow that would break that companion lands on Rux instead; he survives it by the narrator's grace.

**The Unfound** (avoidance)
- *Already Dismissed* — once per scene, an enemy's eye slides past Rux; their targeted action resolves against someone or something else. The narrator describes why.
- *Joints of a Thing* — any Tismenni-make lock, door, or mechanism opens at his touch without check. Period.
- *Not Where the Blade Lands* — **1/arc.** For one exchange, Rux is not in the room as far as enemies can perceive. The narrator writes him out and back in.

**Servitude Thread** (pick ONE at any path's tier 2)
- **The Tongue Kept** — Rux begins to speak Tismenni aloud. NPCs who hear it stop for a beat; some lose composure. *Cost:* the Wazdia writes his name in ink.
- **The Master Remembered** — Rux carries a named Tismenni scholar's relic; once per long rest, the scholar advises him on one decision. *Cost:* the scholar also judges him, and tells him when he's wrong.
- **The Name That Is Not "Dog"** — once per scene, Rux may force a correction. If the NPC refuses the name, treat them as openly hostile to Rux specifically for the rest of the scene. (No self-sabotage clause — he may let an insult pass in a crisis. He usually won't.)

---

## Prot'Thokk — Half-Orc Fighter, guardian, Cheeney's sworn

**Trunk — *Used to Being Watched*** (persistent)
> When the party enters a new settlement, Prot'Thokk draws the first attention — villagers, informers, Mistos-hired eyes. The narrator grants the rest of the party one scene of reduced scrutiny. The half-orc absorbs the suspicion so the others can work.

**Wall Between** (tank)
- *Stand in Front* — while Prot'Thokk is composed (full Edge), adjacent allies benefit from his bearing; the narrator describes enemies reading the room and picking easier targets.
- *Fought Wounded* — at half composure or worse, Prot'Thokk's violence escalates. The narrator writes him as more dangerous *because* he's hurting.
- *The Last Line* — **1/arc.** When Prot'Thokk would hit composure_break, he refuses once. The scene continues. He pays for it later.

**Fellow Escapee** (guardian of dependents)
- *Broke the Chains* — once per scene, Prot'Thokk frees a bound or captured ally as a single action; narrator does not require a lock-roll or a guard-beat.
- *Mistos Can Wait* — when a pursuing institutional faction (Mistos, guild, company) targets a companion, Prot'Thokk can redirect that attention onto himself for the scene. *Cost:* his own name goes further up the ledger.
- *Open Account Closed* — **1/arc.** Prot'Thokk finishes a named pursuer from his past. The reckoning is his; the narrator does not soften it.

**Over the Horse** (signature)
- *Lil' Sebastian Stands* — any hostile action targeting Cheeney or the horse can be intercepted as a reaction. No movement required. The narrator always allows it.
- *Grief Is a Posture* — if Cheeney falls, Prot'Thokk cannot be knocked prone and cannot drop his weapon for the remainder of the scene. He is literally unmoveable.
- *Die Over the Horse* — **campaign-once.** If the horse or Cheeney would die, Prot'Thokk dies instead. Permanent. He comes back in the next session — the world owes him a resurrection it cannot name. **Use this once per campaign, and only once.**

**Servitude Thread**
- **The Oath That Stood** — Prot'Thokk swears a binding word to Cheeney in the open. From then on, any NPC who has heard the oath treats Prot'Thokk's refusals as load-bearing.
- **The Mines Remembered** — Prot'Thokk carries a chain-link from the Ingurdios mine. Once per session, he can find his way out of any subterranean space by touch.
- **The Chain That Never Re-Closes** — Prot'Thokk can break any lock, manacle, or fetter by hand if the binding is on a person. Not on a door. Not on a chest. On a person.

---

## Hant — Antman Bard, pheromone-composer

**Trunk — *Composition, Not Explanation*** (persistent)
> Hant never names the chemistry. His songs affect scene mood — NPCs find themselves calmed, unsettled, or bold without understanding why. Per narrator_tone, no NPC ever says "pheromone." Astran priests log minor miracles. Vaermm book-checkers narrow their eyes. The narrator describes the effect, never the mechanism.

**Composition** (party support)
- *Drowse* — once per scene, one enemy loses composure visibly; narrator describes sudden fatigue, a misplaced word, a step out of stance.
- *Courage of the Hollow* — when Hant opens a scene with a phrase, the first party member to act does so with the narrator's explicit description of calm.
- *Hive Chord* — **1/arc.** The party acts before all enemies for one exchange. The narrator writes the beat as one unified motion; Hant's composition has moved through all of them.

**Unheard Chord** (read the room)
- *Pheromone-Court Etiquette* — once per scene, Hant reads an NPC's emotional state; narrator answers truthfully and concretely ("she is afraid of the older priest," not "she seems nervous").
- *The Current He Followed* — once per session, Hant knows which exit the scene's danger will come through. The narrator must place the danger there.
- *Drowse the Miracle-Logger* — **1/arc.** Hant causes an institutional record of the party to be misfiled. The next pursuing faction loses one beat of tracking.

**Stay Ahead of a Name** (surface survival)
- *Surface Stranger* — on first meeting, NPCs who have never seen an antman default to wonder or menace, not hostility. Hant's opening move in any social scene resolves unopposed.
- *Legendary Creature* — once per session, an NPC treats Hant's testimony as miraculous, regardless of content. Court officials, priests, and scholars record it.
- *The Name That Doesn't Reach* — **1/arc.** A named pursuer loses Hant's trail permanently. The narrator writes them as giving up, misled, or redirected. It does not matter which.

**Servitude Thread**
- **Composer to the Surface** — Hant stops traveling upward and starts *working*. He can be commissioned; the party gains income from his compositions between sessions.
- **The Current Followed Home** — Hant reaches the Deep Hollows again. The hive remembers him. One hive-kin appears in the next session as a resource.
- **Bard of No One's Court** — Hant renounces the pheromone-courts. He composes for the surface now, permanently. The hive no longer answers.

---

## Ludzo — Human Rogue, Zkęd exile, watched

**Trunk — *No Room Is Entirely Private*** (persistent)
> In any indoor setting, Ludzo gets one free piece of overheard information per scene — a servant's conversation, a ledger entry glimpsed, a door left ajar. He has spent his life in a land where nothing is ever fully closed.

**Beaded Step** (political survival)
- *Which Weeks to Stay Out* — once per session, Ludzo declares a Wazdia informer absent from the scene. The narrator must write them out — they are elsewhere on other business.
- *Positioned or Adjacent* — Ludzo finds one old Zkęd ally per session, usable for one scene. The ally may be out of favor, compromised, or dying — but they will speak to him.
- *Extract Concession* — **1/arc.** Ludzo forces a named authority to grant a real concession. Narrator must honor it as binding. *Earns an oath or debt milestone.*

**Egzami Rim** (survivor)
- *Survived Young* — once per scene, a killing blow against Ludzo becomes "left for dead." He resumes next scene with the injury still mattering.
- *The Waz's Comprehensive Answer* — when a party member would die by a named Zkęd-faction enemy, Ludzo may take the hit in full knowledge of who sent it.
- *Still Leaving* — **1/arc.** Ludzo erases his presence from a concluded scene retroactively. Witnesses cannot name him. Records cannot place him. The narrator rewrites the departure.

**Widząn's Work** (investigation)
- *The Zygwa Question* — once per scene, Ludzo asks the narrator one question about a hidden faction motive. The answer is partial but truthful — genre-true, never misleading.
- *Rumor's Current* — once per session, Ludzo knows the name and goal of the next antagonist the party will encounter, one scene ahead of contact.
- *Found What the Widząn Found* — **1/arc.** Ludzo retrieves a piece of intel that closes one open mystery thread. Narrator commits to the answer; the thread is resolved.

**Servitude Thread**
- **The Bead That Broke the Chain** — Ludzo removes a single bead from his braid. That bead becomes a physical proof-of-exile. Showing it to a Zkęd noble compels a beat of honest response.
- **Return to the Court** — Ludzo goes back. Once. The scene plays out. The session after it, he is either dead, promoted, or reborn.
- **The Widząn's New Recruiter** — Ludzo joins the Widząn Zamzau. The Zygwa search becomes his search. *Cost:* he cannot refuse their next three requests.

---

## Pumblestone Sweedlewit — Gnome Wizard, forgetful sage

**Trunk — *Shape Right, Name Wrong*** (persistent)
> Pumblestone confidently misremembers big canon — factions, history, geography, major NPCs. He gets the *shape* right and the *specifics* wrong. Per narrator_tone, the world does not wink. Once per scene, his wrong answer proves *accidentally actionable* — the wrong-but-close detail opens a path the correct answer would not have.

**Older Alphabet** (knowledge)
- *Read What Others Can't* — any text in an older script resolves for Pumblestone without check. He reads it, even if he misquotes it later.
- *Blank Column at the Back* — once per session, Pumblestone inserts one small detail into world-state ("there's always been a side-door here" / "my grandmother knew a priestess in this town"). Narrator canonizes it. Modest scale.
- *The Reading That Costs* — **1/arc.** Pumblestone deciphers a relic's true nature. Narrator reveals full truth. *Earns a revelation milestone* and grants the party one concrete piece of mechanical intel for the next encounter.

**Unpaid Attention** (the teacher's debt)
- *Owed Future* — once per scene, Pumblestone casts a working without naming the cost aloud. Narrator defers the cost — it comes due later, at a moment of narrator's choosing.
- *Interest Accrues* — the unpaid teacher appears once per session with a small demand. Refusal escalates the demand. Compliance reduces it.
- *Pay in Full* — **1/arc.** Pumblestone settles the teacher-debt in one dramatic scene. *Earns a reckoning milestone.* From that scene forward, the teacher is a permanent resource OR a permanent enemy — Pumblestone's choice at the moment of settlement.

**Three Maps Disagree** (the buried place)
- *One Map Is Right* — once per scene with conflicting intel, Pumblestone declares which source is true. Narrator honors it.
- *Walking Toward It* — travel to the Zbóźny strata site gains narrative momentum. Narrator skips uneventful travel scenes and cuts forward.
- *The Strata Site Opens* — **1/arc, at the buried place only.** Pumblestone reaches the site first. The party arrives in his wake. Whatever is there acknowledges him as the one who came looking.

**Servitude Thread**
- **The Teacher Repaid** — the unpaid teacher is satisfied. Pumblestone gains one permanent older-alphabet working, author's choice.
- **The Book That Held It** — Pumblestone acquires a Vaermm book-checker's ledger blank. He can *write himself* into records that previously did not include him.
- **The Site Found Wrongly** — Pumblestone arrives at the buried place by the wrong road. It still opens. But something follows him back.

---

## Th`rook — Pakook`rook Warlock, reniksnad-dependent

**Name:** Placeholder **Th`rook** until Sebastien confirms a canonical name from prior conversation.

**Trunk — *The Patron Answers the Knotsong*** (persistent)
> The pact is older than the Zkęd kingdom. It lives in the water where reeds meet rock. When Th`rook sings a knotsong — inflated throat-sac, eyes half-closed — something answers. The patron is never fully described, never named in full. Its presence is a pressure and a permission. NPCs who hear the knotsong feel nothing consciously; Pakook`rook who hear it recognize it and know to look away.

**Day-one starting kit — *Sung to the Rock Beneath the Water*:**
- *Knotsung Name* — invocations through knotsong cost 1 less Voice. He inflates the throat-sac and sings the patron's name.
- *Creditor's Mark* — Th`rook recognizes other warlocks' pact-creditors on sight. Narrator reveals one true fact about any such sign on first encounter.
- *The Dose Helps* — **reniksnad-dependent trade-off.** While his reniksnad is above 5, the commit_cost beat costs 1 less Flesh — the drug silences the body. At reniksnad 5 or below (withdrawal), the same beat costs 1 more Flesh. The drug is mechanically productive until it isn't.

**Character resource — Reniksnad (tracked manually by GM this session):**
Starting value: **7** (mid-range, already-addicted baseline).
Decay: **1 per scene**.
Thresholds:
- **At 5** — *first tremor.* His hand shakes slightly when he reaches for water. A Wazdia informer would note it.
- **At 3** — *withdrawal.* His voice thins; knotsongs fail on the high notes. Voice-spends cost 1 more per invocation while he is here.
- **At 0** — *death clock.* He will die within one in-fiction week without another dose. The narrator plays this medically, not dramatically.

Refill: **narrator-authored dose event only.** The Wazdia controls the reniksnad supply south of the Zbóźny foothills. The party may source doses through trade, theft, or a freedman's clandestine line; every option is a scene.

**Backstory:** Born in Pę (the Zkędzała slave-city), force-fed reniksnad from childhood to keep the labor compliant. Somewhere in his teens, working alone in the reed-beds, he heard something in the deep swamp sing back to his knotsong — and negotiated. The pact freed him from the Zkęd. It did not free him from the reniksnad. The patron does not know or care about withdrawal; it cares about the knotsong being sung and the water being deep enough. Th`rook is walking north because the patron named a place, and because the Wazdia's supply is south and he will not go south again.

**The Songsworn** (pact signature path)
- *The Water Is Deep Enough* — pact workings near standing water deeper than waist-height resolve as if rehearsed. Narrator treats invocations as already-steadied.
- *The Patron Remembers the Song* — closing the book on a working at standing water costs less Ledger.
- *Sung Into the Rock* — **1/arc, at the patron's named place only.** The patron answers in full. Whatever is requested arrives; the price is paid simultaneously across all four resources.

**The Pę Quiet** (the addict's hard-won self-knowledge)
- *Tremor as Tell* — recognizes other reniksnad-addicts on sight. Narrator reveals one truth about their supply.
- *The Body Keeps Its Own Ledger* — at withdrawal (reniksnad ≤3), his pact workings gain a bitter precision. Narrator describes the body paying attention for him.
- *Dying But Not Yet* — **1/arc, at reniksnad=0.** Invoke the pact's emergency clause. The patron defers his death by one week at the cost of an unspecified future service the narrator commits to later.

**The North Road** (the buried place, his version)
- *Away From the Supply* — recognizes Wazdia informers, tax-collectors, and reniksnad-trade agents on sight.
- *The Named Place* — once per session, knows whether the current location is closer to or farther from the place the patron named.
- *Arrival* — **1/arc, at arrival only.** The patron speaks in full. Narrator authors the scene. Reniksnad dependency ends or transforms.

**Servitude Thread** (pick ONE at any path's tier 2)
- **The Knotsong Teacher** — takes on an apprentice (freed Pakook`rook child or Waterfolk bard). Their presence grants 1 additional Voice spend per session.
- **The Freed Water** — establishes a safe marsh-settlement for other Pakook`rook walking north. Recurring safe harbor, factional heat.
- **The Reniksnad Broken** — pact-working substitutes patron's presence for the drug. He does not die. But he cannot be more than a day's travel from deep water for the rest of his life.

**Narrator note for Sunday:** Th`rook's reniksnad is the party's shared clock. The GM (Keith) decrements it by 1 at each scene end. At thresholds, the narrator is **required** to deliver the hint prose — not as flavor, as mechanical honesty. If the party finds or trades for a dose, Keith names the refill amount at the moment of administration (typical: +3 to +5, depending on the dose source's quality). Wazdia-supplied reniksnad refills more reliably than street-sourced.

---

## Milestone seeds for Sunday

If you need discrete triggers, here are three per character you can aim for in session — one per likely path. Hit any three to level each character to L2.

| Character | Seed 1 (oath/debt) | Seed 2 (ruin/revelation) | Seed 3 (reckoning) |
|---|---|---|---|
| Rux | swear silence on something he overheard | recognize a Tismenni artifact in a Zbóźny tunnel | correct an NPC who could have killed him for it |
| Prot'Thokk | name Cheeney as his sworn | witness a Mistos fresh-chain on a gnome | finish a Mistos overseer from his past |
| Hant | compose a working no one in scene can explain | learn the current is a *call*, not a current | lose a pursuer by misfiling a record |
| Ludzo | take a Widząn Zamzau coin | survive a Wazdia question he was not meant to survive | grant a concession to a rival faction in exchange for one of his own |
| Pumblestone | confidently misremember something that turns out correct | open an older-alphabet text that names him | decline to pay the teacher in a scene where paying would have been easy |
| Th`rook | swear a knotsong to the party in the patron's hearing | survive a withdrawal scene by a single scene break | refuse a Wazdia dose-offer with a tactical cost |

---

## Narrator contract addendum (Sunday only)

Load this as a system-level instruction for the narrator LLM this weekend:

> **Progression is narrative, not numeric.** You will be told, per scene, which milestones each character has earned. When a milestone's trigger conditions recur, you must honor the milestone's described effect in prose — not as a flavor option but as a *required* scene outcome. Players earn these by play; the milestones change what the world does, not what the numbers do. Composure, damage, and advancement remain narrator-authored this session. Epic 39 will replace this with typed engine effects. Until then: *you* are the engine.

— Hawkeye, 2026-04-18
