import ply.lex as lex
import ply.yacc as yacc
import pandas as pd
import matplotlib.pyplot as plt  # Keep for plotting if needed later

# ------------------ Lexical Analysis ------------------

tokens = (
    'SELECT', 'FROM', 'WHERE', 'PLOT', 'BAR', 'GRAPH', 'LINE', 'PIE', 'CHART',
    'IDENTIFIER', 'NUMBER', 'STRING', 'COMMA', 'GREATER_THAN', 'LESS_THAN', 'EQUALS', 'ASTERISK', 'SEMICOLON',
    'LPAREN', 'RPAREN', 'AVG', 'GROUP', 'BY', 'ORDER', 'LIMIT', 'ASC', 'DESC', 'LIKE',
    'CUSTOM_METRIC', 'ENDS', 'WITH',
    'INSERT', 'DELETE'
)

reserved = {
    'SELECT': 'SELECT', 'FROM': 'FROM', 'WHERE': 'WHERE',
    'PLOT': 'PLOT', 'BAR': 'BAR', 'GRAPH': 'GRAPH',
    'LINE': 'LINE', 'PIE': 'PIE', 'CHART': 'CHART',
    'AVG': 'AVG', 'GROUP': 'GROUP', 'BY': 'BY',
    'ORDER': 'ORDER', 'LIMIT': 'LIMIT', 'ASC': 'ASC', 'DESC': 'DESC',
    'CUSTOM_METRIC': 'CUSTOM_METRIC',
    'LIKE': 'LIKE',
    'ENDS': 'ENDS',
    'WITH': 'WITH',
    'INSERT': 'INSERT',
    'DELETE': 'DELETE'
}

t_SELECT = r'SELECT'
t_FROM = r'FROM'
t_WHERE = r'WHERE'
t_PLOT = r'PLOT'
t_BAR = r'BAR'
t_GRAPH = r'GRAPH'
t_LINE = r'LINE'
t_PIE = r'PIE'
t_CHART = r'CHART'
t_AVG = r'AVG'
t_GROUP = r'GROUP'
t_BY = r'BY'
t_ORDER = r'ORDER'
t_LIMIT = r'LIMIT'
t_ASC = r'ASC'
t_DESC = r'DESC'
t_CUSTOM_METRIC = r'CUSTOM_METRIC'
t_LIKE = r'LIKE'
t_ENDS = r'ENDS'
t_WITH = r'WITH'
t_INSERT = r'INSERT'
t_DELETE = r'DELETE'
t_COMMA = r','
t_GREATER_THAN = r'>'
t_LESS_THAN = r'<'
t_EQUALS = r'='
t_ASTERISK = r'\*'
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ignore = ' \t'

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value.upper(), 'IDENTIFIER')
    return t

def t_STRING(t):
    r'(\"([^\\\"]|\\.)*\")|(\'([^\\\']|\\.)*\')'
    t.value = t.value[1:-1]  # strip quotes
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    if t.value[0] in ['\n', '\r']:
        t.lexer.skip(1)
    else:
        print(f"Illegal character: {t.value[0]}")
        t.lexer.skip(1)

lexer = lex.lex()

# ------------------ Parser ------------------

def p_query(p):
    '''query : select_query
             | insert_query
             | delete_query'''
    p[0] = p[1]

def p_select_query(p):
    '''select_query : SELECT select_list FROM IDENTIFIER where_clause group_by_clause plot_clause order_clause limit_clause SEMICOLON'''
    p[0] = ('SELECT', p[2], p[4], p[5], p[6], p[7], p[8], p[9], p[10])

def p_insert_query(p):
    '''insert_query : INSERT insert_items SEMICOLON'''
    p[0] = ('INSERT', p[2])

def p_insert_items(p):
    '''insert_items : insert_item COMMA insert_items
                    | insert_item'''
    if len(p) == 4:
        # Merge dictionaries with right precedence (later keys override)
        p[0] = {**p[3], **p[1]}
    else:
        p[0] = p[1]

def p_insert_item(p):
    '''insert_item : IDENTIFIER EQUALS value'''
    p[0] = {p[1]: p[3]}

def p_delete_query(p):
    '''delete_query : DELETE where_clause SEMICOLON'''
    p[0] = ('DELETE', p[2])

def p_value(p):
    '''value : NUMBER
             | STRING'''
    p[0] = p[1]

def p_select_list(p):
    '''select_list : ASTERISK
                   | expression COMMA select_list
                   | expression'''
    if p[1] == '*':
        p[0] = ['*']
    elif len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_expression(p):
    '''expression : IDENTIFIER
                  | function_call
                  | avg_function
                  | custom_metric'''
    p[0] = p[1]

def p_function_call(p):
    '''function_call : IDENTIFIER LPAREN arg_list RPAREN'''
    p[0] = ('FUNC_CALL', p[1], p[3])

def p_avg_function(p):
    '''avg_function : AVG LPAREN IDENTIFIER RPAREN'''
    p[0] = ('AVG', p[3])

def p_custom_metric(p):
    '''custom_metric : CUSTOM_METRIC LPAREN IDENTIFIER COMMA arg_list RPAREN'''
    metric_name = p[3].upper()
    p[0] = ('CUSTOM_METRIC', metric_name, *p[5])

