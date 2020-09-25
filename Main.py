from flask import Flask,render_template,request,redirect,send_file
import sqlite3
import datetime
import time




ID = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '010' ]
name = ['Uschi', 'Helga', 'Mete', 'Andreas', 'Maria', 'Thomas', 'Konrad', 'Amed', 'Zusatz1', 'Zusatz2', 'Zusatz3',]

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/Zeiterfassung',methods = ['POST','GET'])
def Zeiterfassung ():
    if request.method == 'POST':
        passwort = request.form.get ( 'passwd' )
        if passwort == "Zeiterfassung2020":
            return render_template ( 'zeiterfassung.html' )
        else:
            return render_template ( 'loginfail.html' )
    return render_template ( 'login.html' )
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
                    conn = sqlite3.connect ( 'datenbank.db' )
                    cursor = conn.cursor ( )
                    cursor.execute ( "SELECT count(*) from zeiterfassung WHERE name == ? and datum == ?" , (name[z],date,) )
                    counter = cursor.fetchall ( )
                    conn.commit ()
                    if counter[0][0] >= 1 :
                        return render_template("fail.html", status= 1)
                    else:
                        global statuscheck
                        statuscheck = 1
                        if eat == '1':
                            global eater
                            global eatid
                            eater = 'Mit Mitagspause!'
                            eatid = 1
                            return redirect ( '/done' )
                        else:
                            eater = 'Ohne Mitagspause'
                            eatid = 0
                            return redirect ( '/done' )
                else:
                    conn = sqlite3.connect ( 'datenbank.db' )
                    cursor = conn.cursor ( )
                    cursor.execute ( "SELECT count(*) from zeiterfassung WHERE name == ? and datum == ?" , (name[z] , date ,) )
                    counter = cursor.fetchall ( )
                    conn.commit ( )

                    cursor.execute (" SELECT count(*) FROM zeiterfassung WHERE name == ? and zeit2 is not NULL",(name[z],))
                    counterout = cursor.fetchall ( )
                    conn.commit ( )


                    if counter[0][0] <= 0:
                        return render_template("fail.html", status = 2 )

                    else:
                        if counterout[0][0] <= 0:
                            statuscheck = 2
                            return redirect ( '/done' )
                        else :
                            return render_template("fail.html", status = 3 )
@app.route('/done')
def done():
    usernamen = name[z]

    date = (datetime.datetime.now ( ).strftime ( "%A  %d.%m.%Y" ))
    time = (datetime.datetime.now ( ).strftime ( "%H:%M" ))


    conn = sqlite3.connect ( 'datenbank.db' )
    cursor = conn.cursor ( )
    cursor.execute ( "SELECT COUNT(*) FROM zeiterfassung" )
    idselect = cursor.fetchall ( )
    idselect2 = int ( idselect[0][0] )
    idselect3 = idselect2 + 1
    conn.commit ( )


    if statuscheck == 2 :
        cursor.execute ( "UPDATE zeiterfassung SET zeit2 == ? WHERE datum == ? AND name ==? AND zeit2 IS NULL " , (time ,date,usernamen) )
        conn.commit ( )
        conn.close ( )
        global eater
        eater = " "
        return render_template ( 'done.html' , eater=eater , name=name[z] , status=statuscheck )

    if statuscheck == 1:
        if eatid == 0 :
            pause = '00:00'
        else:
            pause = '00:15:00'
        cursor.execute ( "INSERT INTO zeiterfassung (id,name, datum,zeit1,essen) VALUES (?,?,?,?,?)" , (idselect3 ,usernamen , date , time,pause) )
        conn.commit ( )
        conn.close ( )
        return  render_template('done.html',eater = eater , name = usernamen,status = statuscheck  )
