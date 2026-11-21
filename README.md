# Architecture Web Distribuée – Microservices (Eureka & Actuator)

ESPRIT – Année universitaire 2026-2027

## Membres de l'équipe

- Rania Ben Hadj Hamida

## Microservices

| Microservice  | Technologie         | Port | Nom dans Eureka |
|---------------|---------------------|------|-----------------|
| Eureka Server | Spring Boot         | 8761 | –               |
| Candidat      | Spring Boot + H2    | 8081 | CANDIDAT        |
| Job           | Spring Boot + MySQL | 8082 | JOB             |
| Candidature   | Spring Boot + MySQL | 8085 | CANDITATURE     |
| Meeting       | Node.js / Express   | 8083 | MEETING         |
| Notification  | Python / FastAPI    | 8084 | NOTIFICATION    |

Code source : `backend/backend/microservices/`

## Atelier 1 – Eureka Server

- Serveur Eureka (`@EnableEurekaServer`) sur le port 8761.
- Candidat, Job et Candidature enregistrés comme clients Eureka.
- Meeting (`eureka-js-client`) et Notification (`py-eureka-client`) enregistrés dans le même serveur.
- Plusieurs instances : Candidat (8081, 8091), Meeting (8083, 8093), Notification (8084, 8094).

## Atelier 2 – Observabilité avec Spring Boot Actuator

- `spring-boot-starter-actuator` dans Candidat, Job et Candidature : endpoints `health`, `info`, `metrics`.
- `eureka.client.healthcheck.enabled=true` : Job passe **DOWN** dans Eureka quand MySQL est arrêté.
- Meeting et Notification : routes `GET /health` et `GET /info`, déclarées dans Eureka (`healthCheckUrl` / `statusPageUrl`).

## Captures

Toutes les captures (Eureka + Actuator) sont dans **[Rendu.pdf](Rendu.pdf)**.

## Lancement

Ordre : MySQL → Eureka → Candidat / Job / Candidature → Meeting → Notification.

```powershell
# Services Spring Boot (dans le dossier de chaque service)
mvn spring-boot:run

# Meeting
cd backend/backend/microservices/meeting; npm install; $env:PORT=8083; npm start

# Notification
cd backend/backend/microservices/notification
python -m venv venv; .\venv\Scripts\pip install -r requirements.txt
$env:PORT=8084; .\venv\Scripts\python -m app.main
```

Dashboard Eureka : http://localhost:8761
