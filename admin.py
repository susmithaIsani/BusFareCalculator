from config import *
from sync_database import *



def admin():
    while(True):
        print("//----------admin----------//")
        print("1.Ticket\n2.Discount\n3.Age Limits\n4.Exit")
        admin_opt = check_input("enter the choice :", 3)
        if (admin_opt == 1):
            ret=get_source_dest()
            if (ret == 0):
                print("1.child cost\n2.adult cost")
                cost_opt = check_input("enter the choice :", 1)
                if (cost_opt == 1):
                    print("1.remove\n2.add")
                    child_opt = check_input("enter the option :", 1)
                    if (child_opt == 1):
                        if "child" in globals.ticket_dic[globals.stop].keys():
                            del(globals.ticket_dic[globals.stop]["child"])
                        else:
                            print("there is no ticket cost for child ")
                    elif(child_opt == 2):
                        cost = check_input("enter the ticket cost for child :", 0)
                        if "child" in globals.ticket_dic[globals.stop].keys():
                            globals.ticket_dic[globals.stop]["child"]=cost
                        else:
                            globals.ticket_dic[globals.stop].update({"child":cost})
                elif(cost_opt == 2):
                    cost = check_input("enter adult cost", 0)
                    globals.ticket_dic[globals.stop]["adult"]=cost
        elif(admin_opt == 2):
            ret=get_source_dest()
            if (ret == 0):
                print("1.Trip Discount\n2.Passenger Discount")
                discount_opt = check_input("enter the choice :", 1)
                if(discount_opt == 1):
                    print("1.remove\n2.add")
                    trip_opt=check_input("enter your choice :",1)
                    if(trip_opt ==1):
                        if "t_disc" in globals.ticket_dic[globals.stop].keys():

                            del(globals.ticket_dic[globals.stop]["t_disc"])
                            del(globals.ticket_dic[globals.stop]["t_count"])
                            del(globals.ticket_dic[globals.stop]["t_flag"])
                        else:
                            print("there is no discount to get removed")
                    else:
                        t_disc=check_input("enter trip discount :",2)
                        t_count=check_input("enter number of trips discount to be given :",0)
                        t_flag=check_input("enter on whom discount to be given :",3)
                        if "t_disc" in globals.ticket_dic[globals.stop].keys():
                            globals.ticket_dic[globals.stop]["t_disc"] = t_disc
                            globals.ticket_dic[globals.stop]["t_count"] = t_count
                            globals.ticket_dic[globals.stop]["t_flag"] = t_flag
                        else:

                            globals.ticket_dic[globals.stop].update({"t_disc":t_disc})
                            globals.ticket_dic[globals.stop].update({"t_count":t_count})
                            globals.ticket_dic[globals.stop].update({"t_flag":t_flag})

                elif(discount_opt == 2):
                    print("1.remove\n2.add")
                    passenger_opt=check_input("enter your choice :",1)
                    if(passenger_opt ==1):
                        if "p_disc" in globals.ticket_dic[globals.stop].keys():

                            del(globals.ticket_dic[globals.stop]["p_disc"])
                            del(globals.ticket_dic[globals.stop]["p_count"])
                            del(globals.ticket_dic[globals.stop]["p_flag"])
                        else:
                            print("there is no discount to get removed")
                    else:


                        p_disc=check_input("enter trip discount :",2)
                        p_count=check_input("enter number of trips discount to be given :",0)
                        p_flag=check_input("enter on whom discount to be given :",3)
                        if "p_disc" in globals.ticket_dic[globals.stop].keys():
                            globals.ticket_dic[globals.stop]["p_disc"] = p_disc
                            globals.ticket_dic[globals.stop]["p_count"] = p_count
                            globals.ticket_dic[globals.stop]["p_flag"] = p_flag
                        else:

                            globals.ticket_dic[globals.stop].update({"p_disc":p_disc})
                            globals.ticket_dic[globals.stop].update({"p_count":p_count})
                            globals.ticket_dic[globals.stop].update({"p_flag":p_flag})
        elif admin_opt == 3:
            verify_age_limit()
            sync_from_age()
        else:
             break










