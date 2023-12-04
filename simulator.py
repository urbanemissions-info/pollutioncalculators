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
    num_zones = st.number_input("Number of Zones in the City: ", value=10)    
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
        default_values = [1.1, 1.3, 1.9, 2.0, 2.1, 1.9, 2.5, 0.5, 1.0, 0.1]
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
        default_values = [55, 65, 75, 85, 95, 100, 110, 35, 65, 20]
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
        st.write('Population weighted concentration: {} μg/m3'.format(round(pop_weighted_conc,1)))

    
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
        st.write('New Population weighted concentration:  {} μg/m3'.format(round(new_pop_weighted_conc,1)))

        net_reduction = round((pop_weighted_conc-new_pop_weighted_conc)/pop_weighted_conc, 1)
        st.write('#### :green[Net reduction:  {} %]'.format(round(net_reduction,1)))

