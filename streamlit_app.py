import streamlit as st
import plotly.express as px
from files.data_proc import data_read, make_data_yearly, make_sal_price_graph, make_revenue_data, make_price_fold_graph, make_borough_data
from files.data_proc import make_borough_sal_data, make_price_borough_graph, make_price_sal_fold_borough_data, make_data_for_map, make_map, make_data_sal_in_fold


data_path = ["data/ukhpi-buyer-status-london-from-1980-01-01-to-2023-01-01.csv",
             "data/ukhpi-property-status-london-from-1980-01-01-to-2023-01-01.csv",
             "data/ukhpi-property-type-london-from-1980-01-01-to-2023-01-01.csv",
             "data/ukhpi-england-from-1996-01-01-to-2023-01-01.csv"
             ]
data_buyer, data_prop, data_prop_type, data_eng = data_read(data_path)

# Data maker ---------------------------------------------------------------------------------
data_prop_yearly = make_data_yearly(data_prop)
data_buyer_yearly = make_data_yearly(data_buyer)
data_prop_type_yearly = make_data_yearly(data_prop_type)
total_weekly = make_revenue_data("London")
data_prop_type_yearly_trim = data_prop_type_yearly[data_prop_type_yearly["Period"] >= 2002].reset_index()
borough_data = make_borough_data()
data_eng = make_data_yearly(data_eng)
data_eng_trim = data_eng[data_eng["Period"] >= 2002].reset_index()

data_prop_type_yearly_trim = make_data_sal_in_fold(data_prop_type_yearly_trim, total_weekly)
data_eng_trim = make_data_sal_in_fold(data_eng_trim, make_revenue_data("England and Wales"))

# Fig maker------------------------------------------------------------------------------------
prop_type_list = ["Average price All property types","Average price Detached houses","Average price Semi-detached houses","Average price Terraced houses","Average price Flats and maisonettes"]


fig_new_vs_exist = px.line(data_prop_yearly, x="Period", y=["Average price New build",
                        "Average price Existing properties"], title="Average price in London of properties per year (£)",
                          labels={"value": "average price (£)", "Period": "Year", "variable": "Legend"}, width=800)
fig_new_vs_exist_rate = px.bar(data_prop_yearly, x="Period", y=["Percentage change (yearly) New build",
                        "Percentage change (yearly) Existing properties"], title="Average Property price change (%)",
                          labels={"value": "Average Property price change (%)", "Period": "Year", "variable": "Legend"}, width=800)

fig_first_vs_former = px.line(data_buyer_yearly, x="Period", y=["Average price First-time buyers",
                        "Average price Former owner-occupiers"], title="Average price in London of properties per year (£)",
                          labels={"value": "average price (£)", "Period": "Year", "variable": "Legend"}, width=800)

fig_first_vs_former_rate = px.bar(data_buyer_yearly, x="Period", y=["Percentage change (yearly) First-time buyers",
                        "Percentage change (yearly) Former owner-occupiers"], title="Average Property price change (%)",
                          labels={"value": "Average Property price change (%)", "Period": "Year", "variable": "Legend"}, width=800)

fig_prop_type = px.line(data_prop_type_yearly, x="Period", y=prop_type_list, title="Average price in London of properties per year (£)",
                          labels={"value": "average price (£)", "Period": "Year", "variable": "Legend"}, width=800)

fig_prop_type_eng = px.line(data_eng, x="Period", y=prop_type_list, title="Average price in England and Wales of properties per year (£)",
                          labels={"value": "average price (£)", "Period": "Year", "variable": "Legend"}, width=800)

fig_trend_prop_price = px.scatter(data_prop_type_yearly, x="Period", y=prop_type_list ,trendline="ols",
                title=" Trends for average price per property types",
                labels={"value": "average price (£)", "Period": "Year", "variable": "Legend"},
                width=800)

fig_sales_volume = px.line(data_prop_type_yearly, x="Period", y="Sales volume", title="Number of sales of all property in London per year",
                           labels={"value": "average price (£)", "Period": "Year", "variable": "Legend"},height=400, width=600)

