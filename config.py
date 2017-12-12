import pymysql
import pymysql.cursors


class globals:
    user_dic = {}
    age_list = []
    passenger_discount_list = []
    trip_discount_list = []
    adult_max = 0
    adult_min = 0
    child_max = 0
    child_min = 0
    ticket_dic = {}
    stop = ()


def check_input(string, flag):
    while True:
        value = input(string)
        if value.isnumeric() and int(value) != 0:
            if flag == 1:
                if int(value) == 1 or int(value) == 2 or int(value) == 3:
                    return int(value)
                else:
                    print("---re_enter correct input-----")
            elif flag == 2:
                if 0 < int(value) < 101:
                    return int(value)
                else:
                    print("---re_enter correct input-----")
            elif flag == 0:
                return int(value)
            elif flag == 3:
                if int(value) <= 4:
                    return int(value)
            else:
                print("---re_enter correct input-----")
        else:
            print("---re_enter correct input-----")


def get_source_dest():
    while True:
        globals.stop = ()
        start = check_input("enter the starting point :", 0)
        if 0 < start <= 5:
            stop = check_input("enter the stop point :", 0)
            if 0 < stop <= 5 and start != stop:
                        globals.stop = list(globals.stop)
                        globals.stop.append(start)
                        globals.stop.append(stop)
                        globals.stop = tuple(globals.stop)
                        return 0
            else:
                print("------wrong start and stop inputs-----")
        else:
            print("------input is out of range re_enter again-----")


def passenger_discount(total, total_adult, total_child):
    if "p_disc" in globals.ticket_dic[globals.stop].keys():
        flag = int(globals.ticket_dic[globals.stop]["p_flag"])
        child_flag = 1; adult_flag = 2; total_flag = 3
        if flag == child_flag:
            total -= (total_child*(int(globals.ticket_dic[globals.stop]["p_disc"]))/100)
            return total
        elif flag == adult_flag:
            total -= (total_adult*(int(globals.ticket_dic[globals.stop]["p_disc"]))/100)
            return total
        else:
            total -= (total*(int(globals.ticket_dic[globals.stop]["p_disc"]))/100)
            return total
    return total


def trip_discount(total, total_adult, total_child):
    if "t_disc" in globals.ticket_dic[globals.stop].keys():
        flag = int(globals.ticket_dic[globals.stop]["t_flag"])
        child_flag = 1; adult_flag = 2; total_flag = 3
        if flag == child_flag:
            total -= (total_child*(int(globals.ticket_dic[globals.stop]["t_disc"]))/100)
            return total
        elif flag == adult_flag:
            total -= (total_adult*(int(globals.ticket_dic[globals.stop]["t_disc"]))/100)
            return total
        else:
            total -= (total*(int(globals.ticket_dic[globals.stop]["t_disc"]))/100)
            return total
    return total


def update_to_database(table_name, stop, passenger, flag, val, admin_choice):
    dbh = database_connection()
    try:
        cur = dbh.cursor()
        cur.execute("select * from user_table")
        if admin_choice == "ticket":
            if flag == "remove":
                cur.execute("update " + table_name + " set " + passenger + " = %d where source = %d and destination = %d;"%(val, stop[0], stop[1]))
                print("executing")
            else:
                cur.execute("update " + table_name + " set " + passenger + " = %d where source = %d and destination = %d;"%(val, stop[0], stop[1]))
        elif admin_choice == "t_disc" or admin_choice == "p_disc":
                cur.execute("update " + table_name + " set %s = %d ,%s=%d ,%s=%d where source = %d and destination = %d;" %(passenger[0], val[0], passenger[1], val[1], passenger[2], val[2], stop[0], stop[1]))
        elif admin_choice == "age_limit":
                cur.execute("update %s set min=%d,max=%d where person='%s';" % (table_name, val[0], val[1], "child"))
                cur.execute("update %s set min=%d,max=%d where person='%s';" % (table_name, val[2], val[3], "adult"))
    finally:
        dbh.close()


def database_connection():
    host_name = "localhost"
    user_name = "root"
    database = "project_sql_no_null"
    password = "susmitha1"
    dbh = pymysql.connect(host=host_name, user=user_name, db=database, passwd=password, autocommit=True, cursorclass=pymysql.cursors.DictCursor)
    return dbh


def verify_age_limit():
    while True :
        child_min = check_input("enter the child min age limit :", 2)
        child_max = check_input("enter the child max age limit :", 2)
        adult_min = check_input("enter the adult min age limit :", 2)
        adult_max = check_input("enter the adult max age limit :", 2)
        if (child_min < child_max) and (child_max == (adult_min-1)) and (adult_min < adult_max):
            update_to_database("age_limit", 0, 0, 0, [child_min, child_max, adult_min, adult_max], "age_limit")
            return 0
        else:
            print("********enter correct age limits********")

