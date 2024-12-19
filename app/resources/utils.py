import sqlalchemy


def validate_limit_param(limit):
    # Validate `limit`
    if limit is not None and not isinstance(limit, int):
        raise TypeError(f"'limit' must be an integer or None, got {type(limit).__name__}")

    return True

def validate_order_by_param(order_by):
    # Validate `order_by`
    if order_by is not None and not isinstance(order_by, sqlalchemy.sql.elements.ClauseElement):
        raise TypeError(f"'order_by' must be a SQLAlchemy column or expression, got {type(order_by).__name__}")

    return True
