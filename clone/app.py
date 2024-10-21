from flask import Flask, render_template, request, session, redirect
from functools import wraps
from dbUtils import getList,add,setfinish,setundone,delete
#from 專案名 import 專案內涵數

# creates a Flask application, specify a static folder on /
app = Flask(__name__, static_folder='static',static_url_path='/')
#set a secret key to hash cookies
app.config['SECRET_KEY'] = '123TyU%^&'

#define a function wrapper to check login session
def login_required(f):
	@wraps(f)
	def wrapper(*args, **kwargs):
		loginID = session.get('loginID') #檢查是否有loginID登入變數
		if not loginID:
			return redirect('/loginPage.html')
		return f(*args, **kwargs)
	return wrapper

#another way to check login session
def isLogin():
	return session.get('loginID')


@app.route("/") 
@login_required #call def login_required(f)，也就是直接打/會跳到登入頁面
def hello(): 
	message = "Hello, World 1"
	return message



@app.route("/test/<string:name>/<int:id>") #檢查是否有登入，
#取得網址作為參數
def useParam(name,id):
	#check login inside the function
	if not isLogin():
		return redirect('/loginPage.html')
	return f"got name={name}, id={id} "


@app.route("/edit")
@login_required
#使用server side render: template 樣板
def h1():
	dat={
		"name": "大牛",
		"content":"內容說明文字"
	}
	#editform.html 存在於 templates目錄下, 將dat 作為參數送進 editform.html, 名稱為 data
	return render_template('editform.html', data=dat)
	

@app.route("/list")
#使用server side render: template 樣板
def h2():
	dat=[
		{
			"name": "大牛",
			"p":"愛吃瓜"
		},
		{
			"name": "小李",
			"p":"怕榴槤"
		},
		{
			"name": "",
			"p":"ttttt"
		},
		{
			"name": "老謝",
			"p":"來者不拒"
		}
	]
	return render_template('list.html', data=dat)

@app.route('/input', methods=['GET', 'POST'])
def userInput():
	if request.method == 'POST': #request來補捉使用者端的動作是否為POST
		form =request.form
	else:
		form= request.args

	txt = form['txt']  # pass the form field name as key
	note =form['note']
	select = form['sel']
	msg=f"method: {request.method} txt:{txt} note:{note} sel: {select}"
	return msg

@app.route("/listJob")# @app....為定義網址
#使用server side render: template 樣板
def gl():
	dat=getList()
	return render_template('todolist.html', data=dat) #'todolist.html'為輸出樣板
#若無@app...可在最後用"static/"定義靜態檔案
#handles login request

@app.route('/login', methods=['POST']) #法一
def login():
	form =request.form
	id = form['ID']
	pwd =form['PWD']
	#validate id/pwd
	if id=='123' and pwd=='456': #判斷是否合法，用DB?
		session['loginID']=id #存起來
		return redirect("/")
	else:
		session['loginID']=False 
		return redirect("/loginPage.html")
	
@app.route('/submiting',methods=['POST'])
def sub():
	name=request.form['name']
	cnt=request.form['content']
	#sql
	html=f"update===> nnn:{name}, cnt={cnt}"
	return html

@app.route('/addJob',methods=['POST'])
def addJob():
	if request.method == 'POST': #request來補捉使用者端的動作是否為POST
		form =request.form
	else:
		form= request.args

	jobName = form['name']  # pass the form field name as key，取三個使用者輸入欄位
	jobcontent =form['content']
	due = form['due']
	add(jobName,jobcontent,due) #將參數傳到dbUtil中的add函數中
	return redirect("/listJob")#轉向listJob網頁

@app.route('/setfinish', methods=['GET'])
def done():
	if request.method == 'POST': #request來補捉使用者端的動作是否為POST
		form =request.form
	else:
		form= request.args
	id = form['id']  # pass the form field name as key
	setfinish(id)
	return redirect("/listJob")

@app.route('/setundone', methods=['GET'])
def undone():
	if request.method == 'POST': #request來補捉使用者端的動作是否為POST
		form =request.form
	else:
		form= request.args
	id = form['id']  # pass the form field name as key
	setundone(id)
	return redirect("/listJob")

@app.route('/delete', methods=['GET'])
def delete():
	if request.method == 'POST': #request來補捉使用者端的動作是否為POST
		form =request.form
	else:
		form= request.args
	id =form['id']  # pass the form field name as key
	delete(id)
	return redirect("/listJob")