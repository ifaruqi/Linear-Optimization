#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 23:13:32 2022

@author: ismailfaruqi
"""

"""
Advertisement Problem
LP Model:
    Define
    AS = x1;  ASA = x3;
    AJ = x2;  AJA = x4;
    
    max 0.8x1 + 1.3x2 - x3 - x4
    s.t.
    x1 - 4x3 = 4000
    x2 - 5x4 = 6000
    0.8x1 + 0.5x2 + x3 + x4 <= 13000
    -52x1 + 17.5x2 - 35x3 - 35x4 <= 0
    -28x1 + 32.5x2 - 65x3 - 65x4 >= 0
    xi>=0

     
Data read from Excel file with the table:
    
	      AS    AJ	 ASA  AJA	RHS
cost	  0.8  1.3	  1	   1	
AS_dem	   1	0	 -4	   0	4000
AJ_dem	   0	1	  0	  -5	6000
budget	  0.8  0.5	  1	   1	13000
AJ_upper  -52  17.5	 -35  -35	0
AJ_lower  -28  32.5	 -65  -65	0

"""

import pandas as pd  # pandas is used to work with data frames
import pulp as pl  # library with an LP Solver is named as pl

# ********************   INPUT; prepare data***********************************

# Read data from a sheet of an excel file as a Pandas DataFrame df
# "index_col=0" indicates no need for creating indices of rows
#                    file             worksheet
file_name='AssignmentTemplate2022_5.xlsx'
df = pd.read_excel(file_name, "Problem5",
                   index_col=0)  # by default header=0, i.e. no need to create



# create dictionary  with pairs "product2 - price; got it from df
product = df.loc[df.index[0], df.columns[0:-1]].to_dict()


# cut off constraint matrix from dataframe; to use format Ax<=b
# use here a dictionary to loop through names of products and constraints
constraint_matrix = pd.DataFrame(df, index=df.index[1:],
                                 columns=df.columns[0:-1]).to_dict('index')


# get RHS associated with the constraints; dictionary: 'constraint'-rhs(from df)
rhs_coefficients_1 = df.loc[df.index[1:3], df.columns[-1]].to_dict()

rhs_coefficients_2 = df.loc[df.index[3:5], df.columns[-1]].to_dict()

rhs_coefficients_3 = df.loc[df.index[5:], df.columns[-1]].to_dict()


# ******************** MODEL **************************************************
# Creates model which is a "Linear Program" with "Maximisation" objective
#  any name for the model/object is fine
model5= pl.LpProblem("The_Apple_Problem", pl.LpMaximize)

# Creates a dictionary of variables. these are continuous varriables (default)
# use keys from the earlier defined dictionary to loop through variables
variables = pl.LpVariable.dicts('Apple', product, lowBound=0)
# add/define the objective function
model5 += pl.lpSum([product[i]*variables[i] for i in product])

# add constraints to the model; format like Ax<=b
for c in rhs_coefficients_1:
    model5 += pl.lpSum(constraint_matrix[c][u]*variables[u]for u in product
                       ) == rhs_coefficients_1[c], c  # c is constraint name
    
# add constraints to the model; format like Ax<=b
for c in rhs_coefficients_2:
    model5 += pl.lpSum(constraint_matrix[c][u]*variables[u]for u in product
                       ) <= rhs_coefficients_2[c], c  # c is constraint name

# add constraints to the model; format like Ax<=b
for c in rhs_coefficients_3:
    model5 += pl.lpSum(constraint_matrix[c][u]*variables[u]for u in product
                       ) >= rhs_coefficients_3[c], c  # c is constraint name


model5.solve()  # solve the problem with the default solver

# The status of the solution is printed to the screen
print("Status:", pl.LpStatus[model5.status])

# The optimised objective function value is printed to the screen
print("Total Profit = ", round(pl.value(model5.objective),2))
# Each of the variables is printed with it's resolved optimum value
if (pl.LpStatus[model5.status] == 'Optimal'):
    for v in model5.variables():
        print(v.name, "=", v.varValue)