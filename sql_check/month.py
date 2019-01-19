from datetime import date

JANUARY = 1
DECEMBER = 12


def previous():
    """
    get the first day of the previous month
    :return: date object set at 1st day of previous month
    """
    today = date.today()

    result_month = today.month - 1 if today.month is not JANUARY else DECEMBER
    result_year = today.year if today.month is not JANUARY else today.year - 1

    return today.replace(year=result_year, month=result_month, day=1)


def from_str(year_month):
    """
    get the first day of the month represented by year_month
    :param year_month: four first characters are the year and last two the month; "201901" is Jan 2019
    :type year_month: str
    :return: date object set the the 1st day of specified month
    """
    year = int(year_month[:4])
    month = int(year_month[4:])

    return date(year, month, 1)
