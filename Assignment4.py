#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 21:49:12 2022

@author: ismailfaruqi
"""

"""
Advertisement Problem
LP Model:
    Define
    LD = x1;  SD = x3;  DN = x5;  HN = x7;
    LH = x2;  SH = x4;  DC = x6;  HC = x8;
    
    min 130x1 + 90x2 + 130x3 + 110x4 + 25x5 + 25x6 + 50x7 + 30x8
    s.t.
    x1 + x2 + x3 + x4 - x5 - x6 - x7 - x8 >= 0
    x1 + x3 - x5 - x6 >= 0
    x2 + x4 - x7 - x8 >= 0
    x3 + x4 <= 32
    x1 + x2 <= 38.5
    x6 + x8 = 17
    x5 + x7 = 26
    xi>=0

     
Data read from Excel file with the table:
    
	          LD  LH  SD  SH   DN  DC   HN   HC  RHS
cost         130  90 130  110  25  25	50	 30	
sup_dem       1	  1	  1	   1   -1  -1   -1	 -1	  0
DA_to_Cust    1	  0	  1	   0   -1  -1	 0	  0	  0
HO_to Cust	  0	  1	  0	   1	0	0	-1	 -1	  0
SA_sup        0	  0	  1	   1	0	0	 0	  0	  32
LA_sup        1	  1	  0	   0	0	0	 0	  0	  38.5
CH_dem	      0	  0	  0	   0	0	1	 0	  1	  17
NY_dem	      0	  0	  0	   0	1	0	 1	  0	  26

"""

import pandas as pd  # pandas is used to work with data frames
import pulp as pl  # library with an LP Solver is named as pl

# ********************   INPUT; prepare data***********************************

# Read data from a sheet of an excel file as a Pandas DataFrame df
# "index_col=0" indicates no need for creating indices of rows
#                    file             worksheet
file_name='AssignmentTemplate2022_5.xlsx'
df = pd.read_excel(file_name, "Problem4",
                   index_col=0)  # by default header=0, i.e. no need to create



# create dictionary  with pairs "product2 - price; got it from df
product = df.loc[df.index[0], df.columns[0:-1]].to_dict()


# cut off constraint matrix from dataframe; to use format Ax<=b
# use here a dictionary to loop through names of products and constraints
constraint_matrix = pd.DataFrame(df, index=df.index[1:],
                                 columns=df.columns[0:-1]).to_dict('index')


# get RHS associated with the constraints; dictionary: 'constraint'-rhs(from df)
rhs_coefficients_1 = df.loc[df.index[1:4], df.columns[-1]].to_dict()

rhs_coefficients_2 = df.loc[df.index[4:6], df.columns[-1]].to_dict()

rhs_coefficients_3 = df.loc[df.index[6:], df.columns[-1]].to_dict()


# ******************** MODEL **************************************************
# Creates model which is a "Linear Program" with "Minimisation" objective
#  any name for the model/object is fine
model4= pl.LpProblem("The_Oil_Problem", pl.LpMinimize)

# Creates a dictionary of variables. these are continuous varriables (default)
# use keys from the earlier defined dictionary to loop through variables
variables = pl.LpVariable.dicts('Oil', product, lowBound=0)
# add/define the objective function
model4 += pl.lpSum([product[i]*variables[i] for i in product])

# add constraints to the model; format like Ax<=b
for c in rhs_coefficients_1:
    model4 += pl.lpSum(constraint_matrix[c][u]*variables[u]for u in product
                       ) >= rhs_coefficients_1[c], c  # c is constraint name
    
# add constraints to the model; format like Ax<=b
for c in rhs_coefficients_2:
    model4 += pl.lpSum(constraint_matrix[c][u]*variables[u]for u in product
                       ) <= rhs_coefficients_2[c], c  # c is constraint name

# add constraints to the model; format like Ax<=b
for c in rhs_coefficients_3:
    model4 += pl.lpSum(constraint_matrix[c][u]*variables[u]for u in product
                       ) == rhs_coefficients_3[c], c  # c is constraint name


model4.solve()  # solve the problem with the default solver

# The status of the solution is printed to the screen
print("Status:", pl.LpStatus[model4.status])

# The optimised objective function value is printed to the screen
print("Total Cost = ", round(pl.value(model4.objective),2))
# Each of the variables is printed with it's resolved optimum value
if (pl.LpStatus[model4.status] == 'Optimal'):
    for v in model4.variables():
        print(v.name, "=", v.varValue)