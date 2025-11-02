# 🚀 Crypto Project — Cryptocurrency Trend Monitoring System

![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Python](https://img.shields.io/badge/Python-3.11+-yellow)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A projekt célja kriptovaluta árfolyamok folyamatos gyűjtése, feldolgozása és vizuális megjelenítése mikroszervizekkel és Dockerrel.  
A rendszer automatikusan lekéri a legfrissebb árakat, trendeket számol belőlük és egy dashboardon megjeleníti.

---

## 🧩 Architektúra

| Szolgáltatás | Port | Leírás |
|---|---|---|
| **db (PostgreSQL)** | 5432 | Adatbázis |
| **collector-service** | 5000 | Árfolyamok lekérése és mentése |
| **processor-service** | 5001 | Trendek számítása |
| **api-service** | 5002 | API a feldolgozott adatokhoz |
| **dashboard-service** | 5003 | Webes dashboard |

---

## 📁 Projekt Struktúra

```
crypto-project/
 ├ collector-service/
 │  ├ app.py
 │  ├ requirements.txt
 │  └ Dockerfile
 ├ processor-service/
 │  ├ app.py
 │  ├ requirements.txt
 │  └ Dockerfile
 ├ api-service/
 │  ├ app.py
 │  ├ requirements.txt
 │  └ Dockerfile
 ├ dashboard-service/
 │  ├ app.py
 │  ├ requirements.txt
 │  └ Dockerfile
 ├ .env
 ├ init.sql
 ├ docker-compose.yml
 └ README.md
```

---

## 🔧 Konfiguráció

A projekt gyökerében hozz létre egy `.env` fájlt:
```bash
DB_PASSWORD=postgres
```
---

## 🚀 Indítás Dockerrel

Build + futtatás
```bash
docker-compose up -d --build
```
Konténerek állapota
```bash
docker ps
```
Logok megtekintése
```bash
docker-compose logs -f
```
Leállítás
```bash
docker-compose down
```
---

### 🌐 Webes Elérés

| URL                                                          | Mit látsz?          |
| ------------------------------------------------------------ | ------------------- |
| [http://localhost:5003](http://localhost:5003)               |   **Dashboard**     |
| [http://localhost:5002/trends](http://localhost:5002/trends) | API válasz JSON-ben |
| [http://localhost:5001](http://localhost:5001)               | Processor status    |
| [http://localhost:5000](http://localhost:5000)               | Collector status    |

---

### 🗄 Adatbázis hozzáférés

Belépés:
```bash
docker exec -it crypto-db psql -U postgres -d crypto
```

Táblák megjelenítése:
```bash
\dt;
```

---

### ♻️ Részleges újra buildelés

Ha csak a processor kódját módosítanánk:
```bash
docker-compose build processor
docker-compose up -d processor
```

---

### 🏆 Kiegészíthető funkciók (opcionális fejlesztési irányok)
| Fejlesztés                      | Nehézség | Mit ad?                          |
| ------------------------------- | -------- | -------------------------------- |
| Grafana + Prometheus monitoring | ⭐⭐       | Rendszer monitorozás             |
| Discord/Telegram értesítések    | ⭐⭐⭐      | Alert, ha nagy ármozgás történik |
| Dashboard UI → React            | ⭐⭐⭐      | Modern reszponzív felület        |

---

### 📜 Licenc

MIT License — Szabadon használható és bővíthető.

---
