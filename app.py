from flask import Flask, render_template, request
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-GUI backend for plotting
import matplotlib.pyplot as plt
import io
import base64

from edsql_compiler import parser
from convert_to_edsql import convert_entities_to_edsql
from intent_classifier import classify_intent

app = Flask(__name__)

# Load dataset once at startup
df = pd.read_csv("students.csv")


def execute_query(parsed_query):
    """Execute the parsed EDSQL query."""
    try:
        _, select_list, table, where_clause, group_by_clause, plot_clause, order_clause, limit_clause, _ = parsed_query
    except ValueError:
        return "Invalid parsed query format."

    result = df.copy()

    # WHERE clause
    if where_clause:
        try:
            column, op, value = where_clause[1][1:]  # Unpack CONDITION tuple

            if op == 'LIKE':
                pattern = '^' + value.replace('%', '.*') + '$'
                result = result[result[column].str.match(pattern, case=False, na=False)]
            else:
                if pd.api.types.is_numeric_dtype(result[column]):
                    value = float(value)
                else:
                    value = str(value)

                if op == '>':
                    result = result[result[column] > value]
                elif op == '<':
                    result = result[result[column] < value]
                elif op == '=':
                    result = result[result[column] == value]

        except Exception as e:
            return f"Error in WHERE clause: {e}"

    # GROUP BY and Aggregation
    if group_by_clause:
        try:
            group_col = group_by_clause[1]
            if isinstance(select_list[0], tuple) and select_list[0][0] == 'AVG':
                result = result.groupby(group_col)[select_list[0][1]].mean().reset_index()
        except Exception as e:
            return f"Error in GROUP BY clause: {e}"

    # Aggregation without GROUP BY
    elif any(isinstance(sel, tuple) and sel[0] == 'AVG' for sel in select_list):
        try:
            agg_results = {}
            for sel in select_list:
                if isinstance(sel, tuple) and sel[0] == 'AVG':
                    agg_results[sel[1]] = [result[sel[1]].mean()]
                elif isinstance(sel, str):
                    agg_results[sel] = [result[sel].iloc[0]]
            result = pd.DataFrame(agg_results)
        except Exception as e:
            return f"Error processing aggregation without GROUP BY: {e}"

    # ORDER BY
    if order_clause:
        try:
            _, order_col, order_dir = order_clause
            result = result.sort_values(by=order_col, ascending=(order_dir.upper() == 'ASC'))
        except Exception as e:
            return f"Error in ORDER BY clause: {e}"

    # LIMIT
    if limit_clause:
        try:
            _, limit_val = limit_clause
            result = result.head(int(limit_val))
        except Exception as e:
            return f"Error in LIMIT clause: {e}"

    # Column selection (remove duplicates, preserve order)
    try:
        def unique_preserve_order(seq):
            seen = set()
            return [x for x in seq if not (x in seen or seen.add(x))]

        columns = [sel if isinstance(sel, str) else sel[1] for sel in select_list]
        columns = unique_preserve_order(columns)
        result = result[columns]
    except Exception as e:
        return f"Error selecting columns: {e}"

    return result


@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    sql_query = ""
    output = None
    graph = None

    if request.method == "POST":
        query = request.form.get("query", "").strip()

        if not query:
            output = "Please enter a valid query."
            return render_template("index.html", query=query, sql_query=sql_query, output=output, graph=graph)

        intent = classify_intent(query)

        # Show full table if intent is show_table
        if intent == "show_table":
            output = df.to_html(classes="table table-bordered")
            return render_template("index.html", query=query, sql_query="SELECT * FROM students;", output=output, graph=None)

        if "select" not in query.lower():
            sql_query = convert_entities_to_edsql(query, intent)
            if not sql_query:
                output = "Sorry, couldn't understand the NLP."
                return render_template("index.html", query=query, sql_query=sql_query, output=output, graph=graph)
        else:
            sql_query = query

        try:
            parsed = parser.parse(sql_query)
            if not parsed:
                output = "Error parsing the SQL query."
                return render_template("index.html", query=query, sql_query=sql_query, output=output, graph=graph)

            result = execute_query(parsed)

            if isinstance(result, str):
                output = result  # It's an error message
                return render_template("index.html", query=query, sql_query=sql_query, output=output, graph=graph)

            # Generate plot if requested
            plot_clause = parsed[5]
            if plot_clause:
                try:
                    plot_type = plot_clause[1]
                    fig, ax = plt.subplots()

                    if plot_type == "BAR":
                        result.plot(kind="bar", x=result.columns[0], y=result.columns[1], ax=ax)
                    elif plot_type == "LINE":
                        result.plot(kind="line", x=result.columns[0], y=result.columns[1], ax=ax)
                    elif plot_type == "PIE":
                        if result.shape[1] >= 2:
                            data = result.set_index(result.columns[0])[result.columns[1]]
                        else:
                            data = result[result.columns[0]].value_counts()
                        data.plot(kind="pie", ax=ax, autopct='%1.1f%%')
                        ax.set_ylabel("")

                    buf = io.BytesIO()
                    plt.savefig(buf, format="png")
                    buf.seek(0)
                    graph = base64.b64encode(buf.getvalue()).decode()
                    buf.close()
                    plt.close(fig)
                except Exception as e:
                    output = f"Error generating graph: {e}"
                    return render_template("index.html", query=query, sql_query=sql_query, output=output, graph=None)
            else:
                output = result.to_html(classes="table table-bordered")

        except Exception as e:
            output = f"Unexpected error: {e}"

    return render_template("index.html", query=query, sql_query=sql_query, output=output, graph=graph)


if __name__ == "__main__":
    app.run(debug=True)
