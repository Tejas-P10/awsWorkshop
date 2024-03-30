import streamlit as st
import psycopg2

# Function to establish connection with PostgreSQL database
def connect_to_db(host, dbname, user, password):
    conn = psycopg2.connect(
        host=host,
        database=dbname,
        user=user,
        password=password
    )
    return conn

# Function to create a table in the database if not exists
def create_table(conn):
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS content (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    cur.close()

# Function to insert content into the database
def insert_content(conn, name, content):
    cur = conn.cursor()
    cur.execute("INSERT INTO content (name, content) VALUES (%s, %s)", (name, content))
    conn.commit()
    cur.close()

# Function to fetch all content from the database
def fetch_all_content(conn):
    cur = conn.cursor()
    cur.execute("SELECT name, content FROM content")
    rows = cur.fetchall()
    cur.close()
    return rows

def main():
    st.title("Database Service Tester")

    # Input fields for database connection
    host = st.text_input("Enter Host URL", key = "host")
    dbname = st.text_input("Enter Database Name", key = "dbname")
    user = st.text_input("Enter User", key = "user")
    password = st.text_input("Enter Password", type="password", key = "password")

    # Connect to the database
    if host and dbname and user and password:
        conn = connect_to_db(host, dbname, user, password)
        create_table(conn)


        # Input boxes for name and content to be inserted into the database
        name = st.text_input("Enter Name")
        content = st.text_area("Enter Content")

        # Button to commit content to the database
        if st.button("Commit to Database"):
            if name and content:
                insert_content(conn, name, content)
                st.success("Content committed successfully!")

        # Button to fetch all content from the database
        if st.button("Fetch All Content"):
            rows = fetch_all_content(conn)
            if rows:
                st.write("Content in the Database:")
                for row in rows:
                    st.write(f"Name: {row[0]}, Content: {row[1]}")
            else:
                st.write("No content found in the database.")

if __name__ == "__main__":
    main()
