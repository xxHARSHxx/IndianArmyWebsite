from flask import Flask,render_template,request,redirect,url_for,session
from flask_socketio import SocketIO
from flask_mysqldb import MySQL
import MySQLdb.cursors

app=Flask(__name__)
app.secret_key='SecKey'
socketio = SocketIO(app)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='butterscotch'
app.config['MYSQL_DB']='gkm'

mysql=MySQL(app)

@app.route('/')
@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/userlogin',methods=['GET','POST'])
def userlogin():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        username=request.form['username']
        password=request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username=%s and password=%s',(username,password,))
        account=cursor.fetchone()
        if account:
            session['loggedin']=True
            session['username']=account['username']
            msg='Logged in successfully!'
            return render_template('homepage.html',msg=msg)
        else:
            msg='Incorrect username/password !'
    return render_template('userlogin.html',msg=msg)

@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        username=request.form['username']
        password=request.form['password']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE username=%s and password=%s',(username,password,))
        account=cursor.fetchone()
        if account:
            session['loggedin']=True
            session['username']=account['username']
            msg='Logged in successfully!'
            return render_template('adminpage.html',msg=msg)
        else:
            msg='Incorrect username/password !'
    return render_template('adminlogin.html',msg=msg)

@app.route('/requests',methods=['POST','GET'])
def requests():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM accounts")
    result = cur.fetchall()
    if result:
        return render_template('requests.html',detail=result)
    else:
        return render_template('requests.html',msg='No Users Found')

@app.route('/newsofficer',methods=['POST','GET'])
def newsofficer():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT title, link FROM news WHERE about=%s",("Officer",))
    result = cur.fetchall()
    if result:
        return render_template('newsofficer.html',detail=result)
    else:
        return render_template('newsofficer.html',msg='No News Found')

@app.route('/newsjco',methods=['POST','GET'])
def newsjco():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT title, link FROM news WHERE about=%s",("JCO/OR",))
    result = cur.fetchall()
    if result:
        return render_template('newsjco.html',detail=result)
    else:
        return render_template('newsjco.html',msg='No News Found')

@app.route('/notifofficer',methods=['POST','GET'])
def notifofficer():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT title, link FROM notifications WHERE about=%s",("Officer",))
    result = cur.fetchall()
    if result:
        return render_template('notifofficer.html',detail=result)
    else:
        return render_template('notifofficer.html',msg='No Notifications Found')

@app.route('/notifjco',methods=['POST','GET'])
def notifjco():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT title, link FROM notifications WHERE about=%s",("JCO/OR",))
    result = cur.fetchall()
    if result:
        return render_template('notifjco.html',detail=result)
    else:
        return render_template('notifjco.html',msg='No Notifications Found')

@app.route('/articles',methods=['POST','GET'])
def articles():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT title,link FROM articles")
    result = cur.fetchall()
    if result:
        return render_template('articles.html',detail=result)
    else:
        return render_template('articles.html',msg='No Articles Found')

@app.route('/addarticle',methods=['GET','POST'])
def addarticle():
    msg=''
    if request.method=='POST' and 'articleid' in request.form and 'title' in request.form and 'link' in request.form:
        articleid=request.form['articleid']
        title=request.form['title']
        link=request.form['link']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM articles WHERE articleid=%s',(articleid,))
        account=cursor.fetchone()
        if account:
            msg='ArticleID already exists!'
        elif not articleid or not title or not link:
            msg='Please Fill The Fields!'
        else:
            cursor.execute('INSERT INTO articles VALUES(%s,%s,%s)',(articleid,title,link))
            mysql.connection.commit()
            msg='Article Added Successfully!'
    elif request.method=='POST':
        msg='Please Fill The Fields!'
    return render_template('addarticle.html',msg=msg)

@app.route('/deletearticle')
def deletearticle():
    return render_template('deletearticle.html')

@app.route('/delarticle/<string:id>',methods=['POST','GET'])
def delarticle(id):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("DELETE FROM articles WHERE articleid=%s",([id]))
    mysql.connection.commit()
    cur.close()
    return render_template('fetcharticles.html',msg='Article Deleted Successfully')

