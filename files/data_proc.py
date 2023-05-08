import pandas as pd
import os
import glob
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import geopandas as gpd
import plotly.express as px

def data_read(path):
    data_buyer_raw = pd.read_csv(path[0]).dropna()
    data_prop = pd.read_csv(path[1]).dropna()
    data_prop_type = pd.read_csv(path[2]).dropna()
    data_eng = pd.read_csv(path[3])

    data_buyer_raw["Period"] = pd.to_datetime(data_buyer_raw["Period"], yearfirst=True)
    data_prop["Period"] = pd.to_datetime(data_prop["Period"], yearfirst=True)
    data_prop_type["Period"] = pd.to_datetime(data_prop_type["Period"], yearfirst=True)
    data_eng["Period"] = pd.to_datetime(data_eng["Period"], yearfirst=True)

    return data_buyer_raw, data_prop, data_prop_type, data_eng

def make_data_yearly(data):
    data_yearly = data.groupby(by=pd.Grouper(key="Period", freq='Y')).mean().reset_index()
    data_yearly["Period"] = data_yearly["Period"].apply(lambda x: x.year)
    return data_yearly

def make_revenue_data(area):
    path = "data/Revenue/"
    csv_file = glob.glob(os.path.join(path, "*Total, weekly.csv"))
    data_test = pd.read_csv(csv_file[0])
    data = data_test[data_test["Area"] == area].drop(["Code", "Area"], axis=1).T[::2].reset_index()
    data = data.rename(columns={data.columns[-1]:"salary","index":"year"})
    data = data.apply(lambda col:pd.to_numeric(col, errors='coerce'))
    return data

def make_data_sal_in_fold(data, data_sal):
    data["Average price All property types in salary fold"] = data["Average price All property types"] / (data_sal["salary"] *52)
    data["Average price Detached houses in salary fold"] = data["Average price Detached houses"] / (data_sal["salary"] *52)
    data["Average price Semi-detached houses in salary fold"] = data["Average price Semi-detached houses"]/ (data_sal["salary"] *52)
    data["Average price Terraced houses in salary fold"] = data["Average price Terraced houses"] / (data_sal["salary"] *52)
    data["Average price Flats and maisonettes in salary fold"] = data["Average price Flats and maisonettes"] / (data_sal["salary"] *52)
    return data

def make_sal_price_graph(data_prop, data_sal, h=600, w=1000):
    y_all=data_prop["Average price All property types"]/data_prop["Average price All property types"][0]
    y_det=data_prop["Average price Detached houses"]/data_prop["Average price Detached houses"][0]
    y_semi=data_prop["Average price Semi-detached houses"]/data_prop["Average price Semi-detached houses"][0]
    y_ter=data_prop["Average price Terraced houses"]/data_prop["Average price Terraced houses"][0]
    y_flat=data_prop["Average price Flats and maisonettes"]/data_prop["Average price Flats and maisonettes"][0]
    y_salary = data_sal["salary"]/data_sal["salary"][0]

    fig = make_subplots()

    fig.add_trace(go.Scatter(name='Price All Properties', x=data_prop["Period"], y=y_all))
    fig.add_trace(go.Scatter(name='Price Detached Houses', x=data_prop["Period"], y=y_det))
    fig.add_trace(go.Scatter(name='Price Semi Detached Houses', x=data_prop["Period"], y=y_semi))
    fig.add_trace(go.Scatter(name='Price Terraced Houses', x=data_prop["Period"], y=y_ter))
    fig.add_trace(go.Scatter(name='Price Flat and Maisonette', x=data_prop["Period"], y=y_flat))
    fig.add_trace(go.Scatter(name="Average Weekly salary", x=data_sal["year"], y=y_salary))

    fig.update_layout(height=h, width=w, title="House and yearly salary increase in fold over the year")
    fig.update_xaxes(title_text="year")
    fig.update_yaxes(title_text="Average increase in fold")

    return fig

