import pulp as p

solver_list = p.listSolvers(onlyAvailable=True)


net_reduction = 10  # user input
default_pollutions = [55, 65, 75, 85, 95, 100, 110, 35, 65, 20]
populations = [1.1, 1.3, 1.9, 2.0, 2.1, 1.9, 2.5, 0.5, 1.0, 0.1]

avg_conc_default = sum(x * y for x, y in zip(default_pollutions, populations)) / sum(
    populations
)
avg_conc_new = avg_conc_default * (1 - net_reduction / 100)


max_pollution_reduction = [
    40,
    40,
    40,
    40,
    30,
    30,
    30,
    30,
    30,
    30,
]  # This should be user input

# Create a LP Minimization problem
Lp_prob = p.LpProblem("Problem", sense=p.LpMinimize)

# Create problem Variables


def calculate_pollution_after_reduction(values, percentages):
    reduced_values = [
        value - (value * percentage / 100)
        for value, percentage in zip(values, percentages)
    ]
    return reduced_values


max_pollution_reduced = calculate_pollution_after_reduction(
    default_pollutions, max_pollution_reduction
)

num_zones = 10  # user input

var_dict = dict()

for i in range(1, num_zones + 1, 1):
    var_dict["x" + str(i)] = p.LpVariable(
        "x" + str(i),
        lowBound=max_pollution_reduced[i - 1],
        upBound=default_pollutions[i - 1],
    )
# x1 = p.LpVariable("x1", lowBound = 38.5, upBound = 55)   # Create a variable x
# x2 = p.LpVariable("x2", lowBound = 45.5, upBound = 65)
# x3 = p.LpVariable("x3", lowBound = 60, upBound = 75)
# x4 = p.LpVariable("x4", lowBound = 76.5, upBound = 85)
# x5 = p.LpVariable("x5", lowBound = 66.5, upBound = 95)
# x6 = p.LpVariable("x6", lowBound = 70, upBound = 100)
# x7 = p.LpVariable("x7", lowBound = 77, upBound = 110)
# x8 = p.LpVariable("x8", lowBound = 35, upBound = 35)
# x9 = p.LpVariable("x9", lowBound = 65, upBound = 65)
# x10 = p.LpVariable("x10", lowBound = 20, upBound = 20)


# Objective Function
Lp_prob += (
    p.lpSum(
        [
            populations[i - 1] * var_dict["x" + str(i)]
            for i in range(1, num_zones + 1, 1)
        ]
    )
) / sum(populations)

# Constraints:
Lp_prob += (
    p.lpSum(
        [
            populations[i - 1] * var_dict["x" + str(i)]
            for i in range(1, num_zones + 1, 1)
        ]
    )
) / sum(populations) == avg_conc_new

# Lp_prob += (1.1 * x1 + 1.3 * x2 + 1.9 * x3 + 2.0 * x4 + 2.1 * x5 + 1.9 * x6 + 2.5 * x7 + 0.5 * x8 + 1.0 * x9 + 0.1 * x10)/14.4  == 67

# Display the problem
print(Lp_prob)
status = Lp_prob.solve()
print(p.LpStatus[status])  # The solution status

# Printing the final solution
# print(p.value(x1), p.value(x2), p.value(x3), p.value(x4), p.value(x5),
#        p.value(x6), p.value(x7), p.value(x8), p.value(x9), p.value(x10),
#       p.value(Lp_prob.objective))

print(
    [p.value(var_dict["x" + str(i)]) for i in range(1, num_zones + 1, 1)],
    p.value(Lp_prob.objective),
)

new_pollutions = [p.value(var_dict["x" + str(i)]) for i in range(1, num_zones + 1, 1)]


def calculate_pct_reduction(old_pollutions, new_pollutions):
    reductions = [
        100 * (old - new) / old for old, new in zip(old_pollutions, new_pollutions)
    ]
    return reductions


actual_reductions = calculate_pct_reduction(default_pollutions, new_pollutions)
print(actual_reductions)
