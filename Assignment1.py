#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 13:37:37 2022

@author: ismailfaruqi
"""

"""
Advertisement Problem
LP Model:
    Define
    Newspaper = x1, and
    Radio     = x2
    
    
    min x1+x2
    s.t.
    50x1+40x2 >= 109000
    30x1+60x2 >= 123000 
    xi >= 0
    
     
Data read from Excel file with the table:
    
	           Newspaper Radio	RHS
cost             1	      1 
below_25	     50	      40     109000
above_25    	 30	      60     123000



"""
import pandas as pd  # pandas is used to work with data frames
import pulp as pl  # library with an LP Solver is named as pl

# ********************   INPUT; prepare data***********************************

# Read data from a sheet of an excel file as a Pandas DataFrame df
# "index_col=0" indicates no need for creating indices of rows
#                    file             worksheet
file_name='AssignmentTemplate2022_5.xlsx'
df = pd.read_excel(file_name, "Problem1",
                   index_col=0)  # by default header=0, i.e. no need to create


# create dictionary  with pairs product -cost; got it from df
product = df.loc[df.index[0], df.columns[0:-1]].to_dict()



# cut off constraint matrix from dataframe; to use format Ax<=b
# use here a dictionary to loop through names of products and constraints
constraint_matrix = pd.DataFrame(df, index=df.index[1:],
                                 columns=df.columns[0:-1]).to_dict('index')


# get RHS associated with the constraints; dictionary: 'constraint'-rhs(from df)
rhs_coefficients = df.loc[df.index[1:], df.columns[-1]].to_dict()




# ******************** MODEL **************************************************
# Creates model which is a "Linear Program" with "Minimisation" objective
#  any name for the model/object is fine
model1 = pl.LpProblem("The_Advertisement_Problem", pl.LpMinimize)

# Creates a dictionary of variables. these are continuous varriables (default)
# use keys from the earlier defined dictionary to loop through variables
variables = pl.LpVariable.dicts('Advertisement_Count', product, lowBound=0)
# add/define the objective function
model1 += pl.lpSum([product[i]*variables[i] for i in product])

# add constraints to the model; format like Ax<=b
for c in rhs_coefficients:
    model1 += pl.lpSum(constraint_matrix[c][u]*variables[u]for u in product
                       ) >= rhs_coefficients[c], c  # c is constraint name

model1.solve()  # solve the problem with the default solver

# The status of the solution is printed to the screen
print("Status:", pl.LpStatus[model1.status])

# The optimised objective function value is printed to the screen
print("Total Cost = ", round(pl.value(model1.objective),2))
# Each of the variables is printed with it's resolved optimum value
if (pl.LpStatus[model1.status] == 'Optimal'):
    for v in model1.variables():
        print(v.name, "=", v.varValue)

