from pulp import *
import pandas as pd
#next import our data, I already removed min&max constraints rows
Data = pd.read_excel("diet.xls")
Data.head()
Data.tail()
#convert dataframe to list
foodData = Data.values.tolist()
foodData[0] #should output list of brocolli and its variables
foodData[0][0] #should output "brocolli"

#minimum and maximum intake for each nutrients:
mintake = [1500,30,20,800,130,125,60,1000,400,700,10]
maxtake = [2500,240,70,2000,450,250,100,10000,5000,1500,40]

#list of foods
foods = [x[0] for x in foodData]
len(foods) #how many foods we have

#create a dictionary for the costs of the foods
cost = dict((x[0], float(x[1])) for x in foodData)
#using a for loop, loop through all the nutrients and store them as dicts
intake = []
for i in range(3, Data.shape[1]):
    intake.append(dict((x[0], float(x[i])) for x in foodData))

#define the optimization problem by Pulp
problem = LpProblem("Diet Problem", LpMinimize)
#define our variables
amountVars = LpVariable.dicts("Amounts", foods, 0)

#Next, we add the objective function to the diet problem, which is the
#inner product of cost and amount of foods
problem += lpSum([cost[i] * amountVars[i] for i in foods]), 'total cost'

#append constraint for each intake
for i in range(11): #11 intakes
    problem += lpSum([intake[i][j] * amountVars[j] for j in foods]) >= mintake[i], 'min' + foods[i]
    problem += lpSum([intake[i][j] * amountVars[j] for j in foods]) <= maxtake[i], 'max' + foods[i]
    
#solve problem
problem.solve()
#print solution
varsDictionary = {} #a dictionary with all the foods and its solved amount
for v in problem.variables():
    varsDictionary[v.name] = v.varValue
easytosee = {} #new dictionary to see foods that only used to minimize cost
for i,j in varsDictionary.items():
    if j != 0.0:
        easytosee[i] = j
print(easytosee)
#{'Amounts_Celery,_Raw': 52.64371, 'Amounts_Frozen_Broccoli': 0.25960653, 
#'Amounts_Lettuce,Iceberg,Raw': 63.988506, 'Amounts_Oranges': 2.2929389, 
#'Amounts_Poached_Eggs': 0.14184397, 'Amounts_Popcorn,Air_Popped': 13.869322}
resultfood = ['Celery, Raw', 'Frozen Broccoli', 'Lettuce,Iceberg,Raw',
              'Oranges', 'Poached Eggs','Popcorn,Air-Popped']
#get the cost for each resulted food
eachcost = list(easytosee.values())
#calculate total cost
totalcost = sum([cost[i] * j for i,j in zip(resultfood, eachcost)])

#question 15.2.2
#a.If a food is selected, then a minimum of 1/10 serving must be chosen.
binaryVars = LpVariable.dicts("InOrOut", foods, 0, 1, LpBinary)
for i in foods:
    problem += amountVars[i] >= 0.1 * binaryVars[i]
    problem += amountVars[i] <= 1000000 * binaryVars[i]

#b.Many people dislike celery and frozen broccoli. So at most one, 
#but not both, can beselected.
problem += binaryVars['Frozen Broccoli'] + binaryVars['Celery, Raw'] <= 1

#c.To get day-to-day variety in protein, at least 3 kinds of 
#meat/poultry/fish/eggs must beselected.
protein = ['Tofu', 'Roasted Chicken', 'Spaghetti W/ Sauce',  
           'Cheddar Cheese', '3.3% Fat,Whole Milk', 
           '2% Lowfat Milk', 'Poached Eggs', 
           'Scrambled Eggs', 'Bologna,Turkey', 'Frankfurter, Beef', 'Pork',
           'White Tuna in Water']
problem += binaryVars[protein[0]] + binaryVars[protein[1]] +\
binaryVars[protein[2]] + binaryVars[protein[3]] + binaryVars[protein[4]] +\
binaryVars[protein[5]] + binaryVars[protein[6]] + binaryVars[protein[7]] +\
binaryVars[protein[8]] + binaryVars[protein[9]] + \
binaryVars[protein[10]] + binaryVars[protein[11]] >= 3

#solve the problem
problem.solve()
#print solution
varsDictionary2 = {} #a dictionary with all the foods and its solved amount
for v in problem.variables():
    varsDictionary2[v.name] = v.varValue
easytosee2 = {} #new dictionary to see foods that only used to minimize cost
for i,j in varsDictionary2.items():
    if j != 0.0:
        easytosee2[i] = j

    