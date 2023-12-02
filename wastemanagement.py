import streamlit as st
st.set_page_config(layout="wide", page_title="Waste management calculator")

# Following line will help in seeing dynamic session states
#"st.session_state object:" , st.session_state

# Type of update
if 'update_type' not in st.session_state:
    st.session_state.update_type = 'primary_input'

# Static value on which delta will be caclulated
if 'collection_efficiency_static' not in st.session_state:
    st.session_state.collection_efficiency_static = 55

# Static value on which delta will be caclulated
if 'burnrate_static' not in st.session_state:
    st.session_state.burnrate_static = 30

def update_collection_efficiency():
    st.session_state.update_type = 'callback'
    st.session_state.collection_efficiency = st.session_state.collection_efficiency_static * (1 + st.session_state.delta_wastecollection/100)
    if st.session_state.collection_efficiency >100:
        st.session_state.collection_efficiency = 100

def update_burn_rate():
    st.session_state.update_type = 'callback'
    st.session_state.burnrate = st.session_state.burnrate_static * (1 - st.session_state.delta_wasteburn/100)
    if st.session_state.burnrate < 0:
        st.session_state.burnrate = 0


def reset_delta_efficiency():
    if st.session_state.update_type == 'primary_input':
        st.session_state.collection_efficiency_static =  st.session_state.collection_efficiency
        st.session_state.delta_wastecollection = 0
    # Make the default update type primary so that the static value changes on user input
    st.session_state.update_type = 'primary_input'

def reset_burn_efficiency():
    if st.session_state.update_type == 'primary_input':
        st.session_state.burnrate_static =  st.session_state.burnrate
        st.session_state.delta_wasteburn = 0
    # Make the default update type primary so that the static value changes on user input
    st.session_state.update_type = 'primary_input'

    

    

## CSS Custom styles
## metric label font size and weight
## sidebar width
hide_streamlit_style = """
<style>
.st-emotion-cache-16idsys p {
    font-size:24px;
    font-weight:bold;
}


section[data-testid="stSidebar"] {
            width: 500px !important; # Set the width of side bar to your desired value
        }

</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# SIDE BAR
## Sidebar title
st.sidebar.write("## Input your city waste management details  :gear:")

## User inputs
pop = st.sidebar.number_input('Population (in millions):', placeholder="Population of the city ...", value = 2.3)
urbanshare = st.sidebar.slider('Urban share of population (%)', min_value=0, max_value=100, value=80)

percapita_waste_gen_urban = st.sidebar.number_input('Per capita waste generated (urban) (kg/cap/day):',
                                                    placeholder="Per capita waste generated (urban) (kg/cap/day)",
                                                    value = 0.4)
percapita_waste_gen_rural = st.sidebar.number_input('Per capita waste generated (rural) (kg/cap/day):',
                                                    placeholder="Per capita waste generated (rural) (kg/cap/day)",
                                                    value = 0.3)

wet_waste_urban = st.sidebar.slider('Wet waste in Urban (%)', min_value=0, max_value=100, value=30)
wet_waste_rural = st.sidebar.slider('Wet waste in Rural (%)', min_value=0, max_value=100, value=30)


waste_collection_efficiency_urban = st.sidebar.slider('Waste collection efficiency in Urban (%)', min_value=0, max_value=100, value=55,
                                                      key='collection_efficiency', on_change=reset_delta_efficiency)
waste_collection_efficiency_rural = st.sidebar.slider('Waste collection efficiency in Rural (%)', min_value=0, max_value=100, value=5)

waste_burn_rate_urban = st.sidebar.slider('Waste burn rate in Urban (%)', min_value=0, max_value=100, value=30,
                                          key='burnrate', on_change=reset_burn_efficiency)
waste_burn_rate_rural = st.sidebar.slider('Waste burn rate in Rural (%)', min_value=0, max_value=100, value=100)

landfill_capacity = st.sidebar.number_input('Landfilll capacity (tons/day):',
                                                    placeholder="Landfill capacity (tons/day)",
                                                    value = 300)

landfill_burn_rate = st.sidebar.slider('Landfill burn rate (%)', min_value=0, max_value=100, value=2)

## intermediary variables calculations
urban_population = pop * urbanshare/100
rural_population = pop - urban_population

urban_waste_generated = 1000000 * urban_population * percapita_waste_gen_urban/1000 # 1000 - Tonnes per day
rural_waste_generated = 1000000 * rural_population * percapita_waste_gen_rural/1000 # Tonnes per day
total_waste_generated = (urban_waste_generated + rural_waste_generated)

dry_waste_urban = urban_waste_generated * (1 - wet_waste_urban/100)
dry_waste_rural = rural_waste_generated * (1 - wet_waste_rural/100)
total_dry_waste = dry_waste_urban + dry_waste_rural

urban_waste_collected = (dry_waste_urban * waste_collection_efficiency_urban/100)
rural_waste_collected = (dry_waste_rural * waste_collection_efficiency_rural/100)
total_waste_collected = urban_waste_collected + rural_waste_collected

waste_uncollected_urban = dry_waste_urban - urban_waste_collected
waste_uncollected_rural = dry_waste_rural - rural_waste_collected
total_waste_uncollected = waste_uncollected_urban + waste_uncollected_rural

waste_burnt_urban = waste_uncollected_urban * waste_burn_rate_urban/100
waste_burnt_rural = waste_uncollected_rural * waste_burn_rate_rural/100
total_waste_burnt_kerbside = waste_burnt_urban + waste_burnt_rural #burnt at kerbside

landfillwaste_burnt_urban = landfill_burn_rate/100 * urban_waste_collected
landfillwaste_burnt_rural = landfill_burn_rate/100 * rural_waste_collected
total_waste_burnt_landfill = landfillwaste_burnt_urban + landfillwaste_burnt_rural

total_waste_burnt = total_waste_burnt_kerbside + total_waste_burnt_landfill
tab1, tab2 = st.tabs(["V1", "V2"])

with tab1:
    # Title
    st.write("## Waste management calculator")
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
    st.write("## Waste management calculator")
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
        
    st.write("# Actionables")
    
    increase_waste_collection = st.slider('I want to increase my waste collection efficiency by (%)', min_value=0, max_value=100, value=0,
                                          key='delta_wastecollection',
                                          on_change=update_collection_efficiency)
    
    c1, c2 = st.columns(2)
    c1.write("#### Old Waste collection Efficiency {}".format(round(st.session_state.collection_efficiency_static)))
    c2.write("#### New Waste collection Efficiency {}".format(round(st.session_state.collection_efficiency)))
    if(waste_collection_efficiency_urban>=100):
        st.write("##### :green[Max efficiency acheived]")

    reduce_waste_burn = st.slider('I want to reduce my waste burn rate by (%)', min_value=0, max_value=100, value=0,
                                          key='delta_wasteburn',
                                          on_change=update_burn_rate)
    c1, c2 = st.columns(2)
    c1.write("#### Old Waste burn rate {}".format(round(st.session_state.burnrate_static)))
    c2.write("#### New Waste burn rate {}".format(round(st.session_state.burnrate)))
    if(waste_burn_rate_urban<=0):
        st.write("##### :green[Max efficiency acheived]")
