BASE_PRICE = {"adult": 300, "student": 150, "child": 100, "senior": 200}


def ticket_price(category, age, day, with_guided_tour):
    if category not in BASE_PRICE:
        raise ValueError("unknown category")
    if age < 0:
        raise ValueError("invalid age")
    if age < 5:
        return 0
    price = BASE_PRICE[category]
    if day == "monday":
        price = price // 2
    elif day in ("saturday", "sunday"):
        price += 50
    if with_guided_tour:
        if category == "student":
            price += 50
        else:
            price += 100
    return price


def group_discount(group_size, is_school):
    if group_size < 1:
        raise ValueError("invalid group size")
    if is_school:
        if group_size >= 20:
            return 40
        return 25
    if group_size >= 15:
        return 20
    elif group_size >= 8:
        return 10
    return 0


def gallery_entry(visitors_inside, capacity, has_timed_slot):
    if visitors_inside >= capacity:
        return "wait"
    if visitors_inside * 10 >= capacity * 9 and not has_timed_slot:
        return "queue"
    return "enter"
