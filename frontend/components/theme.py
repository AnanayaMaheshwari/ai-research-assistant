import streamlit as st


def apply_theme():
    st.markdown(
        """
        <style>
        .stApp {
            background: #0b1020;
            color: #e5e7eb;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        [data-testid="stSidebar"] {
            background: #10172a;
            border-right: 1px solid #202b42;
        }

        .page-eyebrow {
            color: #818cf8;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 2px;
            margin-bottom: 10px;
        }

        .page-title {
            color: #f8fafc;
            font-size: 36px;
            font-weight: 750;
            line-height: 1.2;
            margin: 0;
        }

        .page-description {
            color: #94a3b8;
            font-size: 14px;
            line-height: 1.7;
            margin-top: 10px;
            margin-bottom: 25px;
        }

        .hero-card {
            background: linear-gradient(120deg, #182447, #252052, #241b40);
            border: 1px solid #35345f;
            border-radius: 18px;
            padding: 28px;
            margin: 12px 0 25px 0;
        }

        .hero-tag {
            display: inline-block;
            background: #34336a;
            color: #c4b5fd;
            border-radius: 20px;
            padding: 6px 12px;
            font-size: 11px;
            font-weight: 600;
            margin-bottom: 15px;
        }

        .hero-heading {
            color: #f8fafc;
            font-size: 27px;
            font-weight: 750;
            line-height: 1.3;
            margin-bottom: 8px;
        }

        .hero-text {
            color: #cbd5e1;
            font-size: 14px;
            line-height: 1.7;
        }

        .section-heading {
            color: #f1f5f9;
            font-size: 20px;
            font-weight: 700;
            margin: 25px 0 14px 0;
        }

        .feature-card {
            background: #121b30;
            border: 1px solid #25324a;
            border-radius: 14px;
            padding: 19px;
            min-height: 125px;
        }

        .feature-icon {
            font-size: 24px;
            margin-bottom: 10px;
        }

        .feature-title {
            color: #f1f5f9;
            font-size: 15px;
            font-weight: 650;
            margin-bottom: 6px;
        }

        .feature-description {
            color: #94a3b8;
            font-size: 12px;
            line-height: 1.6;
        }

        .info-panel {
            background: #121b30;
            border: 1px solid #25324a;
            border-radius: 14px;
            padding: 18px;
            margin-bottom: 12px;
        }

        .muted-text {
            color: #94a3b8;
            font-size: 13px;
        }

        [data-testid="stMetric"] {
            background: #121b30;
            border: 1px solid #25324a;
            padding: 16px;
            border-radius: 12px;
        }

        [data-testid="stMetricLabel"] {
            color: #94a3b8;
        }

        [data-testid="stMetricValue"] {
            color: #f8fafc;
        }

        [data-testid="stChatMessage"] {
            background: #121b30;
            border: 1px solid #25324a;
            border-radius: 14px;
            padding: 14px;
            margin-bottom: 12px;
        }

        div[data-testid="stTextArea"] textarea,
        div[data-testid="stTextInput"] input {
            background: #121b30;
            color: #f8fafc;
            border: 1px solid #303d59;
            border-radius: 10px;
        }

        .stButton > button,
        .stDownloadButton > button,
        .stLinkButton > a {
            border-radius: 9px;
            font-weight: 600;
            min-height: 42px;
        }

        div[data-testid="stSelectbox"] > div > div {
            background: #121b30;
        }

        hr {
            border-color: #25324a;
        }

        h1, h2, h3, h4 {
            color: #f8fafc !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(eyebrow, title, description):
    st.markdown(
        f"""
        <div class="page-eyebrow">{eyebrow}</div>
        <div class="page-title">{title}</div>
        <div class="page-description">{description}</div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title):
    st.markdown(
        f'<div class="section-heading">{title}</div>',
        unsafe_allow_html=True,
    )


def hero_card(tag, title, description):
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-tag">{tag}</div>
            <div class="hero-heading">{title}</div>
            <div class="hero-text">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )