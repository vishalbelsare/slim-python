import os
import cplex
import numpy as np
import pandas as pd
from slim_python.SLIMCoefficientConstraints import SLIMCoefficientConstraints
#from slim_python.create_slim_IP import create_slim_IP

# load data
data_name = 'breastcancer'
data_dir = os.getcwd() + '/data/'
data_csv_file = data_dir + data_name + '_processed.csv'

df = pd.read_csv(data_csv_file, sep = ',')
data = df.as_matrix()
data_headers = list(df.columns.values)

N = data.shape[0]

# setup Y and Y_name
Y_col_idx = [0]
Y = data[:, Y_col_idx]
Y_name = [data_headers[j] for j in Y_col_idx]
Y[Y == 0] = -1

# setup X and X_names
X_col_idx = [j for j in range(data.shape[1]) if j not in Y_col_idx]
X = data[:, X_col_idx]
X_names = [data_headers[j] for j in X_col_idx]

# insert a column of ones to X for the intercept
X = np.insert(arr = X, obj = 0, values = np.ones(N), axis = 1)
X_names.insert(0, '(Intercept)')

# TODO function to run sanity checks for X, Y
#X, Y = check_data(X = X, Y = Y, X_names = X_names, Y_name = Y_names)

# setup SLIM coefficient set
coef_constraints = SLIMCoefficientConstraints(variable_names = X_names, ub = 5, lb = -5)
coef_constraints.view()

#create SLIM IP
N, P = X.shape

slim_input = {
    'X': X,
    'X_names': X_names,
    'Y': Y,
    'Y_name': Y_name,
    'C_0': 0.01,
    'w_pos': 1.0,
    'w_neg': 1.0,
    'L0_min': 0,
    'L0_max': float('inf'),
    'err_min': 0,
    'err_max': N,
    'pos_err_min': 0,
    'pos_err_max': N,
    'neg_err_min': 0,
    'neg_err_max': N,
    'coef_constraints': coef_constraints
}

#input = slim_input
#print_flag = True
slim_IP, slim_info = create_slim_IP(slim_input)

# setup SLIM IP parameters
#TODO: add these default settings to create_slim_IP
slim_IP.parameters.randomseed.set(0)
slim_IP.parameters.threads.set(1)
slim_IP.parameters.parallel.set(1)
slim_IP.parameters.output.clonelog.set(0)
slim_IP.parameters.mip.tolerances.mipgap.set(np.finfo(np.float).eps)
slim_IP.parameters.mip.tolerances.absmipgap.set(np.finfo(np.float).eps)
slim_IP.parameters.mip.tolerances.integrality.set(np.finfo(np.float).eps)
slim_IP.parameters.emphasis.mip.set(1)


#solve SLIM IP
slim_IP.solve()

#get


