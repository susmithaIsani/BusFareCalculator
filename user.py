from config import *
from math import ceil
from sync_database import *


def user():
    child_min = globals.child_min
    child_max = globals.child_max
    adult_min = globals.adult_min
    adult_max = globals.adult_max
    while (True):
        print("1.sign up\n2.Log in\n3.Exit")
        user_opt = check_input("enter the option :", 1)
        if(user_opt == 3):
            break;
        else:
            name = input("Name : ")
            if ((user_opt == 1 and (name in globals.user_dic.keys()))):
                print("name already exist")
            elif (user_opt == 2 and (name not in globals.user_dic.keys())):
                print("please sign up")
            elif(user_opt == 3):
                break;
            else:
                if (user_opt == 1):
                    globals.user_dic.update({name: {(-1, -1): 0}})
                total = 0;
                child_price = 0;
                adult_price = 0;
                total_adult = 0;
                total_child = 0
                ret = get_source_dest()
                if (ret == 0):
                    no_of_tickets = check_input("enter the number of passengers :", 0)
                    for num in range(no_of_tickets):
                        age = check_input("enter your age :", 2)
                        if (age > 0 and age < 100):
                            if (age > adult_min and age < adult_max):
                                adult_price = int(globals.ticket_dic[globals.stop]["adult"])
                                total_adult = total_adult + adult_price
                            elif (age > adult_max):
                                adult_price = int(globals.ticket_dic[globals.stop]["adult"])
                                adult_price = (adult_price / 2)
                                total_adult = total_adult + adult_price
                            elif (age <= child_min):
                                print("Free ticket")
                                child_price = 0
                                total_child = total_child + child_price
                            elif (age < child_max):
                                if "t_child" in globals.ticket_dic[globals.stop].keys():
                                    child_price = int(globals.ticket_dic[globals.stop]["child"])
                                else:
                                    child_price = int(globals.ticket_dic[globals.stop]["adult"])
                                    child_price = child_price/2
                                    total_child = total_child + ceil((child_price))
                    total = total_adult + total_child
                    print("total adult cost= ", total_adult)
                    print("total child cost= ", total_child)
                    print("Total Ticket cost=", total)
                    stops_LocalTuple = ()
                    stops_LocalTuple = globals.stop
                    if (-1, -1) in globals.user_dic[name].keys():
                        del [globals.user_dic[name][(-1, -1)]]
                        globals.user_dic[name].update({stops_LocalTuple: 1})
                    elif stops_LocalTuple in globals.user_dic[name].keys():
                        globals.user_dic[name][stops_LocalTuple] += 1
                    else:
                        globals.user_dic[name].update({stops_LocalTuple: 1})

                    if "p_disc" in globals.ticket_dic[globals.stop].keys():
                        if( (globals.user_dic[name][globals.stop] % int(globals.ticket_dic[globals.stop]["p_count"])) == 0):
                            total = passenger_discount(total,total_adult,total_child)
                    if "t_disc" in globals.ticket_dic[globals.stop].keys():
                        if( no_of_tickets >= int(globals.ticket_dic[globals.stop]["t_count"])):
                            total=trip_discount(total,total_adult,total_child)
                    if(total < 0):
                        total=0;
                    print("Total cost after discount = " , total)
                    sync_to_user()
