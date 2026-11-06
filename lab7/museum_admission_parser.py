import datetime

MAX_AGE = 150


def format_visitor_name(name):
    """
    Formats a full name as 'Surname, Given names' for the ticket.
    Returns '' for non-string or blank input, and just the name when
    only one word is given.
    """
    if not isinstance(name, str):
        return ""
    parts = name.split()
    if not parts:
        return ""
    if len(parts) == 1:
        return parts[0].title()
    return parts[-1].title() + ', ' + ' '.join(parts[:-1]).title()


def parse_group_ages(text):
    """
    Parses space-separated ages into a list of ints.
    Non-string input gives []. Tokens that are not plain whole numbers
    in the range 0-150 are skipped.
    """
    if not isinstance(text, str):
        return []
    ages = []
    for token in text.split():
        # isascii() + isdigit() rejects '-5', '3.5', 'abc', '1_0' and
        # Unicode digits such as '٣' that int() would otherwise accept.
        if token.isascii() and token.isdigit() and len(token) <= 3:
            age = int(token)
            if age <= MAX_AGE:
                ages.append(age)
    return ages


def parse_visit_date(text):
    """
    Parses a YYYY-MM-DD date into a (year, month, day) tuple.
    Returns None if the input is not a string or not a real calendar date.
    """
    if not isinstance(text, str):
        return None
    parts = text.strip().split('-')
    if len(parts) != 3:
        return None
    year, month, day = parts
    if not all(p.isascii() and p.isdigit() for p in parts):
        return None
    if len(year) != 4 or len(month) > 2 or len(day) > 2:
        return None
    try:
        datetime.date(int(year), int(month), int(day))
    except ValueError:
        return None
    return int(year), int(month), int(day)


def main():
    print("==== Running format_visitor_name ====")
    value = input("Enter a visitor's full name (e.g. asha rao): ")
    print("Name on ticket:", format_visitor_name(value) or "Invalid name")

    print("\n==== Running parse_group_ages ====")
    value = input("Enter the ages in the group separated by spaces (e.g. 34 12 70): ")
    print("Group ages:", parse_group_ages(value))

    print("\n==== Running parse_visit_date ====")
    value = input("Enter the visit date as YYYY-MM-DD (e.g. 2026-11-05): ")
    date = parse_visit_date(value)
    print("Visit date (year, month, day):", date if date else "Invalid date")

if __name__ == "__main__":
    main()
