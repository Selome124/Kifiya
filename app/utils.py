import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_data(path):
    df = pd.read_csv(path)
    time_col = next((col for col in df.columns if "time" in col.lower() or "date" in col.lower()), None)
    if time_col:
        df["Timestamp"] = pd.to_datetime(df[time_col], errors="coerce")
        df = df.dropna(subset=["Timestamp"]).set_index("Timestamp").sort_index()
    return df

def plot_boxplot(df, metric, country_col="country"):
    plt.figure(figsize=(8,5))
    sns.boxplot(data=df, x=country_col, y=metric, palette="Set3")
    plt.title(f"{metric} Distribution by Country")
    plt.xlabel("Country")
    plt.ylabel(metric)
    plt.tight_layout()
    return plt
