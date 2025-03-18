# MAKING GRAPHS IN PYTHON WITH DATA FROM FIREBASE
 
import plotly.graph_objects as go #importing graphing module (plotly)
 
#linking to database
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
 
cred = credentials.Certificate("leaving-cert-database-a27d6-firebase-adminsdk-fbsvc-7c9e2b0b52.json")
firebase_admin.initialize_app(cred, {'databaseURL':'https://leaving-cert-database-a27d6-default-rtdb.europe-west1.firebasedatabase.app/'})
 
ref = db.reference("/years") # create a reference to extract data from it
years = ref.get() #take the values from the reference and store in a dictionary
 
 
 
#------------------------------------------------------------------------creating functions to print the graphs-----------------------------------------------------------------------------------------------------
 
 

def average(l):
    ttl = 0
    for x in l:
         ttl += x
    return(ttl/len(l))
 
def all_years_stats(years,typ):
    disorders_list = [ [],[],[],[],[] ]
    for x in years:
        if typ == 'World':
            for k,v in years[x]['World'].items():
                if 'disorders' in k:
                    if 'anxiety' in k.lower():
                        disorders_list[0].append(v)
                    elif 'bipolar' in k.lower():
                        disorders_list[1].append(v)
                    elif 'depre' in k.lower():
                        disorders_list[2].append(v)
                    elif 'eat' in k.lower():
                        disorders_list[3].append(v)
                    else:
                        disorders_list[4].append(v)
        elif typ != 'World':
            if typ in allcountries:
                for k,v in years[x]['Countries'][typ].items():
                    if 'disorders' in k:
                        if 'anxiety' in k.lower():
                            disorders_list[0].append(v)
                        elif 'bipolar' in k.lower():
                            disorders_list[1].append(v)
                        elif 'depre' in k.lower():
                            disorders_list[2].append(v)
                        elif 'eat' in k.lower():
                            disorders_list[3].append(v)
                        else:
                            disorders_list[4].append(v)
            elif typ in allcontinents:
                for k,v in years[x]['Continents'][typ].items():
                    if 'disorders' in k:
                        if 'anxiety' in k.lower():
                            disorders_list[0].append(v)
                        elif 'bipolar' in k.lower():
                            disorders_list[1].append(v)
                        elif 'depre' in k.lower():
                            disorders_list[2].append(v)
                        elif 'eat' in k.lower():
                            disorders_list[3].append(v)
                        else:
                            disorders_list[4].append(v)
    type_disorders = {'Anxiety':disorders_list[0],'Bipolar':disorders_list[1],'Depressive':disorders_list[2],'Eating':disorders_list[3],'Schizophrenic':disorders_list[4]}
    return type_disorders

 
    
def line_chart(xaxis,years,typ,chosendisorder): # prints the information for a specific country, continent or the world's disorders over all the years

    type_disorders = all_years_stats(years,typ)
    colours = ['gold','red','limegreen','magenta','skyblue']
    colourcounter = 0
    if typ == 'World':
        for k,v in type_disorders.items():
            fig = go.Figure()
            # Create and style traces
            fig.add_trace(go.Scatter(x=xaxis, y=v, name=k,
                                     line=dict(color=colours[colourcounter], width=5)))
            avg = [] # creating a trace for the average
            for x in range(len(xaxis)):
                avg.append(average(v))
            fig.add_trace(go.Scatter(x=xaxis, y=avg, name='Average',
                                     line=dict(color='grey', width=2, dash='dash')))
 
            # Edit graph layout
            fig.update_layout(
                    title=dict(
                        text=f'{typ} {k} Disorders rates'),
                    xaxis=dict(
                        title=dict(
                            text='Year')),
                    yaxis=dict(
                        title=dict(
                            text='% of population'),))
            fig.show()
            colourcounter += 1
    else:
        fig = go.Figure()
        # Create and style traces
        fig.add_trace(go.Scatter(x=xaxis, y=type_disorders[chosendisorder], name=chosendisorder,
                                 line=dict(color=colours[alldisorders.index(chosendisorder)], width=5)))
        avg = [] # creating a trace for the average
        for x in range(len(xaxis)):
            avg.append(average(type_disorders[chosendisorder]))
        fig.add_trace(go.Scatter(x=xaxis, y=avg, name='Average',
                                 line=dict(color='grey', width=2, dash='dash')))
 
        # Edit graph layout
        fig.update_layout(
                title=dict(
                    text=f'{typ} {chosendisorder} Disorders rates'),
                xaxis=dict(
                    title=dict(
                        text='Year')),
                yaxis=dict(
                    title=dict(
                        text='% of population'),))
        fig.show()
    #--------------end of function------------------

def bar_chart(years,x,yr,typ,name): #it prints the rates of each disorder in chosen country for chosen year
 
    for i in x:
        i += 'disorders'
    cont = name
    if typ == 'Continents':
        name += ' (IHME GBD)'
    y = []
    for k,v in (years[yr][typ][name]).items():
        if 'disorder' in k:
            v = round(v,3)
            y.append(v)
    colours = ['gold','red','limegreen','magenta','skyblue']
    ht = []
    for i in y:
        ht.append(f'{i}%of {name}')

    fig = go.Figure(data=[go.Bar(x=x, y=y, text = '% of pop',hovertext=ht)])
    # Customize aspect
    fig.update_traces(marker_color=colours, marker_line_color=colours, opacity=0.8,
                      texttemplate=y, textposition='outside')
    fig.update_layout(title_text=f'{cont} Mental disorder Rates in {yr}',barmode='group',xaxis_tickangle=30,)
    fig.show()

# ------------------------------------------------------------calling the functions with the relevant info----------------------------------------------------------------------------------------------------
 
 
allcontinents = [x for x in years['2019']['Continents'].keys()]
allcountries = [x for x in years['2019']['Countries'].keys()]
alldisorders = [x for x in (all_years_stats(years,'Ireland')).keys()]
allyears =  [x for x in years.keys()] # saved as strings, not integers
 
 
'''                               world charts                                '''
# world line chart that prints automatically for all years
line_chart(allyears,years,'World','None') # the line chart function will create graphs of the rates of all disorders of the world, a country or continent over the years
 
 
'''                             continent charts                              '''
choicecontinent = 'Europe'  # Chosen by user but will be Europe by default when launching webpage
choiceyear = '2019' # defaults to the most recent year (2019)
bar_chart(years,alldisorders,choiceyear,'Continents',choicecontinent)
 
 
'''                              country charts                               '''
choicecountry = 'Ireland'     # defaults to Ireland
choiceyear2 = '2019' 
bar_chart(years,alldisorders,choiceyear2,'Countries',choicecountry)
 
choicedisorder = 'Anxiety' # also chosen but will be Anxiety by default
line_chart(allyears,years,choicecountry,choicedisorder) # the line chart function will create graphs of the rates of all disorders of the world, a country or continent over the years
 
 
#---------------------------------------------------------------------------uploading new variables to database-------------------------------------------------------------------------------------------
 
''' now i will upload variables storing different parts of the filtered data to my database so i can access them directly when making more/new graphs
'''

graphingdata = {'alldisorders':alldisorders,
                'allcontinents':allcontinents,
                'allcountries':allcountries,
                'allyears':allyears}

ref = db.reference("/graphingdata") # creating a reference to the database
ref.set(graphingdata) #uploading the data to said reference