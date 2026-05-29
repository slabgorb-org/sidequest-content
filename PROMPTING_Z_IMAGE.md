# Z-Image Prompting Guide (SideQuest)

This is the house style for authoring Flux/Z-Image prompts for genre packs —
portraits, POI landscapes, scene art, LoRA captions. Z-Image Turbo is our
current renderer. It is **not** Stable Diffusion and the old habits do not
apply. Read this before writing a single prompt.

## The two rules you will break first

1. **There is no negative prompt.** Z-Image Turbo runs at `guidance_scale=0`
   and ignores `negative_prompt` entirely. The UI field is cosplay. Every
   "don't do X" constraint goes in the positive prompt, at the end.

2. **Z-Image renders text that appears in your prompt.** It is unusually good
   at text rendering. If you feed it prose full of proper nouns, dates, and
   quoted phrases, it will try to paint them onto the image as a caption,
   title, or label. **Descriptive prose is not a visual prompt.**

## The scaffold

Every prompt uses this order. Short clauses, camera-style, concrete.

```
[Medium + technique] +
[Shot + framing] +
[Subject + age + 2–4 traits] +
[Clothing + modesty if human] +
[Foreground / middle / background layout] +
[Lighting] +
[Mood] +
[Style anchor — artist, period, publication] +
[Safety / cleanup clause]
```

Example (mutant_wasteland POI — verified good output):

> post-apocalyptic digital painting, gritty painterly texture, desaturated
> earth tones with bioluminescent accent color, bruised amber and toxic green
> sky, weathered surfaces and rust, overgrown ruins, visible brush strokes,
> cinematic composition, dramatic volumetric light through haze, repurposed
> radio tower with jury-rigged antenna arrays, lookout platform with scavenged
> optics, wind-battered guy wires, panoramic wasteland view. **No text, no
> caption, no title, no writing, no labels, no watermark.**

## Translating prose lore into a visual prompt

Most of our world data is prose — history, cultural notes, GM flavor. **None
of that is a visual prompt.** A visual prompt is what a cinematographer would
tell a DP. Strip everything else.

### What to cut

- **Temporal / historical clauses.** "shops quieter than they were in '63",
  "winding down from the munitions peak", "since 1864" — not renderable.
- **Conditional / off-camera references.** "visible for a mile up the river
  by its plume alone" — if it's not in the frame, delete it.
- **Social / cultural flavor.** "a Sunday destination for courting couples
  who have read Mount Auburn in the pages of Godey's" — pure lore.
- **Proper nouns.** Place names, street numbers, brand names, people's names,
  publications. Z-Image will try to render these as text. Replace with the
  visual archetype: "Allegheny Arsenal" → "Civil-War-era brick arsenal
  buildings"; "Lucy Furnace" → "tall industrial furnace stack".

### What to keep / add

- Concrete nouns you can point a camera at.
- Spatial layout: foreground / middle / background.
- Materials and surfaces: brick, slate, rust, moss.
- Period shorthand as *style* (not as quoted text): "in the style of an 1870s
  Harper's Weekly engraving" — good. "'Harper's Weekly' masthead at the top"
  — bad, will render as literal text.

### Worked example — the 1870s Pittsburgh fix

**Prose lore (WRONG to feed to Z-Image):**

> 1870s newspaper engraving [...] North and east of the Strip along the
> Allegheny. The Allegheny Arsenal grounds lie between 39th and 40th Streets,
> the buildings Civil-War-era brick, the shops quieter than they were in '63
> [...] The Lucy Furnace (Carnegie) stands at 51st Street, visible for a mile
> up the river by its plume alone; Isabella is across the water at Etna. The
> Allegheny Cemetery [...] Stephen Foster buried since 1864 [...] courting
> couples who have read Mount Auburn in the pages of Godey's.

Failure mode: Z-Image rendered the proper nouns and dates as a garbled
newspaper caption across the bottom of the image.

**Visual rewrite (correct):**

> 1870s newspaper engraving, monochrome sepia, fine ink linework, engraved
> crosshatching detail. Wide elevated view looking north across a broad river.
> Foreground: brick Civil-War-era arsenal buildings, three and four stories,
> pitched slate roofs, tall chimneys, quiet empty grounds. Middle ground:
> the river bending left to right, a few small boats. Background left: a
> rolling rural cemetery on a hillside, scattered broken-column obelisks,
> weeping willow trees, winding paths. Background right: a tall industrial
> furnace stack with a dark plume of smoke rising high above the far
> riverbank. Overcast soft sky. Style of Harper's Weekly engraving, 1870.
> **No text, no caption, no title, no writing, no signatures, no labels, no
> watermark.**

## Named colors override stated medium (and it works)

Z-Image honors literal color words in the subject description even when the
medium is declared monochrome. If the prompt says `1870s newspaper engraving,
monochrome sepia` and the clothing description names `burgundy silk waistcoat`
and `gold watch chain`, Z-Image will paint the waistcoat burgundy and the
chain gold inside the sepia engraving — and the result reads as a
**hand-tinted** plate, which is historically accurate (many period engravings
were hand-colored) and visually beautiful.

