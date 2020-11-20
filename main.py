from flask import Flask,render_template,request,redirect,session
import sqlite3
import datetime
from smtplib import SMTP
import logging




ID = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '010' ]
name = ['Uschi', 'Helga', 'Mete', 'Andreas', 'Maria', 'Thomas', 'Konrad', 'Amed', 'Zusatz1', 'Zusatz2', 'Zusatz3',]
pwd_zeiterfassung = 'Zeiterfassung2020'
pwd_admin = 'Zeiterfassung2020admin'

app = Flask(__name__)
path_db = 'datenbank.db'#'/home/pi/Python-Server/datenbank.db'
path_log = 'static/log.log'  #'/home/pi/Python-Server/static/log.log'
path_dataoutput = 'dataoutput/'#'/home/pi/Python-Server/dataoutput/'

logging.basicConfig(filename=path_log,level=logging.INFO)
logger_zeiterfassung = logging.getLogger("zeiterassung")
logger_zeiterfassung.setLevel(logging.INFO)
logger_login = logging.getLogger("login")
logger_login.setLevel(logging.INFO)
logger_convert = logging.getLogger("login")
logger_convert.setLevel(logging.INFO)


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/logout_zeiterfassung')
def logout_zeiterfassung():
    if 'auto_login_zeiterfassung' in session:
        logger_login.info ( datetime.datetime.now ( ).strftime ("%H:%M:%S :" ) + "Hatte sich ueber die IP " + request.remote_addr + " aus dem autologin von der Zeiterfassung ausgeloggt." )
        session.pop('auto_login_zeiterfassung')
        return redirect("/Zeiterfassung")

    else:
        return redirect("/")
@app.route('/Zeiterfassung',methods = ['POST','GET'])
def Zeiterfassung ():
    if request.method == 'POST':
        passwort = request.form.get ( 'passwd' )
        if passwort == pwd_zeiterfassung:
            session['auto_login_zeiterfassung'] = passwort
            logger_login.info ( datetime.datetime.now ( ).strftime ( "%H:%M:%S :" )  +"Hatte sich ueber die IP " + request.remote_addr + " in das zeiterfassungs system erfolgreich neu eingelockt und damit das auto login aktivirt." )
            return render_template ( 'zeiterfassung.html' )
        else:
            logger_login.info ( datetime.datetime.now ( ).strftime ("%H:%M:%S :" ) + "Hatte sich ueber die IP " + request.remote_addr + " in das zeiterfassungs system nicht erfolgreich eingelockt." )
            return render_template ( 'loginfail.html' )
    elif 'auto_login_zeiterfassung' in session:
        if session['auto_login_zeiterfassung'] == pwd_zeiterfassung:
            return render_template ( 'zeiterfassung.html' )
        else:
            return  redirect('/logout_')
    else:
        return render_template ( 'login.html' )
app.secret_key = "Io H & ( fi & u? +? MZ % ??? t , 4q? U? V_F ? R. G zL ? 3F6? ܺ y Y * aO $ 5? 4 m 9PY M? Kd x ~ 4 # P ? 4 wfR + 4 <Ӕ * ? $ "
@app.route('/check',methods = ['POST','GET'])
def check ():
    date = (datetime.datetime.now ( ).strftime ( "%A  %d.%m.%Y" ))
    if request.method == 'POST':
        userid = request.form.get ('name')
        status = request.form.get ('status')
        eat = request.form.get ( 'eat' )
        global z
        for z in range(len(ID)):
            if ID[z] == userid or name[z] == userid     :
                if status == '1':
                    conn = sqlite3.connect (path_db)
                    cursor = conn.cursor ( )
                    cursor.execute ( "SELECT count(*) from zeiterfassung WHERE name == ? and datum == ?" , (name[z],date,) )
                    countecounter_sel_zeiterfassung_bediung = cursor.fetchall ( )
                    conn.commit ()
                    if countecounter_sel_zeiterfassung_bediung[0][0] >= 1 :
                        logger_zeiterfassung.info ( datetime.datetime.now ( ).strftime ( "%H:%M:%S :" ) + name[z] + " hatte sich ueber die IP " + request.remote_addr + " vergeblich versucht einzugeloggt." )
                        return render_template("fail.html", status= 1,URL='/zeiterfassung')
                    else:
                        global statuscheck
                        statuscheck = 1
                        if eat == '1':
                            logger_zeiterfassung.info ( datetime.datetime.now ( ).strftime ( "%H:%M:%S :" ) + name[z] + " hatte sich ueber die IP " + request.remote_addr + " mit Mittagspause einzugeloggt." )
                            global eat_print
                            global eat_status
                            eat_print = 'Mit Mitagspause!'
                            eat_status = 1
                            return redirect ( '/done' )
                        else:
                            logger_zeiterfassung.info ( datetime.datetime.now ( ).strftime ( "%H:%M:%S :" ) + name[z] + " hatte sich ueber die IP " + request.remote_addr + " ohne Mittagspause einzugeloggt." )
                            eat_print = 'Ohne Mitagspause'
                            eat_status = 0
                            return redirect ( '/done' )
                else:
                    conn = sqlite3.connect (path_db)
                    cursor = conn.cursor ( )
                    cursor.execute ( "SELECT count(*) from zeiterfassung WHERE name == ? and datum == ?" , (name[z] , date ,) )
                    countecounter_sel_zeiterfassung_bediung = cursor.fetchall ( )
                    conn.commit ( )

                    cursor.execute (" SELECT count(*) FROM zeiterfassung WHERE name == ? and zeit2 is not NULL",(name[z],))
                    counter_sel_zeiterfassung_bediung_null = cursor.fetchall ( )
                    conn.commit ( )


                    if countecounter_sel_zeiterfassung_bediung[0][0] <= 0:
                        logger_zeiterfassung.info ( datetime.datetime.now ( ).strftime ( "%H:%M:%S :" ) + name[z] + " hatte sich noch nicht eingloggt IP: " + request.remote_addr + " ." )

                        return render_template("fail.html", status = 2 ,URL='/zeiterfassung')

                    else:
                        if counter_sel_zeiterfassung_bediung_null[0][0] <= 0:
                            logger_zeiterfassung.info ( datetime.datetime.now ( ).strftime ( "%H:%M:%S :" ) + name[z] + " hatte sich ueber die IP " + request.remote_addr + " ausgeloggt." )
                            statuscheck = 2
                            return redirect ( '/done' )
                        else :
                            logger_zeiterfassung.info ( datetime.datetime.now ( ).strftime ( "%H:%M:%S :" ) + name[z] + " hatte sich ueber die IP " + request.remote_addr + " vergeblich versucht auszuloggen." )

                            return render_template("fail.html", status = 3,URL='/zeiterfassung' )
