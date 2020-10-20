from flask import Flask,render_template,request,redirect,url_for,session
import sqlite3
import datetime
import time
import os




ID = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '010' ]
name = ['Uschi', 'Helga', 'Mete', 'Andreas', 'Maria', 'Thomas', 'Konrad', 'Amed', 'Zusatz1', 'Zusatz2', 'Zusatz3',]

app = Flask(__name__)
path_db = 'datenbank.db'
path_dataoutput = 'dataoutput/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('auto_login')
    return redirect(url_for('Zeiterfassung'))

@app.route('/Zeiterfassung',methods = ['POST','GET'])
def Zeiterfassung ():
    if request.method == 'POST':
        passwort = request.form.get ( 'passwd' )
        if passwort == "Zeiterfassung2020":
            session['auto_login'] = passwort
            return render_template ( 'zeiterfassung.html' )
        else:
            return render_template ( 'loginfail.html' )
    elif 'auto_login' in session:
        if session['auto_login'] == 'Zeiterfassung2020':
            return render_template ( 'zeiterfassung.html' )
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
                        return render_template("fail.html", status= 1)
                    else:
                        global statuscheck
                        statuscheck = 1
                        if eat == '1':
                            global eat_print
                            global eat_status
                            eat_print = 'Mit Mitagspause!'
                            eat_status = 1
                            return redirect ( '/done' )
                        else:
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
                        return render_template("fail.html", status = 2 )

                    else:
                        if counter_sel_zeiterfassung_bediung_null[0][0] <= 0:
                            statuscheck = 2
                            return redirect ( '/done' )
                        else :
                            return render_template("fail.html", status = 3 )
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
            brakes_print = '00:15:00'
        cursor.execute ( "INSERT INTO zeiterfassung (id,name, datum,zeit1,essen) VALUES (?,?,?,?,?)" , (counter_sel_zeiterfassung ,usernamen , date , time,brakes_print) )
        conn.commit ( )
        conn.close ( )
        return  render_template('done.html' , eater = eat_print , name = usernamen , status = statuscheck )
@app.route('/convert' , methods = ['POST','GET'])
def convert():
    date = (datetime.datetime.now ( ).strftime ( "%A  %d.%m.%Y" ))

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

            file = open (path_dataoutput+name[i]+ ".csv" ,"a" )
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
    if request.method == 'POST':

        search = request.form.get ( 'search' )

        conn = sqlite3.connect (path_db)
        cursor = conn.cursor ( )

        cursor.execute ( "SELECT * FROM zeiterfassung WHERE name == ? " ,(search,) )
        result_search_1 = cursor.fetchall ( )
        conn.commit ( )

        cursor.execute ( "SELECT * FROM zeiterfassungbackup WHERE name == ? " , (search ,) )
        result_search_2 = cursor.fetchall ( )
        conn.commit ( )

        cursor.execute ( "SELECT count(*) FROM zeiterfassungbackup WHERE name == ? " , (search ,) )
        counter_sel_zeiterfassungbackup= cursor.fetchall ( )
        conn.commit ( )

        cursor.execute ( "SELECT count(*) FROM zeiterfassung WHERE name == ? " , (search ,) )
        counter_sel_zeiterfassung = cursor.fetchall ( )
        conn.commit ( )

        return render_template('tabel.html',result1= result_search_1 , result2 = result_search_2, count11 = counter_sel_zeiterfassung[0][0] , count22 = counter_sel_zeiterfassungbackup[0][0],search=search,)
    return render_template('search.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
