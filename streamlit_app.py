import streamlit as st
import plotly.express as px
from files.data_proc import data_read, make_data_yearly, make_sal_price_graph, make_revenue_data, make_price_fold_graph, make_borough_data
from files.data_proc import make_borough_sal_data, make_price_borough_graph, make_price_sal_fold_borough_data, make_data_for_map, make_map


data_path = ["data/ukhpi-buyer-status-london-from-1980-01-01-to-2023-01-01.csv",
             "data/ukhpi-property-status-london-from-1980-01-01-to-2023-01-01.csv",
             "data/ukhpi-property-type-london-from-1980-01-01-to-2023-01-01.csv"
             ]

data_buyer, data_prop, data_prop_type = data_read(data_path)

# Data maker ---------------------------------------------------------------------------------
data_prop_yearly = make_data_yearly(data_prop)
data_buyer_yearly = make_data_yearly(data_buyer)
data_prop_type_yearly = make_data_yearly(data_prop_type)
total_weekly = make_revenue_data()
data_prop_type_yearly_trim = data_prop_type_yearly[data_prop_type_yearly["Period"] >= 2002].reset_index()
borough_data = make_borough_data()

data_prop_type_yearly_trim["Average price All property types in salary fold"] = data_prop_type_yearly_trim["Average price All property types"] / (total_weekly["salary"] *52)
data_prop_type_yearly_trim["Average price Detached houses in salary fold"] = data_prop_type_yearly_trim["Average price Detached houses"] / (total_weekly["salary"] *52)
data_prop_type_yearly_trim["Average price Semi-detached houses in salary fold"] = data_prop_type_yearly_trim["Average price Semi-detached houses"]/ (total_weekly["salary"] *52)
data_prop_type_yearly_trim["Average price Terraced houses in salary fold"] = data_prop_type_yearly_trim["Average price Terraced houses"] / (total_weekly["salary"] *52)
data_prop_type_yearly_trim["Average price Flats and maisonettes in salary fold"] = data_prop_type_yearly_trim["Average price Flats and maisonettes"] / (total_weekly["salary"] *52)



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

fig_trend_prop_price = px.scatter(data_prop_type_yearly, x="Period", y=prop_type_list ,trendline="ols",
                title="Average price per property types trends",
                labels={"value": "average price (£)", "Period": "Year", "variable": "Legend"},
                width=800)

fig_sales_volume = px.line(data_prop_type_yearly, x="Period", y="Sales volume", title="Number of sales of all property in London per year",
                           labels={"value": "average price (£)", "Period": "Year", "variable": "Legend"},height=400, width=600)

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

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

colh, colb = st.columns([0.8, 0.2])

colh.header("London housing prices visualisation")
colb.button(st.session_state["but_label"], key="button1", on_click=click)

st.markdown("Text here explaining where data come from and aim")

# London Data -------------------------------------------------------------------------------

if st.session_state["but_state"] == False:
    #New Build VS Existing Build ------------------------------------------------------------

    st.markdown("### Let's compare new build and existing build prices")

    col1, col2 = st.columns(2)

    col1.plotly_chart(fig_new_vs_exist)
    col2.plotly_chart(fig_new_vs_exist_rate)

    st.markdown("Text here explaining that new build are not cheaper")

    #First time buyer vs Exisiting buyer ---------------------------------------------------------

    st.markdown("### Let's compare first time buyer and former-owner buyer budgets")

    col3, col4 = st.columns(2)

    col3.plotly_chart(fig_first_vs_former)
    col4.plotly_chart(fig_first_vs_former_rate)

    st.markdown("Text here explaining that first time buyer are poorer as expected")

    #Property type prices

    st.markdown("### Let's look at property prices according to their types")

    col5, col6 = st.columns(2)

    col5.plotly_chart(fig_prop_type)
    col5.plotly_chart(fig_sales_volume)
    col6.plotly_chart(fig_trend_prop_price)
    col6.markdown("Mortgage data here??")

    st.markdown("""Text here explaining that:
                - 2009 crash is visible
                - Price keep increasing despite teh crash
                - The more private the house, the more its price grew""")

    st.markdown("### Let's compare with London's salaries")
    st.markdown("Text about that before 2000 in the rest of country a normal house cost around 4 to 5 time yearly salaries (according to the Bank Of england data).")

    st.markdown("The following graph shows the increase of prices and salaries in comparisation of their first value. So for example, in 2015, the price of Terraced House were 2.41 times more expensive than in 2002 (reference).")

    st.plotly_chart(make_sal_price_graph(data_prop_type_yearly_trim, total_weekly))
    st.markdown("Text explaining that house prices are rising much faster than salaries")

    st.plotly_chart(make_price_fold_graph(data_prop_type_yearly_trim, total_weekly))
    st.markdown("Text showing that house price in London are far more than 5 to 7 times yearly salaries.")

# Borough Data ----------------------------------------------------------------------------------

if st.session_state["but_state"] == True:
    st.markdown("### Let's visualise the data on a borough level!")
    st.markdown("You can see below data per sepcific boroughs or switch to a map view of all boroughs.")
    col_dr, col_bb = st.columns([0.8,0.2])
    col_bb.button(st.session_state["but_bo_label"], key="Button_borough", on_click=click_2)

    if st.session_state["but_bo_state"] == False:
        borough = col_dr.selectbox("Borough",borough_data.keys() ,key="dropdown_1")


        borough_sal = make_borough_sal_data(borough)
        col_b1, col_b2 = st.columns(2)
        col_b1.plotly_chart(make_price_borough_graph(borough_data,borough))
        col_b2.plotly_chart(make_price_sal_fold_borough_data(borough_data, borough_sal, borough))

    else:
        value_list = prop_type_list
        value_list.append("Price compare to yearly salary in fold")
        col_bv, col_by = st.columns(2)
        value_to_see = col_bv.selectbox("Value to display on the map",value_list ,key="dropdown_2")

        if value_to_see != "Price compare to yearly salary in fold":
            year_list = list(range(1996,2023))
        else: year_list = list(range(2002,2022))
        year_see = col_by.selectbox("Value to display on the map",year_list ,key="dropdown_3")

        data_map = make_data_for_map(borough_data, value_to_see)

        st.plotly_chart(make_map(data_map,year_see))
