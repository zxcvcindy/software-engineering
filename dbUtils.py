#!/usr/local/bin/python
# Connect to MariaDB Platform
import mysql.connector #mariadb

try:
	#連線DB 若沒錯誤建立一個cursor，如有錯誤則執行底下"except"區塊，目的是不讓使用者知道有出錯
	conn = mysql.connector.connect(
		user="root",
		password="",
		host="localhost",
		port=3306,
		database="test"
	)
	#建立執行SQL指令用之cursor, 設定傳回dictionary型態的查詢結果 [{'欄位名':值, ...}, ...]
	cursor=conn.cursor(dictionary=True)
except mysql.connector.Error as e: # mariadb.Error as e:
	print(e) #把錯誤訊息印出來
	print("Error connecting to DB")
	exit(1) #錯誤代碼


	
def delete(id):
	sql="delete from todolist where id=%s"
	cursor.execute(sql,(id,))
	conn.commit()
	return

def setfinish(id):
	sql="update todolist set status=1 where id=%s;"
	param=(id,)
	cursor.execute(sql,param)
	conn.commit()
	 #有用到變動資料庫語法(eg.delet,insert,update)就必須在最後一行加上"conn.commit()"才能確保連接到mysql.connector套件
	return

def setundone(id):
	sql="update todolist set status=0 where id=%s;"
	param=(id,)
	cursor.execute(sql,param)
	conn.commit()
	 #有用到變動資料庫語法(eg.delet,insert,update)就必須在最後一行加上"conn.commit()"才能確保連接到mysql.connector套件
	return
	
def getList():
	sql="select id,jobcontent,jobName,status,duedate from todolist;"#sql 指令
	#若有過濾條件:sql="select id,jobcontent,jobName,status from todolist where status=0;"，或直接在樣板內過濾
	#param=('值',...) 如果參數值只有一個後面要多加一個","python才會知道他是陣列中其中一個參數
	cursor.execute(sql)
	return cursor.fetchall()#結果用"fetchall"把牠撈出來

def add(name,content,due):#用參數連接
	sql="insert into todolist(jobName,jobcontent,duedate,status) value(%s,%s,%s,%s);"#sql 指令
	param=(name,content,due,0)
	cursor.execute(sql,param) #執行指令
	conn.commit()
	return
