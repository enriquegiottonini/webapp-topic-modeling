from datetime import date, timedelta

import numpy as np
import pandas as pd
import streamlit as st

st.sidebar.markdown("# **Universidad de Sonora**")
st.sidebar.markdown("## Ciencias de la Computación")
st.sidebar.markdown(
    "### Proyecto final para la materia de **Procesamiento de Lenguage Natural**"
)
st.sidebar.markdown("---")
st.sidebar.markdown("### Equipo:")
st.sidebar.markdown(
    """ 
    - **Andrés Burruel**\n
    - **Oscar Galaviz**
    - **Enrique Giottonini**
    - **Abraham Villalba**
    """
)


st.title(
    "Modelando los temas de las mañaneras utilizando alocación de Dirichlet latente."
)
st.image("resources/images/banner.jpeg")
st.markdown("---")

st.markdown("## Introducción")
st.markdown("### ¿En qué consistió el modelado de temas?")
st.markdown(
    "Se utilizó un conjunto de transcripciones de las mañaneras que se encuentra disponible en el siguiente [repositorio](https://github.com/NOSTRODATA/conferencias_matutinas_amlo) gracias al equipo de `@nostrodata`."
)

st.markdown(
    "Las transcripciones fueron agrupadas en semanas y se utilizó el modelo de alocación de Dirichlet latente para agrupar las palabras en temas y asignar a cada semana una distribución de temas."
)

st.markdown("### Tendencias de temas")
st.markdown(
    "El modelado de temas permite identificar las tendencias de temas a lo largo del tiempo. Por ejemplo, podemos observar como ha cambiado los temas a tratar en las mañaneras."
)

raw_data = pd.read_csv("resources/data/data.csv")
raw_data["date"] = pd.to_datetime(raw_data["date"], format="%Y-%m-%d")

topics = set(raw_data["topic"])

options = st.multiselect(
    "Selecciona los temas que quieres visualizar",
    list(topics),
    default="Vacunación",
)

init = raw_data["date"].min().date()
end = raw_data["date"].max().date()

interval = st.slider(
    "Selecciona el intervalo de tiempo que quieres vfisualizar",
    min_value=init,
    max_value=end,
    value=(init, end),
    format="YYYY-MM-DD",
    step=timedelta(days=7),
)

init_s = np.datetime64(interval[0])
end_s = np.datetime64(interval[1])

min_dist = 0.0
df_topics = raw_data[raw_data["topic"].isin(options)]
df_topics = df_topics[df_topics["distribution"] >= min_dist]
df_topics = df_topics[df_topics["date"] >= init_s]
df_topics = df_topics[df_topics["date"] <= end_s]

st.vega_lite_chart(
    df_topics,
    {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "encoding": {
            "x": {"field": "date", "type": "temporal", "title": "Semana"},
            "y": {
                "field": "distribution",
                "type": "quantitative",
                "title": "Distribución",
            },
            "color": {
                "condition": {
                    "param": "hover",
                    "field": "topic",
                    "type": "nominal",
                    "legend": "null",
                },
                "value": "grey",
            },
            "opacity": {
                "condition": {"param": "hover", "value": 1},
                "value": 0.2,
            },
        },
        "layer": [
            {
                "description": "transparent layer to make it easier to trigger selection",
                "params": [
                    {
                        "name": "hover",
                        "value": [{"topic": "Vacunación"}],
                        "select": {
                            "type": "point",
                            "fields": ["topic"],
                            "on": "mouseover",
                        },
                    }
                ],
                "mark": {
                    "type": "line",
                    "strokeWidth": 8,
                    "stroke": "transparent",
                },
            },
            {"mark": "line"},
            {
                "encoding": {
                    "x": {"aggregate": "max", "field": "date"},
                    "y": {
                        "aggregate": {"argmax": "date"},
                        "field": "distribution",
                    },
                },
                "layer": [
                    {"mark": {"type": "circle"}},
                    {
                        "mark": {"type": "text", "align": "left", "dx": 4},
                        "encoding": {
                            "text": {"field": "topic", "type": "nominal"}
                        },
                    },
                ],
            },
        ],
        "config": {"view": {"stroke": "null"}},
    },
    use_container_width=True,
    theme="streamlit",
)

#######################################################################################################################
st.markdown("### Distribución de temas por semana")


def get_pie_values(df, week):
    min_dist = 0.05
    df_w = df[df["week"] == week]
    df_w = df_w.drop(columns=["week"])
    values = []
    for column in df_w.columns:
        if df_w[column].values[0] >= min_dist:
            values.append(
                {"category": column, "value": df_w[column].values[0]}
            )
    return values


pie_spec = {
    "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
    "description": "Pie Chart with percentage_tooltip",
    "data": {"values": []},
    "mark": {"type": "arc", "tooltip": True},
    "encoding": {
        "theta": {
            "field": "value",
            "type": "quantitative",
            "stack": "normalize",
        },
        "color": {"field": "category", "type": "nominal"},
    },
}

raw_df = pd.read_csv("resources/data/raw_data.csv")
semana = st.slider(
    "Selecciona el intervalo de tiempo que quieres visualizar",
    min_value=init,
    max_value=end,
    value=init,
    format="YYYY-MM-DD",
    step=timedelta(days=7),
)
st.metric(label="Semana", value=semana.strftime("%d %B, %Y"))
values = get_pie_values(raw_df, str(semana))
pie_spec["data"]["values"] = values
st.vega_lite_chart(
    spec=pie_spec,
)
