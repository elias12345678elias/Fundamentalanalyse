import streamlit as st
import yfinance as yf

def get_fundamental_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    
    data = {
        "Selskap": info.get("longName", "N/A"),
        "Markedsverdi": f"{info.get('marketCap', 'N/A'):,}" if info.get('marketCap') else "N/A",
        "P/E-forhold": info.get("trailingPE", "N/A"),
        "EPS (Inntjening per aksje)": info.get("trailingEps", "N/A"),
        "Gjeldsgrad (Debt-to-Equity)": info.get("debtToEquity", "N/A"),
        "ROE (Return on Equity)": info.get("returnOnEquity", "N/A"),
        "Inntektsvekst": info.get("revenueGrowth", "N/A")
    }
    return data

def evaluate_stock(data):
    pe = data.get("P/E-forhold")
    roe = data.get("ROE (Return on Equity)")
    debt = data.get("Gjeldsgrad (Debt-to-Equity)")
    growth = data.get("Inntektsvekst")
    
    rating = "Nøytral"
    
    if pe != "N/A" and pe < 20 and roe != "N/A" and roe > 15 and debt != "N/A" and debt < 1.5:
        rating = "Sterk Kjøp"
    elif pe != "N/A" and pe > 30:
        rating = "Overpriset"
    elif growth != "N/A" and growth < 0:
        rating = "Risiko – Inntektsnedgang"
    
    return rating

# Streamlit UI
st.set_page_config(page_title="Fundamental Analyse", layout="centered")
st.title("📈 Fundamental Analyse Bot")

ticker = st.text_input("Skriv inn aksjesymbol (f.eks. AAPL for Apple):")

if ticker:
    try:
        data = get_fundamental_data(ticker)
        rating = evaluate_stock(data)
        
        st.subheader("📊 Analyse av aksjen:")
        st.json(data)
        
        st.subheader("📈 Vurdering:")
        st.success(f"Denne aksjen vurderes som: {rating}")
    except Exception as e:
        st.error(f"Noe gikk galt: {e}")

st.markdown("---")
st.caption("Laget med ❤️ av din personlige AI-assistent")
