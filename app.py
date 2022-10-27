import streamlit as st
import pandas as pd
import plotly.express as px 
import numpy as np
import statsmodels
import openpyxl
import defusedxml

### Config
st.set_page_config(
    page_title="Getaround analysis",
    page_icon="🚗 ",
    layout="wide"
)

### App

st.title("Analysis Getaround")

@st.cache
def load_data():
    df_delay = pd.read_excel('https://github.com/Fanny-Mlmrtl/Bloc_5/blob/main/get_around_delay_analysis.xlsx', engine=openpyxl)
    return df_delay

st.write("To display data, click on the checkbox")
df_delay = load_data()

if st.checkbox('Show raw data'):
    st.write(df_delay)

st.markdown('#')


st.subheader("Consequences of delay on the next driver")
st.write('(analysis made with only few observations because of important missing values)')

df_time_delta_with_previous_rental_in_minutes = df_delay.dropna(axis=0, subset=['time_delta_with_previous_rental_in_minutes']).reset_index(drop=True)
delay_at_co= df_time_delta_with_previous_rental_in_minutes[['previous_ended_rental_id']][df_time_delta_with_previous_rental_in_minutes['state'] == 'canceled'].merge(df_delay[['rental_id', 'car_id','checkin_type','state','delay_at_checkout_in_minutes','time_delta_with_previous_rental_in_minutes']],how='left',left_on='previous_ended_rental_id', right_on='rental_id')
print(delay_at_co)


col1, col2 = st.columns(2)

with col1:
    fig = px.histogram(x=df_time_delta_with_previous_rental_in_minutes['state'], histnorm='percent', title='Status of rental', labels={'x':'Status of rental'})
    fig.update_traces(marker_color='cornflowerblue')
    st.plotly_chart(fig, use_container_width=True)
    st.write('12.5% of people canceled their reservation, is it because of check-out delay from previous rental?')
with col2:
    fig = px.box(x=delay_at_co["delay_at_checkout_in_minutes"],title = 'Delay in minutes when checking out', labels={'x':'Delay in minutes when checking out'})
    fig.update_traces(marker_color='cornflowerblue')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
        On the 12.5% of people who had canceled their reservation, only half had a late check out from previous driver:
        * median time at check out is 2.5 min
        * 50% of delay are between - 300 min (5 hours) and +2.5 min (drivers on time)
        * 50% of early check out are between +2.5 min and + 252 min (4h20)
        In conclusion: late check out accounts for only half of the cancellations.       
        """)

upper_limit = df_time_delta_with_previous_rental_in_minutes['delay_at_checkout_in_minutes'].mean() + 2*df_time_delta_with_previous_rental_in_minutes['delay_at_checkout_in_minutes'].std()
lower_limit = df_time_delta_with_previous_rental_in_minutes['delay_at_checkout_in_minutes'].mean() - 2*df_time_delta_with_previous_rental_in_minutes['delay_at_checkout_in_minutes'].std()
df_time_delta_with_previous_rental_in_minutes_clean = df_time_delta_with_previous_rental_in_minutes[(df_time_delta_with_previous_rental_in_minutes['delay_at_checkout_in_minutes']<upper_limit) & (df_time_delta_with_previous_rental_in_minutes['delay_at_checkout_in_minutes']>lower_limit)]

result = []
for i in df_time_delta_with_previous_rental_in_minutes_clean['delay_at_checkout_in_minutes']:
    if i < 0:
        result.append('driver late')
    elif i == 0:
        result.append('driver on time')
    else:
        result.append('driver in advance')
df_time_delta_with_previous_rental_in_minutes_clean['type_driver'] = result

df_time_delta_with_previous_rental_in_minutes_clean = df_time_delta_with_previous_rental_in_minutes_clean[df_time_delta_with_previous_rental_in_minutes_clean['type_driver'] != 'driver on time']
time_at_check_out = st.selectbox("Relation between time delta previous rental and delay at checkout: select a type of driver 👇", df_time_delta_with_previous_rental_in_minutes_clean['type_driver'].sort_values().unique())
if 'driver late' in time_at_check_out:
    delay = df_time_delta_with_previous_rental_in_minutes_clean[df_time_delta_with_previous_rental_in_minutes_clean['delay_at_checkout_in_minutes'] <0]
    fig = px.scatter(delay, x="delay_at_checkout_in_minutes", y="time_delta_with_previous_rental_in_minutes", labels={'delay_at_checkout_in_minutes':'Delay in minutes when checking out', 'time_delta_with_previous_rental_in_minutes':'Time delta with previous rental'}, trendline="ols")
    fig.update_traces(marker_color='crimson')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    Not surprising, we can see that as the time delta with previous rental increases, the delay at checkout decreases.      
    """)
