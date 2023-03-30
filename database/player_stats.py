import sqlite3

player_stats = sqlite3.connect("player_stats")

#Create table
# e.g of table_fields: id INTEGER PRIMARY KEY, author STRING, book STRING
def create(table_name, table_fields):
  player_stats.execute("CREATE TABLE IF NOT EXISTS",table_name," (",table_fields,");")
  print("CREATE TABLE IF NOT EXISTS",table_name," (",table_fields,");")
  commit()
  
# # Perform CRUD operations

# # Insert
  # e.g of table_values: 1, 'Steve Biko','I write what I like.'
  def insert(table_name, table_values):
    player_stats.execute("INSERT INTO" ,table_name,"VALUES (", table_values,")")
    print("INSERT INTO" ,table_name,"VALUES (", table_values,")")
    commit()
    
# # Read
def read(table_fields, table_name):
  cursor_object = player_stats.execute("SELECT",table_fields, "FROM", table_name)
  print("SELECT",table_fields, "FROM", table_name)
  print(cursor_object.fetchall())
  return cursor_object.fetchall()

# # Update
# e.g set_field: book = 'I WRITE WHAT I LIKE'
# e.g where_field: id = 1
def update(table_name, set_field, where_field):
  player_stats.execute("UPDATE", table_name, "SET", set_field, "WHERE", where_field)
  print("UPDATE", table_name, "SET", set_field, "WHERE", where_field)
  commit()
  
# # Delete
# e.g where_field: id = 1
def delete(table_name, where_field):
  player_stats.execute("DELETE from", table_name, "WHERE", where_field)
  print("DELETE from", table_name, "WHERE", where_field)
  commit()
# connection.execute("DELETE from My_library WHERE id = 1;")

# # Commit changes
def commit():
  player_stats.commit()

# # Close the connection
#consider adding to end of scripts?
def close_db():
  player_stats.close()