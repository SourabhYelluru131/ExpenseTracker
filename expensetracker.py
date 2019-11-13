import pandas as pd
from datetime import datetime, timedelta
import os
import spacy
from dateutil.relativedelta import relativedelta
from dateparser.search import search_dates
from pathlib import Path
password = "password"
my_file = Path("/Users/sourabhyelluru/PycharmProjects/ExpenseTracker/expenserecord.csv")
nlp = spacy.load('en_core_web_sm')
text2int = {"one": 1,
            "two": 2,
            "three": 3,
            "four": 4,
            "five": 5,
            "six": 6,
            "seven": 7,
            "eight": 8,
            "nine": 9,
            "ten": 10}
print("Hello!")
while True:
    # repeating instructions
    print("_________________________________________________________________________________")
    print("What would you like to do?")
    print("1.Record expenses")
    print("2.See expense history")
    print("3.Get particular expense in a particular period")
    print("4.Clear expenses")
    print("5.Quit")
    choice = int(input("Enter your choice of option :"))
    # check if dataframe already exists, if not , creates one
    if my_file.exists():
        df = pd.read_csv("/Users/sourabhyelluru/PycharmProjects/ExpenseTracker/expenserecord.csv")        # Change the address
    else:
        # Dataframe has 3 categories - Time, Category and Amount
        df = pd.DataFrame(columns=["Time", "Category", "Amount"])
        df = df.fillna(0)
    if choice == 1:
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cat = input("Enter the category of expense:")
        amt = float(input("Enter the amount spent:"))
        df_new = pd.DataFrame({'Time': [now],
                               'Category': [cat],
                               'Amount': [amt]})
        frames = [df, df_new]
        result = pd.concat(frames)
        result.to_csv("/Users/sourabhyelluru/PycharmProjects/ExpenseTracker/expenserecord.csv", index=False)
    if choice ==2:
        print(df)
    if choice == 3:
        df['Time'] = pd.to_datetime(df.Time)
        items = []
        query = input()
        # Allow querying using words as dateparser searches only for numbers , else main_time_object ceases to exist
        for a in text2int:
            if a in query:
                query = query.replace(a, str(text2int[a]))
        query.replace("yesterday","last 1 day")
        query.replace("day before yesterday", "last 2 days")
        sconj_perc = ""
        # If main_time_obj exists, take directly, else check for keywords like week, month , year etc
        try:
            main_time_obj = search_dates(query)[0][0]
            begin_time = search_dates(query)[0][1]
        except:
            checklist = ['day', 'days', 'week', 'weeks', 'month', 'months', 'year', 'years', 'fortnight']
            checkflag = 0
            for t in checklist:
                if t in query:
                    checkflag = 1
                    checkword = t
                    break
            if checkflag:
                try:
                    # check if number of periods(day, week, year) is given, else put 1
                    main_time_obj = str(int(query.split()[query.split().index(checkword)-1])) + " " + str(query.split()[query.split().index(checkword)])
                except:
                    try:
                        main_time_obj = "1 " + str(query.split()[query.split().index(checkword)])
                    except:
                        print("Enter correct time period.")
                        break
        doc = nlp(query)
        for t in doc:
            #check for conjugations like "Since"     // NOT COMPLETED
            if t.pos_ == 'SCONJ':
                sconj_perc = t.text
            if sconj_perc == "":
                sconj_perc = None
            if t.pos_ == "NOUN" or t.pos_ == "PROPN":
                if t.dep_ == "pobj" or t.dep_ == "conj":
                    items.append(t.text)
        cardno = 0
        if main_time_obj:
            try:
                cardno = int(main_time_obj.split()[0])
                period = str(main_time_obj.split()[1])
            except:
                # Puts cardno to 1 in the case where main_time_object does not exist . Ex : last week, past year etc
                cardno = 1
                period = None
        else:
            cardno = 0
        # If "since" does not exist in the query ->
        if not sconj_perc:
            if period == "day" or period == "days":
                begin_time = datetime.today() - timedelta(days=cardno)
            elif period == "week" or period == "weeks":
                begin_time = datetime.today() - timedelta(days=7 * cardno)
            elif period == "month" or period == "months":
                begin_time = datetime.today() - relativedelta(months=cardno)
            elif period == "year" or period == "years":
                begin_time = datetime.today() - relativedelta(years=cardno)
            else:
                # Basically display the entire dataframe
                begin_time = "2000-01-01 00:00:01"
            for a in items:
                if df.empty or df.dropna().empty:
                    print("Category {} not found. Either there is NO EXPENDITURE in that Category or check casing and try again!".format(a))
                else:
                    print("_________________________________________________________________________________")
                    print("Category :  {}".format(a))
                    print(df[(df.Time >= begin_time) & (df.Category == a)])
    elif choice == 4:
        entered_password = input("Enter Password:")
        if entered_password != password:
            print("Wrong password")
        else:
            os.remove("/Users/sourabhyelluru/PycharmProjects/ExpenseTracker/expenserecord.csv")
    elif choice == 5:
        print("Bye! See ya ")
        break
    else:
        print("Choose an option between 1 and 5!")