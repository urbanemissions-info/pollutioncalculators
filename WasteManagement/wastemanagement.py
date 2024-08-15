import streamlit as st
st.set_page_config(layout="wide", page_title="Waste management calculator")

import random

# Following line will help in seeing dynamic session states
#"st.session_state object:" , st.session_state

# Type of update
if 'update_type' not in st.session_state:
    st.session_state.update_type = None

def update_collection_efficiency():
    st.session_state.update_type = 'callback'
    st.session_state.collection_efficiency = waste_collection_efficiency_urban * (1 + st.session_state.delta_wastecollection/100)
    if st.session_state.collection_efficiency >100:
        st.session_state.collection_efficiency = 100
    
def update_burn_rate():
    st.session_state.update_type = 'callback'
    st.session_state.burnrate = waste_burn_rate_urban * (1 - st.session_state.delta_wasteburn/100)
    if st.session_state.burnrate < 0:
        st.session_state.burnrate = 0

def update_gen_rate():
    st.session_state.update_type = 'callback'
    st.session_state.genrate = percapita_waste_gen_urban * (1 + st.session_state.delta_wastegeneration/100)

def reset_delta_efficiency():
    st.session_state.update_type = 'primary_input'
    if st.session_state.update_type == 'primary_input':
        st.session_state.delta_wastecollection = 0
    

def reset_burn_efficiency():
    st.session_state.update_type = 'primary_input'
    if st.session_state.update_type == 'primary_input':
        st.session_state.delta_wasteburn = 0

    

    

