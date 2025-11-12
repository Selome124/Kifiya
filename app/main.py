import streamlit as st
import os
import pandas as pd
from app.utils import load_data, plot_boxplot

DATA_DIR = "Kifiya/data"
FILES = {
    "Benin": os.path.join(DATA_DIR, "benin_clean.csv"),
    "Sierraleone": os.path.join(DATA_DIR, "sierraleone_clean.csv"),
    "Togo": os.path.join(DATA_DIR, "togo_clean.csv"),
}

@st.cache_data
def load_all_data():
    dfs = []
    for country, path in FILES.items():
        df = load_data(path)
        df["country"] = country
        dfs.append(df)
    combined = pd.concat(dfs)
    return combined

def main():
    st.title("Solar Data Dashboard")

    # Load data
    combined = load_all_data()

    # Widget: multiselect countries
    countries = combined["country"].unique().tolist()
    selected_countries = st.multiselect("Select countries to include", countries, default=countries)

    filtered_data = combined[combined["country"].isin(selected_countries)]

    # Widget: select metric
    metrics = ["GHI", "DNI", "DHI"]
    selected_metric = st.selectbox("Select metric to visualize", metrics)

    # Plot
    st.write(f"### Boxplot of {selected_metric} for selected countries")
    fig = plot_boxplot(filtered_data.reset_index(), selected_metric)
    st.pyplot(fig)

    # Display top 5 regions by average selected metric (if you have region info)
    if "region" in filtered_data.columns:
        st.write(f"### Top 5 Regions by Average {selected_metric}")
        region_summary = (
            filtered_data.groupby("region")[selected_metric]
            .mean()
            .sort_values(ascending=False)
            .head(5)
            .reset_index()
        )
        st.table(region_summary)
    else:
        st.info("No regional data available.")
if __name__ == "__main__": 
    main()