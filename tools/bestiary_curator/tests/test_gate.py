"""Genre-truth gate contract (story 158-20, AC-1 / AC-2).

GATE 1 of the two-gate pipeline: apply the world's ``world_register.yaml``
allow/deny rules to an SRD corpus row. Loaded from the REAL beneath_sunden
register so the rules under test are the proven ones:

    allow_types: [Undead, Aberration, Ooze, Monstrosity, Construct, Giant, Humanoid, Beast]
    deny.types:  [Celestial, Fey]
    deny.tags:   [titan, metallic, angel, genie]
    deny.name_glob: ["*modron*", "*faerie dragon*", "*pixie*", "*mephit*", ...]
    reskin:      {"Gray Ooze": "The Seep"}
    marquee:     [Lich, Mummy Lord, Vampire]   # exempt from denial (ADR-014)

Each deny path is ISOLATED: where possible the synthetic row has an *allowed*
type so a drop can only be attributed to the rule under test, not a type miss.
"""

import pytest

from bestiary_curator import WorldRegister, apply_genre_truth_gate


@pytest.fixture
def register(register_path) -> WorldRegister:
    return WorldRegister.from_yaml(register_path)


def _entry(name, type_, tags=None, cr=1.0):
    return {"name": name, "type": type_, "tags": tags or [], "cr": cr}


# ── allowed pass-through ──
def test_allowed_type_is_kept(register):
    d = apply_genre_truth_gate(_entry("Aboleth", "Aberration", cr=10.0), register)
    assert d.kept is True
    assert d.name == "Aboleth"
    assert d.reskinned is False


# ── deny.types ──
def test_deny_type_celestial_is_dropped(register):
    d = apply_genre_truth_gate(_entry("Solar", "Celestial", cr=21.0), register)
    assert d.kept is False
    assert d.reason and "celestial" in d.reason.lower()


def test_deny_type_fey_is_dropped(register):
    d = apply_genre_truth_gate(_entry("Dryad", "Fey", cr=1.0), register)
    assert d.kept is False
    assert d.reason and "fey" in d.reason.lower()


# ── allow_types miss (type neither allowed nor explicitly denied) ──
def test_type_not_in_allow_types_is_dropped(register):
    d = apply_genre_truth_gate(_entry("Adult Red Dragon", "Dragon", cr=17.0), register)
    assert d.kept is False
    assert d.reason and "dragon" in d.reason.lower()


# ── deny.tags (isolated: allowed type, denied tag) ──
def test_deny_tag_titan_drops_allowed_type(register):
    # Monstrosity is allowed; the 'titan' tag is what kills it.
    d = apply_genre_truth_gate(_entry("Kraken", "Monstrosity", tags=["titan"], cr=23.0), register)
    assert d.kept is False
    assert d.reason and "titan" in d.reason.lower()


# ── deny.name_glob (isolated: allowed type, name matches a glob) ──
def test_deny_name_glob_drops_allowed_type(register):
    # Construct is allowed; the name matches "*modron*".
    d = apply_genre_truth_gate(_entry("Modron", "Construct", cr=1.0), register)
    assert d.kept is False
    assert d.reason and "modron" in d.reason.lower()


def test_deny_name_glob_is_case_insensitive(register):
    # Beast is allowed; uppercase name must still match the lowercase "*pixie*" glob.
    d = apply_genre_truth_gate(_entry("PIXIE", "Beast", cr=0.25), register)
    assert d.kept is False
    assert d.reason and "pixie" in d.reason.lower()


# ── marquee exemption precedence (Diamonds-and-Coal, ADR-014) ──
def test_marquee_entry_is_kept_even_when_otherwise_denied(register):
    """A marquee name survives even if its type AND tag would both be denied."""
    d = apply_genre_truth_gate(_entry("Lich", "Celestial", tags=["titan"], cr=21.0), register)
    assert d.kept is True, "marquee rows are exempt from the deny gate"


def test_non_marquee_with_same_denied_attrs_is_dropped(register):
    """Control for the marquee test: identical denied attrs, non-marquee name -> dropped."""
    d = apply_genre_truth_gate(
        _entry("Random Angel", "Celestial", tags=["titan"], cr=21.0), register
    )
    assert d.kept is False


# ── reskin ──
def test_reskin_renames_kept_entry(register):
    d = apply_genre_truth_gate(_entry("Gray Ooze", "Ooze", cr=0.5), register)
    assert d.kept is True
    assert d.name == "The Seep"
    assert d.reskinned is True


def test_non_reskinned_keep_reports_reskinned_false(register):
    d = apply_genre_truth_gate(_entry("Aboleth", "Aberration", cr=10.0), register)
    assert d.reskinned is False