@app.route('/convert' , methods = ['POST','GET'])
def convert():
    date = (datetime.datetime.now ( ).strftime ( "%A  %d.%m.%Y" ))

    for i in range ( len ( name ) ):
        conn = sqlite3.connect ( 'datenbank.db' )
        cursor = conn.cursor ( )
        cursor.execute ( "SELECT COUNT(*) FROM zeiterfassung WHERE name = ? " , (name[i] ,) )
        select = cursor.fetchall ( )
        conn.commit ( )
        select = select[0][0] - 1
        z = 0


        while z <= select:
            conn = sqlite3.connect ( 'datenbank.db' )
            cursor = conn.cursor ( )
            cursor.execute ( "SELECT * FROM zeiterfassung WHERE name = ? " , (name[i] ,) )
            conn.commit ( )
            searchquery = cursor.fetchall ( )
            conn.close ( )

            file = open ( "dataoutput/" +name[i]+ ".csv" ,"a" )
            file.write ( str ( searchquery[z][2] ) + "," )
            file.write ( str ( searchquery[z][3] ) + "," )
            file.write ( str ( searchquery[z][4] ) + "," )
            file.write ( str ( searchquery[z][5] ) + "\n" )
            file.close ( )
            z = z + 1


    for j in range ( len ( name ) ):


        conn = sqlite3.connect ( 'datenbank.db' )
        cursor = conn.cursor ( )
        cursor.execute ( "SELECT COUNT(*) FROM zeiterfassung WHERE name = ? " , (name[j] ,) )
        select = cursor.fetchall ( )
        conn.commit ( )
        select = select[0][0]-1
        y = 0


        while y <= select:
            conn = sqlite3.connect ( 'datenbank.db' )
            cursor = conn.cursor ( )
            cursor.execute ( "SELECT * FROM zeiterfassung WHERE name = ? " , (name[j] ,) )
            conn.commit ( )
            searchquery1 = cursor.fetchall ( )
            conn.close ( )


            conn = sqlite3.connect ( 'datenbank.db' )
            cursor = conn.cursor ( )
            cursor.execute ( "SELECT COUNT(*) FROM zeiterfassungbackup" )
            idselect1 = cursor.fetchall ( )
            idselect1 = int ( idselect1[0][0] )
            idselect1 = idselect1 + 1
            conn.commit ( )


            cursor.execute ( "INSERT INTO zeiterfassungbackup  VALUES (?,?,?,?,?,?)" , (idselect1 , searchquery1[y][1] , searchquery1[y][2] , searchquery1[y][3] , searchquery1[y][4] , searchquery1[y][5]) )
            conn.commit ( )
            conn.close ( )
            y = y + 1

    conn = sqlite3.connect ( 'datenbank.db' )
    cursor = conn.cursor ( )
    cursor.execute ( "DELETE  FROM zeiterfassung" )
    conn.commit ( )
    conn.close ( )


    return render_template('convert.html')
@app.route("/search", methods=['POST','GET'])
def search ():
    if request.method == 'POST':

        search = request.form.get ( 'search' )

        conn = sqlite3.connect ( 'datenbank.db' )
        cursor = conn.cursor ( )

        cursor.execute ( "SELECT * FROM zeiterfassung WHERE name == ? " ,(search,) )
        result1 = cursor.fetchall ( )
        conn.commit ( )

        cursor.execute ( "SELECT * FROM zeiterfassungbackup WHERE name == ? " , (search ,) )
        result2 = cursor.fetchall ( )
        conn.commit ( )

        cursor.execute ( "SELECT count(*) FROM zeiterfassungbackup WHERE name == ? " , (search ,) )
        count2 = cursor.fetchall ( )
        conn.commit ( )

        cursor.execute ( "SELECT count(*) FROM zeiterfassung WHERE name == ? " , (search ,) )
        count1 = cursor.fetchall ( )
        conn.commit ( )

        return render_template('tabel.html',result1= result1 , result2 = result2, count11 = count1[0][0] , count22 = count2[0][0],search=search,)
    return render_template('search.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
