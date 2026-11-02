"""Lab 6 - Step 5: tests written to reach >= 90% LINE (code) coverage."""
import pytest
from museum_admission import ticket_price, group_discount, gallery_entry


# ---------- ticket_price ----------
def test_adult_weekday():
    assert ticket_price("adult", 30, "tuesday", False) == 300


def test_unknown_category():
    with pytest.raises(ValueError, match="unknown category"):
        ticket_price("alien", 30, "tuesday", False)


def test_negative_age():
    with pytest.raises(ValueError, match="invalid age"):
        ticket_price("adult", -1, "tuesday", False)


def test_under_five_free():
    assert ticket_price("child", 3, "tuesday", False) == 0


def test_monday_half_price():
    assert ticket_price("adult", 30, "monday", False) == 150


def test_weekend_surcharge():
    assert ticket_price("adult", 30, "saturday", False) == 350


def test_student_guided_tour():
    assert ticket_price("student", 20, "tuesday", True) == 200


def test_adult_guided_tour():
    assert ticket_price("adult", 30, "tuesday", True) == 400


# ---------- group_discount ----------
def test_small_group():
    assert group_discount(4, False) == 0


def test_invalid_group_size():
    with pytest.raises(ValueError, match="invalid group size"):
        group_discount(0, False)


def test_large_school_group():
    assert group_discount(25, True) == 40


def test_small_school_group():
    assert group_discount(10, True) == 25


def test_large_general_group():
    assert group_discount(20, False) == 20


def test_medium_general_group():
    assert group_discount(10, False) == 10


# ---------- gallery_entry ----------
def test_gallery_full():
    assert gallery_entry(100, 100, False) == "wait"


def test_gallery_queue():
    assert gallery_entry(90, 100, False) == "queue"


def test_gallery_enter():
    assert gallery_entry(10, 100, False) == "enter"
