
# Kriptovaluta Árelemző Microservice Projekt – Előtervezet

## Cél
A projekt célja kriptovaluta árak gyűjtése, elemzése és publikálása microservice alapú architektúrában.

## Microservice-ek

| Szolgáltatás | Feladat | Technológia | Output |
|-------------|---------|-------------|--------|
| **collector-service** | Kriptovaluta árak lekérése API-ból és mentése adatbázisba | Python + Flask + Requests | Nyers ár-adatok (PostgreSQL-ben) |
| **processor-service** | Átlag és ártrendek számítása | Python + Flask | Feldolgozott statisztikai adatok (PostgreSQL-ben) |
| **api-service** | Eredmények elérhetővé tétele REST API-n keresztül | Python + Flask vagy FastAPI | `/prices` és `/trends` endpointok |

## Adatbázis
**PostgreSQL**

### Táblák

#### price_raw
| mező | típus | példa |
|------|-------|--------|
| symbol | VARCHAR | "bitcoin" |
| price | FLOAT | 42150.55 |
| timestamp | TIMESTAMP | 2025-01-01 12:00:00 |

#### trend_stats
| mező | típus | példa |
|------|-------|--------|
| symbol | VARCHAR | "bitcoin" |
| avg_1h | FLOAT | 42120.22 |
| avg_24h | FLOAT | 41780.11 |
| change_percent_24h | FLOAT | 1.45 |

## Adatfolyam

```
collector-service → price_raw (PostgreSQL)
processor-service → trend_stats (PostgreSQL)
api-service → REST API → felhasználó / dashboard
```

## Mappa Struktúra

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
 ├ docker-compose.yml
 └ README.md
```

## Docker Compose vázlat

```yaml
version: "3.9"
services:
  postgres:
    image: postgres:14
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: crypto
    ports:
      - "5432:5432"
    volumes:
      - pg_data:/var/lib/postgresql/data

  collector:
    build: ./collector-service
    depends_on:
      - postgres

  processor:
    build: ./processor-service
    depends_on:
      - postgres

  api:
    build: ./api-service
    ports:
      - "8000:8000"
    depends_on:
      - postgres

volumes:
  pg_data:
```