@app.route('/fetcharticles',methods=['POST','GET'])
def fetcharticles():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT articleid,title,link FROM articles")
    result=cur.fetchall()
    if result:
        return render_template('fetcharticles.html',detail=result)
    else:
        return render_template('fetcharticles.html',msg='No Articles Found')

@app.route('/searcharticles',methods=['POST','GET'])
def searcharticles():
    msg=''
    if request.method=='POST' and 'title' in request.form:
        title=request.form['title']
        title1="%"+title+"%"
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT articleid,title,link FROM articles WHERE title like %s",(title1,))
        result=cur.fetchall()
        if not title:
            msg='Please Enter Title to Search'
        else:
            if result:
                return render_template('fetcharticles.html',detail=result)
            else:
                return render_template('fetcharticles.html',msg='No Articles Found')
    elif request.method=='POST':
        msg='Please Enter Title to Search'
    return render_template('fetcharticles.html',msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('username',None)
    return redirect(url_for('main'))

@app.route('/register',methods=['GET','POST'])
def register():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form and 'category' in request.form and 'name' in request.form:
        username=request.form['username']
        password=request.form['password']
        mobno=request.form['mobno']
        category=request.form['category']
        gender=request.form['gender']
        name=request.form['name']
        email=request.form['email']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username=%s',(username,))
        account=cursor.fetchone()
        if account:
            msg='Account already exists!'
        elif not username or not password or not category or not name:
            msg='Please Fill The form!'
        else:
            cursor.execute('INSERT INTO accounts(username,password,mobno,category,gender,name,email) VALUES(%s,%s,%s,%s,%s,%s,%s)',(username,password,mobno,category,gender,name,email,))
            mysql.connection.commit()
            msg='You Have Successfully Registered!'
    elif request.method=='POST':
        msg='Please Fill The form!'
    return render_template('register.html',msg=msg)

@app.route('/aboutarmy')
def aboutarmy():
    return render_template('about_army.html')

@app.route('/lifeinarmy')
def lifeinarmy():
    return render_template('life_in_army.html')

@app.route('/imagegallery')
def imagegallery():
    return render_template('image gallery.html')

@app.route('/videogallery')
def videogallery():
    return render_template('video_gallery.html')

@app.route('/awards')
def awards():
    return render_template('awards.html')

@app.route('/imagesports')
def imagesports():
    return render_template('image_sports.html')

@app.route('/imageevents')
def imageevents():
    return render_template('image_events.html')

@app.route('/armyinaction')
def armyinaction():
    return render_template('image_armyinaction.html')

@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/search')
def search():
    msg=''
    return render_template('search.html',msg=msg)

@app.route('/searchjobs')
def searchjobs():
    return render_template('searchjobs.html')

@app.route('/searchusername',methods=['POST','GET'])
def searchusername():
    msg=''
    if request.method=='POST' and 'username' in request.form:
        username=request.form['username']
        username1="%"+username+"%"
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT username, mobno,category,gender,name,email,verification FROM accounts WHERE username like %s",(username1,))
        result=cur.fetchall()
        if not username:
            msg='Please Enter Username to Search'
        else:
            if result:
                return render_template('fetch.html',detail=result)
            else:
                return render_template('fetch.html',msg='No Users Found')
    elif request.method=='POST':
        msg='Please Enter Username to Search'
    return render_template('fetch.html',msg=msg)

@app.route('/adminsearchusername',methods=['POST','GET'])
def adminsearchusername():
    msg=''
    if request.method=='POST' and 'username' in request.form:
        username=request.form['username']
        username1="%"+username+"%"
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT username, mobno,category,gender,name,email,verification FROM accounts WHERE username like %s",(username1,))
        result=cur.fetchall()
        if not username:
            msg='Please Enter Username to Search'
        else:
            if result:
                return render_template('adminfetch.html',detail=result)
            else:
                return render_template('adminfetch.html',msg='No Users Found')
    elif request.method=='POST':
        msg='Please Enter Username to Search'
    return render_template('adminfetch.html',msg=msg)

@app.route('/searchname',methods=['POST','GET'])
def searchname():
    msg=''
    if request.method=='POST' and 'name' in request.form:
        name=request.form['name']
        name1="%"+name+"%"
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT username, mobno,category,gender,name,email,verification FROM accounts WHERE name like %s",(name1,))
        result=cur.fetchall()
        if not name:
            msg='Please Enter Name to Search'
        else:
            if result:
                return render_template('fetch.html',detail=result)
            else:
                return render_template('fetch.html',msg='No Users Found')
    elif request.method=='POST':
        msg='Please Enter Name to Search'
    return render_template('fetch.html',msg=msg)

@app.route('/adminsearchname',methods=['POST','GET'])
def adminsearchname():
    msg=''
    if request.method=='POST' and 'name' in request.form:
        name=request.form['name']
        name1="%"+name+"%"
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT username, mobno,category,gender,name,email,verification FROM accounts WHERE name like %s",(name1,))
        result=cur.fetchall()
        if not name:
            msg='Please Enter Name to Search'
        else:
            if result:
                return render_template('adminfetch.html',detail=result)
            else:
                return render_template('adminfetch.html',msg='No Users Found')
    elif request.method=='POST':
        msg='Please Enter Name to Search'
    return render_template('adminfetch.html',msg=msg)

@app.route('/fetchuser',methods=['POST','GET'])
def fetchuser():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT username, mobno,category,gender,name,email,verification FROM accounts")
    result=cur.fetchall()
    if result:
        return render_template('adminfetch.html',detail=result)
    else:
        return render_template('adminfetch.html',msg='No Users Found')

@app.route('/fetchcivilian',methods=['POST','GET'])
def fetchcivilian():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT username, mobno,category,gender,name,email,verification FROM accounts WHERE category=%s",("Civilian",))
    result=cur.fetchall()
    if result:
        return render_template('fetch.html',detail=result)
    else:
        return render_template('fetch.html',msg='No Users Found')

@app.route('/fetchofficer',methods=['POST','GET'])
def fetchofficer():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT username, mobno,category,gender,name,email,verification FROM accounts WHERE category=%s",("Officer",))
    result=cur.fetchall()
    if result:
        return render_template('fetch.html',detail=result)
    else:
        return render_template('fetch.html',msg='No Users Found')

@app.route('/fetchnews',methods=['POST','GET'])
def fetchnews():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT newsid,title,link,about FROM news")
    result=cur.fetchall()
    if result:
        return render_template('fetchnews.html',detail=result)
    else:
        return render_template('fetchnews.html',msg='No News Found')

@app.route('/searchnews',methods=['POST','GET'])
def searchnews():
    msg=''
    if request.method=='POST' and 'title' in request.form:
        title=request.form['title']
        title1="%"+title+"%"
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT newsid,title,link,about FROM news WHERE title like %s",(title1,))
        result=cur.fetchall()
        if not title:
            msg='Please Enter Title to Search'
        else:
            if result:
                return render_template('fetchnews.html',detail=result)
            else:
                return render_template('fetchnews.html',msg='No News Found')
    elif request.method=='POST':
        msg='Please Enter Title to Search'
    return render_template('fetchnews.html',msg=msg)

@app.route('/fetchnotif',methods=['POST','GET'])
def fetchnotif():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT notifid,title,link,about FROM notifications")
    result=cur.fetchall()
    if result:
        return render_template('fetchnotif.html',detail=result)
    else:
        return render_template('fetchnotif.html',msg='No Notifications Found')

@app.route('/searchnotif',methods=['POST','GET'])
def searchnotif():
    msg=''
    if request.method=='POST' and 'title' in request.form:
        title=request.form['title']
        title1="%"+title+"%"
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT notifid,title,link,about FROM notifications WHERE title like %s",(title1,))
        result=cur.fetchall()
        if not title:
            msg='Please Enter Title to Search'
        else:
            if result:
                return render_template('fetchnotif.html',detail=result)
            else:
                return render_template('fetchnotif.html',msg='No Notifications Found')
    elif request.method=='POST':
        msg='Please Enter Title to Search'
    return render_template('fetchnotif.html',msg=msg)

@app.route('/eligibility',methods=['GET','POST'])
def eligibility():
    msg=''
    if request.method=='POST' and 'age' in request.form and 'gender' in request.form and 'qualification' in request.form:
        age=request.form['age']
        gender=request.form['gender']
        qualification=request.form['qualification']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT title FROM jobs WHERE minage<=%s and maxage>=%s and gender=%s and qualification=%s",(age,age,gender,qualification,))
        result=cur.fetchall()
        if result:
            return render_template('eligibility.html',detail=result)
        else:
            return render_template('eligibility.html',msg='Not Eligible')

@app.route('/deleteacc/<string:id>',methods=['POST','GET'])
def deleteacc(id):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("DELETE FROM accounts WHERE username=%s",([id]))
    mysql.connection.commit()
    cur.close()
    return render_template('adminfetch.html',msg='Account Deleted Successfully')

@app.route('/deleteuser')
def deleteuser():
    return render_template('deleteuser.html')

@app.route('/addnews',methods=['GET','POST'])
def addnews():
    msg=''
    if request.method=='POST' and 'newsid' in request.form and 'title' in request.form and 'link' in request.form and 'about' in request.form:
        newsid=request.form['newsid']
        title=request.form['title']
        link=request.form['link']
        about=request.form['about']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM news WHERE newsid=%s',(newsid,))
        account=cursor.fetchone()
        if account:
            msg='NewsID already exists!'
        elif not newsid or not title or not link or not about:
            msg='Please Fill The Fields!'
        else:
            cursor.execute('INSERT INTO news VALUES(%s,%s,%s,%s)',(newsid,title,link,about,))
            mysql.connection.commit()
            msg='Entry Added Successfully!'
    elif request.method=='POST':
        msg='Please Fill The Fields!'
    return render_template('addnews.html',msg=msg)

@app.route('/deletenews')
def deletenews():
    return render_template('deletenews.html')

@app.route('/delnews/<string:id>',methods=['POST','GET'])
def delnews(id):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("DELETE FROM news WHERE newsid=%s",([id]))
    mysql.connection.commit()
    cur.close()
    return render_template('fetchnews.html',msg='News Deleted Successfully')

@app.route('/addnotif',methods=['GET','POST'])
def addnotif():
    msg=''
    if request.method=='POST' and 'notifid' in request.form and 'title' in request.form and 'link' in request.form and 'about' in request.form:
        notifid=request.form['notifid']
        title=request.form['title']
        link=request.form['link']
        about=request.form['about']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM notifications WHERE notifid=%s',(notifid,))
        account=cursor.fetchone()
        if account:
            msg='NotifID already exists!'
        elif not notifid or not title or not link or not about:
            msg='Please Fill The Fields!'
        else:
            cursor.execute('INSERT INTO notifications VALUES(%s,%s,%s,%s)',(notifid,title,link,about,))
            mysql.connection.commit()
            msg='Entry Added Successfully!'
    elif request.method=='POST':
        msg='Please Fill The Fields!'
    return render_template('addnotif.html',msg=msg)

@app.route('/deletenotif')
def deletenotif():
    return render_template('deletenotif.html')

@app.route('/delnotif/<string:id>',methods=['POST','GET'])
def delnotif(id):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("DELETE FROM notifications WHERE notifid=%s",([id]))
    mysql.connection.commit()
    cur.close()
    return render_template('fetchnotif.html',msg='Notification Deleted Successfully')

@app.route('/verify',methods=['POST','GET'])
def verify():
    msg=''
    username=session['username']
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE username=%s',(username,))
    account=cursor.fetchone()
    cursor.close()
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM vrequests WHERE username=%s',(username,))
    acc=cur.fetchone()
    mobno=account['mobno']
    gender=account['gender']
    name=account['name']
    email=account['email']
    if account['category']=="Civilian":
        msg='Civilians do not require verification!'
    elif acc:
        msg='You have already submitted a verification request!'
    elif account['verification']=="Yes":
        msg='You have already been verified!'
    else:
        cur.execute('INSERT INTO vrequests VALUES(%s,%s,%s,%s,%s)',(username,mobno,gender,name,email))
        mysql.connection.commit()
        msg='Your verification request has been successfully submitted!'
    return render_template('verify.html',msg=msg)

@app.route('/verifyofficer',methods=['POST','GET'])
def verifyofficer():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM vrequests")
    result=cur.fetchall()
    if result:
        return render_template('verifyofficer.html',detail=result)
    else:
        return render_template('verifyofficer.html',msg='No Requests Found')

@app.route('/verifyacc/<string:id>',methods=['POST','GET'])
def verifyacc(id):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("UPDATE accounts set verification=%s WHERE username=%s",("Yes",[id]))
    mysql.connection.commit()
    cur.execute("DELETE FROM vrequests WHERE username=%s",([id]))
    mysql.connection.commit()
    cur.close()
    return render_template('verifyofficer.html',msg='Account Verified Successfully')

@app.route('/blog',methods=['POST','GET'])
def blog():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT blogid,username,title,blog FROM blog")
    result=cur.fetchall()
    if result:
        return render_template('blog.html',detail=result)
    else:
        return render_template('blog.html',msg='No Blog Posts Found')

@app.route('/showblog/<string:id>',methods=['POST','GET'])
def showblog(id):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT title,blog FROM blog where blogid=%s",([id]))
    result=cur.fetchall()
    if result:
        return render_template('showblog.html',detail=result)
    else:
        return render_template('showblog.html',msg='Blog Not Found')

@app.route('/addblog',methods=['GET','POST'])
def addblog():
    msg=''
    if request.method=='POST' and 'blogid' in request.form and 'title' in request.form and 'blog' in request.form:
        blogid=request.form['blogid']
        username=session['username']
        title=request.form['title']
        blog=request.form['blog']
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM blog WHERE blogid=%s',(blogid,))
        account=cursor.fetchone()
        if account:
            msg='BlogID Already Exists!'
        elif not blogid or not title or not blog:
            msg='Please Fill The Fields!'
        else:
            cursor.execute('INSERT INTO blog VALUES(%s,%s,%s,%s)',(blogid,username,title,blog,))
            mysql.connection.commit()
            msg='Blog Added Successfully!'
    elif request.method=='POST':
        msg='Please Fill The Fields!'
    return render_template('addblog.html',msg=msg)

@app.route('/deleteblog')
def deleteblog():
    return render_template('deleteblog.html')

@app.route('/delblog/<string:id>',methods=['POST','GET'])
def delblog(id):
    cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("DELETE FROM blog WHERE blogid=%s",([id]))
    mysql.connection.commit()
    cur.close()
    return render_template('fetchblog.html',msg='Blog Post Deleted Successfully')

@app.route('/fetchblog',methods=['POST','GET'])
def fetchblog():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT blogid,username,title,blog FROM blog")
    result=cur.fetchall()
    if result:
        return render_template('fetchblog.html',detail=result)
    else:
        return render_template('fetchblog.html',msg='No Blog Posts Found')

@app.route('/searchblogusername',methods=['POST','GET'])
def searchblogusername():
    msg=''
    if request.method=='POST' and 'username' in request.form:
        username=request.form['username']
        username1="%"+username+"%"
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT blogid,username,title,blog FROM blog WHERE username like %s",(username1,))
        result=cur.fetchall()
        if not username:
            msg='Please Enter Username to Search'
        else:
            if result:
                return render_template('fetchblog.html',detail=result)
            else:
                return render_template('fetchblog.html',msg='No Blog Posts Found')
    elif request.method=='POST':
        msg='Please Enter Username to Search'
    return render_template('fetchblog.html',msg=msg)

@app.route('/searchblogtitle',methods=['POST','GET'])
def searchblogtitle():
    msg=''
    if request.method=='POST' and 'title' in request.form:
        title=request.form['title']
        title1="%"+title+"%"
        cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT blogid,username,title,blog FROM blog WHERE title like %s",(title1,))
        result=cur.fetchall()
        if not title:
            msg='Please Enter Title to Search'
        else:
            if result:
                return render_template('fetchblog.html',detail=result)
            else:
                return render_template('fetchblog.html',msg='No Blog Posts Found')
    elif request.method=='POST':
        msg='Please Enter Title to Search'
    return render_template('fetchblog.html',msg=msg)



#CHAT

@app.route('/sessions')
def sessions(methods=['GET', 'POST']):
    return render_template('session.html')

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)

if __name__ == "__main__":
    socketio.run(app, debug=True)