@app.route('/done')
def done():
    usernamen = name[z]

    date = (datetime.datetime.now ( ).strftime ( "%A  %d.%m.%Y" ))
    time = (datetime.datetime.now ( ).strftime ( "%H:%M" ))


    conn = sqlite3.connect (path_db)
    cursor = conn.cursor ( )
    cursor.execute ( "SELECT COUNT(*) FROM zeiterfassung" )
    counter_sel_zeiterfassung = cursor.fetchall ( )
    counter_sel_zeiterfassung = int ( counter_sel_zeiterfassung[0][0] )
    counter_sel_zeiterfassung = counter_sel_zeiterfassung + 1
    conn.commit ( )


    if statuscheck == 2 :
        cursor.execute ( "UPDATE zeiterfassung SET zeit2 == ? WHERE datum == ? AND name ==? AND zeit2 IS NULL " , (time ,date,usernamen) )
        conn.commit ( )
        conn.close ( )
        global eat_print
        eat_print = " "
        return render_template ( 'done.html' , eater=eat_print , name=name[z] , status=statuscheck )

    if statuscheck == 1:
        if eat_status == 0 :
            brake_print = '00:00'
        else:
            brake_print = '00:15:00'
        cursor.execute ( "INSERT INTO zeiterfassung (id,name, datum,zeit1,pausenzeit) VALUES (?,?,?,?,?)" , (counter_sel_zeiterfassung ,usernamen , date , time,brake_print) )
        conn.commit ( )
        conn.close ( )
        return  render_template('done.html' , eater = eat_print , name = usernamen , status = statuscheck )
