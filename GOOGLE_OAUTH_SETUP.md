# Google OAuth 2.0 (Web) Setup

This project uses Google Identity Services (GIS) client-side to sign users in.
Follow these steps to create an OAuth client and get a `client_id`.

1. Open Google Cloud Console: https://console.cloud.google.com/
2. Select your project or create a new one.

3. Configure OAuth Consent Screen:
   - Navigate to `APIs & Services` → `OAuth consent screen`.
   - Choose `External` for testing (or `Internal` if using G Suite domain).
   - Fill in `App name`, `User support email`, and developer contact.
   - Save.

4. Create OAuth 2.0 Client ID:
   - Go to `APIs & Services` → `Credentials` → `Create Credentials` → `OAuth client ID`.
   - Application type: `Web application`.
   - Name: `DPDP Frontend` (or any name).
   - **Authorized JavaScript origins**: add `http://localhost:5173` (and `http://localhost:5174` if Vite picks another port during dev).
   - **Authorized redirect URIs**: not required for Google Identity Services basic client flow, but you can add `http://localhost:5173` if using server-based flows.
   - Create and copy the `Client ID`.

5. Paste the client ID into `dpdp-frontend/.env` as `VITE_GOOGLE_CLIENT_ID`.

6. Start the frontend:

```bash
cd dpdp-frontend
npm run dev
```

7. Open http://localhost:5173 and click the Google sign-in button.

8. (Optional) Backend verification:
   - If you want the backend to verify tokens, send the `id_token` returned by Google (credential) to a backend endpoint and verify using Google API or libraries.

Troubleshooting:
- If the sign-in button does not appear, ensure `VITE_GOOGLE_CLIENT_ID` is set and the dev server was restarted.
- If you get `origin_mismatch` errors, check the Authorized JavaScript origins in Google Cloud Console.

Security note:
- Do not commit `.env` with real credentials to the repository.
- For production, follow OAuth verification and publishing steps in Google Cloud Console.
