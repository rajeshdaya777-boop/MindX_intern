import mysql.connector

def connect_to_database():
  connection = mysql.connector.connect(
            host='HOST',
            database='DATABASE',
            user='USER',
            password='PASSWORD'
        )
  return connection
print(connect_to_database)
def get_table_names(conn):
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    tables = [table[0] for table in cursor.fetchall()]
    return tables

def get_column_names(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"DESCRIBE {table_name};")
    columns = [column[0] for column in cursor.fetchall()]
    return columns

def get_database_info(conn):
    table_dicts = []
    table_names = get_table_names(conn)
    for table_name in table_names:
        columns_names = get_column_names(conn, table_name)
        table_dicts.append({"table_name": table_name, "column_names": columns_names})
    return table_dicts
conn = connect_to_database()
database_schema_dict = get_database_info(conn)
database_schema_string = "\n".join(
    [
        f"Table: {table['table_name']}\nColumns: {', '.join(table['column_names'])}"
        for table in database_schema_dict
    ]
)
print(database_schema_string)
tools = [
    {
        "type": "function",
        "function": {
            "name": "ask_database",
            "description": "Use this function to answer user questions about music. Input should be a fully formed SQL query.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": f"""
                                SQL query extracting info to answer the user's question.
                                SQL should be written using this database schema:
                                {database_schema_string}
                                The query should be returned in plain text, not in JSON.
                                """,
                    }
                },
                "required": ["query"],
            },
        }
    }
]
def ask_database(conn, query):
    """Function to query SQLite database with a provided SQL query."""
    try:
        results = str(conn.execute(query).fetchall())
    except Exception as e:
        results = f"query failed with error: {e}"
    return results
# Prompt with content that may result in function call. In this case the model can identify the information requested by the user is potentially available in the database schema passed to the model in Tools description.
messages = [{
    "role": "user",
    "content": "What is the the total sales order?"
}]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

# Append the message to messages list
response_message = response.choices[0].message
messages.append(response_message)

print(response_message)

#determine if the response from the model includes a tool call.
tool_calls = response_message.tool_calls
if tool_calls:
    # If true the model will return the name of the tool / function to call and the argument(s)
    tool_call_id = tool_calls[0].id
    tool_function_name = tool_calls[0].function.name
    tool_query_string = json.loads(tool_calls[0].function.arguments)['query']

    #ONLY PRINT THE GENERATED SQL QUERY (No execution)
    print("Generated SQL Query:\n", tool_query_string)

else:
    # Model did not identify a function to call, result can be returned to the user
    print("No SQL query generated. Model response:\n", response_message.content)
