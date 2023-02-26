#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 00:02:30 2022

@author: ismailfaruqi
"""

"""
Advertisement Problem
LP Model:
    Define
    X_T1 = x1;  X_T2 = x4;  X_T3 = x7;  
    X_M1 = x2;  X_M2 = x5;  X_M3 = x8;
    X_B1 = x3;  X_B2 = x6;  X_B3 = x9;
    
    
    min 1.1(x1+x4+x7) + 2.2(x2+x5+x8) + 2.5(x3+x6+x9)
    s.t.
    3x1 - x2 - x3 <= 0
    9x4 - 11x5 - 11x6 <=0
    2x7 - 3x8 - 3x9 <= 0
    -7x1 + 13x2 - 7x3 >= 0
    -7x4 + 13x5 - 7x6 >= 0
    3x7 - 2x8 - 2x9 >=0
    -3x1 - 3x2 + 17x3 >= 0
    -3x4 - 3x5 + 17x6 >= 0
    -2x7 - 2x8 + 3x9 >= 0
    x1 + x2 + x2 >= 1500
    x4 + x5 + x6 >= 600
    x7 + x8 + x9 >= 850
    xij>=0
    
    
    
     
Data read from Excel file with the table:
    
    	X_T1  X_M1  X_B1  X_T2	 X_M2   X_B2  X_T3  X_M3  X_B3  RHS
Price	1.1	  2.2   2.5	   1.1	 2.2	2.5	   1.1	 2.2   2.5	
E1_T_25	 3	  -1	-1	    0	  0	     0	    0	  0	    0	 0
E2_T_55	 0	  0	     0	    9	 -11	-11	    0	  0	    0	 0
E3_T_60	 0	  0	     0	    0	  0	     0	    2	 -3	   -3	 0
E1_M_35	-7	  13	-7	    0	  0	     0	    0	  0	    0	 0
E2_M_35	 0	  0	     0	   -7	  13	-7	    0	  0	    0	 0
E3_T_40	 0	  0	     0	    0	  0	     0	    3	 -2	   -2	 0
E1_B_15	-3	 -3	     17	    0	  0	     0	    0	  0	    0	 0
E2_B_15	 0	  0	     0	   -3	 -3	     17	    0	  0	    0	 0
E3_B_40	 0	  0	     0	    0	  0	     0	   -2	 -2	    3	 0
E1_Sum	 1	  1	     1	    0	  0	     0	    0	  0	    0	 1500
E2_Sum	 0	  0	     0	    1	  1	     1	    0	  0	    0	 600
E3_Sum	 0	  0	     0	    0	  0	     0	    1	  1	    1	 850
    


"""

import pandas as pd  # pandas is used to work with data frames
import pulp as pl  # library with an LP Solver is named as pl

# ********************   INPUT; prepare data***********************************

# Read data from a sheet of an excel file as a Pandas DataFrame df
# "index_col=0" indicates no need for creating indices of rows
#                    file             worksheet
file_name='AssignmentTemplate2022_5.xlsx'
df = pd.read_excel(file_name, "Problem3",
                   index_col=0)  # by default header=0, i.e. no need to create



# create dictionary  with pairs Grass - price; got it from df
product = df.loc[df.index[0], df.columns[0:-1]].to_dict()


# cut off constraint matrix from dataframe; to use format Ax<=b
# use here a dictionary to loop through names of products and constraints
constraint_matrix = pd.DataFrame(df, index=df.index[1:],
                                 columns=df.columns[0:-1]).to_dict('index')


# get RHS associated with the constraints; dictionary: 'constraint'-rhs(from df)
rhs_coefficients_1 = df.loc[df.index[1:4], df.columns[-1]].to_dict()

rhs_coefficients_2 = df.loc[df.index[4:], df.columns[-1]].to_dict()


# ******************** MODEL **************************************************
# Creates model which is a "Linear Program" with "Minimisation" objective
#  any name for the model/object is fine
model3= pl.LpProblem("The_Grass_Problem", pl.LpMinimize)

# Creates a dictionary of variables. these are continuous varriables (default)
# use keys from the earlier defined dictionary to loop through variables
variables = pl.LpVariable.dicts('Grass', product, lowBound=0)
# add/define the objective function
model3 += pl.lpSum([product[i]*variables[i] for i in product])

# add constraints to the model; format like Ax<=b
for c in rhs_coefficients_1:
    model3 += pl.lpSum(constraint_matrix[c][u]*variables[u]for u in product
                       ) <= rhs_coefficients_1[c], c  # c is constraint name
    
# add constraints to the model; format like Ax<=b
for c in rhs_coefficients_2:
    model3 += pl.lpSum(constraint_matrix[c][u]*variables[u]for u in product
                       ) >= rhs_coefficients_2[c], c  # c is constraint name



model3.solve()  # solve the problem with the default solver

# The status of the solution is printed to the screen
print("Status:", pl.LpStatus[model3.status])

# The optimised objective function value is printed to the screen
print("Total Cost = ", round(pl.value(model3.objective),2))
# Each of the variables is printed with it's resolved optimum value
if (pl.LpStatus[model3.status] == 'Optimal'):
    for v in model3.variables():
        print(v.name, "=", v.varValue)




