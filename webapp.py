from flask import Flask, url_for, render_template, request, Markup, flash
import os
import json

app = Flask(__name__) #__name__ = "__main__" if this is the file that was run.
#Otherwise, it is the name of the file (ex. webapp)
global stateChosen
global departmentChosen

@app.route("/")
def render_main():
    return render_template('home.html')

@app.route("/p1")
def render_page1():
    with open('county_crime.json') as demographics_data:
        counties = json.load(demographics_data)

        if "state" in request.args:
            setStateChosen(request.args["state"])
            return render_template('page1.html', departments_options= sortDepartments(counties,getStateChosen()), stateShow = False, departmentShow=True)

        elif "department" in request.args:
            setDepartmentChosen(request.args["department"])
            return render_template('page1.html', year_options= sortYear(counties,getDepartmentChosen()),departmentShow=False, yearShow=True)

        elif "year" in request.args:
            year=int(request.args["year"])
            this_response = "State chosen: "+getStateChosen()+ " <p> department chosen: "+getDepartmentChosen()+ "</p>" +"<p> year chosen: "+ str(year)+ "</p>"+ "<p> total violent crimes reported: "+str(getCrimeRates(counties,getStateChosen(),getDepartmentChosen(),year))+"</p>"
            return render_template('page1.html', state_options= sortState(counties),response=this_response, yearShow=False, stateShow=True)

        else:
            return render_template('page1.html', state_options= sortState(counties), stateShow=True)



@app.route("/p2")
def render_page2():
    with open('county_crime.json') as demographics_data:
        counties = json.load(demographics_data)
        #might have to make a new sort counties to pass the correct values to the graph.
        if "state" in request.args:
            setStateChosen(request.args["state"])
            #print(getStateChosen())
            return render_template('page2.html', departments_options= sortDepartments(counties,getStateChosen()), stateShow = False, departmentShow=True,counties=counties)

        elif "department" in request.args:
            setDepartmentChosen(request.args["department"])
            #print(getDepartmentChosen())
            return render_template('page2.html', departmentShow=False, stateShow=True, graphShow=True,graphValues=sortGraph(counties,getStateChosen(),getDepartmentChosen()),state_options=sortState(counties))

        else:
            return render_template('page2.html', stateShow=True, graphShow=False, state_options=sortState(counties), department=getDepartmentChosen, state=getStateChosen)


def sortState(counties):
    #the json uses departments instead of counties
    #sort the data by state, then within that the departments within that state
    states= []
    options=""
    for c in counties:
        if c["State"] not in states:
            states.append(c["State"])

            options += Markup("<option value=\"" + c["State"] + "\">" + c["State"] + "</option>")
    return options

def sortDepartments(counties, state):
    department= []
    options=""
    for c in counties:
        if c["Department"] not in department and state==c["State"]:
            department.append(c["Department"])

            options += Markup("<option value=\"" + c["Department"] + "\">" + c["Department"] + "</option>")
    return options

def sortYear(counties, department):
    year= []
    options=""
    for c in counties:
        if c["Year"] not in year and department==c["Department"]:
            year.append(c["Year"])

            options += Markup("<option value=\"" + str(c["Year"]) + "\">" + str(c["Year"]) + "</option>")
    return options

def getCrimeRates(counties,state,department,year):
    crime=""
    for c in counties:
        if department==c["Department"] and c["State"]==state and c["Year"]==year:
            crime=c["Data"]["Rates"]["Violent"]["All"]
            return crime
    return "try again"

def sortGraph(counties,state,department):
    options=""
    finalOptions=""
    departmentFound=False
    printCalled=False
    for c in counties:
        if department==c["Department"] and c["State"]==state:
            options+=Markup(" { label: " + str(c["Year"])+ ",y: " + str(c["Data"]["Rates"]["Violent"]["All"])+"},")
            departmentFound=True
            if printCalled==False:
                print("yay")
                printCalled=True
        elif c["Department"]!=department and departmentFound==True:
        #if options.endsWith(",",beg=0,end=len(options)):
            finalOptions= options[:len(options)-1]
            #print("@@@@@@@@@@@@" + str(finalOptions))

    return finalOptions
def getStateChosen():
    global stateChosen
    #print(stateChosen)
    return stateChosen
def setStateChosen(state):
    global stateChosen
    stateChosen=state
def getDepartmentChosen():
    global departmentChosen
    department=departmentChosen
    return department
def setDepartmentChosen(department):
    global departmentChosen
    departmentChosen=department

if __name__=="__main__":
    #make debug False when you are done with website.
    app.run(debug=False, port=54321)

    '''fun facts:
    1) chart of average crime rate in a given state
    2) crime rate in given county
    3) '''
