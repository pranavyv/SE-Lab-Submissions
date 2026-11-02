"""Lab 6 - Step 7: tests written to reach >= 90% BRANCH coverage (aiming for 100%).

Every decision is exercised both ways, including boundary values.
"""
import pytest
from museum_admission import ticket_price, group_discount, gallery_entry


# ---------- ticket_price ----------
@pytest.mark.parametrize("category,base", [
    ("adult", 300), ("student", 150), ("child", 100), ("senior", 200),
])
def test_every_category_on_weekday(category, base):
    assert ticket_price(category, 30, "tuesday", False) == base


def test_unknown_category():
    with pytest.raises(ValueError, match="unknown category"):
        ticket_price("alien", 30, "tuesday", False)


def test_negative_age():
    with pytest.raises(ValueError, match="invalid age"):
        ticket_price("adult", -1, "tuesday", False)


def test_age_zero_is_free_not_invalid():
    assert ticket_price("adult", 0, "tuesday", False) == 0


def test_age_four_free_boundary():
    assert ticket_price("adult", 4, "tuesday", True) == 0


def test_age_five_pays_boundary():
    assert ticket_price("adult", 5, "tuesday", False) == 300


def test_monday_half_price():
    assert ticket_price("adult", 30, "monday", False) == 150


@pytest.mark.parametrize("day", ["saturday", "sunday"])
def test_weekend_surcharge(day):
    assert ticket_price("adult", 30, day, False) == 350


@pytest.mark.parametrize("day", ["tuesday", "friday"])
def test_other_weekdays_no_change(day):
    assert ticket_price("adult", 30, day, False) == 300


def test_no_guided_tour():
    assert ticket_price("student", 20, "tuesday", False) == 150


def test_student_guided_tour():
    assert ticket_price("student", 20, "tuesday", True) == 200


@pytest.mark.parametrize("category,expected", [
    ("adult", 400), ("child", 200), ("senior", 300),
])
def test_non_student_guided_tour(category, expected):
    assert ticket_price(category, 30, "tuesday", True) == expected


def test_monday_with_guided_tour():
    assert ticket_price("adult", 30, "monday", True) == 250


def test_weekend_student_guided_tour():
    assert ticket_price("student", 20, "sunday", True) == 250


# ---------- group_discount ----------
def test_invalid_group_size_zero():
    with pytest.raises(ValueError, match="invalid group size"):
        group_discount(0, False)


def test_invalid_group_size_negative_school():
    with pytest.raises(ValueError, match="invalid group size"):
        group_discount(-3, True)


def test_minimum_valid_group():
    assert group_discount(1, False) == 0


@pytest.mark.parametrize("size,expected", [(19, 25), (20, 40), (50, 40), (1, 25)])
def test_school_groups(size, expected):
    assert group_discount(size, True) == expected


@pytest.mark.parametrize("size,expected", [
    (7, 0), (8, 10), (14, 10), (15, 20), (40, 20),
])
def test_general_groups(size, expected):
    assert group_discount(size, False) == expected


# ---------- gallery_entry ----------
def test_gallery_full_wait():
    assert gallery_entry(100, 100, False) == "wait"


def test_gallery_over_capacity_wait():
    assert gallery_entry(120, 100, True) == "wait"


def test_gallery_near_full_no_slot_queue():
    assert gallery_entry(90, 100, False) == "queue"


def test_gallery_near_full_with_slot_enter():
    assert gallery_entry(90, 100, True) == "enter"


def test_gallery_just_below_threshold_enter():
    assert gallery_entry(89, 100, False) == "enter"


def test_gallery_empty_enter():
    assert gallery_entry(0, 100, False) == "enter"
