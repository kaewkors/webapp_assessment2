import connect, psycopg2
print("import done - establishing connection")
conn = psycopg2.connect(dbname=connect.dbname, user=connect.dbuser, \
     password=connect.dbpass, host=connect.dbhost, port=connect.dbport)
print(f"connection done - {conn}")
with conn:
    cur = conn.cursor()
    cur.execute("select * from categories;")
    select_result = cur.fetchall()
    print(f"{select_result[0]}")
    # print(select_result)
    # print(type(select_result)) # type=list
#     for result in select_result:
          # print(f"{result}")
          # print(type(result)) # type=tuple
               # for entry in result:
               #      print(f"{type(entry)} - {entry}")