Use this deliberately:

- Want a pure monochrome engraving? Describe clothing in tonal terms
  (`dark waistcoat`, `light shirt`, `pale trousers`) — no color names.
- Want a hand-tinted look? Name 1–3 colors in the subject — waistcoat,
  accessory, a flower. Let the rest stay tonal. Don't color-saturate the
  whole subject; the charm is the selective tint.
- The same principle applies to any medium/palette combo: if you name a
  color, Z-Image honors it over the stated palette. This is a feature, not
  a bug — but it means "desaturated earth tones" + "bright red jacket" in
  the same prompt will give you a bright red jacket in a desaturated world,
  not a muted red jacket.

## Style anchors and stray domain words are taken literally

Z-Image honors the *associations* of the words you feed it, not just their
denotation. Two failure modes from the aureate_span set (2026-05-29):

**A style anchor imports its whole medium.** Naming a comic-anthology lineage —
"European retro-futurist comic art," "Métal Hurlant," "Moebius," "Druillet" —
together with "bold confident contour linework with strong weight variation,
flat planar color fields" rendered flat comic-book cel: heavy black ink
outlines, flat fills, exaggerated faces. The intent was lush painterly Art
Nouveau. Fix: name painterly sources only (Mucha, Privat-Livemont) and describe
the rendering itself — "soft painterly rendering, luminous gradient shading and
rich tonal modeling, delicate fine linework subordinate to the painted form."
If you name a comic, you get a comic. Don't try to undo it with "no comic, no
cartoon" — style negations backfire like object negations do; steer with
positive painterly vocabulary instead.

**A common noun imports its real-world setting.** A spaceport POI that used
"docking berth," "yachts," and "berth" rendered a present-day water marina with
a moored motor yacht — despite "riveted steel decking," "freighter,"
"plasma-shielded dome," and "the corona of a dying star" in the same prompt.
"Berth / dock / yacht" are nautical, so the model drew water. Fix: medium-correct
nouns — "docking cradle," "private starcruiser," "space freighter," "hull
clamped in armatures above a dry metal deck," "thruster nacelles." This is the
proper-noun rule extended to *common* nouns: a word that belongs to another
setting or era drags the render toward that setting. Scan for them and swap in
the genre's own archetype.

## The mandatory safety clause

Every prompt ends with a cleanup clause. Tune which items you include, but
**always** include at least `no text, no watermark`.

Standard clause:

> **No text, no caption, no title, no writing, no signatures, no labels, no
> watermark, no logos.**

Extended clause when the model tends to add people/clutter:

> …no extra figures, no background crowd, no UI elements, no frame or border,
> no motion blur, no lens distortion.

For human subjects, also include the SOUL-safe clause (adapt for the genre):

> …fully clothed, modest outfit, correct human anatomy, natural hands and
> fingers, non-sexualized depiction.

## Length

- 80–250 words of **concrete** description is the sweet spot.
- Long is fine if it's precise. Long and novelistic is worse than short.
- Proper nouns are expensive — each one is a chance Z-Image tries to write
  it down. Use them sparingly, and only when the style anchor benefits
  (e.g. "in the style of Harper's Weekly" once is fine; mentioning Harper's
  Weekly three times is not).

## Worked example — period portrait

**Close-but-not-quite (caption smudge at the bottom):**

> 1870s newspaper engraving, lines, ink on sepia [...] A Black American man in
> his early fifties, . Short-trimmed hair [...] close cropped hair [...]
> Never a top hat — a plain felt homburg at most.

Three failures:
1. No safety clause → Z-Image tried to sign/caption the engraving at the bottom.
2. `Never a top hat — a plain felt homburg at most` — Z-Image ignores negations
   and reads this as *two* hats. Always phrase wardrobe positively.
3. Duplicated trait (`short-trimmed hair` + `close cropped hair`) and a dead
   clause (`, early fifties, .`). Tighten the language.

**Fixed:**

> 1870s newspaper engraving, fine ink linework on sepia, engraved
> crosshatching detail, monochrome. Chest-up portrait of an adult Black
> American man in his early fifties, warm medium-dark skin, short-cropped
> hair, neatly trimmed goatee, thoughtful expression looking off to one side.
> Wearing a black wool frock coat slightly rumpled with a small scorch mark
> on the left cuff, burgundy silk waistcoat, white high-collar shirt with
> dark cravat, gold watch chain, dark trousers, workshop apron pushed down
> around the waist. Plain felt homburg hat or bareheaded. Plain aged-paper
> background, no border, no frame. Style of Harper's Weekly portrait
> engraving, 1870. **No text, no caption, no title, no writing, no signature,
> no labels, no watermark, no page numbers.**

Pattern:
- Every negation turned positive (`never a top hat` → `plain felt homburg or bareheaded`).
- Duplicates collapsed.
- Safety clause added and extended with period-specific items (`no signature,
  no page numbers`) because the medium invites them.

## Prompting for portraits (humans)

Scaffold:

