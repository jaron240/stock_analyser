import streamlit as st
import yfinance as yf

st.title("📈 Stock Analyzer")

symbol = st.text_input("Welche Aktie? (z. B. AAPL oder BRK-B)")

if symbol:
    # Fix für BRK-B → BRK.B
    symbol = symbol.upper().replace("-", ".")

    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        debt = info.get("debtToEquity", None)
        roe = info.get("returnOnEquity", None)



        pe = info.get("trailingPE", None)
        growth = info.get("revenueGrowth", 0)
        margin = info.get("profitMargins", 0)

        # 📊 Chart
        st.write("### Kursverlauf (1 Jahr)")
        hist = ticker.history(period="1y")

        if hist.empty:
            st.error("Keine Kursdaten gefunden")
        else:
            st.line_chart(hist["Close"])

        # 📊 Kennzahlen
        st.write("### Kennzahlen")
        st.write(f"KGV (PE): {round(pe, 2) if pe else 'N/A'}")
        st.write(f"Wachstum: {round(growth*100, 2)} %")
        st.write(f"Profit-Marge: {round(margin*100, 2)} %")
        st.write(f"ROE: {round(roe*100,2) if roe else 'N/A'} %")
        st.write(f"Verschuldung (Debt/Equity): {round(debt,2) if debt else 'N/A'}")

        # 🧠 Bewertung
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

        # Eigenkapitalrendite (ROE)
        if roe and roe > 0.15:
            score += 1

        # Verschuldung (weniger ist besser)
        if debt and debt < 100:
            score += 1


        # Ergebnis
        st.write(f"Score: {score}/5")

        if score >= 4:
            st.success("🟢 Kaufen – starke Firma insgesamt")
        elif score == 3:
            st.info("🟡 Halten – solide Firma")
        elif score == 2:
            st.warning("⚪ Neutral – gemischt")
        else:
            st.error("🔴 Verkaufen – schwache Kennzahlen")




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
                analysis.append("Das Unternehmen nutzt Kapital sehr effizient.")

        if debt:
            if debt > 150:
                analysis.append("Das Unternehmen ist relativ hoch verschuldet.")
            elif debt < 50:
                analysis.append("Die Verschuldung ist gering.")

        if len(analysis) == 0:
            st.write("Keine ausreichende Analyse möglich.")
        else:
            for point in analysis:
                st.write("• " + point)


        st.write("### 🧾 Fazit")

        if score >= 4:
            st.success("👉 Insgesamt eine sehr starke Aktie mit guten Fundamentaldaten.")
        elif score == 3:
            st.info("👉 Solide Aktie, aber nichts Außergewöhnliches.")
        elif score == 2:
            st.warning("👉 Gemischte Signale – genauer hinschauen.")
        else:
            st.error("👉 Schwache Fundamentaldaten – eher riskant.")
            
    
    except Exception as e:
        st.error("Fehler beim Laden der Daten")


    
    
    st.write("---")
    st.write("## 📚 Erklärung der Kennzahlen")

    with st.expander("📊 KGV (PE Ratio)"):
        st.write("""
        Das Kurs-Gewinn-Verhältnis zeigt, wie teuer eine Aktie ist.
        
        👉 Niedrig (<20): eher günstig  
        👉 Hoch (>30): eher teuer  
        """)

    with st.expander("📈 Wachstum"):
        st.write("""
        Zeigt, wie stark das Unternehmen wächst (Umsatz).
        
        👉 Hoch (>10%): sehr gut  
        👉 Niedrig (<5%): eher schwach  
        """)

    with st.expander("💰 Profit-Marge"):
        st.write("""
        Wie viel Gewinn ein Unternehmen macht.
        
        👉 Hoch (>15%): sehr profitabel  
        👉 Niedrig: wenig Gewinn  
        """)

    with st.expander("🏆 ROE (Eigenkapitalrendite)"):
        st.write("""
        Zeigt, wie effizient ein Unternehmen arbeitet.
        
        👉 Hoch (>15%): sehr gut  
        👉 Niedrig: ineffizient  
        """)

    with st.expander("⚖️ Verschuldung (Debt/Equity)"):
        st.write("""
        Zeigt, wie stark ein Unternehmen verschuldet ist.
        
        👉 Niedrig (<100): gesund  
        👉 Hoch: riskant  
        """)