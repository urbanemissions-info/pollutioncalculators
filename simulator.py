import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
st.set_page_config(layout="wide", page_title="AQI Simulator")

# Following line will help in seeing dynamic session states
#"st.session_state object:" , st.session_state


import random
import string

## CSS Custom styles
## metric label font size and weight
## customise slider
hide_streamlit_style = """
<style>
.st-emotion-cache-16idsys p {
    font-size:24px;
    font-weight:bold;
}

.st-emotion-cache-z5fcl4 {
    padding: 1rem 2rem 10rem !important;
        }

.st-di {
    padding-top: 13.3px;
}

.st-dh {
    padding-top: 13.3px;
}

.st-emotion-cache-1inwz65 {
    font-size: 0px;
}

code {
    font-size: 1.6em;
}
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


st.title("AQI Simulator")
tab1, tab2, tab3, tab4 = st.tabs(["V1", "V2", "V3", "V4"])

#*************** TAB 1 - V1 ***************#
with tab1:
    num_zones = st.number_input("Number of Zones in the City: ", value=5)    
    col1, col2, col3, col4, col5 = st.columns(5)

    variables_dict = dict()

    with col1:
        st.write("### Zone")
        default_values_zones = ['Z1', 'Z2', 'Z3', 'Z4', 'Z5', 'Z6', 'Z7', 'Z8', 'Z9', 'Z10']
        for i in range(num_zones):
            st.text_input("Zone", value=default_values_zones[i],
                            label_visibility='collapsed')

    with col2:
        st.write("### Zone.pop (mil)")
        default_values = [1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3, 1.3]
        var_name = f"pop_{i}"
        for i in range(num_zones):
            keyplace = default_values_zones[i]+'_pop'
            if keyplace not in st.session_state:
                st.session_state[keyplace] = default_values[i] #Default val
            variables_dict[var_name] = st.number_input("Avg.Conc μg/m3",
                        label_visibility='collapsed', key=keyplace)
            
        pops = []
        for i in range(num_zones):
            keyplace = default_values_zones[i]+'_pop'
            pops.append(st.session_state[keyplace])
            total_pop = sum(pops)
        
        st.write('Total: {} mil'.format(total_pop))
            
    with col3:
        st.write("### Avg.Conc μg/m3")
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
        st.write("### % reduction")
        var_name = f"reduction_{i}"
        for i in range(num_zones):
            keyplace = default_values_zones[i]+'_reduction'
            # if keyplace not in st.session_state:
            #     st.session_state[keyplace] = default_values[i] #Default val
            variables_dict[var_name] = st.slider("Avg.Conc μg/m3",
                        label_visibility='collapsed', key=keyplace)
            
            
    with col5:
        st.write("### New zone average")
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


#*************** TAB 3 - V3 ***************#
with tab3:
    c1, c2 = st.columns(2)
    zone_concentrations_df = pd.read_csv('zone_concentrations_default.csv')
    
    with c1:
        zone_concentrations_df['Zone.pop (mil)'] = zone_concentrations_df['Zone.pop (mil)'].astype(str)
        # Because streamlit better edits floats when they are like strings. We will reconvert them to floats
        zone_concentrations_df = st.data_editor(zone_concentrations_df, num_rows="dynamic",
                                                column_config= {
                                                    "Zone.pop (mil)": st.column_config.TextColumn(
                                                        "Zone.pop (mil)"
                                                )})
        zone_concentrations_df['Zone.pop (mil)'] = zone_concentrations_df['Zone.pop (mil)'].astype(float)
        


    sourceapportionment_df = pd.read_csv('sourceapportionment_default.csv')
    reduction_sourcewise_df = pd.read_csv('reduction_sourcewise.csv')
    with c2:
        column_config_dict = {}
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

    zone_concentrations_df['new_conc'] = zone_concentrations_avg_new
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
    
    ## *** All calculations done *** ##

    #num_zoness = st.number_input("Number of Zones in the City: ", value=5)    
    

    
    st.write(np.sum(zone_populations_array))
    c1, c2 = st.columns(2)
    
    with c1:
        st.metric(label='Population weighted concentration - old',
                  value = round(pop_weighted_conc[0][0],2))
        st.write("### Source apportionment - old")
        st.plotly_chart(source_pmsa_old_pct_fig,
                        theme=None
                        )

    with c2:
        st.metric(label='Population weighted concentration - new',
                  value = round(pop_weighted_conc_new[0],2))
        st.write("### Source apportionment - new")
        st.plotly_chart(source_pmsa_new_pct_fig,
                        theme=None)
    
