# Magic/Powers Design — Space Opera

> **Revised 2026-04-27.** This file previously stated the genre had no magic
> system and that psionics were strictly a narrative condition (the "River Tam
> Rule"). That was a *world-level* rule baked into the genre layer. Space opera
> as a genre supports both Firefly-style worlds (River Tam Rule) AND Star
> Wars-style worlds (the Force as full magic system) AND Dune-style worlds
> (Voice + spice prescience). Each world picks a tuple from the genre's
> allowance space. See `docs/design/magic-taxonomy.md` and the planned
> `magic.yaml` schema for the framework.

## System Name
**Variable per world.** Space opera at the genre layer permits multiple magic
configurations:

- **No psychic magic + tech-only** (Firefly *most of the time*, the Expanse).
  River Tam Rule active — psionics as narrative condition, never player toolkit.
- **The Force / Innate-developed Psychic** (Star Wars across all eras).
  Player-class-buildable when the world's era permits.
- **Bargained-with-substance prescience** (Dune — spice melange, Bene Gesserit
  conditioning).
- **Telepathic minorities** (Babylon 5 telepaths, Mass Effect biotics) — biology-
  or experiment-derived, often regulated.

The genre commits to limits that hold across all worlds:
- Magic, where present, must follow rules with consequences (no "wizard fixes
  the hyperdrive" — tech and magic stay separate domains)
- Resurrection forbidden in all worlds
- McCoy (engineering) is always present and always carries narrative weight
- "Crew competence under pressure" is the genre's emotional engine regardless
  of magic level

## What Fills the Magic Slot

### Advanced Technology
Tech can be exotic — personal shields, neural interfaces, medical nanites,
jump drives — but it follows rules, has power sources, and breaks. It is
engineering, not sorcery. An engineer who reroutes the shield matrix in
combat is doing the space opera equivalent of casting a spell, but they'd
be offended if you called it that.

### Crew Synergy
The "magic" of space opera is what happens when a crew works together.
The pilot threads the needle while the engineer holds the engines together
while the officer talks them past the blockade. That's not supernatural —
it's trust and competence under pressure. It's better than magic.

### Xeno Biology (World-Defined)
Some alien species may have abilities that SEEM supernatural — empathic
perception, bio-luminescent communication, distributed consciousness.
These are biological, not magical, and are defined at the world level
via the Xeno flexibility slot. The genre does not provide these — worlds do.

## What Fills the Magic Slot

### Advanced Technology
Tech can be exotic — personal shields, neural interfaces, medical nanites,
jump drives — but it follows rules, has power sources, and breaks. It is
engineering, not sorcery. An engineer who reroutes the shield matrix in
combat is doing the space opera equivalent of casting a spell, but they'd
be offended if you called it that.

### Crew Synergy
The "magic" of space opera is what happens when a crew works together.
The pilot threads the needle while the engineer holds the engines together
while the officer talks them past the blockade. That's not supernatural —
it's trust and competence under pressure. It's better than magic.

### Xeno Biology (World-Defined)
Some alien species may have abilities that SEEM supernatural — empathic
perception, bio-luminescent communication, distributed consciousness.
These are biological, not magical, and are defined at the world level
via the Xeno flexibility slot. The genre does not provide these — worlds do.

## Psionics — World-Level Configuration

Psionics in space opera is **always world-configured**, never genre-default.
Three canonical configurations:

### The River Tam Rule (Firefly worlds)
Psionics exists but is **never a toolkit**. It is a plot driver. Someone with
psionic abilities was made that way, or born wrong, or experimented on. The
power is real but came at a terrible cost, and powerful people want to
control, weaponize, or eliminate the person who has it. A psionic character
is not a wizard — they are a liability, a mystery, and a moral question the
crew has to answer.

- Psionics is NOT a class or a learnable skill in this world
- It is a narrative condition, like a curse or a secret
- The narrator introduces it as plot, not as player option
- World-knowledge is **classified** — the world doesn't know psychic powers exist
- Think River Tam, not Jean Grey

### The Force Rule (Star Wars worlds)
Psionics is a **full magic system** — Innate-developed, Karma-cost (the dark
side), emotion-gated reliability. Player builds permitted when the era allows
(High Republic = celebrated/regulated; Imperial = persecuted; Sequel-era =
mythic-lapsed). The chosen-one narrative tag rides on top of Innate-developed
for specific characters.

- Psionics IS a class / build-option
- Karma is the load-bearing cost (dark side stain compounds)
- World-knowledge varies by era — acknowledged, mythic-lapsed, or persecuted
- Think Anakin, Luke, Rey — not River Tam

### The Bene Gesserit Rule (Dune worlds)
Psionic-adjacent abilities tied to **substance + training**: spice prescience,
Voice conditioning, distillation breeding programs. Source = Innate-developed
*plus* Bargained-for (the substance dependency). Cost = Vitality + social/
political entanglement. Player builds permitted but always world-gated by
substance access and lineage.

## If a Player Tries "Magic" (default genre register)
For tech-focused worlds (Firefly, Expanse), the default register applies:
- The narrator does not offer magical options
- If a player describes something magical, reframe it as tech or skill
- "I sense their emotions" → "You read their body language expertly."
- "I cast a fireball" → "You throw a thermite grenade."
- If a player wants psionics in such a world, it must come through narrative —
  backstory, world events, consequences. It is never free.

For magic-permitted worlds (Star Wars, Dune), the world's `magic.yaml` declares
the active tuple and the narrator follows that instead.

## Superstitions
Spacers are superstitious. They don't call it magic — they call it luck,
tradition, ritual. Naming a ship is serious. Renaming one is bad luck.
Some crews won't launch on certain days. Voidborn have elaborate rituals
for jump transitions. None of it is "real" — but disrespecting it will
cost you socially.

## Draft Narrator Instructions

**Read the active world's `magic.yaml` first.** Default narrator instructions
below apply when the world declares no psychic magic system (Firefly / Expanse
register). Worlds with active magic systems (Star Wars / Dune) override these
with their own narrator register.

Default register (no-psychic worlds):
Technology is advanced but follows rules and has limits — it breaks, runs out
of power, and requires expertise to use. When describing tech in action,
emphasize the human skill operating it, not the tech itself. The engineer
saving the ship is impressive because of the engineer, not the engine. If
alien species have unusual abilities, treat them as biology — remarkable but
natural. Spacer superstitions are culturally real even if not physically
real — respect them narratively.

## Draft NPC Instructions
For no-psychic worlds: NPCs do not reference magic, spells, or supernatural
forces. They may be superstitious — especially Voidborn and Frontier folk —
but frame it as tradition and luck, not mysticism. When describing advanced
technology, NPCs treat it as mundane. Nobody is impressed by a blaster —
they're impressed by the person holding it.

For magic-permitted worlds (Star Wars, Dune, etc.): NPC reactions to magic
follow the world's `world_knowledge` and `visibility` settings. In an
acknowledged-and-celebrated world, NPCs may revere casters. In a
persecuted world, NPCs fear them. The narrator must read the world tuple
before deciding NPC posture.
