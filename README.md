# World-Party-Federation-Branches-managers: Sovereign Deploy (Epoch 3)

This repository implements the **Final Nexus** automation process, connecting local development with the Sovereign Cloud through a secure, integrity-verified pipeline.

## 🚀 Sovereign Deployment Workflow

The "Final Nexus" workflow (found in `.github/workflows/final-nexus.yml`) automates the deployment of audit bundles to AWS S3 using modern security practices.

### 1. Identity Handshake (OIDC)
GitHub Actions authenticates with AWS using **OpenID Connect (OIDC)**, eliminating the need for long-lived static credentials (IAM Access Keys).

### 2. Sovereign Upload
The `src/sovereign_upload.py` script performs a parallel multipart upload. It calculates the **SHA256** integrity hash locally and injects it into the S3 object's metadata (`x-amz-meta-sha256`).

### 3. The Oracle Check
Post-upload, the workflow verifies that the hash recorded in the cloud matches the local calculation, ensuring absolute data integrity during the "Descent" from local to cloud.

---

## 🔐 הגדרת OIDC Trust ב-AWS (Setup Instructions)

כדי שה-Workflow יעבוד, עליך להגדיר Identity Provider בתוך ה-IAM של AWS:

### 1. יצירת ה-Identity Provider

* **Provider Type:** OpenID Connect
* **Provider URL:** `https://token.actions.githubusercontent.com`
* **Audience:** `sts.amazonaws.com`

### 2. הגדרת ה-Trust Policy של ה-Role

ה-Role שמוגדר ב-`AWS_ROLE_ARN` חייב לאפשר ל-GitHub Actions לגשת אליו. להלן ה-Policy (החלף את הנתונים שלך):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::<ACCOUNT_ID>:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:<ORG_OR_USER>/<REPO_NAME>:*"
        },
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        }
      }
    }
  ]
}
```

---

## 🛠️ Configuration Required

The following **GitHub Secrets** must be configured for the workflow:

- `AWS_ROLE_ARN`: The ARN of the IAM Role with the Trust Policy above.
- `AWS_REGION`: The target AWS region (e.g., `us-east-1`).
- `S3_BUCKET`: The destination S3 bucket name.

---

## 📈 Epoch 3 Status: SYSTEM FULLY INTEGRATED

The system is now capable of 100% automated, verified deployments. Every `git push` triggers the Oracle Check to maintain the governing constant between intellect and reality.

---

## 📁 Repository Structure

- `src/` — Core logic including the `watchtower_governor` and `sovereign_upload`.
- `.github/workflows/` — CI/CD automation.
- `tests/` — Quality adherence verification.