fig_sales_volume_eng = px.line(data_eng, x="Period", y="Sales volume", title="Number of sales of all property in England and Wales per year",
                           labels={"value": "average price (£)", "Period": "Year", "variable": "Legend"},height=400, width=600)

fig_sal_london = px.line(total_weekly, x="year", y=total_weekly["salary"]*52, title = "Average Yearly salary in London", height=400, width=600)
fig_sal_london.update_yaxes(title_text = "Average salary (£)")

fig_sal_eng = px.line(make_revenue_data("England and Wales"), x="year", y=make_revenue_data("England and Wales")["salary"]*52, title = "Average Yearly salary in England and Wales", height=400, width=600)
fig_sal_eng.update_yaxes(title_text = "Average salary (£)")

# Session state --------------------------------------------------------------------------------------------

if "but_state" not in st.session_state:
    st.session_state["but_state"] = False
    st.session_state["but_label"] = "Switch to Borough"

if "but_bo_state" not in st.session_state:
    st.session_state["but_bo_state"] = False
    st.session_state["but_bo_label"] = "View all Boroughs"


def click():
    if st.session_state["but_state"] == False:
       st.session_state["but_state"] = True
       st.session_state["but_label"] = "Switch to London"

    else:
        st.session_state["but_state"] = False
        st.session_state["but_label"] = "Switch to Borough"

def click_2():
    if st.session_state["but_bo_state"] == False:
       st.session_state["but_bo_state"] = True
       st.session_state["but_bo_label"] = "View specific Borough"

    else:
        st.session_state["but_bo_state"] =False
        st.session_state["but_bo_label"] = "View all Boroughs"

# App layout ----------------------------------------------------------------------------------------------

#st.set_page_config(layout="wide", initial_sidebar_state="expanded")

st.header("London housing prices visualisation")
colh, colb = st.columns([0.7, 0.3])

colb.button(st.session_state["but_label"], key="button1", on_click=click)

st.markdown("""The aim of this dashboard is to visualise the evolution of housing prices in London (and its borough) and compare them to revenue data of its inhabitant.
            Also I want to compare that data to the whole of the UK in order to see how inflated are house prices in London.
            Data for the housing prices have been sourced from the Land Registry: UK house Price Index. https://landregistry.data.gov.uk/app/ukhpi/browse
            Data for the revenue have been sourced from the Organisation of National Statistics.""")

#England and Wales Data ----------------------------------------------------------------------------

