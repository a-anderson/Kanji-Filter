def css():
    return """
<style>
    /* Main background */
    .main { background-color: #FDF6E3; }
    
    /* Headings */
    h1, h2, h3 { 
        color: #3B3B98; 
        font-family: 'Noto Sans JP', sans-serif; 
    }
            
    /* Progress bar color */
    .stProgress > div > div > div > div {
        background-color: #D72638;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #D72638;
        color: white;
        border-radius: 8px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #B51D2E;
    }
            
    /* Change sidebar background */
    [data-testid="stSidebar"] {
        background-color: #FAEDD0;
    }

    /* Sidebar text colour */
    [data-testid="stSidebar"] * {
        color: #3B3B98; /* Indigo */
    }

    /* Sidebar search input — remove Streamlit's default white container border */
    [data-testid="stSidebar"] [data-testid="stTextInput"] > div {
        border: none !important;
        box-shadow: none !important;
        background-color: transparent !important;
    }
    [data-testid="stSidebar"] [data-testid="stTextInput"] input {
        background-color: #FAEDD0;
        border: 1px solid rgba(49, 51, 63, 0.2);
        border-radius: 8px;
        color: #3B3B98;
    }
    [data-testid="stSidebar"] [data-testid="stTextInput"] input:focus {
        border-color: #3B3B98;
        box-shadow: 0 0 0 2px rgba(59, 59, 152, 0.15);
        outline: none;
    }
    [data-testid="stSidebar"] [data-testid="stTextInput"] input::placeholder {
        color: #9B8FC0;
    }
</style>
"""