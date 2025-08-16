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
</style>
"""