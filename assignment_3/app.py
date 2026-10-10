from pathlib import Path
import json
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Lluvias y declaratorias", page_icon="🌧️", layout="wide")

BASE = Path(__file__).resolve().parent
RUTA_DATOS = BASE / "datos" / "dataset.csv"
RUTA_GEO = BASE / "datos" / "distritos.geojson"

@st.cache_data
def cargar():
    df = pd.read_csv(RUTA_DATOS, dtype={"ubigeo":"string"})
    df["ubigeo"] = df["ubigeo"].str.zfill(2)
    with open(RUTA_GEO, "r", encoding="utf-8") as f:
        geojson = json.load(f)
    filas = []
    for feat in geojson.get("features", []):
        p = feat.get("properties", {})
        u6 = str(p.get("ubigeo", "")).zfill(6)
        if u6:
            filas.append({"ubigeo_distrito":u6, "ubigeo":u6[:2]})
    return df, geojson, pd.DataFrame(filas)

df, geojson, geo_tabla = cargar()

st.title("🌧️ Lluvias y declaratorias de emergencia en el Perú")
st.caption("Grupo 7 · Temporada enero–mayo de 2024")
st.markdown("**Pregunta:** ¿Los departamentos con mayor lluvia acumulada son también los que registran más declaratorias de emergencia durante enero–mayo de 2024?")

st.sidebar.header("Filtros")
deps = sorted(df["departamento"].dropna().unique())
sel = st.sidebar.multiselect("Departamento", deps, default=deps)
rmin, rmax = int(df["declaratorias"].min()), int(df["declaratorias"].max())
rango = st.sidebar.slider("Rango de declaratorias", rmin, rmax, (rmin, rmax))

f = df[df["departamento"].isin(sel) & df["declaratorias"].between(*rango)].copy()
st.sidebar.caption(f"{len(f)} de {len(df)} departamentos visibles")

c1,c2,c3,c4 = st.columns(4)
c1.metric("Departamentos", len(f))
c2.metric("Lluvia promedio", f"{f['lluvia_total_mm'].mean():,.1f} mm" if len(f) else "—")
c3.metric("Declaratorias", int(f["declaratorias"].sum()) if len(f) else 0)
c4.metric("Prórrogas", int(f["prorrogas"].sum()) if len(f) else 0)

if f.empty:
    st.warning("No hay datos para los filtros seleccionados.")
    st.stop()

st.subheader("1. Declaratorias por departamento")
orden = f.sort_values(["declaratorias","lluvia_total_mm"], ascending=[True,True])
fig1 = px.bar(
    orden, x="declaratorias", y="departamento", orientation="h",
    text="declaratorias",
    labels={"declaratorias":"Número de declaratorias","departamento":"Departamento"},
    title="Los filtros permiten identificar dónde se concentran las declaratorias"
)
fig1.update_traces(textposition="outside")
fig1.update_layout(template="plotly_white", height=max(420, 28*len(orden)), xaxis=dict(dtick=1))
st.plotly_chart(fig1, width="stretch")

st.subheader("2. Lluvia acumulada vs. declaratorias")
fig2 = px.scatter(
    f, x="lluvia_total_mm", y="declaratorias", hover_name="departamento",
    hover_data={"dias_lluvia_fuerte":True,"prorrogas":True,"lluvia_total_mm":":.1f"},
    labels={"lluvia_total_mm":"Lluvia acumulada (mm)","declaratorias":"Número de declaratorias"},
    title="La lluvia acumulada no se traduce automáticamente en más declaratorias"
)
fig2.update_traces(marker=dict(size=12, opacity=.8))
fig2.update_layout(template="plotly_white")
st.plotly_chart(fig2, width="stretch")

st.subheader("3. Mapa de lluvia acumulada")
mapa_df = geo_tabla.merge(f[["ubigeo","departamento","lluvia_total_mm","declaratorias"]], on="ubigeo", how="inner")
if mapa_df.empty:
    st.info("Los departamentos seleccionados no tienen geometría disponible en el GeoJSON.")
else:
    figm = px.choropleth(
        mapa_df, geojson=geojson, locations="ubigeo_distrito",
        featureidkey="properties.ubigeo", color="lluvia_total_mm",
        hover_name="departamento",
        hover_data={"lluvia_total_mm":":.1f","declaratorias":True,"ubigeo_distrito":False},
        color_continuous_scale="Blues",
        labels={"lluvia_total_mm":"Lluvia acumulada (mm)","declaratorias":"Declaratorias"}
    )
    figm.update_geos(fitbounds="locations", visible=False)
    figm.update_layout(height=650, margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(figm, width="stretch")

    sin_geo = f.loc[~f["ubigeo"].isin(set(geo_tabla["ubigeo"])), ["departamento"]]
    if not sin_geo.empty:
        st.caption("Sin geometría disponible: " + ", ".join(sin_geo["departamento"].tolist()))

st.subheader("4. Datos filtrados")
cols = ["ubigeo","departamento","capital","lluvia_total_mm","dias_lluvia_fuerte","declaratorias","prorrogas"]
tabla = f[cols].sort_values(["declaratorias","lluvia_total_mm"], ascending=[False,False])
st.dataframe(tabla, width="stretch", hide_index=True)

st.download_button(
    "Descargar datos filtrados (.csv)",
    data=tabla.to_csv(index=False).encode("utf-8-sig"),
    file_name="datos_filtrados_assignment_3.csv",
    mime="text/csv"
)

st.subheader("Hallazgos principales")
st.markdown("- Los departamentos con mayor lluvia acumulada no coinciden necesariamente con los de mayor número de declaratorias.\n- La relación lluvia–declaratorias observada en el Assignment 2 fue débil.")
st.info("Limitación: la lluvia corresponde a la capital departamental y el GeoJSON del curso no contiene geometrías para los 25 departamentos.")
