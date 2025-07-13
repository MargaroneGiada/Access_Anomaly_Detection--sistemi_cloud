# Access_Anomaly_Detection

# ✅ Access Anomaly Detection – To-Do List (Cloud Native + CI/CD + Docker)

---

## 🔧 FASE 0 – Preparazione progetto

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

## 🌐 FASE 1 – Hosting frontend statico (S3 + CloudFront)

- [ ] Sviluppa una prima versione del frontend (anche base)
- [x] Crea bucket S3 per il sito statico
- [ ] Abilita l'hosting statico su S3
- [ ] Configura CloudFront:
  - [ ] Collegalo al bucket S3
  - [ ] Aggiungi HTTPS con certificato
- [ ] Testa la pubblicazione manuale del frontend

---

## 🔐 FASE 2 – Autenticazione con AWS Cognito

- [ ] Crea User Pool su Cognito
- [ ] Configura App Client (senza client secret)
- [ ] Integra Cognito nel frontend:
  - [ ] Signup
  - [ ] Login
  - [ ] Logout
- [ ] Proteggi le API tramite autorizzazione Cognito

---

## 📡 FASE 3 – API REST (API Gateway + Lambda o Docker)

- [ ] Definisci le API necessarie:
  - [ ] POST /log-access
  - [ ] GET /accesses
  - [ ] GET /anomalies
- [ ] Scegli linguaggio per Lambda (es. Python)
- [ ] Scrivi le funzioni Lambda
- [ ] (Opzionale) Containerizza le funzioni Lambda con Docker
  - [ ] Dockerfile
  - [ ] Test locale
  - [ ] Push su ECR
- [ ] Crea API Gateway e collega le rotte alle funzioni
- [ ] Proteggi le rotte con Cognito Authorizer

---

## 💾 FASE 4 – Database con DynamoDB

- [ ] Crea tabella DynamoDB:
  - [ ] PK: userId
  - [ ] SK: timestamp
  - [ ] Attributi: ip, location, device, status
- [ ] Funzione Lambda log-access salva nel DB
- [ ] Funzione accesses legge gli accessi dell'utente
- [ ] Testa il salvataggio e la lettura dati

---

## 🧠 FASE 5 – Rilevamento anomalie + SNS

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

## 🐳 FASE 6 – Dockerizzazione componenti

- [ ] Scrivi Dockerfile per Lambda container
- [ ] Build e test locali con docker run
- [ ] Crea repository su ECR
- [ ] Pusha le immagini su ECR
- [ ] Collega container a Lambda (oppure ECS)

---

## 🔁 FASE 7 – CI/CD con GitHub Actions

### Frontend
- [ ] Crea workflow .github/workflows/deploy-frontend.yml
- [ ] Sync automatico su S3 ad ogni push su main
- [ ] (Opzionale) Invalida cache CloudFront dopo il deploy

### Backend
- [ ] Crea workflow .github/workflows/deploy-backend.yml
- [ ] Build Docker image
- [ ] Push su ECR
- [ ] Deploy su Lambda o ECS
- [ ] Test automatici prima del deploy (opzionale)

---

## 📊 FASE 8 – Visualizzazione accessi e anomalie

- [ ] Aggiungi pagina dashboard al frontend
- [ ] Visualizza elenco accessi per utente
- [ ] Visualizza elenco anomalie
- [ ] Usa grafici (es. Chart.js) per mostrare frequenza accessi

---

## 📈 FASE 9 – Monitoring e debug

- [ ] Abilita CloudWatch Log per tutte le Lambda
- [ ] Verifica log durante test manuali
- [ ] (Opzionale) Aggiungi allarmi CloudWatch per errori o accessi anomali frequenti
- [ ] Verifica la latenza e costi stimati

---

## 🎁 FASE FINALE – Consegna e documentazione

- [ ] Scrivi README con:
  - [ ] Obiettivo del progetto
  - [ ] Architettura usata (con schema)
  - [ ] Tecnologie e servizi AWS
  - [ ] Come eseguire il deploy e testare
- [ ] Fai uno screencast/demo (se richiesto)
- [ ] Controlla la checklist e carica il progetto