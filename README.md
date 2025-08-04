#IN PROGRESS

# Access_Anomaly_Detection

# Reminder
<img width="781" height="421" alt="Grafico_sistemi_cloud drawio" src="https://github.com/user-attachments/assets/0eb271e5-d839-4cad-ac95-c049c325201b" />

#### Inserire credenziali in file .aws/credentials e su github!

# To-Do List 

---

## FASE 0 – Preparazione progetto

- [x] Crea repo GitHub access-anomaly-detection
- [x] Organizza struttura progetto:
  - [x] /frontend/
  - [x] /backend/
  - [x] /infrastructure/
  - [x] .github/workflows/
<!-- non si può fare con aws learner lab
- [ ] Configura utente IAM con permessi adeguati su:
  - [ ] S3, Lambda, API Gateway, DynamoDB
  - [ ] Cognito, SNS, CloudWatch, ECR/ECS -->

---

## FASE 1 – S3

- [x] Sviluppa una prima versione del frontend (anche base)
- [x] Crea bucket S3 per il sito statico
- [x] Abilita l'hosting statico su S3
<!-- non si può fare cib aws learner lab
- [ ] Configura CloudFront:
  - [ ] Collegalo al bucket S3
  - [ ] Aggiungi HTTPS con certificato -->
- [x] Testa la pubblicazione manuale del frontend
- [x] Aggiungere github action (funziona!)
- [x] Creare script python creazione e cancellazione bucket S3

---

## FASE 2 – IN PAUSA - Cognito 
<!-- 
- [ ] Crea User Pool su Cognito
- [ ] Configura App Client (senza client secret)
- [ ] Integra Cognito nel frontend:
  - [ ] Signup
  - [ ] Login
  - [ ] Logout
- [ ] Proteggi le API tramite autorizzazione Cognito -->

---

## FASE 3 – API REST (API Gateway + Lambda  Docker)

- [ ] Definisci le API necessarie:
  - [ ] POST /login 
  - [x] POST /signup 
  - [ ] POST /log-access
  - [ ] POST /log-access
  - [ ] GET /accesses
  - [ ] GET /anomalies
- [ ] Scegli linguaggio per Lambda (es. Python)
- [ ] Scrivi le funzioni Lambda
- [ ] Containerizza le funzioni Lambda con Docker
  - [ ] Dockerfile
  - [ ] Test locale
  - [ ] Push su ECR
- [ ] Crea API Gateway e collega le rotte alle funzioni

---

## FASE 4 – DynamoDB

- [ ] Crea tabella DynamoDB:
  - [ ] PK: userId
  - [ ] SK: timestamp
  - [ ] Attributi: ip, location, device, status
- [ ] Funzione Lambda log-access salva nel DB
- [ ] Funzione accesses legge gli accessi dell'utente
- [ ] Testa il salvataggio e la lettura dati

---

## FASE 5 

- [ ] Definisci regole base di anomalia:
  - [ ] IP sconosciuto / Paese diverso
  - [ ] Orari inconsueti
  - [ ] Accessi ravvicinati / troppi tentativi
- [ ] Funzione Lambda identifica anomalie su log-access
- [ ] Configura SNS topic
- [ ] Sottoscrivi email di test a SNS
- [ ] Lambda pubblica notifica se rileva un’anomalia
- [ ] Salva anomalie in tabella DynamoDB (opzionale)

---

## FASE 6

- [ ] Scrivi Dockerfile per Lambda container
- [ ] Build e test locali con docker run
- [ ] Crea repository su ECR
- [ ] Pusha le immagini su ECR
- [ ] Collega container a Lambda (oppure ECS)

---

## FASE 6 

- [ ] Crea un'istanza EC2 per il backend (es. app Flask o Node.js)
- [ ] Installa Docker su EC2
- [ ] Avvia i container (backend/API) su EC2 con Docker
- [ ] Esporre il container su porta pubblica (es. 3000 o 8000)
- [ ] Crea un Load Balancer (ALB):
  - [ ] Configura listener su porta 80/443
  - [ ] Collega il target group all'istanza EC2
- [ ] (Opzionale) Autoscaling del backend
- [ ] (Opzionale) Esporre anche il frontend da EC2 (se non usi più S3)

---

## FASE 7 – CI/CD con GitHub Actions

### Frontend
- [x] Crea workflow .github/workflows/deploy-frontend.yml
- [x] Sync automatico su S3 ad ogni push su main
- [ ] (Opzionale) Invalida cache CloudFront dopo il deploy

### Backend
- [x] Crea workflow .github/workflows/deploy-backend.yml
- [ ] Build Docker image
- [ ] Push su ECR
- [ ] Deploy su Lambda o ECS
- [ ] Test automatici prima del deploy (opzionale)

---

## FASE 8 – Visualizzazione accessi e anomalie

- [x] Aggiungi pagina dashboard al frontend
- [ ] Visualizza elenco accessi per utente
- [ ] Visualizza elenco anomalie
- [ ] Usa grafici (es. Chart.js) per mostrare frequenza accessi

---

## FASE 9 

- [ ] Abilita CloudWatch Log per tutte le Lambda
- [ ] Verifica log durante test manuali
- [ ] (Opzionale) Aggiungi allarmi CloudWatch per errori o accessi anomali frequenti
- [ ] Verifica la latenza e costi stimati

---

## FASE 10

- [ ] Scrivi README con:
  - [ ] Obiettivo del progetto
  - [ ] Architettura usata (con schema)
  - [ ] Tecnologie e servizi AWS
  - [ ] Come eseguire il deploy e testare
- [ ] Fai uno screencast/demo (se richiesto)
- [ ] Controlla la checklist e carica il progetto