## CSS Custom styles
## metric label font size and weight
## sidebar width
hide_streamlit_style = """
<style>
.st-emotion-cache-16idsys p {
    font-size:24px;
    font-weight:bold;
}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# SIDE BAR
## Sidebar title
st.sidebar.write("## Input your city waste management details  :gear:")

## User inputs
pop = st.sidebar.number_input('Population (in millions):', placeholder="Population of the city ...", value = 2.3)

st.sidebar.write("### Urban inputs  :gear:")
urbanshare = st.sidebar.slider('Urban share of population (%)', min_value=0, max_value=100, value=80)

# URBAN GEN RATE - HAS CALLBACK
if 'urban_genrate' not in st.session_state:
    st.session_state.urban_genrate = 0.4 #Default val
percapita_waste_gen_urban = st.sidebar.number_input('Per capita waste generated (urban) (kg/cap/day):',
                                                    placeholder="Per capita waste generated (urban) (kg/cap/day)",
                                                    key = 'urban_genrate'
                                                    )
if st.session_state.update_type != 'callback':
    st.session_state.genrate = percapita_waste_gen_urban
urban_genrate = st.session_state.genrate

# URBAN COLLECTION RATE - HAS CALLBACK
if 'urban_col_efficiency' not in st.session_state:
    st.session_state.urban_col_efficiency = 55 #Default val
waste_collection_efficiency_urban = st.sidebar.slider('Waste collection efficiency in Urban (%)',
                                                      min_value=0, max_value=100,
                                                      key = 'urban_col_efficiency',
                                                      on_change=reset_delta_efficiency)
if st.session_state.update_type != 'callback':
    st.session_state.collection_efficiency = waste_collection_efficiency_urban
urban_col_efficiency = st.session_state.collection_efficiency

# URBAN BURN RATE - HAS CALLBACK
if 'urban_burnrate' not in st.session_state:
    st.session_state.urban_burnrate = 30 #Default val
waste_burn_rate_urban = st.sidebar.slider('Waste burn rate in Urban (%)',
                                          min_value=0, max_value=100,
                                          key='urban_burnrate',
                                          on_change=reset_burn_efficiency)
if st.session_state.update_type != 'callback':
    st.session_state.burnrate = waste_burn_rate_urban
urban_burnrate = st.session_state.burnrate

landfill_capacity = st.sidebar.number_input('Landfill capacity (tons/day):',
                                                    placeholder="Landfill capacity (tons/day)",
                                                    value = 250)

landfill_burn_rate = st.sidebar.slider('Landfill burn rate (%)', min_value=0, max_value=100, value=2)
wet_waste_urban = st.sidebar.slider('Wet waste in Urban (%)', min_value=0, max_value=100, value=30)

## RURAL INPUTS
st.sidebar.write("### Rural inputs  :gear:")
percapita_waste_gen_rural = st.sidebar.number_input('Per capita waste generated (rural) (kg/cap/day):',
                                                    placeholder="Per capita waste generated (rural) (kg/cap/day)",
                                                    value = 0.3)


waste_collection_efficiency_rural = st.sidebar.slider('Waste collection efficiency in Rural (%)', min_value=0, max_value=100, value=5)

waste_burn_rate_rural = st.sidebar.slider('Waste burn rate in Rural (%)', min_value=0, max_value=100, value=100)
wet_waste_rural = st.sidebar.slider('Wet waste in Rural (%)', min_value=0, max_value=100, value=30)

## intermediary variables calculations
urban_population = pop * urbanshare/100
rural_population = pop - urban_population

urban_waste_generated = 1000000 * urban_population * urban_genrate/1000 # 1000 - Tonnes per day
rural_waste_generated = 1000000 * rural_population * percapita_waste_gen_rural/1000 # Tonnes per day
total_waste_generated = (urban_waste_generated + rural_waste_generated)

dry_waste_urban = urban_waste_generated * (1 - wet_waste_urban/100)
dry_waste_rural = rural_waste_generated * (1 - wet_waste_rural/100)
total_dry_waste = dry_waste_urban + dry_waste_rural

urban_waste_collected = (dry_waste_urban * urban_col_efficiency/100)
rural_waste_collected = (dry_waste_rural * waste_collection_efficiency_rural/100)
total_waste_collected = urban_waste_collected + rural_waste_collected

waste_uncollected_urban = dry_waste_urban - urban_waste_collected
waste_uncollected_rural = dry_waste_rural - rural_waste_collected
total_waste_uncollected = waste_uncollected_urban + waste_uncollected_rural

waste_burnt_urban = waste_uncollected_urban * urban_burnrate/100 #Used sessoin state var
waste_burnt_rural = waste_uncollected_rural * waste_burn_rate_rural/100
total_waste_burnt_kerbside = waste_burnt_urban + waste_burnt_rural #burnt at kerbside

landfillwaste_burnt_urban = landfill_burn_rate/100 * urban_waste_collected
landfillwaste_burnt_rural = landfill_burn_rate/100 * rural_waste_collected
total_waste_burnt_landfill = landfillwaste_burnt_urban + landfillwaste_burnt_rural

total_waste_burnt = total_waste_burnt_kerbside + total_waste_burnt_landfill
col1, col2, col3 = st.columns([11,1,1])
with col3:
    st.image("assets/logo.grid.3_transp.png", width=70)

with col1:
    st.write("## Waste management calculator")

tab1, tab2 = st.tabs(["Calculator", "Simulator"])

with tab1:
    # Title
    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label = "Total waste generated",
            label_visibility = "visible",
            value = "{} TPD".format(round(total_waste_generated)),
            #delta="1.2 TPD"
            )

    with col2:
        st.metric(label = "Total waste collected",
                label_visibility = "visible",
            value = "{} TPD".format(round(total_waste_collected)),
            #delta="1.2 TPD"
            )
        
        st.write("")
        
        st.metric(label = "Current Landfill capacity",
                label_visibility = "visible",
            value = "{} TPD".format(round(landfill_capacity)),
            #delta="1.2 TPD"
            )
        
        if (total_waste_collected > landfill_capacity):
            st.write("#### :red[Total waste collected is more than landfill capacity]")
        else:
            st.write("#### :blue[Landfill capacity can manage the waste collected]")


    with col3:
        st.metric(label = "Total waste burnt",
                label_visibility = "visible",
                value = "{} TPD".format(round(total_waste_burnt)),
                #delta="1.2 TPD"
                )
    
with tab2:
    # Title        
    st.write("### Actionables - Urban interventions")
    
    if 'delta_wastecollection' not in st.session_state:
        st.session_state.delta_wastecollection = 0 #Default val
    increase_waste_collection = st.slider('I want to increase my waste collection efficiency by (%)',
                                          min_value=0, max_value=100,
                                          key='delta_wastecollection',
                                          on_change=update_collection_efficiency)
    
    c1, c2 = st.columns(2)
    c1.write("**Old Waste collection Efficiency**: {} %".format(round(waste_collection_efficiency_urban)))
    c2.write("**New Waste collection Efficiency**: {} %".format(round(st.session_state.collection_efficiency)))
    if(waste_collection_efficiency_urban>=100):
        st.write("##### :green[Max efficiency acheived]")

    if 'delta_wasteburn' not in st.session_state:
        st.session_state.delta_wasteburn = 0 #Default val
    reduce_waste_burn = st.slider('I want to reduce my waste burn rate by (%)',
                                  min_value=0, max_value=100,
                                  key='delta_wasteburn',
                                  on_change=update_burn_rate)
    c1, c2 = st.columns(2)
    c1.write("**Old Waste burn rate**: {} %".format(round(waste_burn_rate_urban)))
    c2.write("**New Waste burn rate**: {} %".format(round(st.session_state.burnrate)))
    if(waste_burn_rate_urban<=0):
        st.write("##### :green[Max efficiency acheived]")

    if 'delta_wastegeneration' not in st.session_state:
        st.session_state.delta_wastegeneration = 0 #Default val
    change_waste_generation = st.slider('I want to change my waste generate rate by (%)',
                                        min_value=-100, max_value=100,
                                          key='delta_wastegeneration',
                                          on_change=update_gen_rate)

    c1, c2 = st.columns(2)
    c1.write("**Old Waste generation rate**: {} (kg/cap/day)".format(round(percapita_waste_gen_urban, 2)))
    c2.write("**New Waste generation rate**: {} (kg/cap/day)".format(round(st.session_state.genrate, 2)))

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label = "Total waste generated",
            label_visibility = "visible",
            value = "{} TPD".format(round(total_waste_generated)),
            #delta="1.2 TPD"
            )
        
    with col2:
        st.metric(label = "Total waste collected",
                label_visibility = "visible",
            value = "{} TPD".format(round(total_waste_collected)),
            #delta="1.2 TPD"
            )
        
        st.write("")
        
        st.metric(label = "Current Landfill capacity",
                label_visibility = "visible",
            value = "{} TPD".format(round(landfill_capacity)),
            #delta="1.2 TPD"
            )
        
        if (total_waste_collected > landfill_capacity):
            st.write("#### :red[Total waste collected is more than landfill capacity]")
        else:
            st.write("#### :blue[Landfill capacity can manage the waste collected]")


    with col3:
        st.metric(label = "Total waste burnt",
                label_visibility = "visible",
                value = "{} TPD".format(round(total_waste_burnt)),
                #delta="1.2 TPD"
                )
        