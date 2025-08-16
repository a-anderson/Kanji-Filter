import json
import pandas as pd
import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import utils.styling as styling
from utils.data import load_kanji_data

KANJI_FILE = "data/kanji.json"
KNOWN_KANJI_FILE = "data/known_kanji.json"

# --- PAGE CONFIG ---
st.set_page_config(page_title="Kanji Filter", layout="wide")


window_size = streamlit_js_eval(js_expressions="""
    ({width: window.parent.innerWidth, height: window.parent.innerHeight})
""", key="get_size")

# fallback to a default height if JS hasn't returned yet
window_height = window_size["height"] if window_size is not None else 800

# --- CUSTOM CSS FOR VISUAL STYLE ---
st.markdown(styling.css(), unsafe_allow_html=True)

# --- LOAD DATA ---
df, known_flags = load_kanji_data(KANJI_FILE, KNOWN_KANJI_FILE)
if "known_flags" not in st.session_state:
    st.session_state.known_flags = known_flags

# --- SIDEBAR FILTERS ---
st.sidebar.image("images/logo.png", use_container_width=True)  
st.sidebar.title("🔍 Filters")

def sidebar_multiselect_filter(label, series, include_unknown=True):
    options = sorted(series.dropna().unique())
    selected = st.multiselect(f"Select {label}", options, default=options)
    include_unknown_checkbox = st.checkbox(f"Include Unknown {label}", include_unknown)
    
    mask = series.isin(selected)
    if include_unknown_checkbox:
        mask |= series.isna()
    return mask

with st.sidebar.expander("📚 Grade"):
    grade_mask = sidebar_multiselect_filter("Grades", df["grade"])

with st.sidebar.expander("🦀 WaniKani Level"):
    wk_mask = sidebar_multiselect_filter("WK Levels", df["wk_level"])

with st.sidebar.expander("📊 Frequency"):
    min_freq, max_freq = int(df["freq"].min(skipna=True)), int(df["freq"].max(skipna=True))
    freq_range = st.slider("Frequency Range", min_freq, max_freq, (min_freq, max_freq))
    include_unknown_freq = st.checkbox("Include Unknown Frequency", True)

    between_selection = df["freq"].between(*freq_range)
    if include_unknown_freq:
        freq_mask = between_selection | df["freq"].isna()
    else:
        freq_mask = between_selection

with st.sidebar.expander("🎯 JLPT Level"):
    jlpt_mask = sidebar_multiselect_filter("JLPT", df["jlpt_new"])

show_only_known = st.sidebar.toggle("✅ Show Only Known", False)
show_only_unknown = st.sidebar.toggle("❓ Show Only Unknown", False)

toggle_mask = pd.Series(True, index=df.index)
if show_only_known:
    toggle_mask = df["kanji"].map(st.session_state.known_flags).fillna(False)
elif show_only_unknown:
    toggle_mask = ~df["kanji"].map(st.session_state.known_flags).fillna(False)

# --- APPLY FILTERS ---
filtered_df = df[grade_mask & wk_mask & freq_mask & jlpt_mask & toggle_mask].copy()
filtered_df["known"] = filtered_df["kanji"].map(st.session_state.known_flags).fillna(False)
cols = ["known", "kanji"] + [c for c in filtered_df.columns if c not in ["known", "kanji"]]
filtered_df = filtered_df[cols]

# --- SESSION STATE FOR TABLE ---
if "kanji_df" not in st.session_state:
    st.session_state.kanji_df = filtered_df.copy()
else:
    # keep previous known values for unchanged rows
    existing_flags = st.session_state.kanji_df.set_index("kanji")["known"]
    filtered_df["known"] = filtered_df["kanji"].map(existing_flags).fillna(filtered_df["known"])
    st.session_state.kanji_df = filtered_df.copy()

if "refresh_table_key" not in st.session_state:
    st.session_state.refresh_table_key = 0

# --- LAYOUT SETUP ---
placeholder_col1, placeholder_col2, placeholder_col3 = st.columns(3)
total_placeholder = placeholder_col1.empty()
known_placeholder = placeholder_col2.empty()
progress_placeholder = placeholder_col3.empty()
table_placeholder = st.empty()

# --- BUTTON ROW ---
col1, col2, col3, col4 = st.columns([1,1,2,1])

def set_all_known(known=True):
    st.session_state.kanji_df["known"] = known
    st.session_state.known_flags.update(
        dict(zip(st.session_state.kanji_df["kanji"], [known]*len(st.session_state.kanji_df)))
    )
    st.session_state.refresh_table_key += 1

with col1:
    if st.button("✅ Set All Known"):
        set_all_known(True)

with col2:
    if st.button("❌ Set All Unknown"):
        set_all_known(False)

with col4:
    if st.button("💾 Save Known Kanji"):
        updated_flags = dict(zip(st.session_state.kanji_df["kanji"], st.session_state.kanji_df["known"]))
        st.session_state.known_flags.update(updated_flags)
        with open(KNOWN_KANJI_FILE, "w", encoding="utf-8") as f:
            json.dump(st.session_state.known_flags, f, ensure_ascii=False, indent=4)
        st.success("✅ Progress saved!")

# --- TABLE CONFIG ---
column_configuration = {
    "known": st.column_config.CheckboxColumn("Known", default=False),
    "kanji": st.column_config.TextColumn("Kanji", width="small", help="Click to mark known"),
    "strokes": "Strokes",
    "grade": "Grade",
    "freq": "Frequency",
    "jlpt_new": "JLPT",
    "meanings": "Meanings",
    "readings_on": "音読み",
    "readings_kun": "訓読み",
    "wk_level": "WaniKani",
}

# --- DISPLAY TABLE ---
def sync_known_flags(df):
    st.session_state.kanji_df = df
    st.session_state.known_flags.update(dict(zip(df["kanji"], df["known"])))

edited_df = table_placeholder.data_editor(
    st.session_state.kanji_df,
    column_config=column_configuration,
    use_container_width=True,
    hide_index=True,
    height=max(window_height - 350, 250),
    disabled=[c for c in st.session_state.kanji_df.columns if c != "known"],
    key=f"kanji_table_{st.session_state.refresh_table_key}",  # dynamic key
    on_change=sync_known_flags,
    args=(st.session_state.kanji_df,)
)

st.session_state.kanji_df = edited_df

# --- STATS & PROGRESS CALCULATIONS ---
total_kanji = len(st.session_state.kanji_df)
known_count = st.session_state.kanji_df["known"].sum()
progress_pct = 0 if total_kanji == 0 else known_count / total_kanji

total_placeholder.metric("Total Kanji", f"{total_kanji:,}")
known_placeholder.metric("Known Kanji", f"{known_count:,}")
progress_placeholder.progress(progress_pct, text=f"{100*progress_pct:.1f}% of Total")