def p_arg_list(p):
    '''arg_list : IDENTIFIER COMMA arg_list
                | IDENTIFIER'''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]

def p_where_clause(p):
    '''where_clause : WHERE condition
                    | empty'''
    p[0] = ('WHERE', p[2]) if len(p) == 3 else None

def p_condition(p):
    '''condition : IDENTIFIER GREATER_THAN NUMBER
                 | IDENTIFIER LESS_THAN NUMBER
                 | IDENTIFIER EQUALS STRING
                 | IDENTIFIER LIKE STRING
                 | IDENTIFIER EQUALS NUMBER
                 | IDENTIFIER ENDS WITH STRING'''
    if len(p) == 4:
        p[0] = ('CONDITION', p[1], p[2], p[3])
    else:
        # ENDS WITH case (5 tokens)
        p[0] = ('CONDITION', p[1], 'ENDS WITH', p[4])

def p_group_by_clause(p):
    '''group_by_clause : GROUP BY IDENTIFIER
                       | empty'''
    p[0] = ('GROUP BY', p[3]) if len(p) == 4 else None

def p_order_clause(p):
    '''order_clause : ORDER BY IDENTIFIER order_direction
                    | empty'''
    if len(p) == 5:
        p[0] = ('ORDER BY', p[3], p[4])
    else:
        p[0] = None

def p_order_direction(p):
    '''order_direction : ASC
                       | DESC'''
    p[0] = p[1]

def p_limit_clause(p):
    '''limit_clause : LIMIT NUMBER
                    | empty'''
    if len(p) == 3:
        p[0] = ('LIMIT', p[2])
    else:
        p[0] = None

def p_plot_clause(p):
    '''plot_clause : PLOT BAR GRAPH
                   | PLOT LINE GRAPH
                   | PLOT PIE CHART
                   | empty'''
    p[0] = ('PLOT', p[2]) if len(p) == 4 else None

def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type} ('{p.value}')")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

# ------------------ Data and Execution ------------------

# Sample DataFrame simulating a table named "students"
df_students = pd.DataFrame({
    'id': [1, 2, 3, 4],
    'name': ['Aarav Choudhary', 'Rohan Sharma', 'Meera Choudhary', 'Ishita Gupta']
})

def evaluate_condition(df, condition):
    """Filter DataFrame based on simple condition tuples."""
    col, op, val = condition[1], condition[2], condition[3]
    if op == '=':
        return df[df[col] == val]
    elif op == '>':
        return df[df[col] > val]
    elif op == '<':
        return df[df[col] < val]
    elif op == 'LIKE':
        pattern = val.replace('%', '.*')
        return df[df[col].str.match(pattern)]
    elif op == 'ENDS WITH':
        return df[df[col].str.endswith(val)]
    else:
        print(f"Unsupported operator {op}")
        return df

def process_query(parsed):
    global df_students  # Declare once at the start

    if parsed[0] == 'SELECT':
        # Unpack 9 elements from parsed tuple (including semicolon at the end)
        _, select_list, table_name, where_clause, group_by, plot, order_by, limit, _ = parsed
        df = df_students if table_name == 'students' else pd.DataFrame()

        # WHERE filtering
        if where_clause and where_clause[1]:
            df = evaluate_condition(df, where_clause[1])

        # SELECT columns (handle '*')
        if select_list == ['*']:
            selected_df = df
        else:
            columns = []
            for item in select_list:
                if isinstance(item, tuple) and item[0] == 'AVG':
                    # For now, skip aggregate processing (can be added later)
                    continue
                elif isinstance(item, tuple) and item[0] == 'FUNC_CALL':
                    # For now, skip function calls (can be added later)
                    continue
                else:
                    columns.append(item)
            selected_df = df[columns] if columns else df

        # TODO: Implement GROUP BY, ORDER BY, LIMIT, and PLOT if needed
        print(selected_df)

    elif parsed[0] == 'INSERT':
        data_to_insert = parsed[1]
        # Append new data row to df_students
        df_students = pd.concat([df_students, pd.DataFrame([data_to_insert])], ignore_index=True)
        print("Inserted:", data_to_insert)

    elif parsed[0] == 'DELETE':
        where_clause = parsed[1]
        if where_clause and where_clause[1]:
            filtered_df = evaluate_condition(df_students, where_clause[1])
            to_delete_ids = filtered_df.index
            df_students = df_students.drop(to_delete_ids).reset_index(drop=True)
            print(f"Deleted rows matching condition: {where_clause[1]}")

# ------------------ Testing the Combined Parser ------------------

if __name__ == "__main__":
    sql_example = '''
    SELECT name FROM students WHERE name ENDS WITH "Gupta";
    '''

    result = parser.parse(sql_example)
    print("Parsed:", result)
    process_query(result)

    sql_insert = '''
    INSERT id=5, name="Karan Singh";
    '''
    result = parser.parse(sql_insert)
    print("Parsed:", result)
    process_query(result)

    sql_delete = '''
    DELETE WHERE name = "Karan Singh";
    '''
    result = parser.parse(sql_delete)
    print("Parsed:", result)
    process_query(result)
