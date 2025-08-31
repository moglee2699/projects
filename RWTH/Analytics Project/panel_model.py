import streamlit as st
import pandas as pd
import os
import unicodedata

# Optional import for plotting
try:
    import matplotlib.pyplot as plt
except ImportError:
    st.warning("matplotlib not installed; plots won't display.")

# Biogeme backend estimation (remains, not shown in UI)
try:
    from biogeme.database import Database
    from biogeme.biogeme import BIOGEME
    from biogeme.models import logit
    from biogeme.expressions import Beta, Variable, PanelLikelihoodTrajectory
except ImportError:
    st.warning("biogeme package is missing. Ensure it is installed in your environment.")

st.set_page_config(page_title="Penalty Model", layout="wide")
st.title("⚽ Panel Logit Model")

selected_players = [
    "Ronaldo", "Messi", "Ibrahimovic", "Lewandowski", "Cavani", "Aguero", "Immobile", "Suarez", "Kane", "Vidal",
    "Fernandes", "Jorginho", "Parejo", "Muller", "Ramos"
]
player_photo_map = {
    "Ronaldo": "players/Ronaldo.jpg",
    "Messi": "players/Messi.jpg",
    "Ibrahimovic": "players/Ibrahimovic.jpg",
    "Lewandowski": "players/Lewandowski.jpg",
    "Cavani": "players/Cavani.jpg",
    "Aguero": "players/Aguero.jpg",
    "Immobile": "players/Immobile.jpg",
    "Suarez": "players/Suarez.jpg",
    "Kane": "players/Kane.jpg",
    "Vidal": "players/Vidal.jpg",
    "Fernandes": "players/Fernandes.jpg",
    "Jorginho": "players/Jorginho.jpg",
    "Parejo": "players/Parejo.jpg",
    "Muller": "players/Muller.jpg",
    "Ramos": "players/Ramos.jpg"
}
player_photo_map = {unicodedata.normalize('NFKD', k).encode('ascii', 'ignore').decode('ascii').strip(): v for k, v in player_photo_map.items()}

def normalize_ascii(s):
    if pd.isnull(s):
        return ""
    return unicodedata.normalize('NFKD', str(s)).encode('ascii', 'ignore').decode('ascii').strip()

@st.cache_data(show_spinner=True)
def load_data():
    try:
        df = pd.read_csv("DataSetModel0NA6Alt.csv")
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        st.stop()
    df.columns = [col.strip().lower() for col in df.columns]
    #st.write("Detected columns after normalization:", df.columns.tolist())

    colmap = {
        'player name': 'player_name', 'id': 'ID', 'foot': 'foot', 'status': 'status', 'choice': 'Choice'
    }
    missing = [c for c in colmap if c not in df.columns and c != 'status']
    if missing:
        st.error(f"Missing columns after normalization: {missing}")
        st.stop()
    df = df.rename(columns={k: v for k, v in colmap.items() if k in df.columns})
    df['player_name'] = df['player_name'].map(normalize_ascii)
    player_list_norm = [normalize_ascii(name) for name in selected_players]
    df = df[df['player_name'].isin(player_list_norm)].copy()
    if df.empty:
        st.error("No data found for the selected players. Check names in the CSV!")
        st.stop()
    foot_map = {1: 'Right', 0: 'Left'}
    df['Footedness'] = df['foot'].map(foot_map)
    if 'altid' not in df.columns:
        df = df.reset_index(drop=True)
        df = df.sort_values('ID').reset_index(drop=True)
        df['ChoiceSituationID'] = df.groupby('ID').cumcount() // 3
        df['AltID'] = df.groupby(['ID', 'ChoiceSituationID']).cumcount() + 1
    return df

df = load_data()

# Model estimation cached, not displayed
@st.cache_data(show_spinner=True)
def estimate_panel_model(df_input):
    try:
        df_bio = df_input[['ID', 'ChoiceSituationID', 'AltID', 'foot', 'Choice']]
        database = Database("penalty_model", df_bio)
        database.panel("ID")
        AltID = Variable("AltID")
        Choice = Variable("Choice")
        foot = Variable("foot")
        ASC1 = Beta("ASC1", 0, None, None, 0)
        ASC2 = Beta("ASC2", 0, None, None, 0)
        ASC3 = Beta("ASC3", 0, None, None, 1)
        B_FOOT = Beta("B_FOOT", 0, None, None, 0)
        V = {1: ASC1 + B_FOOT * foot, 2: ASC2 + B_FOOT * foot, 3: ASC3}
        av = {1: 1, 2: 1, 3: 1}
        logprob = logit(V, av, AltID)
        panel_loglike = PanelLikelihoodTrajectory(logprob)
        biogeme = BIOGEME(database, panel_loglike, model_name="penalty_model")
        biogeme.generate_html = False
        biogeme.generate_pickle = False
        results = biogeme.estimate()
        return results.get_estimated_parameters()
    except Exception as e:
        print(f"Estimation failed in backend (not shown to user): {e}")
        return pd.DataFrame()
_ = estimate_panel_model(df)