def make_price_fold_graph(data_prop, h=600, w=1000):

    fig = make_subplots()
    fig.add_trace(go.Scatter(name='All Properties', x=data_prop["Period"], y=data_prop["Average price All property types in salary fold"]))
    fig.add_trace(go.Scatter(name='Detached Houses', x=data_prop["Period"], y=data_prop["Average price Detached houses in salary fold"]))
    fig.add_trace(go.Scatter(name='Semi Detached Houses', x=data_prop["Period"], y=data_prop["Average price Semi-detached houses in salary fold"]))
    fig.add_trace(go.Scatter(name='Terraced Houses', x=data_prop["Period"], y=data_prop["Average price Terraced houses in salary fold"]))
    fig.add_trace(go.Scatter(name='Flat and Maisonette', x=data_prop["Period"], y=data_prop["Average price Flats and maisonettes in salary fold"]))

    fig.update_layout(height=h, width=w, title = "House prices per type expressed in fold of Yearly salary")
    fig.update_xaxes(title_text="year")
    fig.update_yaxes(title_text="Average increase in fold")

    return fig

def make_borough_data():

    path_b = "data/Boroughs/"
    csv_files_b = glob.glob(path_b + "*.csv")

    boroughs_data = {}
    for file in csv_files_b:
        up = file.find("from")
        down = file.find("pi")
        key = file[down + 3:up - 1].replace("-"," ").title()
        data = pd.read_csv(file)
        data["Period"] = pd.to_datetime(data["Period"], yearfirst=True)
        boroughs_data[key] = data

    return boroughs_data

def make_borough_sal_data(borough):
    path = "data/Revenue/"
    csv_file = glob.glob(os.path.join(path, "*Total, weekly.csv"))
    print(csv_file)

    data_test = pd.read_csv(csv_file[0])
    s_data_b = data_test[data_test["Area"] == borough].drop(["Code", "Area"], axis=1).T[::2].reset_index()
    s_data_b.rename(columns={s_data_b.columns[-1]:"salary","index":"year"}, inplace=True)
    s_data_b.index.name = borough
    s_data_b = s_data_b.apply(lambda col:pd.to_numeric(col, errors='coerce'))

    return s_data_b

def make_price_borough_graph(data_prop, borough):
    b_data_prop = data_prop[borough].groupby(by=pd.Grouper(key="Period", freq='Y')).mean().reset_index()
    b_data_prop["Period"] = b_data_prop["Period"].apply(lambda x: x.year)

    fig = make_subplots()

    fig.add_trace(go.Scatter(name='Average price All property types',x=b_data_prop["Period"] , y=b_data_prop["Average price All property types"]))
    fig.add_trace(go.Scatter(name='Average price Detached House',x=b_data_prop["Period"], y=b_data_prop["Average price Detached houses"]))
    fig.add_trace(go.Scatter(name='Average price Semi Detached House',x=b_data_prop["Period"], y=b_data_prop["Average price Semi-detached houses"]))
    fig.add_trace(go.Scatter(name='Average price Terraced House',x=b_data_prop["Period"], y=b_data_prop["Average price Terraced houses"]))
    fig.add_trace(go.Scatter(name='Average price Flat and Maisonette',x=b_data_prop["Period"], y=b_data_prop["Average price Flats and maisonettes"]))

    fig.update_xaxes(title_text="year")
    fig.update_yaxes(title_text="Average property prices")

    fig.update_layout(height=400, width=800, title=f'Property prices over the years in {borough}')

    return fig