```
[Medium / style anchor] +
[Shot type — headshot, medium portrait, full-body] +
[Age + gender + 2–4 physical traits] +
[Clothing — concrete and modest] +
[Expression + pose] +
[Setting / background — usually simple] +
[Lighting] +
[LoRA trigger token if applicable] +
[Safety clause]
```

Always say "adult" for every human subject. Always specify clothing. Always
end with the safety clause.

### Interpretive face-language causes cartoon drift

(Learned from the pulp_noir/annees_folles portrait set, 2026-05-25.)

When a character description editorializes the face into an *impression* or
*expression* rather than a physical fact, Z-Image reads it as "caricature
this" and shifts the whole render from painterly illustration to comic-book
or grotesque cel style. The rest of the set stays painterly; the editorialized
ones drift cartoony.

The tell is adjectives that describe how a face *makes you feel* or *what it
suggests*, not what it physically *is*:

| Drifts cartoony (cut) | Renders painterly (keep) |
|---|---|
| "eyes magnified into something **owlish and unsettling**" | "pale blue eyes behind thick wire-rimmed lenses" |
| "a scar pulling his face into a **permanent half-smile that isn't one**" | "a scar from ear to mouth" |
| "**wild** hair that defies any comb," "**manic** expression" | "untidy grey hair," "alert expression" |
| "**bloodshot** eyes that still catch everything" | "tired blue eyes, dark circles" |

Rule: in the `appearance` field, describe the **physical fact** (the scar, the
lens thickness, the hair length/color, the brow shape) and let the face be
what it is. Interpretation ("unsettling," "manic," "owlish") belongs in lore
the narrator reads — never in the render prompt. A grotesque or exaggerated
*physical* feature (broken nose, heavy brow) is fine; it's the emotional/
impressionistic gloss on top of it that tips the medium.

### Non-visual sentences become painted captions

A description that ends with sentences Z-Image **cannot render** — character
judgments, backstory, personality — will be painted as a literal text caption
across the image. Observed: an `appearance` ending "His French is flawless.
His patience is not." rendered those two sentences as a caption strip along
the bottom of the portrait.

- Every sentence in a render prompt must describe something a camera could
  see. "His French is flawless" is not visual — cut it.
- The same applies to `element_visual` props that *carry text*: "a student
  identity card," "a letter in Vietnamese script," "banned pamphlets" all
  invite the model to render writing. Replace with the visual archetype
  ("a worn book bag," "a folded paper") or drop them.

This is the same root cause as the proper-noun rule (Z-Image renders text it
sees in the prompt) — it just shows up through *whole non-visual sentences*
rather than single proper nouns.

### World style suffix bleeds concrete nouns into every portrait

(Cross-reference: the visual_style.yaml authoring rule.) If a world's
`positive_suffix` names concrete objects or locations ("rain-slicked streets,
Montmartre rooftops, Seine reflections"), those get layered onto **every**
render in the world — so a head-and-shoulders portrait ends up with a rainy
Paris street behind it whether the shot wanted one or not. The world suffix
must be style/medium/palette vocabulary only. Concrete setting belongs in the
per-portrait `element_visual` (for the ones that want it), not the world layer.

### Scars and other tiny features render unreliably

Z-Image renders a thin facial scar as a jagged white crack or gash across the
cheek, not a fine line (observed on Commander Aurien Vex, aureate_span). Small,
precise features are low-confidence. Use scars sparingly — and in a high-tech
setting they're also a worldbuilding mismatch (cosmetic regeneration would
erase them; an unscarred face is the default). If a character genuinely needs
one, expect the artifact or choose a more render-friendly distinctive (bone
structure, an augment, a marking).

## Prompting for POI landscapes

Scaffold:

```
[Medium / style anchor from visual_style.yaml] +
[Wide / medium / close landscape shot] +
[Foreground — 1–3 concrete elements] +
[Middle ground — 1–3 concrete elements] +
[Background — 1–3 concrete elements, usually silhouette/atmospheric] +
[Sky + weather] +
[Lighting — time of day, light direction, quality] +
[Mood] +
[Period / style anchor] +
[Safety clause — especially "no text, no caption, no label"]
```

No human subjects unless the POI is people-centric. If people must appear,
they are silhouettes in the middle ground unless the shot demands otherwise.

## LoRA captions

LoRA captions are a different beast and follow ADR 032. They are short
(≈150 chars), structured tag schema, and end in the trigger token. They do
NOT follow this Z-Image prompt scaffold — they are training labels, not
generation prompts. See `lora/{genre}/` and the existing caption set for the
schema in use.

## Checklist before you hit generate

1. Did I delete every proper noun that doesn't have to be there?
2. Did I delete every non-visual clause (history, social context, conditional)?
3. Did I structure as foreground / middle / background?
4. Did I name a concrete style anchor (artist, publication, period)?
5. Did I specify lighting?
6. Did I end with the safety clause (`no text, no caption, no watermark`)?
7. For humans: did I say "adult", specify clothing, and add the SOUL clause?
8. Is it 80–250 words and all of it is renderable?
9. Does any style anchor or common noun import the wrong medium/setting (comic → cel, nautical → water)? Swap it for the genre's own vocabulary.

If all yes: generate. If not: rewrite.
