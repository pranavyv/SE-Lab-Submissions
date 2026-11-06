from hypothesis import given, strategies as st
from museum_admission_parser import format_visitor_name, parse_group_ages, parse_visit_date


@given(st.text() | st.none())
def test_format_visitor_name_no_crash(s):
    try:
        result = format_visitor_name(s)
    except Exception as e:
        assert False, f"format_visitor_name crashed with: {e!r} on input {s!r}"
    assert isinstance(result, str)


@given(st.text() | st.none())
def test_parse_group_ages_no_crash(s):
    try:
        result = parse_group_ages(s)
    except Exception as e:
        assert False, f"parse_group_ages crashed with: {e!r} on input {s!r}"
    assert isinstance(result, list)
    assert all(isinstance(a, int) and 0 <= a <= 150 for a in result)


@given(st.text() | st.none())
def test_parse_visit_date_no_crash(s):
    try:
        result = parse_visit_date(s)
    except Exception as e:
        assert False, f"parse_visit_date crashed with: {e!r} on input {s!r}"
    assert result is None or (
        isinstance(result, tuple) and len(result) == 3
        and all(isinstance(x, int) for x in result)
    )
