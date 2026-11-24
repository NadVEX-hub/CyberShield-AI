import streamlit as st
import base64
from predict import predict_url

st.set_page_config(
    page_title="CyberShield",
    layout="wide"
)

# Original geometric background artwork
artwork = """
<svg xmlns="http://www.w3.org/2000/svg"
     viewBox="0 0 1440 900">

<rect width="1440" height="900" fill="#030409"/>

<g fill="none" stroke="#101978" stroke-width="3">
    <path d="M0 90 L180 230 L70 450 L310 610
             L190 900 M180 230 L390 70 L500 0"/>
    <path d="M0 500 L70 450 L200 530 L310 610
             L530 480 L670 750 L830 900"/>
    <path d="M530 480 L720 300 L850 600
             L1120 800 L1440 650"/>
    <path d="M720 300 L600 100 L850 0
             M850 600 L1200 520 L1380 210"/>
    <path d="M1380 210 L1160 80 L1300 0
             M1200 520 L1440 450"/>
    <path d="M0 760 L200 650 L420 850
             L790 700 L1040 840 L1440 560"/>
    <path d="M350 0 L420 250 L690 290
             L850 80 L1160 130"/>
</g>

<g fill="#101765" opacity="0.5">
    <polygon points="180,230 390,70 250,280"/>
    <polygon points="310,610 530,480 430,660"/>
    <polygon points="850,600 1200,520 1030,650"/>
    <polygon points="1380,210 1160,80 1270,300"/>
    <polygon points="70,450 200,530 0,470"/>
    <polygon points="420,250 690,290 580,320"/>
    <polygon points="790,700 1040,840 850,800"/>
</g>

<!-- Original low-poly parrot -->
<g transform="translate(670 130) scale(1.8)">

    <polygon points="220,30 250,20 275,45 240,50"
             fill="#12C66C"/>
    <polygon points="220,30 240,50 227,78 210,52"
             fill="#E5E7EB"/>
    <polygon points="240,50 275,45 265,80 227,78"
             fill="#A4B1BE"/>
    <polygon points="227,78 210,52 194,70 215,92"
             fill="#404650"/>

    <polygon points="240,50 265,80 295,106 250,115"
             fill="#06B6D4"/>
    <polygon points="227,78 250,115 225,150 215,106"
             fill="#EAC51C"/>
    <polygon points="265,80 295,106 325,170 268,133"
             fill="#007FDD"/>
    <polygon points="250,115 268,133 225,150"
             fill="#9B7D0C"/>

    <!-- Wing -->
    <polygon points="250,115 190,70 70,92 220,87"
             fill="#10C4EB"/>
    <polygon points="220,87 70,92 25,116 232,102"
             fill="#087CF1"/>
    <polygon points="232,102 80,145 160,108 250,115"
             fill="#1744DC"/>
    <polygon points="250,115 110,200 190,130"
             fill="#1436B7"/>
    <polygon points="250,115 180,215 225,150"
             fill="#182C91"/>

    <!-- Tail feathers -->
    <polygon points="268,133 225,150 240,225"
             fill="#103DC9"/>
    <polygon points="268,133 325,170 290,220"
             fill="#08B5E8"/>
    <polygon points="268,133 290,220 260,315"
             fill="#0756ED"/>
    <polygon points="290,220 325,170 330,280"
             fill="#142EA4"/>
    <polygon points="240,225 268,133 245,280"
             fill="#1E3A8A"/>

    <circle cx="229" cy="50" r="3" fill="#030409"/>

</g>
</svg>
"""

background = base64.b64encode(
    artwork.encode("utf-8")
).decode("ascii")

# Website styling
st.markdown(f"""
<style>

.stApp {{
    background-color: #030409;
    background-image: url("data:image/svg+xml;base64,{background}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

[data-testid="stHeader"] {{
    background: transparent;
}}

.block-container {{
    max-width: 1300px;
    padding-top: 45px;
}}

.brand {{
    color: #28C7EE;
    font-family: monospace;
    font-size: 22px;
    letter-spacing: 3px;
}}

.heading {{
    color: #F3F4F6;
    font-size: 34px;
    font-weight: 600;
    margin-top: 70px;
}}

.description {{
    color: #A4AFC4;
    font-size: 15px;
    margin-bottom: 28px;
}}

.stTextInput input {{
    background-color: #101319;
    color: #FFFFFF;
    font-family: monospace;
    border-radius: 3px;
}}

.stFormSubmitButton button {{
    background-color: #102B46;
    color: #50D9F5;
    border: 1px solid #24A6CD;
    border-radius: 3px;
    padding: 8px 24px;
}}

.stFormSubmitButton button:hover {{
    background-color: #163C5E;
    color: white;
    border-color: #50D9F5;
}}

[data-testid="stForm"] {{
    border: none;
    padding: 0;
}}

@media (max-width: 768px) {{
    .stApp {{
        background-position: left center;
        background-size: auto 100%;
    }}

    .heading {{
        font-size: 28px;
        margin-top: 35px;
    }}
}}

</style>
""", unsafe_allow_html=True)

# Brand name
st.markdown(
    '<div class="brand">CYBERSHIELD</div>',
    unsafe_allow_html=True
)

st.divider()

# Keep the analyzer on the left
left, right = st.columns([1, 1.1])

with left:

    st.markdown("""
    <div class="heading">Phishing URL Checker</div>
    <div class="description">
        Analyze a website address before opening it.
    </div>
    """, unsafe_allow_html=True)

    with st.form("url_check"):

        url = st.text_input(
            "Website address",
            placeholder="https://example.com",
            label_visibility="collapsed",
            max_chars=4096
        )

        submitted = st.form_submit_button("Analyze URL")

    if submitted:

        try:
            prediction, risk = predict_url(url)

            if prediction == 0:
                st.error("Potential phishing website")
                st.write("Avoid entering sensitive information.")
            else:
                st.info("Predicted legitimate")
                st.write("Website safety is not guaranteed.")

            st.write(f"Model phishing score: {risk:.2f}%")
            st.progress(float(risk / 100))

            st.caption(
                "The score is not a verified probability of danger."
            )

        except ValueError:
            st.warning("Please enter a valid HTTP or HTTPS URL.")

    st.caption(
    "Research prototype. URL analysis only. "
    "Results do not guarantee website safety. "
    "Avoid submitting private links."
)
    