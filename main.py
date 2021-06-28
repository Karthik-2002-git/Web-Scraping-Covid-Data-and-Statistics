import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as soup
from datetime import date, datetime
from urllib.request import Request, urlopen
import time
from tkinter import *
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

def web_scraper():
    url="https://www.worldometers.info/coronavirus/"
    req=Request(url,headers={"User-agent":"Mozilla/5.0"})
    webpage=urlopen(req)
    page_soup=soup(webpage,"html.parser")
    table=page_soup.findAll("table",{"id":"main_table_countries_today"})
    containers=table[0].findAll('tr',{'style':""})
    title=containers[0]
    all_data=[]
    clean= True
    for country in containers:
        country_data=[]
        country_container=country.findAll('td')


        for i in range(1,len(country_container)):
            final_feature=country_container[i].text
            if clean:
                if i!=1 and i!= len(country_container)-1:
                    final_feature=final_feature.replace(",","")

                    if final_feature.find("+")!=-1:
                        final_feature=final_feature.replace("+","")
                        final_feature=float(final_feature)
                    elif final_feature.find("-")!=-1:
                        final_feature=final_feature.replace("-","")
                        final_feature=float(final_feature)
            if final_feature=="N\A":
                final_feature=0
            elif final_feature == "" or final_feature == " ":
                final_feature = -1
            country_data.append(final_feature)

        all_data.append(country_data)
    df=pd.DataFrame(all_data)
    df.drop([15,16,17,18,19,20],inplace= True, axis = 1)
    df.head()

    col_labels=["Country","Total Cases","New Cases","Total Deaths","New Deaths","Total Recovered","New Recovered","Active Cases","Critical","Total Cases/1M","Deaths/1M","Total Tests","Tests/1M","Population","Continent"]
    df.columns=col_labels
    #print(df)
    df.to_csv('covid stats.csv')



def quote():
    global win1
    win1 = Tk()
    win1.geometry("600x400")
    win1.resizable(False, False)
    win1.configure(bg="black")
    text1 = Label(win1, text="We  are  in  this  Together - \nand we will get through this,\nTogether",
                  font=("Times", 30, "bold italic"))
    text1.place(relx=0.5, rely=0.5, anchor='center')
    text1.config(fg="white")
    text1.config(bg="black")

    win1.after(3500, lambda: home())
    win1.mainloop()


def home():
    win1.destroy()
    win2 = Tk()
    win2.title('Plotting in Tkinter')
    win2.geometry("600x400")
    win2.resizable(False, False)
    win2.configure(bg="black")

    l1 = Label(win2, text="Select/Enter country  - ", font=("Arial", 15, "bold"))
    l1.config(fg="white")
    l1.config(bg="black")
    l1.place(x=80, y=100)

    n = StringVar()
    select_country = ttk.Combobox(win2, width=20, textvariable=n, font=("Arial", 13))

    global countries_list
    countries_list = countries()

    select_country['values'] = tuple(countries_list)
    select_country.place(x=310, y=105)
    select_country.current(countries_list.index("India"))

    fetch_data = Button(win2, command=lambda: show_data(n.get()), text="Show Data", width=10, font=("Arial", 15))
    fetch_data.place(x=60, y=190)

    plot_graph = Button(win2, command=lambda: plot_data(n.get()), text="Plot Graph", width=10, font=("Arial", 15))
    plot_graph.place(x=240, y=190)

    reload = Button(win2, command=lambda: web_scraper(), text="Reload", width=10, font=("Arial", 15))
    reload.place(x=420, y=190)

    credits= Label(win2, text="Credits -  \"Worldometers\"", font=("Arial", 15, "bold"))
    credits.place(x=175, y=300)
    credits.config(fg="navajo white")
    credits.config(bg="black")
    win2.mainloop()


def to_roundedoff_string(x):
    x = str(x)
    if len(x) == 3 or (len(x) == 4 and x[2] == '.'):
        x += '0'
    x += '%'
    return x


