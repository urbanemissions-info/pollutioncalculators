import pulp as p 
import pandas as pd
import numpy as np

net_reduction = 20 #user input in %

zone_pollutions_old = np.array([55, 65, 75, 85, 95, 100, 110, 35, 65, 20])
zone_populations = [1.1, 1.3, 1.9, 2.0, 2.1, 1.9, 2.5, 0.5, 1.0, 0.1]
avg_pollution_old = sum(x * y for x, y in zip(zone_pollutions_old, zone_populations))/sum(zone_populations)
avg_pollution_new = avg_pollution_old*(1-net_reduction/100)

sourceapportionment_df = pd.read_csv('sourceapportionment_default.csv')
sourceapportionment_array = np.array(sourceapportionment_df.iloc[:,1:].values)
zone_pollutions_old_sourcewise = sourceapportionment_array * zone_pollutions_old

pmsa_old = np.dot(zone_pollutions_old_sourcewise,zone_populations)/np.sum(zone_populations)
max_reductions_sourcewise = {'C':50,
                             'H':30,
                             'W':50,
                             'I':30,
                             'F':30,
                             'P':30,
                             'D':30,
                             'B':10
                             }

pmsa_new_maxreduced = pmsa_old * (100 - np.array(list(max_reductions_sourcewise.values())))/100

print(pmsa_new_maxreduced)
# Create a LP Minimization problem 
Lp_prob = p.LpProblem('Problem', sense = p.LpMinimize)  

num_zones = 10 #user input

var_dict = dict()
# Source wise reduction in each zone
for i in range(1,num_zones+1,1):
    var_dict['R'+str(i)+'C'] = p.LpVariable("R"+str(i)+'C', lowBound = 0, upBound = 1)
    var_dict['R'+str(i)+'H'] = p.LpVariable("R"+str(i)+'H', lowBound = 0, upBound = 1)
    var_dict['R'+str(i)+'W'] = p.LpVariable("R"+str(i)+'W', lowBound = 0, upBound = 1)
    var_dict['R'+str(i)+'I'] = p.LpVariable("R"+str(i)+'I', lowBound = 0, upBound = 1)
    var_dict['R'+str(i)+'F'] = p.LpVariable("R"+str(i)+'F', lowBound = 0, upBound = 1)
    var_dict['R'+str(i)+'P'] = p.LpVariable("R"+str(i)+'P', lowBound = 0, upBound = 1)
    var_dict['R'+str(i)+'D'] = p.LpVariable("R"+str(i)+'D', lowBound = 0, upBound = 1)
    var_dict['R'+str(i)+'B'] = p.LpVariable("R"+str(i)+'B', lowBound = 0, upBound = 1)

# Upper bounds -- currently for each zone. need to change it to ovr all.

# Objective Function 
Lp_prob += (p.lpSum([zone_populations[i-1] * zone_pollutions_old_sourcewise[idx][i-1] * var_dict['R'+str(i)+s] for idx, s in enumerate(['C', 'H', 'W', 'I', 'F', 'P' ,'D', 'B']) for i in range(1,num_zones+1,1)]))/sum(zone_populations)

# Constraints: 
Lp_prob += (p.lpSum([zone_populations[i-1] * zone_pollutions_old_sourcewise[idx][i-1] * var_dict['R'+str(i)+s] for idx, s in enumerate(['C', 'H', 'W', 'I', 'F', 'P' ,'D', 'B']) for i in range(1,num_zones+1,1)]))/sum(zone_populations) == (avg_pollution_old - avg_pollution_new)

for idx, s in enumerate(['C', 'H', 'W', 'I', 'F', 'P' ,'D', 'B']):
    Lp_prob += p.lpSum([zone_populations[i-1] * zone_pollutions_old_sourcewise[0][i-1] * var_dict['R'+str(i)+s] for i in range(1,num_zones+1,1)])/sum(zone_populations) <= pmsa_old[idx] - pmsa_new_maxreduced[idx]

 # Display the problem 
print(Lp_prob) 

status = Lp_prob.solve()   
print(p.LpStatus[status])   # The solution status 

#print([p.value(var_dict['Z'+str(i)]) for i in range(1,num_zones+1,1)], p.value(Lp_prob.objective))
reductions = [p.value(var_dict['R'+str(i)+s]) for s in ['C', 'H', 'W', 'I', 'F', 'P' ,'D', 'B'] for i in range(1,num_zones+1,1)]
reductions_array = np.array(reductions).reshape(8, 10)
print(reductions_array)
print( p.value(Lp_prob.objective))