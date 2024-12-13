from datetime import datetime, timedelta

def calculate_next_date(date_string: str, date_format: str = "%Y-%m-%d") -> str:
    """
    calculates the next date given a date string and returns it in the same format.

    parameters:
    date_string (str): The starting date as a string.
    date_format (str): The format of the input date string (default: 'YYYY-MM-DD').

    Returns:
    str: The next date as a string in the same format.

    Raises:
    ValueError: If the input date is invalid or doesn't match the expected format.

    Example:
    calculate_next_date("2023-12-31")
    '2024-01-01'
    """
    try:
        # parse the input date
        given_date = datetime.strptime(date_string, date_format)
        # Add one day
        next_date = given_date + timedelta(days=1)
        # Return the next date in the same format
        return next_date.strftime(date_format)
    except ValueError as e:
        raise ValueError(f"Invalid date or format: {e}")

calculate_next_date("2020-10-12")