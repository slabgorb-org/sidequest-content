"""Fail-loud input-validation contract (158-20 review rework).

The "No Silent Fallbacks" project rule (content CLAUDE.md, <critical>) requires
malformed/empty config to fail loud, not silently produce wrong-or-empty output.
These tests pin each fail-loud path the reviewer flagged:

- empty / non-mapping world_register.yaml      -> ValueError (not a zero-config register)
- empty allow_types                            -> ValueError (an empty allow list denies everything)
- negative CR                                  -> ValueError (not a silent level-1 stat block)
- empty / non-list / non-dict-row corpus       -> ValueError (not a cryptic TypeError)
"""

import pytest

from bestiary_curator import WorldRegister, cr_to_level, curate

VALID_REGISTER = """
register: "test"
allow_types: [Undead, Beast]
deny:
  types: [Celestial]
  tags: [titan]
  name_glob: ["*pixie*"]
reskin: {}
marquee: []
"""


def _write(tmp_path, name, text):
    p = tmp_path / name
    p.write_text(text)
    return p


# ── world_register.yaml must be a non-empty mapping ──
def test_from_yaml_rejects_empty_file(tmp_path):
    path = _write(tmp_path, "world_register.yaml", "")
    with pytest.raises(ValueError):
        WorldRegister.from_yaml(path)


def test_from_yaml_rejects_comment_only_file(tmp_path):
    path = _write(tmp_path, "world_register.yaml", "# just a comment, no data\n")
    with pytest.raises(ValueError):
        WorldRegister.from_yaml(path)


def test_from_yaml_rejects_non_mapping(tmp_path):
    path = _write(tmp_path, "world_register.yaml", "- a\n- b\n")  # a list, not a mapping
    with pytest.raises(ValueError):
        WorldRegister.from_yaml(path)


# ── allow_types must be non-empty (an empty allow list denies the whole corpus) ──
def test_from_yaml_rejects_empty_allow_types(tmp_path):
    path = _write(tmp_path, "world_register.yaml", 'register: "x"\nallow_types: []\n')
    with pytest.raises(ValueError):
        WorldRegister.from_yaml(path)


def test_from_yaml_rejects_missing_allow_types(tmp_path):
    path = _write(tmp_path, "world_register.yaml", 'register: "x"\nmarquee: [Lich]\n')
    with pytest.raises(ValueError):
        WorldRegister.from_yaml(path)


def test_from_yaml_accepts_valid_register(tmp_path):
    path = _write(tmp_path, "world_register.yaml", VALID_REGISTER)
    reg = WorldRegister.from_yaml(path)
    assert reg.allow_types == ["Undead", "Beast"]


# ── cr_to_level must reject negative CR (no silent level-1) ──
def test_cr_to_level_rejects_negative_cr():
    with pytest.raises(ValueError):
        cr_to_level(-1.0)


def test_cr_to_level_still_accepts_zero():
    assert cr_to_level(0.0) == 1


# ── curate must reject a non-list / empty / non-dict-row corpus ──
@pytest.fixture
def register(tmp_path):
    return WorldRegister.from_yaml(_write(tmp_path, "world_register.yaml", VALID_REGISTER))


def test_curate_rejects_none_corpus(register):
    with pytest.raises(ValueError):
        curate(None, register)


def test_curate_rejects_empty_corpus(register):
    with pytest.raises(ValueError):
        curate([], register)


def test_curate_rejects_dict_shaped_corpus(register):
    # author wrapped rows in a mapping instead of a list
    with pytest.raises(ValueError):
        curate({"Aboleth": {"type": "Aberration"}}, register)


def test_curate_rejects_non_dict_row(register):
    with pytest.raises(ValueError):
        curate(["Aboleth"], register)


def test_curate_accepts_a_valid_row(register):
    result = curate([{"name": "Bat", "type": "Beast", "tags": [], "cr": 0.25}], register)
    assert len(result.kept) == 1
    assert result.kept[0]["name"] == "Bat"