if st.session_state["but_state"] == False:

    st.markdown("### For reference, let's look at the England and Wales data.")

    #col_e1, col_e2 = st.columns(2)

    st.plotly_chart(fig_prop_type_eng)
    st.plotly_chart(fig_sal_eng)

    st.markdown("""The graphs below are comparing the house prices with the average yearly salary.
                Top, the housing prices are expressed in fold of average price (How much of the yearly salary a house cost).
                Below, the increase of prices and salary expressed in fold of their first value taken in 2002. It is meant to show if the salary increase are keeping up with house prices.""")

    #col_e3, col_e4 = st.columns(2)

    st.plotly_chart(make_price_fold_graph(data_eng_trim, 400, 800))
    st.plotly_chart(make_sal_price_graph(data_eng_trim, make_revenue_data("England and Wales"), 400, 800))

    st.markdown("""My original thought was that an expensive house was calculated to be more than 5 to 7 times the average yearly salary. And this was the case in 2002 where average price of all properties in England and Wales were at 6.5 times average yearly salaries.
                But this hasn't been the case in the last 2 decades where it has been hovering between 8 to 10 times the average yearly salary.
                The graphs also show that the house prices has been climbing much faster than salaries, now being 2 to 3 times more than in 2002, compare to only 54% increase for salaries.""")

    # London Data -------------------------------------------------------------------------------

    #New Build VS Existing Build ------------------------------------------------------------

    st.markdown("### Let's compare new build and existing build prices")

    #col1, col2 = st.columns(2)

    st.plotly_chart(fig_new_vs_exist)
    #st.plotly_chart(fig_new_vs_exist_rate)

    st.markdown("""As we can see on the graph above, new builds in London are not cheaper that existing build. They can even been seen to be slightly more expensive recently.
                So the only way new build can help with the rise of prices is to use them to increase the supply of available housing.""")

    #First time buyer vs Exisiting buyer ---------------------------------------------------------

    st.markdown("### Let's compare first time buyer and former-owner buyer budgets")

    #col3, col4 = st.columns(2)

    st.plotly_chart(fig_first_vs_former)
    #st.plotly_chart(fig_first_vs_former_rate)

    st.markdown("""As expected, first time buyer have a lower budget than former owners and consisitantly buy cheaper housing.
                It is worth noting that first time buyer are paying more than £400000 in average since 2016 on their first home which is a substantial amount of money to find without having a property to sell.""")

    #Property type prices

    st.markdown("### Let's look at property prices according to their types")

    #col5, col6 = st.columns(2)

    st.plotly_chart(fig_prop_type)
    st.plotly_chart(fig_trend_prop_price)
    st.markdown("For reference")
    st.plotly_chart(fig_sales_volume)
    st.plotly_chart(fig_sal_london)

    st.markdown("""While it was visible on the other graphs, we can see the influence the 2008 fincial crash had on the market: the number of houses buying sold halfed in 2009 and nerver went back to its pre crash peak.
                With the exception of 2009, the housing prices kept increasing despite the crash.
                While the prices for all type of properties increases, the more private is the property, the more valuable it is.
                So we can see that since 1996, the pirces of Terraced houses increased by nearly £33000 per years compare to flats where their prices increased £15000 per year.""")

    st.markdown("### Let's compare with London's salaries")
    st.markdown("Text about that before 2000 in the rest of country a normal house cost around 4 to 5 time yearly salaries (according to the Bank Of england data).")

    st.markdown("The following graph shows the increase of prices and salaries in comparisation of their first value. So for example, in 2015, the price of Terraced House were 2.41 times more expensive than in 2002 (reference).")

    st.plotly_chart(make_sal_price_graph(data_prop_type_yearly_trim, total_weekly, 400, 800))
    st.markdown("""We can see on this graph that housing prices are increasing much faster than income in London.
                Since 2002, salaries icreased by around 46% in 2021. While property prices increase by 150% to 200% since 2002.
                We can also note that the prices of flats in London didn't follow the same trend of prices than the other during the COVID 19 pandemic.""")

    st.plotly_chart(make_price_fold_graph(data_prop_type_yearly_trim, 400, 800))
    st.markdown("""We can see that houses price in London are much greater than the rest of country which is around 5 to 7 times average yearly salary.
                Here even flats are around 13 times the average salary in 2022 while the price of Terraced houses are a stagering 31 time the average salary.""")

# Borough Data ----------------------------------------------------------------------------------

if st.session_state["but_state"] == True:
    st.markdown("### Let's visualise the data on a borough level!")
    st.markdown("You can see below data per sepcific boroughs or switch to a map view of all boroughs.")
    col_dr, col_bb = st.columns([0.8,0.2])
    col_bb.button(st.session_state["but_bo_label"], key="Button_borough", on_click=click_2)

    if st.session_state["but_bo_state"] == False:
        borough = col_dr.selectbox("Borough",borough_data.keys() ,key="dropdown_1")

        borough_sal = make_borough_sal_data(borough)
        #col_b1, col_b2 = st.columns(2)
        st.plotly_chart(make_price_borough_graph(borough_data,borough))

        data_spec_bo = make_price_sal_fold_borough_data(borough_data, borough_sal, borough)
        if data_spec_bo != "Data unavailable":
            st.plotly_chart(data_spec_bo)
        else: st.markdown("Salary data unavailable")

    else:
        value_list = prop_type_list
        value_list.append("Price compare to yearly salary in fold")
        col_bv, col_by = st.columns(2)
        value_to_see = col_bv.selectbox("Value to display on the map",value_list ,key="dropdown_2")

        if value_to_see != "Price compare to yearly salary in fold":
            year_list = list(range(1996,2023))
        else: year_list = list(range(2002,2022))
        year_see = col_by.selectbox("Year",year_list ,key="dropdown_3")

        data_map = make_data_for_map(borough_data, value_to_see)

        st.plotly_chart(make_map(data_map,year_see))