def fetch_data(country, operation):
    df = pd.read_csv('covid stats.csv')
    for x in df.index:

        if df.loc[x, "Country"] == country:

            cases = int(df.loc[x, "Total Cases"])
            population = int(df.loc[x, "Population"])
            deaths = int(df.loc[x, "Total Deaths"])
            recovered = int(df.loc[x, "Total Recovered"])
            active = int(df.loc[x, "Active Cases"])

            if operation == "plot_data":
                return cases, population, deaths, recovered, active
            if operation == "show_data":
                country = str(df.loc[x, "Country"])
                new_cases = int(df.loc[x, "New Cases"])
                new_deaths = int(df.loc[x, "New Deaths"])
                new_recovered = int(df.loc[x, "New Recovered"])
                critical = int(df.loc[x, "Critical"])
                cases_1M = int(df.loc[x, "Total Cases/1M"])
                deaths_1M = int(df.loc[x, "Deaths/1M"])
                total_tests = int(df.loc[x, "Total Tests"])
                tests_1M = int(df.loc[x, "Tests/1M"])
                continent = str(df.loc[x, "Continent"])
                return country, cases, new_cases, deaths, new_deaths, recovered, new_recovered, active, critical, cases_1M, deaths_1M, total_tests, tests_1M, population, continent


def plot_data(country):
    if country not in countries_list:
        print("No match")
        return

    cases, population, deaths, recovered, active = fetch_data(country, "plot_data")

    if cases == -1 or population == -1 or deaths == -1 or recovered == -1 or active == -1:  # -1 denotes the unavailability of data
        print("Data unavailable")
        return

    data1 = np.array([cases, population - cases])
    data2 = np.array([deaths, recovered, active])

    case_percent = round((cases / population) * 100, 2)
    unaffected_percent = round(((population - cases) / population) * 100, 2)
    death_percent = round((deaths / cases) * 100, 2)
    recovered_percent = round((recovered / cases) * 100, 2)
    active_percent = round((active / cases) * 100, 2)

    case_percent = to_roundedoff_string(case_percent)
    unaffected_percent = to_roundedoff_string(unaffected_percent)
    death_percent = to_roundedoff_string(death_percent)
    recovered_percent = to_roundedoff_string(recovered_percent)
    active_percent = to_roundedoff_string(active_percent)

    labels1 = [case_percent, unaffected_percent]
    labels2 = [death_percent, recovered_percent, active_percent]

    colors1 = ["orange", "darkblue"]
    colors2 = ["red", "forestgreen", "gold"]

    labels1_explode = [0.2, 0]
    labels2_explode = [0.2, 0, 0]

    # create a figure with two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2)

    # plot each pie chart in a separate subplot
    ax1.pie(data1, labels=labels1, explode=labels1_explode, colors=colors1, startangle=0)
    ax2.pie(data2, labels=labels2, explode=labels2_explode, colors=colors2, startangle=10)
    ax1.legend(["Total Cases", "Unaffected"], loc='lower center', bbox_to_anchor=(0.45, -0.25), ncol=1)
    ax2.legend(["Deaths", "Recovered", "Active Cases"], loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=1)
    plt.show()


def countries():
    df = pd.read_csv('covid stats.csv')
    l = []
    for x in df.index:
        if df.loc[x, "Country"] == df.loc[x, "Country"] and df.loc[x, "Country"] != "Total:":  # removing NaN
            l.append(df.loc[x, "Country"])
    l.sort()
    return l


