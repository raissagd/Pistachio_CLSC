import gurobipy as grb

def add_continous_variables(self, model, data):
    # Define a dictionary of variable types and their dimensions
    var_types = {
        "X": (data.I, data.J),
        "Go": (data.J, data.K),
        "Gr": (data.J, data.E),
        "Gw": (data.J, data.Q),
        "O": (data.E, data.N2),
        "Oc": (data.E, data.S),
        "Ow": (data.E, data.Q),
        "L": (data.S, data.N3),
        "P": (data.K, data.N1),
        "D": (data.Q, data.M)
    }

    # Loop through the dictionary to add variables to the model
    for var_name, (dim1, dim2) in var_types.items():
        model.addVars(int(dim1), int(dim2), vtype=grb.GRB.CONTINUOUS, 
                      name=var_name, lb=0.)

def add_binary_variables(self, model, data):
    # Define a list of tuples with variable names and their dimensions
    binary_vars = [
        ("U", data.J),
        ("Y", data.Q),
        ("W", data.K),
        ("R", data.E),
        ("V", data.S)
    ]

    # Loop through the list to add binary variables to the model
    for var_name, dimension in binary_vars:
        model.addVars(int(dimension), vtype=grb.GRB.BINARY, name=var_name)

def compute_opening_costs(data, U, Y, W, R, V):

    cost_components = [
        (data.Fu, U, data.J),
        (data.Fy, Y, data.Q),
        (data.Fw, W, data.K),
        (data.Fr, R, data.E),
        (data.Fv, V, data.S)
    ]

    z1 = sum(grb.quicksum(f[i] * var[i] for i in range(int(dim)))
             for f, var, dim in cost_components)
    
    return z1