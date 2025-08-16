import json
import pandas as pd

def load_kanji_data(kanji_file, known_file):
    with open(kanji_file, "r", encoding="utf-8") as f:
        kanji_data = json.load(f)
    
    try:
        with open(known_file, "r", encoding="utf-8") as f:
            known_flags = json.load(f)
    except FileNotFoundError:
        known_flags = {kanji: False for kanji in kanji_data.keys()}

    use_columns = ["strokes", "grade", "freq", "jlpt_new", "meanings",
                   "readings_on", "readings_kun", "wk_level"]
    df = pd.DataFrame.from_dict(kanji_data, orient="index", columns=use_columns).reset_index()
    df.rename(columns={"index": "kanji"}, inplace=True)

    numeric_cols = ["strokes", "grade", "freq", "jlpt_new", "wk_level"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='raise').astype("Int64")
    
    return df, known_flags