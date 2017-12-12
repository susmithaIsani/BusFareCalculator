import pymysql
import pymysql.cursors
from config import *



def sync_from_main():
    ticket_dic = {}
    keys = ["adult","child","t_disc","t_count","t_flag","p_disc","p_count","p_flag"]
    items = ["fare","discount","number","flag"]
    dbh = database_connection()
    cur = dbh.cursor()
    cur.execute("select stops.id,stops.source,stops.dest,ticket_fare.passenger, ticket_fare.fare,discounts.discount_type,discounts.discount,discounts.number,discounts.flag  from stops INNER JOIN ticket_fare ON ticket_fare.id = stops.id LEFT JOIN discounts ON discounts.id = stops.id;")
    for row in cur.fetchall():
        start=0;end=0
        sub_dic = {}
        sub_dic.update({keys[keys.index(row["passenger"])]:row["fare"]})
        stops=()
        stops=(row["source"],row["dest"])
        if(row["discount_type"] == "p_disc"):
            start=5;end=len(keys)
        elif(row["discount_type"] == "t_disc"):
            start=2;end=5
        if(start and end):
            for key,val in zip(range(start,end),range(1,len(items))):
                sub_dic.update({keys[key]:row[items[val]]})
        if stops in ticket_dic.keys():
            for k,v in sub_dic.items():
                ticket_dic[(row["source"],row["dest"])].update({k:v})
        else:
            ticket_dic.update({stops:sub_dic})
    globals.ticket_dic=ticket_dic
    dbh.close()

def sync_to_main():
    dbh=database_connection()
    cur=dbh.cursor()
    cur.execute("delete from ticket_fare")
    cur.execute("delete from discounts")
    for k,v in globals.ticket_dic.items():
        if "p_disc" in v.keys():
            cur.execute("insert into discounts values((select id from stops where source=%d and dest = %d),'%s',%d,%d,%d);"%(k[0],k[1],"p_disc",v["p_disc"],v["p_count"],v["p_flag"]))
        if "t_disc" in v.keys():
            cur.execute("insert into discounts values((select id from stops where source=%d and dest = %d),'%s',%d,%d,%d);" % (k[0], k[1], "t_disc", v["t_disc"], v["t_count"], v["t_flag"]))
        if "adult" in v.keys():
            cur.execute("insert into ticket_fare values((select id from stops where source=%d and dest = %d),'%s',%d);"%(k[0],k[1],"adult",v["adult"]))
        if "child" in v.keys():
            cur.execute("insert into ticket_fare values((select id from stops where source=%d and dest = %d),'%s',%d);" % (k[0], k[1], "child", v["child"]))

    dbh.close()

def sync_to_user():
    dbh=database_connection()
    cur=dbh.cursor()
    cur.execute("delete from user_table;")
    user_dic=globals.user_dic
    for k,v in user_dic.items():
        for k1,v1 in v.items():
            cur.execute("insert into user_table values('%s',%d,%d,%d);"%(k,k1[0],k1[1],v1))
    dbh.close()

def sync_from_user():
        globals.user_dic = {}
        dbh = database_connection()
        cur = dbh.cursor()
        cur.execute("select * from user_table")

        for sub_dict in cur.fetchall():
            name = sub_dict["name"]
            stop = (sub_dict["source"], sub_dict["dest"])
            count = sub_dict["count"]
            if name in globals.user_dic.keys():
                (globals.user_dic[name].update({stop: count}))
            else:
                globals.user_dic.update({name: {stop: count}})
        dbh.close()


def sync_from_age():
    dbh = database_connection()
    cur = dbh.cursor()
    cur.execute("select * from age_limit")
    row = cur.fetchall()
    globals.child_min = row[0]["min"]; globals.child_max = row[0]["max"]
    globals.adult_min = row[1]["min"]; globals.adult_max = row[1]["max"]
    dbh.close()


'''if __name__ == "__main__":
    dbh = pymysql.connect(host=host_name,user=user_name,db=database,passwd=password,autocommit=True,cursorclass=pymysql.cursors.DictCursor)
    sync_from_main(dbh)
    sync_from_user(dbh)
    dbh.close()'''