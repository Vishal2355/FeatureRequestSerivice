# FeatureRequestService

A simple backend built with **FastAPI** and **AWS CDK** that uses **DynamoDB** to store feature requests.

---

## 🧩 Requirements
Before running this project on a Mac:
- Python 3.10 or newer
- Node.js and npm (for AWS CDK)
- AWS CLI configured with your credentials (`aws configure`)
- AWS CDK installed globally:
  ```bash
  npm install -g aws-cdk
  ```

---

## ⚙️ 1. Setup
After downloading or cloning this folder:

### Create virtual environment and install FastAPI
```bash
cd FeatureRequestSerivice
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Create `.env` file
```bash
echo "TABLE_NAME=FeatureRequestsService" > .env
```

---

## 🏗️ 2. Deploy DynamoDB with AWS CDK
```bash
cd infra
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cdk bootstrap --app "python3 app.py"   # only first time
cdk deploy --app "python3 app.py"
```

Wait until you see  
`FeatureRequestsStack.TableName = FeatureRequestsService`

---

## 🚀 3. Run FastAPI App
```bash
cd ..
source .venv/bin/activate
uvicorn app:app --reload
```

Then open in browser:  
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Example API Use
**POST /requests**  
Header:
```
X-Client-Id: vishal
```
Body:
```json
{
  "title": "Dark mode",
  "description": "Add dark theme support"
}
```

---

## 🧹 4. Delete DynamoDB Table (optional)
```bash
cd infra
source .venv/bin/activate
cdk destroy --app "python3 app.py"
```
Type **y** to confirm deletion.

---

You’re done ✅  
Run it anytime by redeploying the table and restarting the FastAPI server.