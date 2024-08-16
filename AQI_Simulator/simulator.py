import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
st.set_page_config(layout="wide", page_title="Air Quality Simulator")

# Following line will help in seeing dynamic session states
#"st.session_state object:" , st.session_state


import random
import string
import pulp as p

## CSS Custom styles
## metric label font size and weight
## customise slider
hide_streamlit_style = """
<style>
.st-emotion-cache-16idsys p {
    font-size:24px;
    font-weight:bold;
}

.st-e3 {
    padding-top: 13.3px;
}


.st-emotion-cache-1inwz65 {
    font-size: 0px;
}

code {
    font-size: 1.6em;
}

.st-do {
    height: 12px;
}


.st-dk {
    height: 12px;
}

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

col1, col2, col3 = st.columns([11,1,1])
with col3:
    st.image("assets/logo.grid.3_transp.png", width=70)

with col1:
    st.title("AQI Simulator")


tab1, tab2, tab3, tab4 = st.tabs(["AQ Calculator", "AQ Solver", "Source apportionment", "Source apportionment Solver"])

#*************** TAB 1 - V1 ***************#
with tab1:
    num_zones = st.number_input("Number of Zones in the City: ", value=5)    
    col1, col2, col3, col4, col5 = st.columns([1,2,2,2,2])

    variables_dict = dict()

    with col1:
        st.write("#### Zone")
        default_values_zones = ['Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6', 'Z7', 'Z8', 'Z9', 'Z10']
        for i in range(num_zones):
            st.text_input("Zone", value=default_values_zones[i],
                            label_visibility='collapsed')

    with col2:
        st.write("#### Pop. (M)")
        default_values = [1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3]
        var_name = f"pop_{i}"
        for i in range(num_zones):
            keyplace = default_values_zones[i]+'_pop'
            if keyplace not in st.session_state:
                st.session_state[keyplace] = default_values[i] #Default val
            variables_dict[var_name] = st.number_input("Population",
                        label_visibility='collapsed', key=keyplace)
            
        pops = []
        for i in range(num_zones):
            keyplace = default_values_zones[i]+'_pop'
            pops.append(st.session_state[keyplace])
            total_pop = sum(pops)
        
        st.write('Total: {} M'.format(total_pop))
            
    with col3:
        st.write("#### Conc. μg/m3")
        default_values = [60, 60, 60, 60, 60, 60, 60, 60, 60, 60]
        var_name = f"conc_{i}"
        for i in range(num_zones):
             keyplace = default_values_zones[i]+'_conc'
             if keyplace not in st.session_state:
                 st.session_state[keyplace] = int(default_values[i]) #Default val
             variables_dict[var_name] = st.number_input("Avg.Conc μg/m3",
                            label_visibility='collapsed', key=keyplace, step=1)
             
        sumprod = 0
        for i in range(num_zones):
            conc_keyplace = default_values_zones[i]+'_conc'
            pop_keyplace = default_values_zones[i]+'_pop'
            prod = st.session_state[pop_keyplace] * st.session_state[conc_keyplace]
            sumprod = sumprod+prod
        
        pop_weighted_conc = sumprod/total_pop
        st.write('#### :green[Population weighted concentration: {} μg/m3]'.format(round(pop_weighted_conc,1)))

    
    with col4:
        st.write("#### % reduction")
        var_name = f"reduction_{i}"
        for i in range(num_zones):
            keyplace = default_values_zones[i]+'_reduction'
            # if keyplace not in st.session_state:
            #     st.session_state[keyplace] = default_values[i] #Default val
            variables_dict[var_name] = st.slider("Avg.Conc μg/m3",
                        label_visibility='collapsed', key=keyplace)
            
            
    with col5:
        st.write("#### New zone avg.")
        new_concs = []
        for i in range(num_zones):
            reduction_keyplace = default_values_zones[i]+'_reduction'
            oldconc_keyplace = default_values_zones[i]+'_conc'
            new_concs.append(st.session_state[oldconc_keyplace]*(1 - st.session_state[reduction_keyplace]/100))
        
        sumprod = 0
        for i in range(num_zones):
            st.write(round(new_concs[i],1))
            pop_keyplace = default_values_zones[i]+'_pop'
            prod = st.session_state[pop_keyplace] * new_concs[i]
            sumprod = sumprod+prod
        
        new_pop_weighted_conc = sumprod/total_pop
        st.write('#### :green[New Population weighted concentration:  {} μg/m3]'.format(round(new_pop_weighted_conc,1)))

    with col4:
        net_reduction = round(100*(pop_weighted_conc-new_pop_weighted_conc)/pop_weighted_conc, 1)
        st.write('#### :green[Net reduction:  {} %]'.format(round(net_reduction,1)))

#*************** TAB 2 - V2 ***************#
with tab2:
    net_reduction = st.slider('I want to reduce pollution in the city by: (%)', value=30)

    num_zones = st.number_input("Number of Zones in the City", value=10)    
    col1, col2, col3, col4, col5, col6 = st.columns([1,1,2,2,2,2])

    variables_dict = dict()

    with col1:
        st.write("#### Zone")
        default_values_zones = ['Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6', 'Z7', 'Z8', 'Z9', 'Z10']
        for i in range(num_zones):
            st.text_input("Zone ", value=default_values_zones[i],
                            label_visibility='collapsed')

    with col2:
        st.write("#### Pop. (M)")
        default_values = [1.1, 1.3, 1.9, 2.0, 2.1, 1.9, 2.5, 0.5, 1.0, 0.1]
        var_name = f"pop_{i}"
        for i in range(num_zones):
            keyplace = default_values_zones[i]+'_population'
            if keyplace not in st.session_state:
                st.session_state[keyplace] = default_values[i] #Default val
            variables_dict[var_name] = st.number_input("Population",
                        label_visibility='collapsed', key=keyplace)
            
        pops = []
        for i in range(num_zones):
            keyplace = default_values_zones[i]+'_population'
            pops.append(st.session_state[keyplace])
            total_pop = sum(pops)
        
        st.write('Total: {} M'.format(total_pop))
            
    with col3:
        st.write("#### Conc. μg/m3")
        default_values = [55, 65, 75, 85, 95, 100, 110, 35, 65, 20]
        var_name = f"conc_{i}"
        for i in range(num_zones):
             keyplace = default_values_zones[i]+'_concentration'
             if keyplace not in st.session_state:
                 st.session_state[keyplace] = int(default_values[i]) #Default val
             variables_dict[var_name] = st.number_input("Avg.Conc μg/m3",
                            label_visibility='collapsed', key=keyplace, step=1)
             
        sumprod = 0
        for i in range(num_zones):
            conc_keyplace = default_values_zones[i]+'_concentration'
            pop_keyplace = default_values_zones[i]+'_population'
            prod = st.session_state[pop_keyplace] * st.session_state[conc_keyplace]
            sumprod = sumprod+prod
        
        pop_weighted_conc = sumprod/total_pop
        st.write('#### :green[Population weighted concentration: {} μg/m3]'.format(round(pop_weighted_conc,1)))

    
    with col4:
        st.write("#### Max % reduction")
        max_pollution_reduction_defaults = [40, 40, 40, 40, 30, 30, 30, 30, 30, 30] #This should be user input
        var_name = f"reduction_{i}"
        for i in range(num_zones):
            keyplace = default_values_zones[i]+'_maxreduction'
            if keyplace not in st.session_state:
                st.session_state[keyplace] = max_pollution_reduction_defaults[i] #Default val
            variables_dict[var_name] = st.slider("Max pollution reduction",
                        label_visibility='collapsed', key=keyplace)
            
            
    with col5:
        st.write("#### Actual % reductions")
        avg_conc_new = pop_weighted_conc*(1-net_reduction/100)
        # Create a LP Minimization problem 
        Lp_prob = p.LpProblem('Problem', sense = p.LpMinimize)

        def calculate_pollution_after_reduction(values, percentages):
            reduced_values = [value - (value * percentage / 100) for value, percentage in zip(values, percentages)]
            return reduced_values

        old_concs = []
        max_reds = []
        populations = []
        for i in range(num_zones):
            max_reduction_keyplace = default_values_zones[i]+'_maxreduction'
            oldconc_keyplace = default_values_zones[i]+'_concentration'
            population_keyplace = default_values_zones[i]+'_population'

            old_concs.append(st.session_state[oldconc_keyplace])
            max_reds.append(st.session_state[max_reduction_keyplace])
            populations.append(st.session_state[population_keyplace])
        
        max_pollution_reduced = calculate_pollution_after_reduction(old_concs, max_reds)

        # Define LP Variables
        var_dict = dict()
        for i in range(1,num_zones+1,1):
            var_dict['x'+str(i)] = p.LpVariable("x"+str(i), lowBound = max_pollution_reduced[i-1], upBound = old_concs[i-1])

        # Objective Function 
        Lp_prob += (p.lpSum([populations[i-1] * var_dict['x'+str(i)] for i in range(1,num_zones+1,1)]))/sum(populations)
        
        # Constraints: 
        Lp_prob += (p.lpSum([populations[i-1] * var_dict['x'+str(i)] for i in range(1,num_zones+1,1)]))/sum(populations) == avg_conc_new

        status = Lp_prob.solve()   
        new_pollutions = [p.value(var_dict['x'+str(i)]) for i in range(1,num_zones+1,1)]
        def calculate_pct_reduction(old_pollutions, new_pollutions):
            reductions = [100*(old-new)/old for old, new in zip(old_pollutions, new_pollutions)]
            return reductions

        actual_reductions = calculate_pct_reduction(old_concs, new_pollutions)

        for i in range(num_zones):
            st.write(round(actual_reductions[i],1))        


    with col6:
        st.write("#### New zone average")
        for i in range(num_zones):
            st.write(round(new_pollutions[i],1))  
        st.write('#### :green[New Population weighted concentration:  {} μg/m3]'.format(round(avg_conc_new,1)))
    
#*************** TAB 3 - V3 ***************#
with tab3:
    costs_sourcewise_df = pd.read_csv('AQI_Simulator/inputs/cost_sourcewise.csv')
    costs_sourcewise_array = np.array(costs_sourcewise_df['cost per ug/m3'].values)
    
    c1, c2 = st.columns(2)
    zone_concentrations_df = pd.read_csv('AQI_Simulator/inputs/zone_concentrations_default.csv')
    sourceapportionment_df = pd.read_csv('AQI_Simulator/inputs/sourceapportionment_default.csv')
    reduction_sourcewise_df = pd.read_csv('AQI_Simulator/inputs/reduction_sourcewise.csv')

    reduction_sourcewise_df = reduction_sourcewise_df.round(1)
    with c2:
        st.write('#### Source wise reductions')
        column_config_dict = dict()
        zones = reduction_sourcewise_df.columns
        zones = [zone for zone in zones if zone[0]=='Z']
        for zone in zones:
            column_config_dict[zone] = st.column_config.NumberColumn(
                                                            zone,
                                                            format="%f %%",
                                                            min_value=0,
                                                            max_value=100,
                                                        )
        reduction_sourcewise_df = st.data_editor(reduction_sourcewise_df,
                                                 column_config=column_config_dict)

    sourceapportionment_array = np.array(sourceapportionment_df.iloc[:,1:].values)
    zone_concentrations_array = np.array(zone_concentrations_df.iloc[:,1:2].values)
    zone_populations_array = np.array(zone_concentrations_df.iloc[:,2:3].values)
    pop_weighted_conc = np.dot(zone_concentrations_array.T,zone_populations_array)/np.sum(zone_populations_array)
    
    reduction_sourcewise_array = np.array(reduction_sourcewise_df.iloc[:,1:].values)
    reduction_sourcewise_array = reduction_sourcewise_array/100
    reduction_sourcewise_array = 1- reduction_sourcewise_array

    source_concentrations_old = sourceapportionment_array*(zone_concentrations_array.T)
    source_concentrations_new = source_concentrations_old*reduction_sourcewise_array

    zone_concentrations_avg_new = np.sum(source_concentrations_new, axis=0)

    zone_concentrations_df['Avg.conc ug/m3 (new)'] = zone_concentrations_avg_new.round(1)
    
    with c1:
        zone_concentrations_df['Zone.pop (mil)'] = zone_concentrations_df['Zone.pop (mil)'].astype(str)
        # Because streamlit better edits floats when they are like strings. We will reconvert them to floats
        zone_concentrations_df = st.data_editor(zone_concentrations_df, num_rows="dynamic",
                                                column_config= {
                                                    "Zone.pop (mil)": st.column_config.TextColumn(
                                                        "Zone.pop (mil)"
                                                )})
        zone_concentrations_df['Zone.pop (mil)'] = zone_concentrations_df['Zone.pop (mil)'].astype(float)

    sourceapportionment_new = source_concentrations_new/zone_concentrations_avg_new

    source_pmsa_old = np.dot(source_concentrations_old,zone_populations_array)/np.sum(zone_populations_array)
    source_pmsa_new = np.dot(source_concentrations_new,zone_populations_array)/np.sum(zone_populations_array)

    
    pop_weighted_conc_new = np.dot(zone_concentrations_avg_new.T,zone_populations_array)/np.sum(zone_populations_array)

    net_reduction = 100*(pop_weighted_conc-pop_weighted_conc_new)/pop_weighted_conc
    net_reduction_sourcewise = 100*(source_pmsa_old - source_pmsa_new)/source_pmsa_old

    source_pmsa_new_pct = source_pmsa_new/pop_weighted_conc_new
    source_pmsa_old_pct = source_pmsa_old/pop_weighted_conc

    
    sources_cmap = {
                    'Pass.Travel': 'DarkGoldenRod', #gold
                    'Cooking':'DarkGray', #grey
                    'Freight':'LightCyan',
                    'Boundary':'DarkSlateBlue', #blue
                    'Dust':'SaddleBrown',#brown
                    'Industries': 'DarkMagenta', #magenta
                    'Heating': 'Darkorange', #orange
                    'Waste.Burn': 'IndianRed' #red
                    }
    
    source_pmsa_old_pct_fig = px.pie(values = list(100*source_pmsa_old_pct.T.flatten()),
                                     names = sourceapportionment_df['Source'].to_list(),
                                     color = sourceapportionment_df['Source'].to_list(),
                                     color_discrete_map=sources_cmap)
    
    source_pmsa_new_pct_fig = px.pie(values = list(100*source_pmsa_new_pct.T.flatten()),
                                     names = sourceapportionment_df['Source'].to_list(),
                                     color = sourceapportionment_df['Source'].to_list(),
                                     color_discrete_map=sources_cmap)
    
    
    costs_incurred = costs_sourcewise_array*(source_pmsa_old.T - source_pmsa_new.T).flatten()
    sum_cost_incurred = np.sum(costs_incurred)

    ## *** All calculations done - even for v4 *** ##

    #num_zoness = st.number_input("Number of Zones in the City: ", value=5)    
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.metric(label='Population weighted concentration - old',
                  value = round(pop_weighted_conc[0][0],1))
        
        st.write("### Source apportionment - old")
        column_config_dict = dict()
        zones = sourceapportionment_df.columns
        zones = [zone for zone in zones if zone[0]=='Z']
        for zone in zones:
            sourceapportionment_df[zone] = sourceapportionment_df[zone]*100
            column_config_dict[zone] = st.column_config.NumberColumn(
                                                            zone,
                                                            format="%.1f %%",
                                                            min_value=0,
                                                            max_value=100,
                                                        )
        
                
        sourceapportionment_df = st.data_editor(sourceapportionment_df,
                                              column_config=column_config_dict)
        
        total_df = pd.DataFrame(sourceapportionment_df.sum(numeric_only=True)).round()
        total_df = total_df.T
        total_df['Source'] = 'Total              '
        total_df = total_df[['Source','Z1','Z2','Z3','Z4','Z5','Z6','Z7','Z8','Z9','Z10']]

        if all([True if round(i) ==100 else False for i in sourceapportionment_df.sum(numeric_only=True).to_list()]):
            pass
        else:
            def style(val, props=''):
                return props if val > 100 else None
            
            st.dataframe(total_df.style.format(precision=2).map(style, props='color:red;',
                                            subset=['Z1','Z2','Z3','Z4','Z5','Z6','Z7','Z8','Z9','Z10']))
            st.write('Please check source apportionment values. Column Sum should be 100')

        st.plotly_chart(source_pmsa_old_pct_fig,
                        theme=None
                        )

    with c2:
        st.metric(label='Population weighted concentration - new',
                  value = round(pop_weighted_conc_new[0],1))
        st.write("### Source apportionment - new")

        sourceapportionment_new_df = pd.DataFrame(sourceapportionment_new)
        sourceapportionment_new_df['Source'] = sourceapportionment_df['Source']
        sourceapportionment_new_df.columns = ['Z1','Z2','Z3','Z4','Z5','Z6','Z7','Z8','Z9','Z10','Source']
        sourceapportionment_new_df = sourceapportionment_new_df[['Source','Z1','Z2','Z3','Z4','Z5','Z6','Z7','Z8','Z9','Z10']]

        column_config_dict = dict()
        zones = sourceapportionment_df.columns
        zones = [zone for zone in zones if zone[0]=='Z']
        for zone in zones:
            sourceapportionment_new_df[zone] = sourceapportionment_new_df[zone]*100
            column_config_dict[zone] = st.column_config.NumberColumn(
                                                            zone,
                                                            format="%.1f %%",
                                                            min_value=0,
                                                            max_value=100,
                                                        )
            
        st.data_editor(sourceapportionment_new_df, column_config=column_config_dict)
        
        st.plotly_chart(source_pmsa_new_pct_fig,
                        theme=None)
    
        st.metric(label='Cost incurred',
                  value = round(sum_cost_incurred))

with tab4:
    container = st.container(border=True)
    with container:
        net_reduction = st.slider('I want to reduce pollution in the city by:(%)', value=30)

        c1, c2, c3, c4= st.columns(4)
        max_reduction_cooking = c1.slider('Max reduction for Cooking(%)', value=50)
        max_reduction_heating = c1.slider('Max reduction for Heating(%)', value=30)
        max_reduction_wasteburn = c2.slider('Max reduction for WasteBurn(%)', value=50)
        max_reduction_industries = c2.slider('Max reduction for Industries(%)', value=30)
        max_reduction_freight = c3.slider('Max reduction for Freight(%)', value=30)
        max_reduction_passtravel = c3.slider('Max reduction for Pass Travel(%)', value=30)
        max_reduction_dust = c4.slider('Max reduction for Dust(%)', value=30)
        max_reduction_boundary = c4.slider('Max reduction for Boundary(%)', value=10)

    zone_concentrations_df = pd.read_csv('AQI_Simulator/inputs/zone_concentrations_default.csv')
    zone_pollutions_old = np.array(zone_concentrations_df['Avg.Conc ug/m3'])
    zone_populations = list(zone_concentrations_df['Zone.pop (mil)'])
    
    avg_pollution_old = sum(x * y for x, y in zip(zone_pollutions_old, zone_populations))/sum(zone_populations)
    avg_pollution_new = avg_pollution_old*(1-net_reduction/100)

    sourceapportionment_df = pd.read_csv('AQI_Simulator/inputs/sourceapportionment_default.csv')
    sourceapportionment_array = np.array(sourceapportionment_df.iloc[:,1:].values)
    zone_pollutions_old_sourcewise = sourceapportionment_array * zone_pollutions_old

    pmsa_old = np.dot(zone_pollutions_old_sourcewise,zone_populations)/np.sum(zone_populations)
    
    max_reductions_sourcewise = {'C':max_reduction_cooking,
                                'H':max_reduction_heating,
                                'W':max_reduction_wasteburn,
                                'I':max_reduction_industries,
                                'F':max_reduction_freight,
                                'P':max_reduction_passtravel,
                                'D':max_reduction_dust,
                                'B':max_reduction_boundary
                                }

    pmsa_new_maxreduced = pmsa_old * (100 - np.array(list(max_reductions_sourcewise.values())))/100

    # Create a LP Minimization problem 
    Lp_prob = p.LpProblem('Problem', sense = p.LpMinimize)  

    num_zones = 10 #user input

    var_dict = dict()
    # Source wise reduction in each zone
    for i in range(1,num_zones+1,1):
        var_dict['R'+str(i)+'C'] = p.LpVariable("R"+str(i)+'C', lowBound = 0, upBound = max_reductions_sourcewise['C']/100)
        var_dict['R'+str(i)+'H'] = p.LpVariable("R"+str(i)+'H', lowBound = 0, upBound = max_reductions_sourcewise['H']/100)
        var_dict['R'+str(i)+'W'] = p.LpVariable("R"+str(i)+'W', lowBound = 0, upBound = max_reductions_sourcewise['W']/100)
        var_dict['R'+str(i)+'I'] = p.LpVariable("R"+str(i)+'I', lowBound = 0, upBound = max_reductions_sourcewise['I']/100)
        var_dict['R'+str(i)+'F'] = p.LpVariable("R"+str(i)+'F', lowBound = 0, upBound = max_reductions_sourcewise['F']/100)
        var_dict['R'+str(i)+'P'] = p.LpVariable("R"+str(i)+'P', lowBound = 0, upBound = max_reductions_sourcewise['P']/100)
        var_dict['R'+str(i)+'D'] = p.LpVariable("R"+str(i)+'D', lowBound = 0, upBound = max_reductions_sourcewise['D']/100)
        var_dict['R'+str(i)+'B'] = p.LpVariable("R"+str(i)+'B', lowBound = 0, upBound = max_reductions_sourcewise['B']/100)

    # Upper bounds -- currently for each zone. need to change it to ovr all.

    # Objective Function 
    Lp_prob += (p.lpSum([zone_populations[i-1] * zone_pollutions_old_sourcewise[idx][i-1] * var_dict['R'+str(i)+s] for idx, s in enumerate(['C', 'H', 'W', 'I', 'F', 'P' ,'D', 'B']) for i in range(1,num_zones+1,1)]))/sum(zone_populations)

    # Constraints: 
    Lp_prob += (p.lpSum([zone_populations[i-1] * zone_pollutions_old_sourcewise[idx][i-1] * var_dict['R'+str(i)+s] for idx, s in enumerate(['C', 'H', 'W', 'I', 'F', 'P' ,'D', 'B']) for i in range(1,num_zones+1,1)]))/sum(zone_populations) == (avg_pollution_old - avg_pollution_new)

    for idx, s in enumerate(['C', 'H', 'W', 'I', 'F', 'P' ,'D', 'B']):
        Lp_prob += p.lpSum([zone_populations[i-1] * zone_pollutions_old_sourcewise[0][i-1] * var_dict['R'+str(i)+s] for i in range(1,num_zones+1,1)])/sum(zone_populations) <= pmsa_old[idx] - pmsa_new_maxreduced[idx]

    # Display the problem 
    #print(Lp_prob) 

    status = Lp_prob.solve()
    print("############")   
    print(p.LpStatus[status])   # The solution status 

    #print([p.value(var_dict['Z'+str(i)]) for i in range(1,num_zones+1,1)], p.value(Lp_prob.objective))
    reductions = [p.value(var_dict['R'+str(i)+s]) for s in ['C', 'H', 'W', 'I', 'F', 'P' ,'D', 'B'] for i in range(1,num_zones+1,1)]
    reductions_array = np.array(reductions).reshape(8, 10)

    c1, c2 = st.columns(2)
    if status < 1:
        st.write("## :red[Problem cannot be solved with given constraints]")
    else:
        with c2:
            st.write('### Source wise reductions')
            reduction_sourcewise_df = pd.DataFrame(reductions_array*100)
            reduction_sourcewise_df.columns = ['Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6', 'Z7', 'Z8', 'Z9', 'Z10']
            reduction_sourcewise_df.index = list(sourceapportionment_df.Source)
            reduction_sourcewise_df = reduction_sourcewise_df.reset_index().rename(columns={'index':'Source'})
            column_config_dict = dict()
            zones = reduction_sourcewise_df.columns
            zones = [zone for zone in zones if zone[0]=='Z']
            for zone in zones:
                column_config_dict[zone] = st.column_config.NumberColumn(
                                                                zone,
                                                                format="%0.1f %%",
                                                                min_value=0,
                                                                max_value=100,
                                                            )
            reduction_sourcewise_df = st.data_editor(reduction_sourcewise_df,
                                                    column_config=column_config_dict
                                                    )
            
        reduction_sourcewise_array = np.array(reduction_sourcewise_df.iloc[:,1:].values)
        reduction_sourcewise_array = reduction_sourcewise_array/100
        reduction_sourcewise_array = 1 - reduction_sourcewise_array
        zone_pollutions_new_sourcewise = zone_pollutions_old_sourcewise*reduction_sourcewise_array

        zone_concentrations_avg_new = np.sum(zone_pollutions_new_sourcewise, axis=0)

        zone_concentrations_df['Avg.conc ug/m3 (new)'] = zone_concentrations_avg_new.round(1)

        with c1:
            zone_concentrations_df['Zone.pop (mil)'] = zone_concentrations_df['Zone.pop (mil)'].astype(str)
            # Because streamlit better edits floats when they are like strings. We will reconvert them to floats
            zone_concentrations_df = st.data_editor(zone_concentrations_df, num_rows="dynamic",
                                                    column_config= {
                                                        "Zone.pop (mil)": st.column_config.TextColumn(
                                                            "Zone.pop (mil)"
                                                    )},
                                                    key='zone_pollutions')
            zone_concentrations_df['Zone.pop (mil)'] = zone_concentrations_df['Zone.pop (mil)'].astype(float)

        sourceapportionment_new = zone_pollutions_new_sourcewise/zone_concentrations_avg_new
        pmsa_old = np.dot(zone_pollutions_old_sourcewise,zone_populations)/np.sum(zone_populations)
        pmsa_new = np.dot(zone_pollutions_new_sourcewise,zone_populations)/np.sum(zone_populations)

        pop_weighted_conc_new = np.dot(zone_concentrations_avg_new.T,zone_populations)/np.sum(zone_populations)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric(label='Pop. weighted concentration - old',
                    value = round(avg_pollution_old,1))
        with c3:
            st.metric(label='Pop. weighted concentration - new',
                    value = round(pop_weighted_conc_new,1))
        with c4:
            st.metric(label='Net reduction (%)',
                    value = round(100*(avg_pollution_old-pop_weighted_conc_new)/avg_pollution_old,1))
        
        c1, c2 = st.columns(2)
        with c1:        
            st.write("### Source apportionment - old")
            column_config_dict = dict()
            zones = sourceapportionment_df.columns
            zones = [zone for zone in zones if zone[0]=='Z']
            for zone in zones:
                sourceapportionment_df[zone] = sourceapportionment_df[zone]*100
                column_config_dict[zone] = st.column_config.NumberColumn(
                                                                zone,
                                                                format="%.1f %%",
                                                                min_value=0,
                                                                max_value=100,
                                                            )
            
                    
            sourceapportionment_df = st.data_editor(sourceapportionment_df,
                                                column_config=column_config_dict,
                                                key='sourceapportionment_v4')
            
            total_df = pd.DataFrame(sourceapportionment_df.sum(numeric_only=True)).round()
            total_df = total_df.T
            total_df['Source'] = 'Total              '
            total_df = total_df[['Source','Z1','Z2','Z3','Z4','Z5','Z6','Z7','Z8','Z9','Z10']]

            if all([True if round(i) ==100 else False for i in sourceapportionment_df.sum(numeric_only=True).to_list()]):
                pass
            else:
                def style(val, props=''):
                    return props if val > 100 else None
                
                st.dataframe(total_df.style.format(precision=2).map(style, props='color:red;',
                                                subset=['Z1','Z2','Z3','Z4','Z5','Z6','Z7','Z8','Z9','Z10']))
                st.write('Please check source apportionment values. Column Sum should be 100')

            ## PLOTLY FIGURE
            source_pmsa_old_pct_fig = px.pie(values = list(100*pmsa_old.T.flatten()),
                                        names = sourceapportionment_df['Source'].to_list(),
                                        color = sourceapportionment_df['Source'].to_list(),
                                        color_discrete_map=sources_cmap)
        
            
            st.plotly_chart(source_pmsa_old_pct_fig,
                            theme=None
                            )

        with c2:
            st.write("### Source apportionment - new")

            sourceapportionment_new_df = pd.DataFrame(sourceapportionment_new)
            sourceapportionment_new_df['Source'] = sourceapportionment_df['Source']
            sourceapportionment_new_df.columns = ['Z1','Z2','Z3','Z4','Z5','Z6','Z7','Z8','Z9','Z10','Source']
            sourceapportionment_new_df = sourceapportionment_new_df[['Source','Z1','Z2','Z3','Z4','Z5','Z6','Z7','Z8','Z9','Z10']]

            column_config_dict = dict()
            zones = sourceapportionment_df.columns
            zones = [zone for zone in zones if zone[0]=='Z']
            for zone in zones:
                sourceapportionment_new_df[zone] = sourceapportionment_new_df[zone]*100
                column_config_dict[zone] = st.column_config.NumberColumn(
                                                                zone,
                                                                format="%.1f %%",
                                                                min_value=0,
                                                                max_value=100,
                                                            )
                
            st.data_editor(sourceapportionment_new_df, column_config=column_config_dict, key='sourceapportionment_new_v4')
            
            ## PLOTLY FIGURE
            source_pmsa_new_pct_fig = px.pie(values = list(100*pmsa_new.T.flatten()),
                                        names = sourceapportionment_df['Source'].to_list(),
                                        color = sourceapportionment_df['Source'].to_list(),
                                        color_discrete_map=sources_cmap)
            
            st.plotly_chart(source_pmsa_new_pct_fig,
                            theme=None)
            
            costs_incurred = costs_sourcewise_array*(pmsa_old.T - pmsa_new.T).flatten()
            sum_cost_incurred = np.sum(costs_incurred)
            st.metric(label='Cost incurred',
                    value = round(sum_cost_incurred))