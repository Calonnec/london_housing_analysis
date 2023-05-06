import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

prop_type_list = ["Average price All property types","Average price Detached houses","Average price Semi-detached houses","Average price Terraced houses","Average price Flats and maisonettes"]

def new_vs_existing_build(data, h=400, w=1500):
    fig = make_subplots(rows=1, cols=2, subplot_titles=('Average price in London of properties per year (£)',
                                                    'Average price changes in London of properties compare to previous year (%)'))

    fig.add_trace(go.Scatter(name='Price New Build', x=data["Period"], y=data["Average price New build"], legendgroup="1"),row=1, col=1)
    fig.add_trace(go.Scatter(name='Price Existing Build', x=data["Period"], y=data["Average price Existing properties"], legendgroup="1"),row=1, col=1)
    fig.add_trace(go.Bar(name='Price New Build', x=data["Period"], y=data["Percentage change (yearly) New build"], legendgroup="2"),row=1, col=2)
    fig.add_trace(go.Bar(name='Price Existing Build', x=data["Period"], y=data["Percentage change (yearly) Existing properties"], legendgroup="2"),row=1, col=2)

    fig.update_yaxes(title_text="Avergae Property price (£)", row=1, col=1)
    fig.update_yaxes(title_text="Average Property price change (%)", row=1, col=2)

    fig.update_xaxes(title_text="Year", row=1, col=1)
    fig.update_xaxes(title_text="Year", row=1, col=2)

    fig.update_layout(height=h, width=w,legend_tracegroupgap = (h/2)-40)
    return fig

def new_vs_former_owner(data, h=400, w=1500):

    fig = make_subplots(rows=1, cols=2, subplot_titles=('Average price in London of properties per year (£)',
                                                   'Average price changes in London of properties compare to previous year (%)'))

    fig.add_trace(go.Scatter(name='Price First-time buyers', x=data["Period"], y=data["Average price First-time buyers"], mode="lines", legendgroup="1"),row=1, col=1)
    fig.add_trace(go.Scatter(name='Price Former owner', x=data["Period"], y=data["Average price Former owner-occupiers"], mode="lines", legendgroup="1"),row=1, col=1)
    fig.add_trace(go.Bar(name='Price First-time buyers', x=data["Period"], y=data["Percentage change (yearly) First-time buyers"], legendgroup="2"),row=1, col=2)
    fig.add_trace(go.Bar(name='Price Former owner', x=data["Period"], y=data["Percentage change (yearly) Former owner-occupiers"], legendgroup="2"),row=1, col=2)

    fig.update_yaxes(title_text="Avergae Property price (£)", row=1, col=1)
    fig.update_yaxes(title_text="Average Property price change (%)", row=1, col=2)

    fig.update_xaxes(title_text="Year", row=1, col=1)
    fig.update_xaxes(title_text="Year", row=1, col=2)

    fig.update_layout(height=h, width=w,legend_tracegroupgap = (h/2)-40)
    return fig

def property_type_graph(data, h=800, w=1000):
    fig = make_subplots(rows=2, cols=1, subplot_titles=('Average price in London of properties per year (£)',
                                                    'Number of sales of all property in London per year'))

    fig.add_trace(go.Scatter(name='Price All Properties', x=data["Period"], y=data["Average price All property types"], legendgroup="1"),row=1, col=1)
    fig.add_trace(go.Scatter(name='Price Detached Houses', x=data["Period"], y=data["Average price Detached houses"], legendgroup="1"),row=1, col=1)
    fig.add_trace(go.Scatter(name='Price Semi Detached Houses', x=data["Period"], y=data["Average price Semi-detached houses"], legendgroup="1"),row=1, col=1)
    fig.add_trace(go.Scatter(name='Price Terraced Houses', x=data["Period"], y=data["Average price Terraced houses"], legendgroup="1"),row=1, col=1)
    fig.add_trace(go.Scatter(name='Price Flat and Maisonette', x=data["Period"], y=data["Average price Flats and maisonettes"], legendgroup="1"),row=1, col=1)
    fig.add_trace(go.Scatter(name='Sales Volume', x=data["Period"], y=data["Sales volume"], mode="lines", legendgroup="2"),row=2, col=1)

    fig.update_yaxes(title_text="Avergae Property price (£)", row=1, col=1)
    fig.update_yaxes(title_text="Number of sales", row=2, col=1)

    fig.update_xaxes(title_text="Year", row=1, col=1)
    fig.update_xaxes(title_text="Year", row=2, col=1)

    fig.update_layout(height=h, width=w,legend_tracegroupgap = (h/3)+25)
    return fig

def data_trendlines(data):
    fig = px.scatter(data,
                x="Period", y=prop_type_list,
                trendline="ols",
                title="Average price per property types trends",
                labels={"value": "average price (£)", "Period": "Year", "variable": "Legend"})
    fig.update_layout(height=600, width=1000)
    return fig
