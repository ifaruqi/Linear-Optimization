#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 15:54:55 2022

@author: ismailfaruqi
"""

"""
Advertisement Problem
LP Model:
    Define
    High_Grade = x1, and
    Low_Grade  = x2
    
    max 330x1+265x2
    s.t.
    25x1+25x2 <= 900
    15x1+45x2 <= 1700
    30x1+15x2 <= 500
    xi>=0
     
Data read from Excel file with the table:
    
           High_Grade  Low_Grade   RHS
income       330	      265 
wool	     50	          40     109000
nylon   	 30	          60     123000
labor        30           15      500

"""

import pandas as pd  # pandas is used to work with data frames
import pulp as pl  # library with an LP Solver is named as pl

# ********************   INPUT; prepare data***********************************

# Read data from a sheet of an excel file as a Pandas DataFrame df
# "index_col=0" indicates no need for creating indices of rows
#                    file             worksheet
file_name='AssignmentTemplate2022_5.xlsx'
df = pd.read_excel(file_name, "Problem2",
                   index_col=0)  # by default header=0, i.e. no need to create


# create dictionary  with pairs product - income ; got it from df
product = df.loc[df.index[0], df.columns[0:-1]].to_dict()



# cut off constraint matrix from dataframe; to use format Ax<=b
# use here a dictionary to loop through names of products and constraints
constraint_matrix = pd.DataFrame(df, index=df.index[1:],
                                 columns=df.columns[0:-1]).to_dict('index')


# get RHS associated with the constraints; dictionary: 'constraint'-rhs(from df)
rhs_coefficients = df.loc[df.index[1:], df.columns[-1]].to_dict()



# ******************** MODEL **************************************************
# Creates model which is a "Linear Program" with "Maximisation" objective
#  any name for the model/object is fine
model2 = pl.LpProblem("The_Rug_Problem", pl.LpMaximize)

# Creates a dictionary of variables. these are continuous varriables (default)
# use keys from the earlier defined dictionary to loop through variables
variables = pl.LpVariable.dicts('Rug', product, lowBound=0)
# add/define the objective function
model2 += pl.lpSum([product[i]*variables[i] for i in product])

# add constraints to the model; format like Ax<=b
for c in rhs_coefficients:
    model2 += pl.lpSum(constraint_matrix[c][u]*variables[u]for u in product
                       ) <= rhs_coefficients[c], c  # c is constraint name

model2.solve()  # solve the problem with the default solver

# The status of the solution is printed to the screen
print("Status:", pl.LpStatus[model2.status])

# The optimised objective function value is printed to the screen
print("Total Income = ", round(pl.value(model2.objective),2))
# Each of the variables is printed with it's resolved optimum value
if (pl.LpStatus[model2.status] == 'Optimal'):
    for v in model2.variables():
        print(v.name, "=", v.varValue)







