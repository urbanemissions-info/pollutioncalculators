import streamlit as st

st.set_page_config(layout="wide", page_title="Waste management calculator")

st.write("## Waste management calculator")
hide_streamlit_style = """
<style>
.st-emotion-cache-16idsys p {
    font-size:24px;
}

</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.sidebar.write("## Input your city waste management details  :gear:")
pop = st.sidebar.number_input('Population:', placeholder="Population of the city...", value = 10000000)
urbanshare = st.sidebar.slider('Urban share of population:', min_value=0, max_value=100, value=70)
waste_collection = st.sidebar.slider('Waste Collection (%):', min_value=0, max_value=100, value=90)

## Calculate waste burnt per day
urban_population = pop * urbanshare/100
rural_population = pop - urban_population
urban_waste = urban_population * 1 #1 kg/person
rural_waste = rural_population * 0.5 # 0.5 kg/person

total_waste = (urban_waste + rural_waste)/1000 #Tonnes per day
total_waste_collected = (total_waste * waste_collection/100)/1000 #Tonnes per day
waste_burn_open = total_waste - total_waste_collected

st.write("### Total waste collected")
st.metric(label = "Total waste collected",
          label_visibility = "hidden",
          value = "{} TPD".format(total_waste_collected),
          #delta="1.2 TPD"
          )