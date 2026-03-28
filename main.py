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
    # Formatieren (BRK-B → BRK.B)
    symbol = symbol.upper().replace("-", ".")

    # =========================
    # 📊 Daten laden
    # =========================
    ticker = yf.Ticker(symbol)

    # Kursdaten (zuverlässig)
    hist = ticker.history(period="1y")

    if hist.empty:
        st.error("❌ Keine Kursdaten gefunden – prüfe das Symbol")
        st.stop()

    # Zusatzdaten (kann manchmal fehlschlagen)
    try:
        info = ticker.info
    except:
        info = {}
        st.warning("⚠️ Einige Daten konnten nicht geladen werden")


    # =========================
    # 📈 Kennzahlen holen
    # =========================
    pe = info.get("trailingPE") if info else None
    growth = info.get("revenueGrowth") if info else 0
    margin = info.get("profitMargins") if info else 0
    roe = info.get("returnOnEquity") if info else 0
    debt = info.get("debtToEquity") if info else 0


    # =========================
    # 📊 Chart anzeigen
    # =========================
    st.write("### 📊 Kursverlauf (1 Jahr)")
    st.line_chart(hist["Close"])


    # =========================
    # 📊 Kennzahlen anzeigen
    # =========================
    st.write("### 📊 Kennzahlen")

    st.write(f"KGV (PE): {round(pe, 2) if pe else 'N/A'}")
    st.write(f"Wachstum: {round(growth * 100, 2)} %")
    st.write(f"Profit-Marge: {round(margin * 100, 2)} %")
    st.write(f"ROE: {round(roe * 100, 2)} %")
    st.write(f"Verschuldung: {round(debt, 2) if debt else 'N/A'}")


    # =========================
    # 🧠 Bewertungssystem
    # =========================
    st.write("### 📊 Investment Empfehlung")

    score = 0

    # Bewertung
    if pe and pe < 25:
        score += 1

    # Wachstum
    if growth and growth > 0.05:
        score += 1

    # Profitabilität
    if margin and margin > 0.15:
        score += 1

    # Effizienz
    if roe and roe > 0.15:
        score += 1

    # Risiko
    if debt and debt < 100:
        score += 1

    st.write(f"Score: {score}/5")


    # Ergebnis
    if score >= 4:
        st.success("🟢 Kaufen – starke Fundamentaldaten")
    elif score == 3:
        st.info("🟡 Halten – solide Aktie")
    elif score == 2:
        st.warning("⚪ Neutral – gemischte Signale")
    else:
        st.error("🔴 Verkaufen – schwache Kennzahlen")


    # =========================
    # 🧠 Intelligente Analyse
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
            analysis.append("Das Unternehmen wächst sehr stark.")
        elif growth < 0.03:
            analysis.append("Das Wachstum ist eher schwach.")

    if margin:
        if margin > 0.2:
            analysis.append("Das Unternehmen ist sehr profitabel.")
        elif margin < 0.1:
            analysis.append("Die Profitabilität ist niedrig.")

    if roe:
        if roe > 0.15:
            analysis.append("Das Unternehmen arbeitet effizient.")

    if debt:
        if debt > 150:
            analysis.append("Das Unternehmen ist stark verschuldet.")
        elif debt < 50:
            analysis.append("Die Verschuldung ist gering.")

    if len(analysis) == 0:
        st.write("Keine ausreichende Analyse möglich.")
    else:
        for point in analysis:
            st.write("• " + point)


    # =========================
    # 📚 Erklärung (für Anfänger)
    # =========================
    st.write("---")
    st.write("## 📚 Erklärung der Kennzahlen")

    with st.expander("📊 KGV (PE)"):
        st.write("Wie teuer eine Aktie ist im Verhältnis zum Gewinn.")

    with st.expander("📈 Wachstum"):
        st.write("Wie schnell das Unternehmen wächst.")

    with st.expander("💰 Marge"):
        st.write("Wie viel Gewinn ein Unternehmen macht.")

    with st.expander("🏆 ROE"):
        st.write("Wie effizient das Unternehmen arbeitet.")

    with st.expander("⚖️ Verschuldung"):
        st.write("Wie viel Schulden das Unternehmen hat.")