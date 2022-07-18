from flask import Flask, render_template,request,redirect,url_for,session,flash
from flask_mysqldb import MySQL,MySQLdb
# import bcrypt
# import werkzeug
import pickle
import numpy as np

"""
link drive
tes
https://drive.google.com/drive/folders/10E2MxnJgc-I7hkUaY9NaLp7i40vK-a64?usp=sharing
"""
with open('static/model/model_compfest.pkl', 'rb') as file:  
    file.seek(0)
    load_model = pickle.load(file)

app = Flask(__name__)
mysql = MySQL(app)

decode = {'architectures':0, 'attorney':1, 'business analyst':2, 'counselor':3,
       'criminal investigations':4, 'editor':5, 'flight instructor':6,
       'machine learning':7, 'web designer':8, 'writer':9, 'architectural design':10,
       'arranger':11, 'home offices':12, 'lecturer':13, 'mediator':14, 'patrol':15,
       'photographer':16, 'piloting':17, 'producer':18, 'programmer':19, 'r':20, 'big data':21,
       'composer':22, 'construction disputes':23, 'crime prevention':24,
       'design durable':25, 'director':26, 'flying':27, 'java programmer':28, 'teacher':29,
       'webfocus':30, 'actor':31, 'advocate':32, 'data mining':33, 'design urbain':34,
       'evidence':35, 'graphic designer':36, 'instrument rated pilot':37,
       'mis reporting':38, 'reporter':39, 'researcher':40, 'aviation':41,
       'communication skill':42, 'design architectural':43, 'educator':44,
       'enforcement':45, 'journalism':46, 'legal advice':47, 'python':48, 'webmaster':49,
       'apache spark':50, 'author':51, 'copywriter':52, 'criminal justice':53, 'dancer':54,
       'interpersonal communications':55, 'journalist':56, 'litigation':57, 'php':58,
       'plan darchitecture':59, 'single engine land':60, 'cameraman':61, 'css':62,
       'field training officer':63, 'freelancer':64, 'law firm administration':65,
       'multiengine land':66, 'predictive analytics':67, 'speaker':68,
       'sustainable architecture':69, 'administrator':70, 'attorneys':71,
       'awardwinning writer':72, 'community policing':73, 'discrepancy resolution':74,
       'flight training':75, 'hadoop':76, 'public speaker':77, 'sustainable design':78,
       'web development':79, 'aircraft':80, 'customer relation':81,
       'data visualization':82, 'design research':83, 'filmmaker':84, 'interrogation':85,
       'javascript':86, 'legal counseling':87, 'novelist':88, 'performer':89,
       'adaptive reuse':90, 'big data analytics':91, 'commercial piloting':92,
       'corporate law':93, 'firearms':94, 'social worker':95, 'sviluppo web':96}

app.secret_key = "ideacode"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ideacode'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

@app.route("/")
def awal():
    return render_template('index.html')

@app.route("/daftar",methods = ['POST','GET'])
def daftar():
    if request.method == 'GET':    
        return render_template('daftar.html')
    else:
        Nama = request.form['names']
        Username = request.form['usernames']
        Email = request.form['email']
        Password = request.form['password']#.encode('utf-8')
        #hash_password = bcrypt.hashpw(Password,bcrypt.gensalt())
        con = mysql.connection.cursor()
        cur = mysql.connection.cursor()
        con_mail = mysql.connection.cursor()
        con.execute('SELECT Username FROM data_akun WHERE Username=%s',[Username])
        con_mail.execute('SELECT Email FROM data_akun WHERE Email=%s',[Email])
        result = con.fetchall()
        result_mail = con_mail.fetchall()
        if len(result)>0:
            con.close()
            cur.close()
            flash('username sudah pernah digunakan',category='warning')
            return render_template('daftar.html')
        if len(result_mail)>0:
            con_mail.close()
            cur.close()
            flash('email sudah pernah digunakan','warning')
            return render_template('daftar.html')
        else:
            cur.execute('INSERT INTO data_akun(Nama,Username,Email,Password) VALUES (%s,%s,%s,%s)',(Nama,Username,Email,Password))
            session['names'] = Nama
            session['usernames'] = Username
            session['email'] = Email
            mysql.connection.commit()
            cur.close()
            return redirect('/masuk')
@app.route("/masuk",methods = ['GET','POST'])
def masuk():
    if request.method=='POST':
        user_login = request.form['user-login']
        pass_login = request.form['pass-login']
        con_login = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        con_login.execute("SELECT * FROM data_akun WHERE Username = %s ",[user_login])
        akun = con_login.fetchone()
        con_login.close()
        if akun is not None and len(akun)>0:
            if pass_login == akun['Password']:
                session['usernames'] = akun['Username']
                session['password'] = akun['Password']
                session['names'] = akun['Nama']
                return redirect('/home')
            else:
                flash("Username dan Password tidak cocok","warning")
                return render_template('masuk.html')
    else:
        return render_template('masuk.html')
    return render_template('masuk.html')
@app.route("/home",methods = ["GET","POST"])
def home():
    return render_template('home.html')

@app.route("/main",methods = ["GET","POST"])
def utama():
    if request.method=='POST':
        skill_1 = request.form['skill-1']
        skill_2 = request.form['skill-2']
        skill_3 = request.form['skill-3']
        skill_4 = request.form['skill-4']
        skill_5 = request.form['skill-5']
        skill_6 = request.form['skill-6']
        skill_7 = request.form['skill-7']
        skill_8 = request.form['skill-8']
        skill_9 = request.form['skill-9']
        skill_10 = request.form['skill-10']
        inp_skill = [skill_1,skill_2,skill_3,skill_4,skill_5,skill_6,skill_7,skill_8,skill_9,skill_10]
        index = []
        inputan = [0 for i in range(97)]
        for k,v in decode.items():
            if k in inp_skill:
                index.append(v)
        for i in index:
            inputan[i] = 1
        inputan = np.array(inputan)
        inputan = inputan.reshape(1,-1)
        pred = load_model.predict_proba(inputan)
        sukses = True
        sortir = sorted(range(len(pred[0])),reverse=True, key = lambda i:pred[0][i])
        pekerjaan = ['architecture','data analyst','data science','journalist','lawyer','pilot','police','researcher','teacher','web developer','writer']
        print(pekerjaan[sortir[2]])
        return render_template('main.html',prediksi = sukses,rekomen_1 = pekerjaan[sortir[0]],rekomen_2 = pekerjaan[sortir[1]],rekomen_3 = pekerjaan[sortir[2]])
    return render_template('main.html')
if __name__=="__main__":
    app.run(debug = True,port = '5001')