def show_data(country):
    if country not in countries_list:
        print("No match")
        return

    country, total_cases, new_cases, total_deaths, new_deaths, total_recovered, new_recovered, active_cases, critical, cases_1M, deaths_1M, total_tests, tests_1M, population, continent = fetch_data(
        country, "show_data")

    if str(total_cases)=="-1":
        total_cases="N/A"
    if str(new_cases)=="-1":
        new_cases="N/A"
    if str(total_deaths) == "-1":
        total_deaths = "N/A"
    if str(new_deaths) == "-1":
        new_deaths = "N/A"
    if str(total_recovered) == "-1":
        total_recovered = "N/A"
    if str(new_recovered)=="-1":
        new_recovered="N/A"
    if str(active_cases)=="-1":
        active_cases="N/A"
    if str(critical)=="-1":
        critical="N/A"
    if str(cases_1M)=="-1":
        cases_1M="N/A"
    if str(deaths_1M)=="-1":
        deaths_1M="N/A"
    if str(total_tests)=="-1":
        total_tests="N/A"
    if str(tests_1M)=="-1":
        tests_1M="N/A"
    if str(population)=="-1":
        population="N/A"
    if str(continent)=="-1":
        continent="N/A"


    win3 = Tk()
    win3.title('Data')
    win3.geometry("600x400")
    win3.resizable(False, False)
    win3.configure(bg="black")

    l0 = Label(win3, text=country.upper() + "(" + continent + ")", font=("Arial", 15, "bold"))
    l0.config(fg="white")
    l0.config(bg="black")
    l0.place(x=120, y=20)

    l1 = Label(win3, text="Population - " + str(population), font=("Arial", 13, "bold"))
    l1.config(fg="white")
    l1.config(bg="black")
    l1.place(x=120, y=55)

    l2 = Label(win3, text="Total Cases - " + str(total_cases), font=("Arial", 13, "bold"))
    l2.config(fg="white")
    l2.config(bg="black")
    l2.place(x=120, y=75)

    l3 = Label(win3, text="New Cases - " + str(new_cases), font=("Arial", 13, "bold"))
    l3.config(fg="white")
    l3.config(bg="black")
    l3.place(x=120, y=95)

    l4 = Label(win3, text="Total Deaths - " + str(total_deaths), font=("Arial", 13, "bold"))
    l4.config(fg="white")
    l4.config(bg="black")
    l4.place(x=120, y=130)

    l5 = Label(win3, text="New Deaths - " + str(new_deaths), font=("Arial", 13, "bold"))
    l5.config(fg="white")
    l5.config(bg="black")
    l5.place(x=120, y=150)

    l6 = Label(win3, text="Total Recovered - " + str(total_recovered), font=("Arial", 13, "bold"))
    l6.config(fg="white")
    l6.config(bg="black")
    l6.place(x=120, y=185)

    l7 = Label(win3, text="New Recovered - " + str(new_recovered), font=("Arial", 13, "bold"))
    l7.config(fg="white")
    l7.config(bg="black")
    l7.place(x=120, y=205)

    l8 = Label(win3, text="Active Cases - " + str(active_cases), font=("Arial", 13, "bold"))
    l8.config(fg="white")
    l8.config(bg="black")
    l8.place(x=120, y=240)

    l9 = Label(win3, text="Critical - " + str(critical), font=("Arial", 13, "bold"))
    l9.config(fg="white")
    l9.config(bg="black")
    l9.place(x=120, y=260)

    l10 = Label(win3, text="Cases/1M - " + str(cases_1M), font=("Arial", 13, "bold"))
    l10.config(fg="white")
    l10.config(bg="black")
    l10.place(x=120, y=295)

    l11 = Label(win3, text="Deaths/1M - " + str(deaths_1M), font=("Arial", 13, "bold"))
    l11.config(fg="white")
    l11.config(bg="black")
    l11.place(x=120, y=315)

    l12 = Label(win3, text="Total Tests - " + str(total_tests), font=("Arial", 13, "bold"))
    l12.config(fg="white")
    l12.config(bg="black")
    l12.place(x=120, y=350)

    l13 = Label(win3, text="Tests/1M - " + str(tests_1M), font=("Arial", 13, "bold"))
    l13.config(fg="white")
    l13.config(bg="black")
    l13.place(x=120, y=370)

    win3.mainloop()

web_scraper()
quote()


