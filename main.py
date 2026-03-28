# =========================
# 📦 Imports
# =========================
import streamlit as st
import yfinance as yf


# =========================
# 🎯 Titel
# =========================
st.title("📈 Stock Analyzer")


# =========================
# ⌨️ Eingabe
# =========================
symbol = st.text_input("Welche Aktie? (z. B. AAPL oder BRK-B)")


# =========================
# 🔑 Hauptlogik
# =========================
if symbol:
    symbol = symbol.upper().replace("-", ".")

    ticker = yf.Ticker(symbol)

    # =========================
    # 📊 Kursdaten (Chart)
    # =========================
    hist = ticker.history(period="1y")

    if hist.empty:
        st.error("❌ Keine Kursdaten gefunden")
        st.stop()

    st.write("### 📊 Kursverlauf (1 Jahr)")
    st.line_chart(hist["Close"])


    # =========================
    # 📊 Finanzdaten laden
    # =========================
    financials = ticker.financials


    # =========================
    # 📈 Wachstum berechnen
    # =========================
    growth = None
    revenue_series = None

    try:
        revenue_series = financials.loc["Total Revenue"]

        if len(revenue_series) >= 2:
            latest = revenue_series.iloc[0]
            previous = revenue_series.iloc[1]

            growth = (latest - previous) / previous
    except:
        growth = None


    # =========================
    # 💰 Marge berechnen
    # =========================
    margin = None
    profit = None
    revenue = None

    try:
        profit = financials.loc["Net Income"].iloc[0]
        revenue = financials.loc["Total Revenue"].iloc[0]

        margin = profit / revenue
    except:
        margin = None


    # =========================
    # 📊 Zusatzdaten
    # =========================
    try:
        info = ticker.info
    except:
        info = {}

    pe = info.get("trailingPE") if info else None
    roe = info.get("returnOnEquity") if info else None
    debt = info.get("debtToEquity") if info else None


    # =========================
    # 📊 Kennzahlen anzeigen
    # =========================
    st.write("### 📊 Kennzahlen")

    st.write(f"KGV (PE): {round(pe, 2) if pe else 'Nicht verfügbar'}")
    st.write(f"Wachstum: {round(growth * 100, 2) if growth else 'Nicht verfügbar'} %")
    st.write(f"Profit-Marge: {round(margin * 100, 2) if margin else 'Nicht verfügbar'} %")
    st.write(f"ROE: {round(roe * 100, 2) if roe else 'Nicht verfügbar'} %")
    st.write(f"Verschuldung: {round(debt, 2) if debt else 'Nicht verfügbar'}")


    # =========================
    # 🧠 Bewertungssystem
    # =========================
    st.write("### 📊 Investment Empfehlung")

    score = 0

    if pe and pe < 25:
        score += 1
    if growth and growth > 0.05:
        score += 1
    if margin and margin > 0.15:
        score += 1
    if roe and roe > 0.15:
        score += 1
    if debt and debt < 100:
        score += 1

    st.write(f"Score: {score}/5")

    if score >= 4:
        st.success("🟢 Kaufen – starke Fundamentaldaten")
    elif score == 3:
        st.info("🟡 Halten – solide Aktie")
    elif score == 2:
        st.warning("⚪ Neutral – gemischt")
    else:
        st.error("🔴 Verkaufen – schwach")


    # =========================
    # 🧠 Analyse
    # =========================
    st.write("### 🧠 Analyse")

    analysis = []

    if pe:
        if pe < 20:
            analysis.append("Die Aktie ist günstig bewertet.")
        elif pe > 30:
            analysis.append("Die Aktie ist eher teuer.")

    if growth:
        if growth > 0.1:
            analysis.append("Das Unternehmen wächst stark.")
        elif growth < 0.03:
            analysis.append("Das Wachstum ist schwach.")

    if margin:
        if margin > 0.2:
            analysis.append("Sehr profitables Unternehmen.")
        elif margin < 0.1:
            analysis.append("Niedrige Profitabilität.")

    if roe:
        if roe > 0.15:
            analysis.append("Effiziente Kapitalnutzung.")

    if debt:
        if debt > 150:
            analysis.append("Hohe Verschuldung.")
        elif debt < 50:
            analysis.append("Geringe Verschuldung.")

    if len(analysis) == 0:
        st.write("Keine ausreichende Analyse möglich.")
    else:
        for point in analysis:
            st.write("• " + point)


    # =========================
    # 📊 Berechnung anzeigen
    # =========================
    st.write("---")
    st.write("## 📊 Berechnung im Detail")

    with st.expander("📈 Wachstum berechnen"):
        try:
            latest = revenue_series.iloc[0]
            previous = revenue_series.iloc[1]

            st.write(f"Letzter Umsatz: {latest}")
            st.write(f"Vorheriger Umsatz: {previous}")
            st.code("(latest - previous) / previous")

            calc_growth = (latest - previous) / previous
            st.write(f"Ergebnis: {round(calc_growth * 100, 2)} %")
        except:
            st.write("Keine Daten verfügbar")

    with st.expander("💰 Marge berechnen"):
        try:
            st.write(f"Gewinn: {profit}")
            st.write(f"Umsatz: {revenue}")
            st.code("profit / revenue")

            calc_margin = profit / revenue
            st.write(f"Ergebnis: {round(calc_margin * 100, 2)} %")
        except:
            st.write("Keine Daten verfügbar")


    # =========================
    # 📚 Erklärung
    # =========================
    st.write("---")
    st.write("## 📚 Erklärung der Kennzahlen")

    with st.expander("📊 KGV"):
        st.write("Preis im Verhältnis zum Gewinn.")

    with st.expander("📈 Wachstum"):
        st.write("Wie stark der Umsatz steigt.")

    with st.expander("💰 Marge"):
        st.write("Wie viel Gewinn gemacht wird.")

    with st.expander("🏆 ROE"):
        st.write("Effizienz des Unternehmens.")

    with st.expander("⚖️ Verschuldung"):
        st.write("Wie viele Schulden vorhanden sind.")