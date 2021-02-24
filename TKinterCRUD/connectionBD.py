import psycopg2 as ps
from psycopg2 import Error
import tkinter.messagebox as msg

def ConnectionBD():
    try:
        # Connect to an existing database
        connection = ps.connect(user="postgres",
                                    password="Jesucristo1020",
                                    host="127.0.0.1",
                                    port="5432",
                                    database="pythoncrud")
    except (Exception, Error) as error:            
        print("Error while connecting to PostgreSQL", error)
    return connection

def SaveEmployee(nameP,last_nameP,ageP,id = None,file = None,name_file=None):
        try:
            conn = ConnectionBD()
            cursor = conn.cursor()
            sql = ''
            if id =='':
                sql = 'INSERT INTO employees (full_name,last_name, age,file,name_file) VALUES (%s,%s,%s,%s,%s)'
            else:
                if Search_Employee(id):
                    sql = 'UPDATE employees SET full_name = %s, last_name = %s,age = %s WHERE id = %s'
            name = nameP
            last_name = last_nameP
            if not str(ageP).isnumeric():
                return
            age = int(ageP)                                   
            if not id == '':
                cursor.execute(sql,(name,last_name,age,id))
            else:
                cursor.execute(sql,(name,last_name,age,file,name_file))            
            conn.commit()
            msg.showinfo("Re5686gister","Employee was register succesfuly")
            return True
        except(Exception,ps.DatabaseError) as error:
            msg.showerror("Error","We cannot register the employee: \n" + str(error))
            conn.rollback()
            return False
        finally:
            if conn is not None:
                conn.close()
                cursor.close()

def Execute_Query(sql,parameters = None):    
    try:
        conn = ConnectionBD()
        cursor = conn.cursor()
        data = []
        if sql == '':
            return 
        if parameters is not None:
            cursor.execute(sql,parameters)
        else:
            cursor.execute(sql)

        for employee in cursor:
            data.append(employee)        
    except(Exception,ps.DatabaseError) as error:
        msg.showerror("Error","Query error \n" + str(error))
    finally:
        if conn is not None:
            conn.close()
            cursor.close()
    return data

def Search_Employee(id):
    try:
        sql = 'Select * FROM employees WHERE id = ' + str(id) + ''
        conn = ConnectionBD()
        cursor = conn.cursor()    
        cursor.execute(sql)   
        count = cursor.rowcount     
    except(Exception,ps.DatabaseError) as error:
        msg.showerror("Error","Query error \n" + str(error))
    finally:
        if conn is not None:
            conn.close()
            cursor.close()
    if count >0:
        return True   
    return False

def Delete_Employee(id):   
    try:
        sql = 'DELETE FROM employees WHERE id = ' + str(id) + ''
        conn = ConnectionBD()
        cursor = conn.cursor()
        if id == None: return
        if id == '': return    
        cursor.execute(sql)   
        conn.commit()
        msg.showinfo("Employee","The employee was deleted succesfuly") 
        return True   
    except(Exception,ps.DatabaseError) as error:
        msg.showerror("Error","Query error \n" + str(error))
        conn.rollback()
        return False
    finally:
        if conn is not None:
            conn.close()
            cursor.close()

def File_Employee(id,path):
    try:
        sql = 'SELECT file,name_file FROM employees WHERE id = ' + str(id) + ' AND file IS NOT NULL'
        data = []
        conn = ConnectionBD()
        cursor = conn.cursor()   
        if id == '':
            return 
        cursor.execute(sql)       
        for file in cursor.fetchall():
            data.append(file)
        if len(data) == 0:
            msg.showinfo("File empty",'This employee doesnt have files')
            return

        with open(path + '/' + data[0][1],'wb') as file:            
            file.write(data[0][0])

        msg.showinfo("Correct!","The file was saved in this route: \n" + path + '\n' + 'with this name: \n' + data[0][1])
    except(Exception,ps.DatabaseError) as error:
        msg.showerror("Error","Query error \n" + str(error))
    finally:
        if conn is not None:
            conn.close()
            cursor.close()   


                             