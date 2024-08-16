# AQI Simulator
UEInfo developed 6 calculators to build Air Quality (AQ) scenarios.

1. [Version-01](https://www.urbanemissions.info/wp-content/uploads/misc/AQ-Simualtor-V1-Zone-PopWts.xlsx?_gl=1*86cgf1*_ga*MTU5NTY2MDYyNC4xNzE2MzQ4NTYw*_ga_64XLW7JTP7*MTcyMzc3ODE1NS4xMy4wLjE3MjM3NzgxNTUuMC4wLjA.) – calculates population weighted concentrations based on zonal averages of an airshed and allows to build scenarios against % reduction in zonal pollution

2. [Version-02](https://www.urbanemissions.info/wp-content/uploads/misc/AQ-Simualtor-V2-SourceApp-Scenarios.xlsx?_gl=1*uef408*_ga*MTU5NTY2MDYyNC4xNzE2MzQ4NTYw*_ga_64XLW7JTP7*MTcyMzc3ODE1NS4xMy4wLjE3MjM3NzgxNTUuMC4wLjA.) – based on source apportionment results, allows to build scenarios against % reduction in each source

3. [Version-03](https://www.urbanemissions.info/wp-content/uploads/misc/AQ-Simulator-V3-Zone-Target-Solver.xlsx?_gl=1*59qsm7*_ga*MTU5NTY2MDYyNC4xNzE2MzQ4NTYw*_ga_64XLW7JTP7*MTcyMzc3ODE1NS4xMy4wLjE3MjM3NzgxNTUuMC4wLjA.) – solves for net zonal reductions required to reach an overall target using maximum possible reductions by zone as input

4. [Version-04](https://www.urbanemissions.info/wp-content/uploads/misc/AQ-Simulator-V4-Zone-PMSA-Target-Solver.xlsx?_gl=1*wyc879*_ga*MTU5NTY2MDYyNC4xNzE2MzQ4NTYw*_ga_64XLW7JTP7*MTcyMzc3ODE1NS4xMy4wLjE3MjM3NzgxNTUuMC4wLjA.) – solves for net zonal reductions by source required to reach an overall target using zonal source-apportionment results and maximum possible reductions by zone as input

5. [Version-05](https://www.urbanemissions.info/wp-content/uploads/misc/AQ-Simulator-V5-Zone-PMSA-Target-Solver-Costs.xlsx?_gl=1*wyc879*_ga*MTU5NTY2MDYyNC4xNzE2MzQ4NTYw*_ga_64XLW7JTP7*MTcyMzc3ODE1NS4xMy4wLjE3MjM3NzgxNTUuMC4wLjA.) – solves for net zonal reductions by source required at least cost using zonal source-apportionment results, maximum possible reductions by zone, and cost per unit pollution reduction by source as input

6. [Version-06](https://www.urbanemissions.info/wp-content/uploads/misc/AQ-Simulator-V6-Zone-to-Grid.xlsx?_gl=1*wyc879*_ga*MTU5NTY2MDYyNC4xNzE2MzQ4NTYw*_ga_64XLW7JTP7*MTcyMzc3ODE1NS4xMy4wLjE3MjM3NzgxNTUuMC4wLjA.) – demonstration of source-receptor matrix concept linking zonal concentrations to associated grids (15 x 15 grid airshed) and allows to build scenarios against % reduction in each zone

The first four tools are coded in `simulator.py` 

It can be run by:
`streamlit run ~\AQI_Simulator\simulator.py` 

`inputs` folder has required data inputs.

**Note**: These tools involve optimisation of a linear programming problem. They could contain multiple solutions for a given set of constraints.