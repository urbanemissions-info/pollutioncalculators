import streamlit as st
st.set_page_config(layout="wide", page_title="Waste management calculator")

## CSS Custom styles
hide_streamlit_style = """
<style>
.st-emotion-cache-16idsys p {
    font-size:24px;
}

</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)



# Title
st.write("## Waste management calculator")

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

waste_collection_efficiency_urban = st.sidebar.slider('Waste collection efficiency in Urban (%)', min_value=0, max_value=100, value=55)
waste_collection_efficiency_rural = st.sidebar.slider('Waste collection efficiency in Rural (%)', min_value=0, max_value=100, value=5)

waste_burn_rate_urban = st.sidebar.slider('Waste burn rate in Urban (%)', min_value=0, max_value=100, value=30)
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

st.write("### Total waste generated")
st.metric(label = "Total waste generated",
          label_visibility = "hidden",
          value = "{} TPD".format(round(total_waste_generated)),
          #delta="1.2 TPD"
          )

st.write("### Total waste collected")
st.metric(label = "Total waste collected",
          label_visibility = "hidden",
          value = "{} TPD".format(round(total_waste_collected)),
          #delta="1.2 TPD"
          )

st.write("### Total waste burnt")
st.metric(label = "Total waste burnt",
          label_visibility = "hidden",
          value = "{} TPD".format(round(total_waste_burnt)),
          #delta="1.2 TPD"
          )