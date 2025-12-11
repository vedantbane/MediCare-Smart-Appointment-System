# MediCare App Deployment Guide (Supabase Edition)

## Step 1: Push Code to GitHub (Completed)
Your code is already on GitHub.

## Step 2: Create a Supabase Database
Since Vercel Postgres is not available, **Supabase** is the best alternative (it is also Postgres).

1.  Go to [Supabase](https://supabase.com/) and create a free account/project.
2.  Once your project is created, go to **Project Settings** (cog icon) -> **Database**.
3.  Scroll down to **Connection params** or **Connection String**.
4.  Copy the **URI**. It will look like:
    `postgresql://postgres.xxxx:[YOUR-PASSWORD]@aws-0-us-east-1.pooler.supabase.com:6543/postgres`
    *(Make sure to replace `[YOUR-PASSWORD]` with the real password you set for the database).*

## Step 3: Configure Vercel

1.  Go to your Vercel Project.
2.  Go to **Settings** -> **Environment Variables**.
3.  Add the following variables:

    *   **Key**: `DATABASE_URL`
    *   **Value**: Paste your Supabase Connection String (from Step 2).

    *   **Key**: `SESSION_SECRET`
    *   **Value**: `any-random-secret-string-12345`

4.  **Redeploy**: Go to the **Deployments** tab and redeploy the latest commit (or just push a small change to trigger it) to ensure the new variables are picked up.

## Troubleshooting
*   If you see "Module not found", ensure `requirements.txt` is present (it is).
*   If you see Database errors, verify your Supabase password is correct in the connection string.
