import socket
import pymysql
from datetime import datetime

class booking_system_serverside():
    def __init__(self):
        s = socket.socket()
        print ("Socket created")
        port = 9000

        s.bind(('', port))
        print ("socket binded: %s" %(port))


        s.listen(5)
        print ("socket listening")

        while True:
            c, addr = s.accept()
            print ('Got connection from', addr )

            option = (c.recv(1024).decode("utf-8"))
            print(option)

            if option == "test":

                test_value = []
                self.database_test(test_value)
                reply = str(addr) + 'Thank you for connecting' + str(test_value[0])
                c.send(reply.encode('utf-8'))
                c.close()

            elif option == "login":

                reply = 'OK'
                c.send(reply.encode('utf-8'))

                input_username = (c.recv(1024).decode("utf-8"))
                reply2 = 'input_username received'
                c.send(reply2.encode('utf-8'))
                input_pw = (c.recv(1024).decode("utf-8"))

                #print(input_username)
                #print(input_pw)

                login_reply = ""
                reply3 = str(self.login_check(input_username,input_pw,login_reply))

                #print(reply3)
                c.send(reply3.encode('utf-8'))

                c.close()

            elif option == "timeslot_display":
                reply = 'OK'
                c.send(reply.encode('utf-8'))

                input_date = (c.recv(1024).decode("utf-8"))

                timeslot_reply=''
                reply2 = str(self.timeslot_check(input_date,timeslot_reply))
                c.send(reply2.encode('utf-8'))

                c.close()

            elif option == "confirm_booking":
                reply = 'OK'
                c.send(reply.encode('utf-8'))

                selected_id = (c.recv(1024).decode("utf-8"))
                print(selected_id)

                reply2 = 'id received'
                c.send(reply2.encode('utf-8'))

                confirmed_username = (c.recv(1024).decode("utf-8"))
                print(confirmed_username)



                booking_reply=''
                reply3 = str(self.booking_apply(input_date,selected_id,confirmed_username,booking_reply))
                c.send(reply3.encode('utf-8'))

                c.close()

            elif option == "booking_history":
                reply = 'OK'
                c.send(reply.encode('utf-8'))

                confirmed_username = (c.recv(1024).decode("utf-8"))
                print(confirmed_username)

                history_reply = ''
                history_reply = str(self.booking_check(confirmed_username, history_reply))

                c.send(history_reply.encode('utf-8'))
                c.close()
            elif option == "cancel_booking":
                reply = 'OK'
                c.send(reply.encode('utf-8'))

                confirmed_booking_id = (c.recv(1024).decode("utf-8"))
                print(confirmed_booking_id)

                cancel_reply = ''
                cancel_reply = str(self.cancel_booking(confirmed_booking_id, cancel_reply))
                c.send(cancel_reply.encode('utf-8'))
                c.close()
            else:
                c.close()

    def database_test(self,test_value):
        try:
            connection = pymysql.connect(user='root',
                                         password='',
                                         db='comp5327test',
                                         cursorclass=pymysql.cursors.DictCursor)
            with connection.cursor() as cursor:
                found = False
                cursor.execute('''SELECT * FROM User WHERE 1 ''')
                for e in cursor.fetchall():
                    test_value.append(e)
                    #print(e)
                connection.close
                return test_value
        except NameError as error:
            pass

    def login_check(self,input_username,input_pw,login_reply):
        try:
            connection = pymysql.connect(user='root',
                                         password='',
                                         db='comp5327test',
                                         cursorclass=pymysql.cursors.DictCursor)
            with connection.cursor() as cursor:
                #print(login_reply)
                sql = '''SELECT Password FROM User WHERE Username = "'''+str(input_username)+'''"'''
                cursor.execute(sql)

                for e in cursor.fetchall():
                    #print(e)
                    str_e = str(e)

                length_e = len(str_e)
                #print(length_e)
                #print(str_e[14:length_e-2])
                valid_pw = (str_e[14:length_e-2])

                if valid_pw == str(input_pw):
                    #print("test")
                    login_reply = "True"
                else:
                    login_reply = "False"
                #print(login_reply)
                connection.close()
                return login_reply
        except NameError as error:
            pass

    def timeslot_check(self,input_date,timeslot_reply,):
        try:
            connection = pymysql.connect(user='root',
                                         password='',
                                         db='comp5327test',
                                         cursorclass=pymysql.cursors.DictCursor)
            with connection.cursor() as cursor:
                sql = '''SELECT Slot_id, time_slot FROM Timeslot WHERE date = "''' + str(input_date) + '''" and vacancy > 0'''
                cursor.execute(sql)

                str_e = ''

                for e in cursor.fetchall():
                    #print(e)
                    str_e += str(e)

                print(str_e)
                connection.close()
                timeslot_reply = str_e
                return timeslot_reply
            pass
        except NameError as error:
            pass

    def booking_apply(self,input_date,selected_id,confirmed_username,booking_reply):
        try:
            connection = pymysql.connect(user='root',
                                         password='',
                                         db='comp5327test',
                                         cursorclass=pymysql.cursors.DictCursor)
            with connection.cursor() as cursor:
                sql = '''SELECT vacancy FROM Timeslot WHERE Slot_id = "''' + str(selected_id) + '''"'''
                cursor.execute(sql)

                str_e = ''

                for e in cursor.fetchall():
                    #print(e)
                    str_e += str(e)

                #print(str_e)
                connection.close()

                i=0
                location_a=0
                while i < len(str_e):
                    if str_e[i] == ':':
                        location_a = i
                    i+=1

                #print(str_e[location_a+2:len(str_e)-1])

                if int(str_e[location_a+2:len(str_e)-1]) > 0:
                    connection2= pymysql.connect(user='root',
                                                 password='',
                                                 db='comp5327test',
                                                 cursorclass=pymysql.cursors.DictCursor)
                    with connection2.cursor() as cursor:
                        sql2 = '''SELECT booking_id from Booking where Slot_id = "''' + str(selected_id) +'''" and Cancel = "" and Username = "''' + str(confirmed_username) + '''"'''
                        cursor.execute(sql2)

                        str_e2 = ''

                        for e in cursor.fetchall():
                            # print(e)
                            str_e2 += str(e)
                        print(str_e2)
                        connection2.close()
                        if str_e2 == '':

                            now = datetime.now()
                            current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
                            # print("date and time:", current_date_time)

                            connection3 = pymysql.connect(user='root',
                                                          password='',
                                                          db='comp5327test',
                                                          cursorclass=pymysql.cursors.DictCursor)
                            with connection3.cursor() as cursor:
                                sql3 = '''INSERT INTO `Booking` (`booking_id`, `Slot_id`, `Username`, `apply_date_time`, `Cancel`, `Cancel_date_time`) VALUES (NULL, "''' + str(selected_id) + '''" , "''' + str(confirmed_username) + '''" , "''' + str(current_date_time) + '''" , "", "")'''
                                cursor.execute(sql3)
                                connection3.commit()
                                connection3.close()

                            connection4 = pymysql.connect(user='root',
                                                          password='',
                                                          db='comp5327test',
                                                          cursorclass=pymysql.cursors.DictCursor)
                            new_vacancy = int(str_e[location_a + 2:len(str_e) - 1]) - 1
                            with connection4.cursor() as cursor:
                                sql4 = '''UPDATE TImeslot SET vacancy = ''' + str(new_vacancy) + ''' where slot_id =  "''' + str(selected_id) + '''"'''
                                cursor.execute(sql4)
                                connection4.commit()
                                connection4.close()

                            booking_reply = "done"
                        else:
                            booking_reply = "already"
                else:
                    booking_reply = "full"
                return booking_reply
            pass
        except NameError as error:
            pass

    def booking_check(self, confirmed_username,history_reply):
        try:
            connection = pymysql.connect(user='root',
                                         password='',
                                         db='comp5327test',
                                         cursorclass=pymysql.cursors.DictCursor)
            with connection.cursor() as cursor:
                sql = '''SELECT Booking.booking_id, Booking.Slot_id, Booking.apply_date_time, Timeslot.date, Timeslot.time_slot, Booking.Cancel, Booking.Cancel_date_time FROM Booking Inner Join Timeslot on Booking.Slot_id=Timeslot.Slot_id WHERE Username = "''' + str(confirmed_username) + '''" order by Booking.booking_id DESC'''
                cursor.execute(sql)

                str_e = ''

                for e in cursor.fetchall():
                    #print(e)
                    str_e += str(e)
                connection.close()
                print(str_e)
                history_reply= str_e
                return history_reply
        except NameError as error:
            pass

    def cancel_booking(self, confirmed_booking_id, cancel_reply):
        try:
            connection = pymysql.connect(user='root',
                                         password='',
                                         db='comp5327test',
                                         cursorclass=pymysql.cursors.DictCursor)
            with connection.cursor() as cursor:
                sql = '''SELECT Slot_id FROM Booking WHERE booking_id = "''' + str(confirmed_booking_id) + '''"'''
                cursor.execute(sql)

                str_e = ''

                for e in cursor.fetchall():
                    # print(e)
                    str_e += str(e)

                #print(str_e[12:len(str_e)-1])
                connection.close()
            if str_e != '':
                now = datetime.now()
                current_date = str(now.strftime("%Y-%m-%d %H:%M:%S"))

                connection2 = pymysql.connect(user='root',password='',db='comp5327test',cursorclass=pymysql.cursors.DictCursor)
                with connection2.cursor() as cursor:
                    sql2 = '''UPDATE Booking set Cancel = "Yes", Cancel_date_time = "''' + str(current_date) + '''" WHERE booking_id = ''' + str(confirmed_booking_id)
                    cursor.execute(sql2)
                    connection2.commit()
                    connection2.close()

                connection3 = pymysql.connect(user='root', password='', db='comp5327test',
                                            cursorclass=pymysql.cursors.DictCursor)
                with connection3.cursor() as cursor:
                    sql3 = '''SELECT vacancy FROM Timeslot WHERE Slot_id = ''' + str(str_e[12:len(str_e)-1])
                    cursor.execute(sql3)

                    str_e2 = ''

                    for e in cursor.fetchall():
                        # print(e)
                        str_e2 += str(e)


                    print(str_e2[12:(len(str_e2)-1)])
                    connection3.close()

                connection4 = pymysql.connect(user='root', password='', db='comp5327test',
                                                cursorclass=pymysql.cursors.DictCursor)
                with connection4.cursor() as cursor:
                    sql4 = '''UPDATE Timeslot SET vacancy = ''' + str(int(str_e2[12:len(str_e2)-1])+1) + ''' WHERE Slot_id = ''' + str(str_e[12:len(str_e)-1])
                    cursor.execute(sql4)
                    connection4.commit()
                    connection4.close()

                    cancel_reply = 'Done'
            else:
                cancel_reply = 'error'
            return cancel_reply
        except NameError as error:
            pass


if __name__ == "__main__":
    booking_system_serverside()