def make_price_sal_fold_borough_data(data_prop, data_sal, borough):
    if data_sal.get("salary") is not None:
        b_data_prop = data_prop[borough].groupby(by=pd.Grouper(key="Period", freq='Y')).mean().reset_index()
        b_data_prop["Period"] = b_data_prop["Period"].apply(lambda x: x.year)
        b_data_prop_trim = b_data_prop[b_data_prop["Period"]>=2002].reset_index()

        y_prop=b_data_prop_trim["Average price All property types"]/b_data_prop_trim["Average price All property types"][0]
        y_det=b_data_prop_trim["Average price Detached houses"]/b_data_prop_trim["Average price Detached houses"][0]
        y_semi=b_data_prop_trim["Average price Semi-detached houses"]/b_data_prop_trim["Average price Semi-detached houses"][0]
        y_ter=b_data_prop_trim["Average price Terraced houses"]/b_data_prop_trim["Average price Terraced houses"][0]
        y_flat=b_data_prop_trim["Average price Flats and maisonettes"]/b_data_prop_trim["Average price Flats and maisonettes"][0]
        y_salary = data_sal["salary"]/data_sal["salary"][0]

        fig = make_subplots()

        fig.add_trace(go.Scatter(name='Average price All property types', x=b_data_prop_trim["Period"], y=y_prop))
        fig.add_trace(go.Scatter(name='Average price Detached House', x=b_data_prop_trim["Period"], y=y_det))
        fig.add_trace(go.Scatter(name='Average price Semi Detached House', x=b_data_prop_trim["Period"], y=y_semi))
        fig.add_trace(go.Scatter(name='Average price Terraced House', x=b_data_prop_trim["Period"], y=y_ter))
        fig.add_trace(go.Scatter(name='Average price Flat and Maisonette', x=b_data_prop_trim["Period"], y=y_flat))
        fig.add_trace(go.Scatter(name="Average Weekly salary", x=data_sal["year"], y=y_salary))

        fig.update_xaxes(title_text="year")
        fig.update_yaxes(title_text="Increase in fold")

        fig.update_layout(height=400, width=800, title=f'House and salary increase in fold over the year in {borough}')
        return fig
    else: return "Data unavailable"

def make_data_for_map(data_dict, value_to_see):
    res = pd.DataFrame()
    path = "data/Revenue/"
    csv_file = glob.glob(os.path.join(path, "*Total, weekly.csv"))
    data_sal = pd.read_csv(csv_file[0])
    for borough in data_dict.keys():
        if value_to_see == "Price compare to yearly salary in fold":
            b_data_prop = data_dict[borough].groupby(by=pd.Grouper(key="Period", freq='Y')).mean().iloc[6:].reset_index()
            b_data_prop["Period"] = b_data_prop["Period"].apply(lambda x: x.year)
            s_data_b = data_sal[data_sal["Area"] == borough].drop(["Code", "Area"], axis=1).T[::2].reset_index()
            s_data_b.rename(columns={s_data_b.columns[-1]:"salary","index":"year"}, inplace=True)
            s_data_b = s_data_b.apply(lambda col:pd.to_numeric(col, errors='coerce'))
            key = borough
            res["year"] = b_data_prop["Period"]
            if s_data_b.get("salary") is not None:
                res[key] = b_data_prop["Average price All property types"] / (s_data_b["salary"]*52)
            else: res[key] = np.NaN
        else:
            b_data_prop = data_dict[borough].groupby(by=pd.Grouper(key="Period", freq='Y')).mean().reset_index()
            b_data_prop["Period"] = b_data_prop["Period"].apply(lambda x: x.year)
            key = borough
            res["year"] = b_data_prop["Period"]
            res[key] = b_data_prop[value_to_see]
    return res

def make_map(raw_data, year):

    gdf = gpd.read_file("data/london_boroughs.json")

    data = raw_data[raw_data["year"] == year].T[1:].reset_index()
    data = data.rename(columns={"index":"name",data.columns[-1]:"value" })

    gdf_merged = gdf.merge(data, on='name', how='left')
    gdf_merged['value'].fillna(-1, inplace=True)

    fig = px.choropleth_mapbox(
                                gdf_merged,
                                geojson=gdf_merged['geometry'],
                                locations=gdf_merged.index,
                                color='value',
                                color_continuous_scale='Viridis',
                                mapbox_style='carto-positron',
                                center={'lat': 51.5074, 'lon': -0.1278},
                                zoom=9,
                                opacity=0.5,
                                hover_name='name',
                                labels={'value': 'Data Value'}
                            )
    fig.update_layout(width=800, height = 600)
    return fig
