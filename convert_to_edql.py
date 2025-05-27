from matcher_utils import extract_entities

def convert_entities_to_edsql(nl_query, intent=None):
    entities = extract_entities(nl_query)

    column = entities.get("column")           # e.g., "grades", "attendance", "name"
    operator = entities.get("operator")       # e.g., ">", "<", "="
    value = entities.get("value")             # e.g., 80, "a"
    agg = entities.get("aggregation")         # e.g., "AVG", "SUM"
    group_by = entities.get("group_by")
    plot = entities.get("plot")
    x = entities.get("x")
    y = entities.get("y")
    order = entities.get("order")
    limit = entities.get("limit")
    custom = entities.get("custom_metric")

    if operator: operator = operator.upper()
    if order: order = order.upper()

    nl_query_lower = nl_query.lower()

    # Check if user explicitly asked for 'name'
    wants_name = 'name' in nl_query_lower

    # Handle LIKE operator based on natural language clues
    if column == 'name':
        if 'start with' in nl_query_lower:
            # Extract letter after 'start with'
            idx = nl_query_lower.find('start with') + len('start with')
            letter = nl_query_lower[idx:].strip().split()[0]
            pattern = f"'{letter}%'"
            return f"SELECT name FROM students WHERE name LIKE {pattern};"

        elif 'end with' in nl_query_lower:
            idx = nl_query_lower.find('end with') + len('end with')
            letter = nl_query_lower[idx:].strip().split()[0]
            pattern = f"'%{letter}'"
            return f"SELECT name FROM students WHERE name LIKE {pattern};"

        elif 'contains' in nl_query_lower:
            idx = nl_query_lower.find('contains') + len('contains')
            substr = nl_query_lower[idx:].strip().split()[0]
            pattern = f"'%{substr}%'"
            return f"SELECT name FROM students WHERE name LIKE {pattern};"

    # Plot query (x, y, plot type)
    if plot and x and y:
        return f"SELECT {x}, {y} FROM students PLOT {plot} GRAPH;"

    # Aggregation with GROUP BY
    if agg and column and group_by:
        return f"SELECT {agg}({column}) FROM students GROUP BY {group_by};"

    # Custom metric with WHERE
    if custom and operator and value is not None:
        cols = "name, " if wants_name else ""
        return f"SELECT {cols}CUSTOM_METRIC({custom}, grades, attendance) FROM students WHERE {custom} {operator} {value};"

    # Custom metric with ORDER and LIMIT
    if custom and order and limit is not None:
        cols = "name, " if wants_name else ""
        return f"SELECT {cols}CUSTOM_METRIC({custom}, grades, attendance) FROM students ORDER BY {custom} {order} LIMIT {limit};"

    # Simple custom metric
    if custom:
        cols = "name, " if wants_name else ""
        return f"SELECT {cols}CUSTOM_METRIC({custom}, grades, attendance) FROM students;"

    # Filtered WHERE clause
    if column and operator and value is not None:
        cols = f"{column}"
        if wants_name:
            cols = f"name, {column}"
        return f"SELECT {cols} FROM students WHERE {column} {operator} {value};"

    # ORDER BY with column
    if column and order and limit is not None:
        cols = f"{column}"
        if wants_name:
            cols = f"name, {column}"
        return f"SELECT {cols} FROM students ORDER BY {column} {order} LIMIT {limit};"

    # Only column requested (no filters)
    if column:
        cols = f"{column}"
        if wants_name:
            cols = f"name, {column}"
        return f"SELECT {cols} FROM students;"

    # Default fallback
    if wants_name:
        return "SELECT name FROM students;"

    return None