else: 
    advance = df_time_delta_with_previous_rental_in_minutes_clean[df_time_delta_with_previous_rental_in_minutes_clean['delay_at_checkout_in_minutes'] >0]
    fig = px.scatter(advance, x="delay_at_checkout_in_minutes", y="time_delta_with_previous_rental_in_minutes", labels={'delay_at_checkout_in_minutes':'Delay in minutes when checking out', 'time_delta_with_previous_rental_in_minutes':'Time delta with previous rental'}, trendline="ols")
    fig.update_traces(marker_color='chartreuse')
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
    We can note the negative relation between time delta with previous rental & advance on time at checkout.
    As the time delta with previous rental  increases, the advance on time at checkout decreases.
    """)
st.markdown('###')


df_delay = df_delay.drop(columns=['previous_ended_rental_id','time_delta_with_previous_rental_in_minutes'])
df_delay = df_delay.dropna(axis=0, subset='delay_at_checkout_in_minutes')
# Remove outliers
upper_limit = df_delay['delay_at_checkout_in_minutes'].mean() + 2*df_delay['delay_at_checkout_in_minutes'].std()
lower_limit = df_delay['delay_at_checkout_in_minutes'].mean() - 2*df_delay['delay_at_checkout_in_minutes'].std()
df_delay_clean = df_delay[(df_delay['delay_at_checkout_in_minutes']<upper_limit) & (df_delay['delay_at_checkout_in_minutes']>lower_limit)]
result = []
for i in df_delay_clean['delay_at_checkout_in_minutes']:
    if i < 0:
        result.append('driver late')
    elif i == 0:
        result.append('driver on time')
    else:
        result.append('driver in advance')
df_delay_clean['type_driver'] = result

st.subheader("How often drivers are late?")
st.write('(analysis made with the other part of the dataset)')

col1, col2 = st.columns(2)

with col1:
    fig = px.pie(
    values= df_delay_clean.groupby('type_driver').count()['checkin_type'], 
    names=['driver in advance','driver late','driver on time'], 
    color=['driver in advance','driver late','driver on time'],
    color_discrete_map={'driver in advance':'chartreuse','driver late':'crimson','driver on time':'cyan'}, 
    title='Driver type'
    )
    st.plotly_chart(fig, use_container_width=True)


with col2:
    df_delay_clean_bis = df_delay_clean[df_delay_clean['type_driver'] != 'driver on time']
    time_at_check_out = st.selectbox("Early and late checkout distribution: select a type of driver 😇", df_delay_clean_bis['type_driver'].sort_values().unique())
    if 'driver late' in time_at_check_out:
        delay = df_delay_clean_bis[df_delay_clean_bis['delay_at_checkout_in_minutes'] <0]
        fig = px.box(
        x=delay['delay_at_checkout_in_minutes'], 
        title='Delay when checking out', 
        labels={"x": "delay in minutes"}
        )
        fig.update_traces(marker_color='crimson')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        We can consider that 100% of the delays are between -270 min (4h30) and 0 min:
        * the median is at 51 min
        * 75% of the delays are between -119 min (2h) and 0 min        
        """)
    else: 
        advance = df_delay_clean_bis[df_delay_clean_bis['delay_at_checkout_in_minutes'] >0]
        fig = px.box(
        x=advance['delay_at_checkout_in_minutes'], 
        title='Advance when checking out', 
        labels={"x": "advance in minutes"}
        )
        fig.update_traces(marker_color='chartreuse')
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        We can consider that 100% of the early checkout are between 0 min and 296 min (5h):
        * the median is at 52 min
        * 75% of the delays are between 0 min and 126 min (2h)     
        """)
st.markdown('###')


st.subheader('Checkin type & drivers')

col1, col2 = st.columns(2)

with col1:
    fig = px.pie(
    values=df_delay_clean.groupby('checkin_type').count()['type_driver'], 
    names=['connect','mobile'], 
    color=['mobile','connect'],
    color_discrete_map={'mobile':'cyan','connect':'cornflowerblue'}, 
    title='Checkin type'
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.histogram(
    x=df_delay_clean['type_driver'], 
    color=df_delay_clean['checkin_type'], 
    barnorm='percent', labels={"x": "driver type"}, 
    color_discrete_map={'mobile':'cornflowerblue','connect':'cyan'}, 
    title='Checkin type by type of drivers'
    )
    st.markdown("""
    Among drivers late, almost 30% used the connect checkin type
    """)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("""
In conclusion:
      * threshold: the minimum delay between two rentals should be 2 hours, to avoid 75% of delays.
      * scope: the feature should be enabled for all checkin type: mobile & connect. 
""")


