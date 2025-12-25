---
categories: Developer Tools
date: 2024-12-14 13:45:00
tags:
- React
- Firebase
- Firestore
- Web App
- Project
title: Kuber Accounting App - React, Firebase, Firestore
---

{% include toc title="Index" %}

Integrate **Firebase with React**, manage CI/CD pipelines (**Github Actions**),
and deploy a fully functional app on **Firebase** Hosting.

# Summary of Kuber App Requirements
**Purpose**: A P/L tracking app for managing account data related to profits, losses, 
deposits, and withdrawals for multiple Stock Accounts

## Key Features:
- Add accounts with details (account number, alias, currency).
- Add money to accounts with date, amount, and comment.
- Withdraw money from one account to another with date, amount, and comment.
- Monthly accounting to track profit/loss in selected accounts.
- Miscellaneous activities related to money with date, amount, and comment.

# Technical Stack:
**Frontend**: React (UI for adding accounts, deposits, withdrawals, and displaying reports).

**Backend**: Firebase Functions (for dynamic functionality and business logic).

**Database**: Firestore (for storing account, transaction, and report data).

**Hosting**: Firebase Hosting (to host static frontend).

# Database Design (no-sql):
**Accounts Collection:**
accountNumber, alias, currency, balance.

### Accounts:
Fields:
- accountNumber: string (unique identifier for the account).
- alias: string (the account name or alias, e.g., "Family Savings").
- currency: string (currency of the account, e.g., "USD", "EUR").
- balance: number (optional, keeps track of the current balance).

```json
{
  "accountNumber": "123456789",
  "alias": "Family Savings",
  "currency": "USD",
  "balance": 1000
}
```

### 2. Transactions (for deposits, withdrawals, misc activities):
**Transactions Collection:**
accountAlias, date, amount, comment, type (deposit, withdrawal, misc).

Fields:
- accountAlias: string (linked to the alias in the Accounts collection).
- date: timestamp (when the transaction occurred).
- amount: number (positive for deposits, negative for withdrawals).
- comment: string (optional, for additional information).
- type: string (could be "deposit", "withdrawal", or "misc").

```json
{
  "accountNumber": "123456789",
  "alias": "Family Savings",
  "currency": "USD",
  "balance": 1000
}

```

### Monthly Accounting:
**Monthly Accounting:**
accountAlias, date, profitLossAmount.

Fields:
- accountAlias: string (linked to the alias in the Accounts collection).
- date: timestamp (the month/year of the accounting entry).
- profitLossAmount: number (profit/loss for that month in the account’s currency).

```json
{
  "accountAlias": "Family Savings",
  "date": "2024-12-01T00:00:00Z",
  "profitLossAmount": 200
}
```

# UI Design:
- Add Account Screen: Form for adding an account number, alias, and currency.
- Add Money Screen: Form for selecting an account, entering amount, date, and comment.
- Withdraw Money Screen: Form for withdrawing money from one account to another with amount, date, and comment.
- Monthly Accounting Screen: Form for entering profit/loss for an account.
- Misc Activity Screen: Form for logging miscellaneous activities with amount, date, and comment.

# Firebase Hosting and Deployment:
Use Firebase Hosting to serve the static frontend.

Use Firebase Functions to process transactions and business logic (e.g., storing deposits and withdrawals, calculating profits/losses).
Use Firestore to store all the data and allow real-time syncing across devices.

---

# Building and Deploying the React App with Firebase Firestore: A Journey

## 1. **Project Setup**
- Created a new React app using `create-react-app`:
  ```bash
  npx create-react-app my-app
  cd my-app
  ```
  
- Installed necessary dependencies:
  ```bash
  npm install react-router-dom firebase react-icons
  ```

## 2. **Firebase Integration**
- Set up a Firebase project and configured Firestore.
```bash
npm install -g firebase-tools

firebase init
```

- Created a `firebase.js` file to initialize Firebase:
  ```javascript
  import { initializeApp } from 'firebase/app';
  import { getAuth } from 'firebase/auth';
  import { getFirestore } from 'firebase/firestore';

  const firebaseConfig = {
      apiKey: process.env.REACT_APP_API_KEY,
      authDomain: process.env.REACT_APP_AUTH_DOMAIN,
      projectId: process.env.REACT_APP_PROJECT_ID,
      storageBucket: process.env.REACT_APP_STORAGE_BUCKET,
      messagingSenderId: process.env.REACT_APP_MESSAGING_SENDER_ID,
      appId: process.env.REACT_APP_APP_ID
  };

  const app = initializeApp(firebaseConfig);
  export const auth = getAuth(app);
  export const db = getFirestore(app);
  ```

## 3. **Environment Variables**
- Added a `.env` file to store Firebase configuration securely:
- Ensured `.env` was not committed by adding it to `.gitignore`.
```shell
REACT_APP_API_KEY=your-api-key
REACT_APP_AUTH_DOMAIN=your-auth-domain
REACT_APP_PROJECT_ID=your-project-id
REACT_APP_STORAGE_BUCKET=your-storage-bucket
REACT_APP_MESSAGING_SENDER_ID=your-messaging-sender-id
REACT_APP_APP_ID=your-app-id
```

## 4. **Authentication**
- Implemented user login/logout using Firebase Authentication in the `Login` and `Dashboard` components.
- Used `auth.onAuthStateChanged` to manage user sessions:
  ```javascript
  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged((user) => {
      setUser(user || null);
    });
    return () => unsubscribe();
  }, []);
  ```

## 5. **Firestore Integration**
- Created components to interact with Firestore, such as `AddAccount`, `MonthlyAccounting`, and `Withdraw`.
- Used Firestore methods like `collection`, `addDoc`, `getDocs`, and `query` for CRUD operations:
  ```javascript
  const fetchAccounts = async () => {
    const querySnapshot = await getDocs(collection(db, 'Accounts'));
    const accountsData = querySnapshot.docs.map((doc) => doc.data());
    setAccounts(accountsData);
  };
  ```

## 6. **Deployment Challenges**
### Linting Warnings in CI/CD
- Addressed issues like unused imports and missing dependencies in `useEffect` by cleaning up code and including necessary dependencies.

### Firestore Index Errors
- Fixed Firestore index errors by creating required indexes via Firebase Console.

### Suppressing CI Warnings
- Configured GitHub Actions to prevent warnings from failing the build by setting:
  ```yaml
  env:
    CI: false
  ```

## 7. **Deploying to Production**
- Built the app using:
  ```bash
  npm run build
  ```
- Deployed to Firebase Hosting:
  ```bash
  firebase deploy
  ```