@st.cache_data(show_spinner=False)
def compute_summaries(df_input):
    if 'status' in df_input.columns:
        summary_by_foot = df_input.groupby(['Footedness', 'status']).size().unstack(fill_value=0)
        summary_by_foot.index.name = "Footedness"
        summary_by_player = df_input.groupby(['player_name', 'Footedness', 'status']).size().unstack(fill_value=0)
        summary_by_player.index.names = ['Player Name', 'Footedness']
    else:
        alt_map = {1: 'Goal', 2: 'Saved', 3: 'Missed'}
        df_out = df_input.copy()
        df_out['Outcome'] = df_out['AltID'].map(alt_map)
        df_out = df_out[df_out['Choice'] == 1]
        summary_by_foot = df_out.groupby(['Footedness', 'Outcome']).size().unstack(fill_value=0)
        summary_by_foot.index.name = "Footedness"
        summary_by_player = df_out.groupby(['player_name', 'Footedness', 'Outcome']).size().unstack(fill_value=0)
        summary_by_player.index.names = ['Player Name', 'Footedness']
    return summary_by_foot, summary_by_player

summary_by_foot, summary_by_player = compute_summaries(df)

section = st.radio(
    "Choose Feature", 
    ["Footedness Stats", "Player Performance"]
)

if section == "Footedness Stats":
    st.subheader("👣 Goals, Saves, Misses by Footedness")
    st.dataframe(summary_by_foot, use_container_width=True)
    try:
        st.subheader("📊 Bar Chart: Outcomes by Footedness")
        summary = summary_by_foot.copy()
        order = [col for col in ['Goal', 'Missed', 'Saved'] if col in summary.columns]
        summary = summary[order]
        labels = list(summary.index)
        x = range(len(labels))
        bar_width = 0.22
        fig, ax = plt.subplots(figsize=(5.5, 2.5))
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
        for i, col in enumerate(summary.columns):
            bar_pos = [v + bar_width * i - bar_width for v in x]
            bars = ax.bar(bar_pos, summary[col].values, bar_width, label=col, color=colors[i % len(colors)], zorder=3)
            for rect in bars:
                height = rect.get_height()
                ax.annotate(
                    f"{int(height)}",
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 1),
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=5, fontweight='bold'
                )
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=8, fontweight='bold', rotation=0)
        ax.set_ylabel("")
        ax.set_xlabel("")
        ax.set_title("Outcomes by Footedness", fontsize=8, pad=9, weight='bold')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('gray')
        ax.yaxis.set_visible(False)
        ax.legend(title='status', fontsize=5, loc='upper right', title_fontsize=8)
        plt.tight_layout(pad=0.5)
        st.pyplot(fig)
    except Exception as e:
        st.warning(f"Bar chart could not be displayed: {e}")

elif section == "Player Performance":
    st.subheader("🧍 Individual Player Performance")
    players = sorted(df['player_name'].unique())
    selected_player = st.selectbox("Select a player:", players)
    player_rows = df[df['player_name'] == selected_player]
    footedness = player_rows['Footedness'].iloc[0] if not player_rows.empty else "N/A"
    goals = (player_rows['status'] == 'Goal').sum()
    missed = (player_rows['status'] == 'Missed').sum()
    saved  = (player_rows['status'] == 'Saved').sum()
    stats_col, image_col = st.columns([2, 1])
    with stats_col:
        st.markdown(
            f"""
            <b>Player:</b> {selected_player}<br>
            <b>Footedness:</b> {footedness}<br>
            <b>Goals:</b> {goals}<br>
            <b>Missed:</b> {missed}<br>
            <b>Saved:</b> {saved}
            """,
            unsafe_allow_html=True,
        )
    with image_col:
        photo_path = player_photo_map.get(selected_player)
        if photo_path and os.path.exists(photo_path):
            st.image(photo_path, width=220, caption=selected_player)
    try:
        outcomes = ['Goal', 'Saved', 'Missed']
        perf_counts = player_rows['status'].value_counts().reindex(outcomes, fill_value=0)
        max_count = perf_counts.max()
        fig, ax = plt.subplots(figsize=(5.5, 2.5))
        bars = ax.bar(outcomes, perf_counts.values, color=['green', 'orange', 'red'], width=0.6, zorder=3)
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.set_title(f"Penalty Outcomes for {selected_player}", fontsize=7, pad=5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('gray')
        ax.yaxis.set_visible(False)
        ax.set_xticks(range(len(outcomes)))
        ax.set_xticklabels(outcomes, fontsize=5, rotation=0)
        ylim_max = max(max_count * 1.15, 1)
        ax.set_ylim(0, ylim_max)
        for bar in bars:
            height = bar.get_height()
            ax.annotate(
                f"{int(height)}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 4),
                textcoords="offset points",
                ha='center', va='bottom',
                fontsize=5,
                fontweight='bold'
            )
        plt.tight_layout(pad=0.2)
        st.pyplot(fig)
    except Exception:
        st.info("No penalty outcome data available for this player yet.")

else:
    st.info("👆 Select a dashboard feature above to view results.")