@app.route('/convert' , methods = ['POST','GET'])
def convert():
    year = (datetime.datetime.now ( ).strftime ( "%Y" ))
    logger_convert.info ( datetime.datetime.now ( ).strftime ("%H:%M:%S :" ) + "IP: " + request.remote_addr + " hatt dateien convertiert" )
    for i in range ( len ( name ) ):
        conn = sqlite3.connect (path_db)
        cursor = conn.cursor ( )
        cursor.execute ( "SELECT COUNT(*) FROM zeiterfassung WHERE name = ? " , (name[i] ,) )
        counter_sel_zeiterfassung = cursor.fetchall ( )
        conn.commit ( )
        counter_sel_zeiterfassung = counter_sel_zeiterfassung[0][0] - 1
        z = 0


        while z <= counter_sel_zeiterfassung:
            conn = sqlite3.connect (path_db)
            cursor = conn.cursor ( )
            cursor.execute ( "SELECT * FROM zeiterfassung WHERE name = ? " , (name[i] ,) )
            conn.commit ( )
            search_zeiterfassung_bediung_name = cursor.fetchall ( )
            conn.close ( )

            file = open (path_dataoutput+name[i]+" "+year+".csv" ,"a" )
            file.write ( str ( search_zeiterfassung_bediung_name[z][2] ) + "," )
            file.write ( str ( search_zeiterfassung_bediung_name[z][3] ) + "," )
            file.write ( str ( search_zeiterfassung_bediung_name[z][4] ) + "," )
            file.write ( str ( search_zeiterfassung_bediung_name[z][5] ) + "\n" )
            file.close ( )
            z = z + 1


    for j in range ( len ( name ) ):


        conn = sqlite3.connect (path_db)
        cursor = conn.cursor ( )
        cursor.execute ( "SELECT COUNT(*) FROM zeiterfassung WHERE name = ? " , (name[j] ,) )
        counter_sel_zeiterfassung = cursor.fetchall ( )
        conn.commit ( )
        counter_sel_zeiterfassung = counter_sel_zeiterfassung[0][0]-1
        y = 0


        while y <= counter_sel_zeiterfassung:
            conn = sqlite3.connect (path_db)
            cursor = conn.cursor ( )
            cursor.execute ( "SELECT * FROM zeiterfassung WHERE name = ? " , (name[j] ,) )
            conn.commit ( )
            search_zeiterfassung_bediung_name = cursor.fetchall ( )
            conn.close ( )


            conn = sqlite3.connect (path_db)
            cursor = conn.cursor ( )
            cursor.execute ( "SELECT COUNT(*) FROM zeiterfassungbackup" )
            counter_sel_zeiterfassungbackup = cursor.fetchall ( )
            counter_sel_zeiterfassungbackup = int ( counter_sel_zeiterfassungbackup[0][0] )
            counter_sel_zeiterfassungbackup = counter_sel_zeiterfassungbackup + 1
            conn.commit ( )


            cursor.execute ( "INSERT INTO zeiterfassungbackup  VALUES (?,?,?,?,?,?)" , (counter_sel_zeiterfassungbackup , search_zeiterfassung_bediung_name[y][1] , search_zeiterfassung_bediung_name[y][2] , search_zeiterfassung_bediung_name[y][3] , search_zeiterfassung_bediung_name[y][4] , search_zeiterfassung_bediung_name[y][5]) )
            conn.commit ( )
            conn.close ( )
            y = y + 1

    conn = sqlite3.connect (  path_db )
    cursor = conn.cursor ( )
    cursor.execute ( "DELETE  FROM zeiterfassung" )
    conn.commit ( )
    conn.close ( )


    return render_template('convert.html')
@app.route("/search", methods=['POST','GET'])
def search ():
    search = request.args.get ( 'search' )
    if search == None :
        return render_template('search.html')
    if search in name :
        conn = sqlite3.connect ( path_db )
        cursor = conn.cursor ( )

        cursor.execute ( "SELECT * FROM zeiterfassung WHERE name == ? " , (search ,) )
        result_search_1 = cursor.fetchall ( )
        conn.commit ( )

        cursor.execute ( "SELECT * FROM zeiterfassungbackup WHERE name == ? " , (search ,) )
        result_search_2 = cursor.fetchall ( )
        conn.commit ( )

        cursor.execute ( "SELECT count(*) FROM zeiterfassungbackup WHERE name == ? " , (search ,) )
        counter_sel_zeiterfassungbackup = cursor.fetchall ( )
        conn.commit ( )

        cursor.execute ( "SELECT count(*) FROM zeiterfassung WHERE name == ? " , (search ,) )
        counter_sel_zeiterfassung = cursor.fetchall ( )
        conn.commit ( )

        result_search_1.reverse ( )
        result_search_2.reverse ( )

        return render_template ( 'tabel.html' , result_search_1_reverse=result_search_1 ,result_search_2_reverse=result_search_2 , search=search ,counter_sel_zeiterfassung=counter_sel_zeiterfassung[0][0] ,counter_sel_zeiterfassungbackup=counter_sel_zeiterfassungbackup[0][0] )
    else:
        status=4
        return render_template('fail.html',status=status,URL='/search')
@app.route('/send_mail',methods = ['POST','GET'])
def send_mail () :
    if request.method == 'POST':
        RCPT_TO = request.form.get ( 'RCPT_TO' )
        mail_text = 'Hier ist der Google Drive Link zum Datenoutput der Zeiterfassung: \n https://drive.google.com/drive/folders/1rQHZnT_oXpLUULuHgnQPs0r78LYHORl8?usp=sharing '
        user = 'Zeitmessungssystem@gmail.com'
        pwd_mail = 'skit7BIRD!smee3chem'
        subject = 'Link zum Datenoutput der Zeiterfassung :)'

        MAIL_FROM = 'Zeitmessungssystem@gmail.com'
        DATA = 'From:%s\nTo:%s\nSubject:%s\n\n%s' % (MAIL_FROM , RCPT_TO , subject , mail_text)

        server = SMTP ( 'smtp.gmail.com:587' )
        server.starttls ( )
        server.login ( user , pwd_mail )
        server.sendmail ( MAIL_FROM , RCPT_TO , DATA )
        server.quit ()
        logger_convert.info ( datetime.datetime.now ( ).strftime ("%H:%M:%S :" ) + " IP:" + request.remote_addr + " hatt den linke an die E-mail"+RCPT_TO+" gesendet." )
        return render_template('mail_sent.html',RCPT_TO=RCPT_TO)
    else:
        return render_template('mail_input.html')

if __name__ == '__main__': #if __name__ == '__main__':
    app.run ( port=5000 , debug=True ) #app.run(debug=True, port=80, host='0.0.0.0')
