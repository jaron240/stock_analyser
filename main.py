# =========================
# 📦 Imports
# =========================
import streamlit as st          # macht die Web-App
import yfinance as yf          # holt Finanzdaten


# =========================
# 🎯 Titel
# =========================
st.title("📈 Stock Analyzer (Advanced)")


# =========================
# ⌨️ Eingabe
# =========================
symbol = st.text_input("Welche Aktie? (z. B. AAPL oder BRK-B)")


# =========================
# 🔑 Hauptlogik
# =========================
if symbol:
    # Format fix → BRK-B wird zu BRK.B
    symbol = symbol.upper().replace("-", ".")

    # Aktie laden
    ticker = yf.Ticker(symbol)


    # =========================
    # 📊 Kursdaten (Chart)
    # =========================
    hist = ticker.history(period="1y")

    # Wenn keine Daten → abbrechen
    if hist.empty:
        st.error("❌ Keine Kursdaten gefunden")
        st.stop()

    st.write("### 📊 Kursverlauf (1 Jahr)")
    st.line_chart(hist["Close"])   # zeigt Kursverlauf


    # =========================
    # 📊 Finanzdaten laden
    # =========================
    financials = ticker.financials       # Gewinn & Umsatz
    balance = ticker.balance_sheet       # Schulden & Eigenkapital


    # =========================
    # 📈 Wachstum berechnen
    # =========================
    growth = None
    try:
        revenue_series = financials.loc["Total Revenue"]

        # wir brauchen mindestens 2 Jahre
        if len(revenue_series) >= 2:
            latest = revenue_series.iloc[0]    # aktueller Umsatz
            previous = revenue_series.iloc[1]  # Umsatz letztes Jahr

            # Formel:
            # Wachstum = (neu - alt) / alt
            growth = (latest - previous) / previous
    except:
        growth = None


    # =========================
    # 💰 Marge berechnen
    # =========================
    margin = None
    try:
        profit = financials.loc["Net Income"].iloc[0]      # Gewinn
        revenue = financials.loc["Total Revenue"].iloc[0]  # Umsatz

        # Formel:
        # Marge = Gewinn / Umsatz
        margin = profit / revenue
    except:
        margin = None


    # =========================
    # 📊 KGV (PE) berechnen
    # =========================
    pe = None
    try:
        price = hist["Close"].iloc[-1]   # aktueller Aktienpreis
        net_income = financials.loc["Net Income"].iloc[0]

        # Anzahl Aktien (wichtig für Gewinn pro Aktie)
        shares = ticker.info.get("sharesOutstanding")

        if shares and net_income:
            # Gewinn pro Aktie (EPS)
            eps = net_income / shares

            # Formel:
            # KGV = Preis / Gewinn pro Aktie
            pe = price / eps
    except:
        pe = None


    # =========================
    # 🏆 ROE berechnen
    # =========================
    roe = None
    try:
        equity = balance.loc["Total Stockholder Equity"].iloc[0]  # Eigenkapital
        net_income = financials.loc["Net Income"].iloc[0]         # Gewinn

        # Formel:
        # ROE = Gewinn / Eigenkapital
        roe = net_income / equity
    except:
        roe = None


    # =========================
    # ⚖️ Verschuldung berechnen
    # =========================
    debt = None
    try:
        total_debt = balance.loc["Total Debt"].iloc[0]             # Schulden
        equity = balance.loc["Total Stockholder Equity"].iloc[0]   # Eigenkapital

        # Formel:
        # Verschuldung = Schulden / Eigenkapital
        debt = total_debt / equity
    except:
        debt = None


    # =========================
    # 📊 Kennzahlen anzeigen
    # =========================
    st.write("### 📊 Kennzahlen")

    st.write(f"KGV: {round(pe,2) if pe else 'N/A'}")
    st.write(f"Wachstum: {round(growth*100,2) if growth else 'N/A'} %")
    st.write(f"Marge: {round(margin*100,2) if margin else 'N/A'} %")
    st.write(f"ROE: {round(roe*100,2) if roe else 'N/A'} %")
    st.write(f"Verschuldung: {round(debt,2) if debt else 'N/A'}")