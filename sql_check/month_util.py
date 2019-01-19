from datetime import date

JANUARY = 1
DECEMBER = 12


def previous_month():
    """
    get the first day of the previous month
    :return: date object set at 1st day of previous month
    """
    today = date.today()

    result_month = today.month - 1 if today.month is not JANUARY else DECEMBER
    result_year = today.year if today.month is not JANUARY else today.year - 1

    return today.replace(year=result_year, month=result_month, day=1)


def month_from_str(year_month):
    """
    get the first day of the month represented by year_month
    :param year_month: str which four first characters are the year and last two the month; "201901" is Jan 2019
    :return: date object set the the 1st day of specified month
    """
    return None
