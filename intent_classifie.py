import re

def classify_intent(nl_query: str) -> str:
    nl_query = nl_query.lower()

    if re.search(r'\b(average|mean)\b.*\b(grade|score)\b', nl_query):
        return "average_query"
    
    elif re.search(r'\bperformance score\b', nl_query):
        return "performance_query"
    
    elif re.search(r'\b(bar (graph|chart))\b', nl_query):
        return "plot_bar"
    
    elif re.search(r'\b(line (graph|chart))\b', nl_query):
        return "plot_line"
    
    elif re.search(r'\b(pie chart|distribution|proportion)\b', nl_query):
        return "plot_pie"
    
    elif re.search(r'\btop\s+\d+|\bbest\b', nl_query):
        return "top_n_query"
    
    elif re.search(r'\b(filter|greater than|less than|above|below|more than|under)\b', nl_query):
        return "conditional_query"
    
    elif re.search(r'\b(show|list|get|display)\b.*\b(student|students|names)\b', nl_query):
        return "list_students"

    elif re.search(r'\b(show|display|get|list)\b.*\b(table|all data|everything|all)\b', nl_query):
        return "show_table"

    # NEW: Detect insert intent keywords
    elif re.search(r'\b(add|insert|create|new|register)\b.*\b(student|entry|record)\b', nl_query):
        return "insert_query"

    else:
        return "unknown"
