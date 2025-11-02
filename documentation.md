# 📘 Technikai dokumentáció – Crypto Project

## Rendszer áttekintése

A projekt microservice architektúrát használ, ahol minden komponens önálló felelősségi körrel rendelkezik.  
Az egyes szolgáltatások Docker konténerekben futnak és közös PostgreSQL adatbázist használnak.

| Szolgáltatás | Port | Leírás |
|-------------|------|--------|
| **collector-service** | 5000 | Kripto árfolyamadatok külső API-ból történő lekérése |
| **processor-service** | 5001 | Adatok feldolgozása, trendek és százalékos változások számítása |
| **api-service** | 5002 | REST API a feldolgozott adatok lekéréséhez |
| **dashboard-service** | 5003 | Frontend dashboard az adatok megjelenítéséhez |
| **PostgreSQL adatbázis** | 5432 | A nyers és feldolgozott adatok tárolása |

---

## 🗄 Adatbázis séma

### **1. price_raw** – Nyers árfolyam adatok

| Oszlop | Típus | Leírás |
|-------|------|--------|
| id | SERIAL PRIMARY KEY | Rekord azonosító |
| symbol | TEXT | Kriptovaluta rövid neve (pl. BTC, ETH) |
| price | NUMERIC | Ár USD-ben |
| timestamp | TIMESTAMP | Az adat lekérésének időpontja |

### **2. trend_stats** – Feldolgozott árfolyamváltozási adatok

| Oszlop | Típus | Leírás |
|-------|------|--------|
| id | SERIAL PRIMARY KEY | Rekord azonosító |
| symbol | TEXT | Kriptovaluta |
| avg_1h | NUMERIC | Átlag ár 1 óra alatt |
| avg_24h | NUMERIC | Átlag ár 24 óra alatt |
| timestamp | TIMESTAMP | Frissítés ideje |

---

## 🔄 Adatfolyam működése
Collector → DB (/prices) → Processor → DB (/trends) → API → Dashboard


### Részletesen

1. **collector-service**
   - 5 percenként lekéri a top 10 kriptovaluták árát CoinGecko API-ból
   - Az adatokat időbélyeggel elmenti a `price_raw` táblába

2. **processor-service**
   - Időzítve fut
   - Ugyanazon kriptóhoz lekéri a jelenlegi, 1 órás és 24 órás visszatekintő árakat
   - Kiszámítja a 1h és 24h százalékos változást:
   - Az eredményeket a `trend_stats` táblába menti

3. **api-service**
   - GET `/trends` → JSON-ben visszaadja a feldolgozott adatokat

4. **dashboard-service**
   - `http://localhost:5003`
   - Grafikonos megjelenítés

---
### Összefoglaló
A rendszer automatikusan gyűjt, feldolgoz, tárol és megjelenít kriptovaluta árfolyam-trend adatokat.
Az architektúra könnyen bővíthető, illetve a mikro-szolgáltatás modell lehetővé teszi a különálló skálázást.
