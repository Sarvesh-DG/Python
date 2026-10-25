import mysql.connector as m

def fetch_employees(batch_size=1000):
    con=m.connect(
        host="localhost",
        user="root",
        passwd="root",
        database="employees"
    )
    try:
        cur=con.cursor()
        cur.execute("Select * from employees")

        while True:
            row=cur.fetchmany(batch_size)

            if not row:
                break
            for i in row:
                yield i
    finally:
        
        cur.close()
        con.close()

for employee in fetch_employees():
    print(employee)