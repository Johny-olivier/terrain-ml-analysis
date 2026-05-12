import streamlit as st
import joblib
import folium
from folium.plugins import HeatMap
from streamlit.components.v1 import html

from ml_utils import COMMUNE_COORDS, build_prediction_frame, load_dataset


@st.cache_resource
def load_model_artifacts():
    model, columns = joblib.load("model.pkl")
    return model, list(columns)


@st.cache_data
def load_app_data():
    return load_dataset()


def build_map(df):
    m = folium.Map(location=[-18.8792, 47.5079], zoom_start=11)
    mappable_df = df[df["commune"].isin(COMMUNE_COORDS)].copy()

    commune_stats = (
        mappable_df.groupby("commune", as_index=False)["prix_m2"]
        .mean()
        .sort_values("commune")
    )

    for _, row in commune_stats.iterrows():
        commune = row["commune"]
        lat, lon = COMMUNE_COORDS[commune]
        avg_price = row["prix_m2"]

        folium.CircleMarker(
            location=(lat, lon),
            radius=8,
            popup=f"{commune} - {int(avg_price):,} Ar/m²",
            color="blue",
            fill=True,
            fill_opacity=0.7,
        ).add_to(m)

    sample_size = min(5000, len(mappable_df))
    heat_df = mappable_df.sample(sample_size, random_state=42)
    heat_data = [
        [*COMMUNE_COORDS[row["commune"]], row["prix_m2"]]
        for _, row in heat_df.iterrows()
    ]

    if heat_data:
        HeatMap(heat_data, radius=25, blur=15).add_to(m)

    return m, len(mappable_df), len(df) - len(mappable_df)


st.set_page_config(page_title="SIG - Prix des terrains Analamanga", layout="wide")

model, columns = load_model_artifacts()
df = load_app_data()

st.title("SIG - Estimation des prix des terrains a Analamanga")
st.caption(
    "Le modele predit d'abord un prix au m² a partir des caracteristiques du terrain, "
    "puis calcule le prix total avec la surface saisie."
)

col_map, col_info = st.columns([2, 1])

with col_map:
    m, mapped_rows, missing_rows = build_map(df)
    html(m._repr_html_(), height=600)

with col_info:
    st.subheader("Resume du dataset")
    st.metric("Lignes", f"{len(df):,}")
    st.metric("Prix moyen au m²", f"{int(df['prix_m2'].mean()):,} Ar")
    st.metric("Communes", f"{df['commune'].nunique()}")
    st.metric("Points cartographies", f"{mapped_rows:,}")

    if missing_rows:
        st.warning(
            f"{missing_rows:,} lignes ne sont pas affichees sur la carte, faute de coordonnees."
        )

st.subheader("Estimation d'un terrain")

available_communes = sorted(df["commune"].unique())
available_papers = sorted(df["type_papier"].unique())

col1, col2, col3 = st.columns(3)

with col1:
    commune = st.selectbox("Commune", available_communes)
    surface = st.number_input("Surface (m²)", min_value=100, max_value=10000, value=1000)

with col2:
    acces_voiture = st.selectbox("Acces voiture", [0, 1], format_func=lambda x: "Oui" if x else "Non")
    batissable = st.selectbox("Batissable", [0, 1], format_func=lambda x: "Oui" if x else "Non")

with col3:
    distance_rn = st.number_input(
        "Distance a la route nationale (m)", min_value=0, max_value=5000, value=500
    )
    distance_jirama = st.number_input(
        "Distance a la JIRAMA (m)", min_value=0, max_value=3000, value=200
    )

type_papier = st.selectbox("Type de papier", available_papers)

if st.button("Calculer le prix estime"):
    df_input = build_prediction_frame(
        columns,
        acces_voiture=acces_voiture,
        distance_rn=distance_rn,
        batissable=batissable,
        distance_jirama=distance_jirama,
        commune=commune,
        type_papier=type_papier,
    )

    prix_m2 = float(model.predict(df_input)[0])
    prix_total = prix_m2 * surface

    st.success(f"Prix estime au m² : {int(prix_m2):,} Ar")
    st.success(f"Prix total estime : {int(prix_total):,} Ar")
    st.info(
        "Lecture rapide : un acces voiture, une bonne constructibilite et une commune plus "
        "recherchee augmentent generalement le prix, alors que l'eloignement des axes et "
        "des services a tendance a le reduire."
    )
