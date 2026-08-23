from datetime import date, datetime, timedelta


def easter_sunday(year):
    """Berechnet den Ostersonntag nach dem Gauß-Algorithmus."""
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return date(year, month, day)


def solothurn_bankholidays(year):
    """Gesetzliche Feiertage im Kanton Solothurn."""

    easter = easter_sunday(year)

    bankHoliday = {
        date(year, 1, 1),  # Neujahr
        date(year, 1, 2),  # Berchtoldstag
        easter - timedelta(days=2),  # Karfreitag
        easter + timedelta(days=1),  # Ostermontag
        date(year, 5, 1),  # Tag der Arbeit
        easter + timedelta(days=39),  # Auffahrt
        easter + timedelta(days=50),  # Pfingstmontag
        easter + timedelta(days=60),  # Fronleichnam
        date(year, 8, 1),  # Bundesfeier
        date(year, 8, 15),  # Mariä Himmelfahrt
        date(year, 11, 1),  # Allerheiligen
        date(year, 12, 25),  # Weihnachten
        date(year, 12, 26),  # Stephanstag
    }

    return bankHoliday


def expected_hours(start_date, end_date, PENSUM):
    # -----------------------------------
    # Sollzeit berechnen
    # Referenz: 42h Arbeitszeit pro Woche bei 100% beinhaltet 30min bezahlte Pause pro Tag (Referenz: Mitarbeiterhandbuch V2.2)
    # -----------------------------------

    TARGET_HOURS_PER_DAY = 42 / 5
    working_days = 0  # Variable initialisieren
    all_bankholidays = set()
    bankholiday_days = set()

    start = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%SZ")
    end = datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%SZ")

    for year in range(start.year, end.year + 1):
        all_bankholidays.update(solothurn_bankholidays(year))

    for day_offset in range((end.date() - start.date()).days + 1):
        current_date = (start + timedelta(days=day_offset)).date()

        # Montag = 0 ... Freitag = 4
        if current_date.weekday() < 5:  # and current_date not in holidays:
            working_days += 1
            if current_date in all_bankholidays:
                bankholiday_days.add(current_date)

    target_hours = working_days * TARGET_HOURS_PER_DAY * PENSUM / 100

    # Feiertage gewichten:
    # Tag der Arbeit = 0.5 Tag
    # Alle anderen Feiertage = 1.0 Tag
    bankholiday_factor = sum(
        0.5 if day.month == 5 and day.day == 1 else 1.0 for day in bankholiday_days
    )

    target_bankHoliday_hours = bankholiday_factor * TARGET_HOURS_PER_DAY * PENSUM / 100

    return target_hours, target_bankHoliday_hours
