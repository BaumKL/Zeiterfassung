import datetime
import sqlite3

name = ['Uschi', 'Helga', 'Mete', 'Andreas', 'Maria', 'Thomas', 'Konrad', 'Amed', 'Zusatz1', 'Zusatz2', 'Zusatz3',]
end = 0
while 0 == end:
    date = (datetime.datetime.now ( ).strftime ( "%A  %d.%m.%Y" ))
    time = (datetime.datetime.now ( ).strftime ( "%H:%M" ))
    for z in range(len(name)):
        if time == "20:19":
            conn = sqlite3.connect ( 'datenbank.db' )
            cursor = conn.cursor ( )
            cursor.execute ( "SELECT count(*) FROM zeiterfassung WHERE name == ? " ,(name[z],))
            selectentry = cursor.fetchall ( )
            selectentry = selectentry[0][0]
            conn.commit ( )

            if selectentry == 0 :


                cursor.execute ( "SELECT COUNT(*) FROM zeiterfassung" )
                idselect = cursor.fetchall ( )
                idselect2 = int ( idselect[0][0] )
                idselect3 = idselect2 + 1
                conn.commit ( )

                cursor.execute ( "INSERT INTO zeiterfassung (id,name, datum) VALUES (?,?,?)" , (idselect3 , name[z] ,date, ) )
                conn.commit ( )
                conn.close ( )



