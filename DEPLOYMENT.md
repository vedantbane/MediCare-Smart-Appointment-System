# MediCare App Vercel Deployment Guide

This guide details the steps to deploy the MediCare Flask application to Vercel using GitHub.

## Prerequisites

*   A [GitHub](https://github.com/) account.
*   A [Vercel](https://vercel.com/) account.
*   The `requirements.txt` and `vercel.json` files (already created).
*   Code committed to a local git repository.

## Step 1: Push Code to GitHub

Since you have already created a repository on GitHub, run the following commands in your terminal to push your local code. Replace `<YOUR_REPOSITORY_URL>` with your actual GitHub repository URL (e.g., `https://github.com/username/medicare-app.git`).

```bash
git remote add origin <YOUR_REPOSITORY_URL>
git branch -M main
git push -u origin main
```

## Step 2: Deploy on Vercel

1.  Log in to your **Vercel** dashboard.
2.  Click **"Add New..."** -> **"Project"**.
3.  Select **"Continue with GitHub"** if asked.
4.  Find your `medicare-app` repository in the list and click **"Import"**.

## Step 3: Configure Project

1.  **Framework Preset**: Select **Other** (or ensure it detects Python/Flask if available, usually "Other" is fine for custom `vercel.json`).
2.  **Root Directory**: Leave as `./`.
3.  **Environment Variables**: You need to set the following:
    *   `SECRET_KEY`: A long random string for session security.
    *   `DATABASE_URL`: The connection string for your production database.

    > **Important**: SQLite will NOT work permanently on Vercel because the filesystem is ephemeral (it resets). You must use a hosted PostgreSQL database.

## Step 4: Set up a PostgreSQL Database (Vercel Storage)

1.  In your Vercel Project dashboard, go to the **Storage** tab.
2.  Click **"Create Database"** and select **Postgres**.
3.  Follow the prompts to create the database (accept defaults for region etc.).
4.  Once created, Vercel will automatically add environment variables like `POSTGRES_URL` etc. to your project.
5.  **Update Environment Variable**:
    *   Go to **Settings** -> **Environment Variables**.
    *   Ensure `DATABASE_URL` is set to the value of `POSTGRES_URL` (or `POSTGRES_PRISMA_URL` etc.), or relies on the code's auto-detection if compatible.
    *   *Note*: The app logic I added automatically converts `postgres://` to `postgresql://` so Vercel's default variables should work if mapped to `DATABASE_URL`.

## Step 5: Finish Deployment

1.  Click **Deploy**.
2.  Wait for the build to finish.
3.  Visit the provided domain/URL to see your live app!

## Troubleshooting

*   **Database Errors**: Check the Function Logs in Vercel if you see Error 500. Ensure your `DATABASE_URL` is correct.
*   **Missing Dependencies**: Ensure all libraries are listed in `requirements.txt`.
