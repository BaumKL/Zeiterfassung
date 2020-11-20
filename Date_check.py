import datetime
import sqlite3
import main


if __name__ == '__main__':
    while 1 == 1:
        date = (datetime.datetime.now ( ).strftime ( "%A  %d.%m.%Y" ))
        time = (datetime.datetime.now ( ).strftime ( "%H:%M" ))
        for z in range( len( main.name ) ):
            if time == "23:59":
                conn = sqlite3.connect ( 'datenbank.db' )
                cursor = conn.cursor ( )
                cursor.execute ( "SELECT count(*) FROM zeiterfassung WHERE name == ? " , (main.name[z],) )
                counter_sel_zeiterfassung_name_bedinung = cursor.fetchall ( )
                counter_sel_zeiterfassung_name_bedinung = counter_sel_zeiterfassung_name_bedinung[0][0]
                conn.commit ( )

                if counter_sel_zeiterfassung_name_bedinung == 0 :


                    cursor.execute ( "SELECT COUNT(*) FROM zeiterfassung" )
                    counter_sel_zeiterfassung = cursor.fetchall ( )
                    counter_sel_zeiterfassung = int ( counter_sel_zeiterfassung[0][0] )
                    counter_sel_zeiterfassung = counter_sel_zeiterfassung + 1
                    conn.commit ( )

                    cursor.execute ( "INSERT INTO zeiterfassung (id,name, datum) VALUES (?,?,?)" , (counter_sel_zeiterfassung , main.name[z] , date,) )
                    conn.commit ( )
                    conn.close ( )



