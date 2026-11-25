from pathlib import Path
import time

import joblib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ------------------------------------------------------------
# Page setup
# ------------------------------------------------------------
st.set_page_config(
    page_title="ChurnIQ | Customer Analytics",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)
BASE = Path(__file__).parent

# Palette
BG = "#0B1020"
PANEL = "#121B2E"
PANEL_2 = "#17243B"
BORDER = "#263650"
TEXT = "#F4F7FC"
MUTED = "#9BAAC0"
CYAN = "#54D6E8"
BLUE = "#579BFF"
PURPLE = "#9A82FF"
GREEN = "#48D6A2"
RED = "#FF718B"
AMBER = "#F4B860"

# ------------------------------------------------------------
# Styling
# ------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@500;600;700;800&display=swap');

:root { color-scheme: dark; }
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp {
    background:
      radial-gradient(ellipse at 78% -10%, rgba(62,104,190,.22), transparent 34%),
      radial-gradient(ellipse at 8% 28%, rgba(83,72,160,.12), transparent 32%),
      #0B1020;
    color: #F4F7FC;
}
[data-testid="stHeader"] { background: rgba(11,16,32,.82); }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111C31 0%, #0D1526 100%);
    border-right: 1px solid #263650;
}
[data-testid="stSidebar"] p, [data-testid="stSidebar"] label { color: #D8E2F1; }
.main .block-container { max-width: 1500px; padding: 2rem 2.4rem 3rem; }
.brand { font: 800 25px Manrope,sans-serif; letter-spacing: -1.2px; color:#fff; }
.brand span { color:#62D8E8; }
.brand-sub { color:#8294AF; font-size:9px; letter-spacing:2.2px; margin-top:4px; }
.sidebar-caption { color:#8294AF; font-size:10px; font-weight:700; letter-spacing:1.5px; margin:18px 0 8px; }
.hero {
    position:relative; overflow:hidden; padding:30px 34px; border:1px solid #31496D;
    border-radius:20px; margin:0 0 28px;
    background:linear-gradient(110deg,rgba(30,55,94,.96),rgba(20,38,68,.94) 58%,rgba(29,47,83,.96));
    box-shadow:0 18px 48px rgba(0,0,0,.20);
}
.hero:after { content:"◈"; position:absolute; right:42px; top:2px; font-size:112px; color:rgba(112,177,255,.10); }
.eyebrow { color:#72DDED; font-size:10px; font-weight:800; letter-spacing:2px; }
.hero h1 { font:800 30px Manrope,sans-serif; color:#fff; margin:9px 0 5px; letter-spacing:-.8px; }
.hero p { color:#B8C9E0; font-size:13px; margin:0; max-width:720px; }
.section-label { color:#76D9E8; font-size:10px; font-weight:800; letter-spacing:1.8px; margin:22px 0 12px; }
.metric {
    background:linear-gradient(145deg,#192943,#121D31);
    border:1px solid #2A3D59; border-radius:16px; padding:19px 20px 17px;
    min-height:145px; box-shadow:0 10px 26px rgba(0,0,0,.13);
}
.metric-top { display:flex; justify-content:space-between; align-items:center; }
.metric-icon { width:34px; height:34px; display:grid; place-items:center; border-radius:10px; background:#263B5C; font-size:17px; }
.metric-tag { color:#7F93B0; font-size:9px; font-weight:700; letter-spacing:1px; }
.metric-label { color:#AAB9CE; font-size:11px; margin-top:13px; }
.metric-value { color:#fff; font:800 27px Manrope,sans-serif; margin-top:3px; letter-spacing:-.7px; }
.metric-foot { color:#67D8B4; font-size:10px; margin-top:4px; }
div[data-testid="stVerticalBlockBorderWrapper"] {
    background:linear-gradient(145deg,rgba(23,36,59,.90),rgba(16,26,44,.94));
    border:1px solid #283B57; border-radius:17px;
}
.chart-heading { color:#F5F7FC; font:700 15px Manrope,sans-serif; margin-bottom:3px; }
.chart-sub { color:#91A4BF; font-size:10px; margin-bottom:8px; }
.insight {
    background:linear-gradient(120deg,#1B3150,#173449); border:1px solid #315575;
    border-radius:15px; padding:17px 18px; min-height:122px;
}
.insight-label { color:#AABBD0; font-size:9px; font-weight:700; letter-spacing:1px; }
.insight-value { color:#68DCEF; font:800 24px Manrope,sans-serif; margin:8px 0 3px; }
.insight-note { color:#AABBD0; font-size:10px; }
.stButton button, .stFormSubmitButton button {
    background:linear-gradient(100deg,#7564F5,#328EDB) !important; color:white !important;
    border:0 !important; border-radius:10px !important; font-weight:700 !important; min-height:43px;
}
.stButton button:hover, .stFormSubmitButton button:hover { filter:brightness(1.12); box-shadow:0 5px 22px #4D8FFF45; }
[data-baseweb="select"] > div, [data-testid="stNumberInput"] input {
    background:#17263F !important; border-color:#3A5274 !important; color:white !important; border-radius:9px !important;
}
[data-testid="stForm"] { background:#121E32; border:1px solid #2A3D59; border-radius:16px; padding:22px; }
.stTabs [data-baseweb="tab-list"] { gap:8px; }
.stTabs [data-baseweb="tab"] { background:#15243A; border-radius:9px 9px 0 0; }
hr { border-color:#263650; }
small, .stCaption { color:#91A4BF !important; }

/* High-contrast labels for all prediction form controls */
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] *,
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label,
[data-testid="stSlider"] label,
[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label,
[data-testid="stTextInput"] label,
[data-testid="stRadio"] label,
[data-testid="stCheckbox"] label,
[data-testid="stMultiSelect"] label,
.stSelectbox label,
.stSlider label,
.stNumberInput label,
.stTextInput label {
    color: #EAF2FF !important;
    opacity: 1 !important;
    font-weight: 600 !important;
}

/* Streamlit sometimes renders widget labels as markdown paragraphs */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] div {
    color: #EAF2FF !important;
}

/* Make slider values, min/max values and help text readable */
[data-testid="stSlider"] [data-testid="stThumbValue"],
[data-testid="stSlider"] [data-testid="stTickBarMin"],
[data-testid="stSlider"] [data-testid="stTickBarMax"],
[data-testid="stSlider"] [data-testid="stMarkdownContainer"] p {
    color: #DCE8F8 !important;
}

/* Keep section headings bright on the dark form panel */
[data-testid="stForm"] h1,
[data-testid="stForm"] h2,
[data-testid="stForm"] h3,
[data-testid="stForm"] h4 {
    color: #FFFFFF !important;
}
footer { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Load and normalize project assets
# ------------------------------------------------------------
@st.cache_resource
def get_model():
    return joblib.load(BASE / "customer_churn_model.pkl")

@st.cache_data
def get_data():
    data = pd.read_csv(BASE / "telco_churn_data.csv")
    # The source CSV in this project stores Churn as 0/1, not "No"/"Yes".
    # Normalize both representations to consistent labels for all analytics.
    raw = data["Churn"]
    if pd.api.types.is_numeric_dtype(raw):
        data["Churn"] = raw.map({0: "No", 1: "Yes"})
    else:
        data["Churn"] = raw.astype(str).str.strip().replace({
            "0": "No", "1": "Yes", "False": "No", "True": "Yes"
        })
    data["Churn"] = data["Churn"].fillna("Unknown")
    for col in ["MonthlyCharges", "TotalCharges", "tenure"]:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")
    return data

@st.cache_data
def get_comparison():
    path = BASE / "model_comparison.csv"
    return pd.read_csv(path) if path.exists() else pd.DataFrame()

@st.cache_data
def get_importance():
    path = BASE / "feature_importance.csv"
    return pd.read_csv(path) if path.exists() else pd.DataFrame()

df = get_data()
model = get_model()
total = len(df)
churned = int(df["Churn"].eq("Yes").sum())
retained = int(df["Churn"].eq("No").sum())
churn_rate = (churned / total * 100) if total else 0

# ------------------------------------------------------------
# Chart helpers
# ------------------------------------------------------------
PLOT_CONFIG = {"displayModeBar": False, "responsive": True}

def polish(fig, height=310):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family":"DM Sans", "color":MUTED, "size":11},
        margin={"l":12,"r":18,"t":16,"b":12},
        legend={"orientation":"h","y":-0.20,"font":{"color":"#B7C5D9"}},
        hoverlabel={"bgcolor":"#1B2B45","font_color":"white","bordercolor":"#526D91"},
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(145,170,205,.12)", zeroline=False, linecolor="rgba(145,170,205,.18)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(145,170,205,.12)", zeroline=False, linecolor="rgba(145,170,205,.18)")
    return fig

def header(eyebrow, title, subtitle):
    st.markdown(f"""
    <section class="hero">
      <div class="eyebrow">{eyebrow}</div>
      <h1>{title}</h1>
      <p>{subtitle}</p>
    </section>
    """, unsafe_allow_html=True)

def chart_title(title, subtitle):
    st.markdown(f'<div class="chart-heading">{title}</div><div class="chart-sub">{subtitle}</div>', unsafe_allow_html=True)

def metric_card(col, icon, tag, label, value, foot):
    with col:
        st.markdown(f"""
        <div class="metric">
          <div class="metric-top"><div class="metric-icon">{icon}</div><div class="metric-tag">{tag}</div></div>
          <div class="metric-label">{label}</div>
          <div class="metric-value">{value}</div>
          <div class="metric-foot">{foot}</div>
        </div>""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------
with st.sidebar:
    st.markdown('<div style="padding:8px 4px 18px"><div class="brand">◈ ChurnIQ <span>AI</span></div><div class="brand-sub">CUSTOMER INTELLIGENCE</div></div>', unsafe_allow_html=True)
    st.divider()
    st.markdown('<div class="sidebar-caption">WORKSPACE</div>', unsafe_allow_html=True)
    page = st.radio(
        "Navigation",
        ["Overview", "Predict Churn", "Retention Insights", "Model Analytics", "About Project"],
        label_visibility="collapsed",
    )
    st.divider()
    st.markdown('<div class="sidebar-caption">MODEL STATUS</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="padding:13px;border:1px solid #2D4965;background:#142640;border-radius:12px">
      <div style="color:#55DDB0;font-size:11px;font-weight:800">● MODEL ONLINE</div>
      <div style="color:#E4ECF7;font-size:12px;margin-top:8px">Logistic Regression</div>
      <div style="color:#8FA4C0;font-size:10px;margin-top:3px">IBM Telco Customer Dataset</div>
    </div>""", unsafe_allow_html=True)
    st.markdown('<div style="margin-top:30px;color:#7185A2;font-size:9px;letter-spacing:1px">CHURNIQ AI · VERSION 3.0</div>', unsafe_allow_html=True)

# ------------------------------------------------------------
# Overview
# ------------------------------------------------------------
if page == "Overview":
    header("CHURNIQ / CUSTOMER ANALYTICS", "Know your customers. Reduce churn.", "A clear view of customer retention, churn patterns and the factors that influence customer decisions.")

    st.markdown('<div class="section-label">BUSINESS SNAPSHOT</div>', unsafe_allow_html=True)
    cols = st.columns(4, gap="medium")
    metric_card(cols[0], "👥", "CUSTOMER BASE", "Total customers", f"{total:,}", "Records in the dataset")
    metric_card(cols[1], "↗", "AT-RISK / LOST", "Customers churned", f"{churned:,}", "Customers who discontinued")
    metric_card(cols[2], "✦", "RETAINED", "Customers retained", f"{retained:,}", "Customers still subscribed")
    metric_card(cols[3], "％", "CHURN INDICATOR", "Churn rate", f"{churn_rate:.2f}%", "Share of customers lost")

    st.markdown('<div class="section-label">CHURN & RETENTION PATTERNS</div>', unsafe_allow_html=True)
    left, right = st.columns([0.92, 1.08], gap="large")
    with left:
        with st.container(border=True):
            chart_title("Customer mix", "How the customer base is split between retained and churned")
            pie = go.Figure(go.Pie(
                labels=["Retained", "Churned"], values=[retained, churned], hole=.72,
                marker={"colors":[BLUE, RED],"line":{"color":PANEL,"width":4}},
                textinfo="percent", textfont={"color":"white","size":13},
                hovertemplate="%{label}: %{value:,}<br>%{percent}<extra></extra>",
            ))
            pie.add_annotation(text=f"<b>{total:,}</b><br><span style='font-size:10px'>CUSTOMERS</span>", x=.5,y=.5,showarrow=False,font={"size":22,"color":"white"})
            pie.update_layout(showlegend=True, legend={"orientation":"h","y":-.08}, margin={"l":5,"r":5,"t":10,"b":5}, height=300, paper_bgcolor="rgba(0,0,0,0)", font={"color":MUTED})
            st.plotly_chart(pie, use_container_width=True, config=PLOT_CONFIG)
    with right:
        with st.container(border=True):
            chart_title("Churn by contract", "Percentage of customers who left within each contract group")
            contract = df.groupby("Contract", dropna=False)["Churn"].apply(lambda x: x.eq("Yes").mean()*100).sort_values().reset_index(name="Churn rate")
            bar = px.bar(contract, x="Churn rate", y="Contract", orientation="h", text=contract["Churn rate"].map(lambda x:f"{x:.1f}%"), color="Churn rate", color_continuous_scale=[BLUE,PURPLE,RED])
            bar.update_traces(textposition="outside", cliponaxis=False, marker_line_width=0)
            bar.update_layout(showlegend=False,coloraxis_showscale=False,xaxis_title="Churn rate (%)",yaxis_title="",height=300)
            st.plotly_chart(polish(bar,300), use_container_width=True, config=PLOT_CONFIG)

    left, right = st.columns(2, gap="large")
    with left:
        with st.container(border=True):
            chart_title("Churn across customer lifecycle", "Churn rate by customer tenure")
            tenure_df = df.dropna(subset=["tenure"]).copy()
            tenure_df["Tenure group"] = pd.cut(tenure_df["tenure"], bins=[-1,12,24,48,72], labels=["0–12 months","13–24 months","25–48 months","49–72 months"])
            tenure = tenure_df.groupby("Tenure group", observed=False)["Churn"].apply(lambda x:x.eq("Yes").mean()*100).reset_index(name="Churn rate")
            line = px.line(tenure,x="Tenure group",y="Churn rate",markers=True)
            line.update_traces(line={"color":CYAN,"width":3},marker={"size":9,"color":CYAN},fill="tozeroy",fillcolor="rgba(84,214,232,.10)",hovertemplate="%{x}<br>Churn: %{y:.2f}%<extra></extra>")
            line.update_layout(xaxis_title="Customer tenure",yaxis_title="Churn rate (%)",showlegend=False)
            st.plotly_chart(polish(line,290),use_container_width=True,config=PLOT_CONFIG)
    with right:
        with st.container(border=True):
            chart_title("Churn by internet service", "Churn rate across internet service categories")
            internet = df.groupby("InternetService",dropna=False)["Churn"].apply(lambda x:x.eq("Yes").mean()*100).reset_index(name="Churn rate").sort_values("Churn rate")
            internet_fig = px.bar(internet,x="InternetService",y="Churn rate",color="InternetService",text=internet["Churn rate"].map(lambda x:f"{x:.1f}%"),color_discrete_sequence=[CYAN,PURPLE,BLUE])
            internet_fig.update_traces(textposition="outside",cliponaxis=False)
            internet_fig.update_layout(showlegend=False,xaxis_title="Internet service",yaxis_title="Churn rate (%)")
            st.plotly_chart(polish(internet_fig,290),use_container_width=True,config=PLOT_CONFIG)

    left, right = st.columns([1,1],gap="large")
    with left:
        with st.container(border=True):
            chart_title("Monthly charges by status", "Average monthly bill for retained and churned customers")
            billing = df.groupby("Churn")["MonthlyCharges"].mean().reindex(["No","Yes"]).rename(index={"No":"Retained","Yes":"Churned"}).rename_axis("Customer status").reset_index(name="Average monthly charges")
            bill_fig = px.bar(billing,x="Customer status",y="Average monthly charges",color="Customer status",text=billing["Average monthly charges"].map(lambda x:f"${x:.2f}"),color_discrete_map={"Retained":BLUE,"Churned":RED})
            bill_fig.update_traces(textposition="outside",cliponaxis=False)
            bill_fig.update_layout(showlegend=False,yaxis_title="Average monthly charges ($)")
            st.plotly_chart(polish(bill_fig,280),use_container_width=True,config=PLOT_CONFIG)
    with right:
        with st.container(border=True):
            chart_title("Quick read", "Signals worth investigating in retention planning")
            month_rate = df.loc[df["Contract"].eq("Month-to-month"),"Churn"].eq("Yes").mean()*100
            fiber_rate = df.loc[df["InternetService"].eq("Fiber optic"),"Churn"].eq("Yes").mean()*100
            early_rate = df.loc[df["tenure"].le(12),"Churn"].eq("Yes").mean()*100
            st.markdown(f"""
            <div class="insight" style="margin:8px 0 10px"><div class="insight-label">MONTH-TO-MONTH CHURN</div><div class="insight-value">{month_rate:.1f}%</div><div class="insight-note">Highest contract-related churn signal</div></div>
            <div class="insight" style="margin:0 0 10px"><div class="insight-label">FIBER OPTIC CHURN</div><div class="insight-value">{fiber_rate:.1f}%</div><div class="insight-note">Churn rate among fiber optic customers</div></div>
            <div class="insight"><div class="insight-label">FIRST-YEAR CHURN</div><div class="insight-value">{early_rate:.1f}%</div><div class="insight-note">Churn rate among customers with 12 months or less tenure</div></div>
            """,unsafe_allow_html=True)

# ------------------------------------------------------------
# Predict churn
# ------------------------------------------------------------
elif page == "Predict Churn":
    header("MACHINE LEARNING / PREDICTION", "Customer risk analyzer", "Enter a customer profile to estimate churn probability and review a suggested retention response.")
    with st.form("prediction_form"):
        st.markdown("#### 01 · Customer profile")
        a,b,c,d = st.columns(4)
        gender = a.selectbox("Gender",["Male","Female"])
        senior_choice = b.selectbox("Senior citizen",["No","Yes"])
        partner = c.selectbox("Partner",["Yes","No"])
        dependents = d.selectbox("Dependents",["Yes","No"])
        st.divider()
        st.markdown("#### 02 · Subscription")
        a,b,c,d = st.columns(4)
        tenure = a.slider("Tenure (months)",0,72,12)
        contract = b.selectbox("Contract",["Month-to-month","One year","Two year"])
        phone = c.selectbox("Phone service",["Yes","No"])
        multiple = d.selectbox("Multiple lines",["No","Yes","No phone service"])
        st.divider()
        st.markdown("#### 03 · Internet services")
        a,b,c = st.columns(3)
        internet = a.selectbox("Internet service",["DSL","Fiber optic","No"])
        security = b.selectbox("Online security",["Yes","No","No internet service"])
        backup = c.selectbox("Online backup",["Yes","No","No internet service"])
        a,b,c = st.columns(3)
        protection = a.selectbox("Device protection",["Yes","No","No internet service"])
        support = b.selectbox("Tech support",["Yes","No","No internet service"])
        tv = c.selectbox("Streaming TV",["Yes","No","No internet service"])
        movies = st.selectbox("Streaming movies",["Yes","No","No internet service"])
        st.divider()
        st.markdown("#### 04 · Billing")
        a,b,c,d = st.columns(4)
        paperless = a.selectbox("Paperless billing",["Yes","No"])
        payment = b.selectbox("Payment method",["Electronic check","Mailed check","Bank transfer (automatic)","Credit card (automatic)"])
        monthly = c.number_input("Monthly charges ($)",min_value=0.0,value=70.0,step=1.0)
        total_charges = d.number_input("Total charges ($)",min_value=0.0,value=float(monthly*max(tenure,1)),step=10.0)
        submitted = st.form_submit_button("◈  ANALYZE CUSTOMER RISK",use_container_width=True)

    if submitted:
        customer = pd.DataFrame([{
            "gender":gender,"SeniorCitizen":1 if senior_choice=="Yes" else 0,"Partner":partner,"Dependents":dependents,
            "tenure":tenure,"PhoneService":phone,"MultipleLines":multiple,"InternetService":internet,
            "OnlineSecurity":security,"OnlineBackup":backup,"DeviceProtection":protection,"TechSupport":support,
            "StreamingTV":tv,"StreamingMovies":movies,"Contract":contract,"PaperlessBilling":paperless,
            "PaymentMethod":payment,"MonthlyCharges":monthly,"TotalCharges":total_charges,
        }])
        probability = float(model.predict_proba(customer)[0][1])
        prediction = int(model.predict(customer)[0])
        st.markdown('<div class="section-label">PREDICTION REPORT</div>',unsafe_allow_html=True)
        left,right = st.columns([1,1],gap="large")
        with left:
            with st.container(border=True):
                gauge = go.Figure(go.Indicator(mode="gauge+number",value=probability*100,number={"suffix":"%","font":{"size":38,"color":"white"}},title={"text":"ESTIMATED CHURN PROBABILITY","font":{"size":12,"color":MUTED}},gauge={"axis":{"range":[0,100],"tickcolor":MUTED},"bar":{"color":PURPLE},"bgcolor":PANEL_2,"bordercolor":BORDER,"steps":[{"range":[0,30],"color":"#17463F"},{"range":[30,60],"color":"#55452D"},{"range":[60,100],"color":"#542C43"}]}))
                gauge.update_layout(height=300,paper_bgcolor="rgba(0,0,0,0)",font={"color":MUTED},margin={"l":20,"r":20,"t":45,"b":10})
                st.plotly_chart(gauge,use_container_width=True,config=PLOT_CONFIG)
        with right:
            with st.container(border=True):
                if prediction == 1:
                    st.error("### Higher predicted churn risk")
                    st.markdown("**Suggested retention actions**\n\n- Contact the customer proactively.\n- Review service concerns and billing friction.\n- Consider a relevant loyalty offer.\n- Explain the benefits of a longer-term plan.")
                else:
                    st.success("### Lower predicted churn risk")
                    st.markdown("**Suggested customer actions**\n\n- Maintain regular engagement.\n- Monitor customer satisfaction.\n- Recommend relevant service upgrades.\n- Recognize and reward continued loyalty.")
                st.caption("The model estimate is a decision-support signal, not a guarantee of future behavior.")
        st.markdown("#### Customer summary")
        a,b,c,d = st.columns(4)
        a.metric("Tenure",f"{tenure} months")
        b.metric("Contract",contract)
        c.metric("Monthly charges",f"${monthly:,.2f}")
        d.metric("Internet service",internet)

# ------------------------------------------------------------
# Retention insights
# ------------------------------------------------------------
elif page == "Retention Insights":
    header("BUSINESS INTELLIGENCE / ACTIONS","Retention strategy center","Translate observed churn patterns into practical customer retention priorities.")
    contract_rate = df.groupby("Contract")["Churn"].apply(lambda x:x.eq("Yes").mean()*100)
    internet_rate = df.groupby("InternetService")["Churn"].apply(lambda x:x.eq("Yes").mean()*100)
    first_year = df.loc[df["tenure"].le(12),"Churn"].eq("Yes").mean()*100
    churned_bill = df.loc[df["Churn"].eq("Yes"),"MonthlyCharges"].mean()
    a,b,c,d = st.columns(4)
    a.metric("Month-to-month churn",f"{contract_rate.get('Month-to-month',0):.2f}%")
    b.metric("First-year churn",f"{first_year:.2f}%")
    c.metric("Fiber optic churn",f"{internet_rate.get('Fiber optic',0):.2f}%")
    d.metric("Avg. churned monthly bill",f"${churned_bill:.2f}")
    st.markdown('<div class="section-label">RETENTION PLAYBOOK</div>',unsafe_allow_html=True)
    playbook = pd.DataFrame([
        ["New customers (0–12 months)","Strengthen onboarding, check in early and resolve setup issues quickly."],
        ["Month-to-month contracts","Test annual-plan incentives and communicate the value of longer commitments."],
        ["Fiber optic customers","Investigate service quality, support experience and price satisfaction."],
        ["Customers with high monthly bills","Review plan fit and offer relevant lower-cost alternatives."],
        ["Customers without technical support","Promote support options and make help easy to access."],
    ],columns=["Customer segment","Recommended action"])
    st.dataframe(playbook,use_container_width=True,hide_index=True)
    st.info("Prioritize interventions using customer-level context. These patterns show association, not proof that a single factor causes churn.")

# ------------------------------------------------------------
# Model analytics
# ------------------------------------------------------------
elif page == "Model Analytics":
    header("MACHINE LEARNING / MODEL QUALITY","Model analytics","Review the model evaluation results and the customer attributes that carry predictive signal.")
    comparison = get_comparison()
    if not comparison.empty:
        st.markdown("#### Model comparison")
        st.dataframe(comparison,use_container_width=True,hide_index=True)
    else:
        st.warning("model_comparison.csv was not found beside app.py.")
    importance = get_importance()
    if not importance.empty and len(importance.columns)>=2:
        st.markdown('<div class="section-label">FEATURE IMPORTANCE</div>',unsafe_allow_html=True)
        fcol,vcol = importance.columns[:2]
        importance = importance.sort_values(vcol,ascending=True)
        fig = px.bar(importance,x=vcol,y=fcol,orientation="h",color=vcol,color_continuous_scale=[BLUE,PURPLE])
        fig.update_layout(showlegend=False,coloraxis_showscale=False,xaxis_title="Permutation importance",yaxis_title="")
        with st.container(border=True):
            st.plotly_chart(polish(fig,max(360,28*len(importance))),use_container_width=True,config=PLOT_CONFIG)
    else:
        st.warning("feature_importance.csv is missing or does not contain two columns.")
    st.markdown('<div class="section-label">SELECTED MODEL · LOGISTIC REGRESSION</div>',unsafe_allow_html=True)
    a,b,c,d,e = st.columns(5)
    a.metric("Accuracy","73.81%")
    b.metric("Precision","50.43%")
    c.metric("Recall","78.34%")
    d.metric("F1-score","61.36%")
    e.metric("ROC-AUC","84.13%")
    st.caption("Metrics are from the held-out test set. Recall is emphasized to help identify more customers who may churn.")

# ------------------------------------------------------------
# About
# ------------------------------------------------------------
elif page == "About Project":
    header("PROJECT / OVERVIEW","About ChurnIQ AI","A machine-learning application for customer churn prediction and retention analytics.")
    a,b,c = st.columns(3)
    a.metric("Dataset records","7,043")
    b.metric("Original columns","21")
    c.metric("Selected model","Logistic Regression")
    with st.container(border=True):
        st.markdown("""
        ### Project objective
        Identify customers who may discontinue a subscription service and surface patterns that can inform retention planning.

        ### Dataset
        - IBM Telco Customer Churn dataset
        - 7,043 customer records
        - 21 original columns
        - Binary churn classification

        ### Machine-learning workflow
        - Data cleaning and preprocessing
        - Logistic Regression and Random Forest comparison
        - Evaluation using accuracy, precision, recall, F1-score and ROC-AUC
        - Logistic Regression selected based on F1-score and recall

        ### Technology
        Python · Pandas · NumPy · Scikit-learn · Plotly · Streamlit · Joblib

        ### Future enhancements
        Customer segmentation, explainable AI, downloadable prediction reports, customer lifetime value analysis and live business data integration.
        """)
st.markdown('<div style="text-align:center;color:#7185A2;font-size:9px;letter-spacing:1.2px;padding:24px 0 4px;border-top:1px solid #263650;margin-top:30px">◈ CHURNIQ AI  ·  CUSTOMER INTELLIGENCE PLATFORM  ·  POWERED BY MACHINE LEARNING</div>',unsafe_allow_html=True)
