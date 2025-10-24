# Access Anomaly Detection - TODO list

## Frontend

[x] Metti la build React (dist/) su S3.

[] Collega CloudFront a S3.

[] Configura Cognito per gestire auth nella tua webapp.

## Backend

[] Trasforma l’attuale Flask backend in Lambda → così ti togli EC2 e Docker dalla pipeline principale.

[] (Opzionale, per esercizio) Tieni anche la versione Dockerizzata su EC2/ECR, così puoi mostrare entrambe le architetture.

## API Gateway

[] Crea gli endpoint /signup, /login, /dashboard.

[] Collegali a Lambda.

[] Aggiungi integrazione con Cognito Authorizer.

## DynamoDB

[] Definisci bene le tabelle (Users, AccessLogs).

[] Aggiorna le Lambda in modo che scrivano/leggano correttamente.

## Modulo Anomaly Detection (fittizio)

[] Lambda che simula il check degli accessi.

[] Se trova anomalie → pubblica su SNS.

[] Subscrivi un’email al topic SNS → ricevi notifiche.

## CI/CD

Mantieni GitHub Actions:

[x] Job 1: build React → deploy su S3.

[] Job 2: package Lambda in zip → deploy su AWS Lambda (o build Docker → push su ECR).
