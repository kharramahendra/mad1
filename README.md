# SmartReco — Starter Template

Starter for the SmartReco Build Challenge. See the challenge page for the full problem
statement and rubric.

## Getting started

1. **Clone this template repo:**
   ```bash
   git clone git@github.com:kharramahendra/SmartReco-Template.git
   ```
2. **Create your OWN repository** on GitHub and push the code there — your own repo is
   your submission.
   ```bash
   cd SmartReco-Template
   git remote set-url origin git@github.com:<your-username>/<your-repo>.git
   git push -u origin main
   ```

The `.github/workflows/smartreco-checks.yml` file is **mandatory** — keep it exactly as
it is in this template. It runs the automated checks on every push.

---

## Set up GitHub Actions secrets (required)

The automated checks won't run without these three secrets. Add them in **your** repo:

### Step 1 — Open Settings
In your repository, click **Settings** (top-right).

![Settings](docs/1-settings.png)

### Step 2 — Go to Actions secrets
In the left sidebar: **Secrets and variables → Actions**, then click
**New repository secret**.

![Secrets and variables → Actions](docs/2-secrets-actions.png)

### Step 3 — Add each secret
Enter the name and value, then click **Add secret**. Do this for all three below.

![New secret](docs/3-new-secret.png)

Add these three (names must match exactly):

| Secret name | Value |
|-------------|-------|
| `SUBMISSION_TOKEN` | Your submission token (you'll receive this soon on your dashboard) |
| `PINECONE_API_KEY` | Your Pinecone API key |
| `PINECONE_INDEX` | Your Pinecone index name |

Your keys stay in your own repo and are never sent to us.

---

## Run locally

```bash
pip install -r requirements.txt
cp .env.example .env      # then fill in your keys
python app.py
```

## Push and check

Every push runs the checks automatically. See results in the **Actions** tab and on your
dashboard. A failing check just means "fix and push again."

---

Build toward the published rubric. The `agent/`, `models/`, `tracking/`, and `templates/`
folders mark where your work goes. You may reorganize freely — no fixed structure required.
