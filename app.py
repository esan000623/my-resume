from flask import Flask, render_template,request,redirect,flash
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")


hobbies = [ "躺平", "打電動", "看電影", "聽音樂", "旅遊", "烹飪", "台鐵"]
for hobby in hobbies:
    print(hobby)

skills=["基礎python","Flask"]
for skill in skills:
    print(skill)

def get_db():
    conn = sqlite3.connect("messages.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            time TEXT NOT NULL)""")
    conn.commit()
    conn.close()

@app.route("/",methods=["POST","GET"])
def home():
    if request.method=="POST":
        username=request.form["username"]
        message=request.form["message"]
        
        if not username.strip():
            flash("姓名不能是空的！")
            return redirect("/")
            
        if not message.strip():
            flash("留言不能是空的！")
            return redirect("/")
            
        time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn = get_db()
        conn.execute("""INSERT INTO messages(username,message,time) VALUES (?, ?, ?)""", (username, message, time)) 
        conn.commit()
        conn.close()
        
    conn=get_db()
    messages = conn.execute("""SELECT*FROM messages ORDER BY id DESC""").fetchall()
    print("SQLite 留言：", messages)
    conn.close()
    message_count=len(messages)
    return render_template("index.html",hobbies=hobbies,skills=skills,messages=messages,message_count=message_count)

@app.route("/delete/<int:id>",methods=["POST"])
def delete(id):
    conn=get_db()
    conn.execute("""DELETE FROM messages WHERE id=?""",(id,))
    conn.commit()
    conn.close()
    flash("留言已刪除成功了喔!")
    return redirect("/")
    
@app.route("/edit/<int:id>",methods=["POST","GET"])
def edit(id):
    if request.method=="POST":
        username = request.form["username"]
        message = request.form["message"]
        
        if not username.strip():
            flash("姓名不能是空的！")
            return redirect("/")

        if not message.strip():
            flash("留言不能是空的！")
            return redirect("/")
        
        conn=get_db()
        conn.execute("""UPDATE messages SET username = ?, message = ? WHERE id = ?""", (username, message, id))
        conn.commit()
        conn.close()
        flash("留言已編輯成功了喔!")
        return redirect("/")
    
    conn=get_db()
    message = conn.execute("""SELECT*FROM messages WHERE id = ?""",(id,)).fetchone()
    conn.close()           
    return render_template("edit.html", message=message, id=id)
    

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    init_db()
    app.run()
