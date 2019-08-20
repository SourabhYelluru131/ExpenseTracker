import pandas as pd
from datetime import datetime, timedelta
import os
import dateutil.relativedelta as relativedelta
from pathlib import Path
my_file = Path("/Users/sourabhyelluru/PycharmProjects/ExpenseTracker/expenserecord.csv")
text2int = {"one":1,
            "two":2,
            "three":3,
            "four":4,
            "five":5,
            "six":6,
            "seven":7,
            "eight":8,
            "nine":9,
            "ten":10}
print("Hello!")
while(True):
    print("What would you like to do?")
    print("1.Record expenses")
    print("2.See expense history")
    print("3.Get particular expense")
    print("4.Clear expenses")
    print("5.Quit")
    choice = int(input("Enter your choice of option :"))
    if my_file.exists():
        df = pd.read_csv("expenserecord.csv")
    else:
        df = pd.DataFrame(columns = ["Time","Category","Amount"])
    if choice ==1:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cat = input("Enter the category of expense:")
        amt = float(input("Enter the amount spent:"))
        df.append(pd.Series([now,cat,amt],index= df.columns),ignore_index = True)
        df.to_csv("/Users/sourabhyelluru/PycharmProjects/ExpenseTracker/expenserecord.csv")
    if choice ==2:
        print(df)
    if choice ==3:
        query = input("Query:")
        querylist = query.split(" ")
        flag = 0
        try:
            index = querylist.index("spent")
        except:
            index = querylist.index("spend")
        if querylist[index+3 ]== "and":
            flag = 1
        if flag == 0:
            category = querylist[index+2]
            if category in df.columns:
                cardno = text2int[querylist[index+6]]        #Takes in the number of time periods , ex: "one" week, "two" months etc.
                period = querylist[index+7]
                if period == "week" or period=="weeks":
                    timebegin = datetime.today() - timedelta(days= 7*cardno)
                if period == "month" or period == "months":
                    timebegin = datetime.today() - relativedelta(months= cardno)
                if period == "year" or period == "years":
                    timebegin = datetime.today() - relativedelta(years=cardno)
                else:
                    timebegin = 0
                print(df[df.Time >= timebegin])
            else:
                print("Error 404! Category {} not found! Try other categories".format(category))
            if flag == 1:
                category1 = querylist[index + 2]
                category2 = querylist[index+4]
                if category1 in df.columns:
                    if category2 in df.columns:
                        cardno = text2int[
                            querylist[index + 6]]  # Takes in the number of time periods , ex: "one" week, "two" months etc.
                        period = querylist[index + 7]
                        if period == "week" or period == "weeks":
                            timebegin = datetime.today() - timedelta(days=7 * cardno)
                        if period == "month" or period == "months":
                            timebegin = datetime.today() - relativedelta(months=cardno)
                        if period == "year" or period == "years":
                            timebegin = datetime.today() - relativedelta(years=cardno)
                        else:
                            timebegin = 0
                        print(df[df.Time >= timebegin])
                    else:
                        print("Error 404! Category {} not found! Try other categories".format(category2))
                else:
                    print("Error 404! Category {} not found! Try other categories".format(category1))
    elif choice == 4:
        os.remove("/Users/sourabhyelluru/PycharmProjects/ExpenseTracker/expenserecord.csv")
    elif choice == 5:
        print("Bye! See ya ")
        break