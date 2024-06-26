import streamlit as st
import pandas as pd
import numpy as np
from streamlit.components.v1 import html
# from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import pickle
import joblib
import io
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import base64
from functions import *

st.set_page_config(layout="wide",page_title="Carbon Footprint Calculator", page_icon="./media/favicon.ico")

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

background = get_base64("./style/envirovibes.jpg")
icon2 = get_base64("./media/icon2.png")
icon3 = get_base64("./media/icon3.png")

with open("./style/style.css", "r") as style:
    css=f"""<style>{style.read().format(background=background, icon2=icon2, icon3=icon3)}</style>"""
    st.markdown(css, unsafe_allow_html=True)

def script():
    with open("./style/scripts.js", "r", encoding="utf-8") as scripts:
        open_script = f"""<script>{scripts.read()}</script> """
        html(open_script, width=0, height=0)

#for indentation
left, middle, right = st.columns([2,3.5,2])
main, comps , result = middle.tabs([" ", " ", " "])

with open("./style/main.md", "r", encoding="utf-8") as main_page:
    main.markdown(f"""{main_page.read()}""")


_,but,_ = main.columns([1,2,1])
if but.button("Generate Now!", type="primary"):
    click_element('tab-1')

tab1, tab2, tab3, tab4, tab5 = comps.tabs([" Personal"," Travel"," Waste","Energy","Consumption"])
tab_result,_ = result.tabs([" "," "])

def component():
    tab1col1, tab1col2 = tab1.columns(2)
    shower = tab1.selectbox(' Did you take a sub 10 minute shower, this week?', ["Yes", "No"])
    eat_meat = tab1.selectbox(' Did you give up meat for a day, this week?', ["Yes", "No"])
    brush_teeth = tab1.selectbox('Did you turn off the tap while brushing your teeth, this week?', ["Yes", "No"])
    leftovers = tab1.selectbox('Did you not waste any food on your plate, this week?', ["Yes", "No"])

    carpool = tab2.selectbox('Did you carpool at least once, this week? ',["Yes", "No"])

    water_bottle = tab3.selectbox('Did you use your own water bottle instead of a single use one, this week?', ["Yes", "No"])
    recycle = tab3.selectbox('Did you put all your used paper in a recycling bin, this week?', ["Yes", "No"])
    avoid_plastic = tab3.selectbox('Did you avoid taking carry bags from a store, this week?', ["Yes", "No"])

    lights = tab4.selectbox('Did you turn off the lights in your room before leaving your home, this week?', ["Yes", "No"])
    power = tab4.selectbox('Did you reduce your air conditioner use by 2 hours, this week?', ["Yes", "No"])
    charger = tab4.selectbox('Did you unplug your charger once your device was done charging instead of leaving it all night, this week? ', ["Yes", "No"])


    buy_eco = tab5.selectbox('Did you refuse to indulge in fast fashion this week?', ["Yes", "No"])

    # match model column names with the variables
    data = {        
            "Did you carpool?": carpool,
            "Reusable Water Bottle": water_bottle,
            "Lights Off": lights,
            "Recycled Paper": recycle,
            "Short Shower": shower,
            "No Plastic Bags": avoid_plastic,
            "Meatless Day": eat_meat,
            "Brushing Off": brush_teeth,
            "Leftovers":leftovers,
            "Fan Instead of AC": power,
            "Eco Friendly Brands": buy_eco,
            "Charger Unplugged":charger
            }

    return pd.DataFrame(data, index=[0])

df = component()
data = input_preprocessing(df)

# sample_df = pd.DataFrame(data=sample,index=[0])
# sample_df[sample_df.columns] = 0
# # sample_df[data.columns] = data

# ss = pickle.load(open("./models/scale.sav","rb"))
# model = pickle.load(open("./models/carbonemission_model.sav","rb"))
model=joblib.load('carbonemission_model.sav')
# prediction = round(np.exp(model.predict(ss.transform(sample_df))[0]))
prediction = model.predict(data)
class_name_dict = {
    1: 'Movie Night with Kung Fu Panda 4 or a Walk on Marine Drive!', 2: 'Baking Chocolate Chip Cookies or a Game of Monodeal!', 3: 'Thrift Shopping at Thrift Flip or a Dinner at Americano!', 4:'Dynamic Duos Party Night or a Drive to Magnolia!'}
prediction = class_name_dict[prediction[0]]
features_dict = {

    'Movie Night with Kung Fu Panda 4 or a Walk on Marine Drive!': ['For next week, you should try:' , 'Using the AC Less', 'Eating Less Meat', 'Recycling Paper'],
     'Baking Chocolate Chip Cookies or a Game of Monodeal!': ['For next week, you should try:' ,'Eating Less Meat', 'Using The AC Less', 'Finishing All Your Food'],
     'Thrift Shopping at Thrift Flip or a Dinner at Americano!':['For next week, you should try:' ,'Carpooling More','Using A Reusable Water Bottle','Unplugging Your Charger'] ,
     'Dynamic Duos Party Night or a Drive to Magnolia!':['Congratulations, keep at this!']
}
column1,column2 = tab1.columns(2)
_,resultbutton,_ = tab5.columns([1,1,1])
if resultbutton.button(" ", type = "secondary"):
    # tab_result.image(chart(model, sample_df,prediction), use_column_width="auto")
    tab_result.markdown(f"""Your reward for the week is: \n <b>{prediction}</b>! """,  unsafe_allow_html=True)
    suggestion_lst = features_dict[prediction]
    for suggestion in suggestion_lst:
        tab_result.markdown(f"""{suggestion}""",unsafe_allow_html=True)
    click_element('tab-2')

# pop_button = """<button id = "button-17" class="button-17" role="button"> ❔ Did You Know</button>"""
_,home,_ = comps.columns([1,2,1])
_,col2,_ = comps.columns([1,10,1])
# col2.markdown(pop_button, unsafe_allow_html=True)
# pop = """
# <div id="popup" class="DidYouKnow_root">
# <p class="DidYouKnow_title TextNew" style="font-size: 20px;"> ❔ Did you know</p>
#     <p id="popupText" class="DidYouKnow_content TextNew"><span>
#     Each year, human activities release over 40 billion metric tons of carbon dioxide into the atmosphere, contributing to climate change.
#     </span></p>
# </div>
# """
# col2.markdown(pop, unsafe_allow_html=True)

if home.button("🏡"):
    click_element('tab-0')
_,resultmid,_ = result.columns([1,2,1])

tree_count = prediction
#tab_result.markdown(f"""You owe nature <b>{tree_count}</b> tree{'s' if tree_count > 1 else ''} monthly. <br> {f"<a href='https://www.tema.org.tr/en/homepage' id = 'button-17' class='button-17' role='button'> 🌳 Proceed to offset 🌳</a>" if tree_count > 0 else ""}""",  unsafe_allow_html=True)

if resultmid.button("  ", type="secondary"):
    click_element('tab-1')

with open("./style/footer.html", "r", encoding="utf-8") as footer:
    footer_html = f"""{footer.read()}"""
    st.markdown(footer_html, unsafe_allow_html=True)

script()
