# Firebase Setup Instructions

## Step 1: Create Firebase Project
1. Go to https://console.firebase.google.com
2. Click "Create a project" or "Add project"
3. Enter project name: `dpdp-compliance-checker`
4. Enable Google Analytics (optional)
5. Choose Google Analytics account or create new
6. Click "Create project"

## Step 2: Enable Authentication
1. In Firebase Console, go to "Authentication" (left sidebar)
2. Click "Get started"
3. Go to "Sign-in method" tab
4. Find "Google" and click on it
5. Toggle "Enable"
6. Enter project support email
7. Click "Save"

## Step 3: Add Web App
1. Click the "</>" icon (Web app) in the project overview
2. Enter app nickname: `DPDP Compliance Checker`
3. Check "Also set up Firebase Hosting" (optional)
4. Click "Register app"

## Step 4: Copy Firebase Config
1. Copy the `firebaseConfig` object
2. Replace the values in `src/firebase.js`:

```javascript
const firebaseConfig = {
  apiKey: "your-api-key-here",
  authDomain: "your-project-id.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project-id.appspot.com",
  messagingSenderId: "your-messaging-sender-id",
  appId: "your-app-id"
};
```

## Step 5: Add Authorized Domain
1. In Firebase Console → Authentication → Settings
2. Scroll to "Authorized domains"
3. Add: `http://localhost:5173`
4. Click "Add domain"

## Step 6: Test the Application
1. Start the frontend: `npm run dev`
2. Open http://localhost:5173
3. Click "Sign in with Google"
4. Select your Google account
5. You should be redirected to the dashboard

## Troubleshooting

### If popup doesn't work:
- Make sure `http://localhost:5173` is in authorized domains
- Check browser console for errors
- Try incognito mode

### If authentication fails:
- Verify Firebase config is correct
- Check that Google provider is enabled
- Ensure project is not in test mode restrictions

## Optional: Backend Integration

To send the Google token to your backend, uncomment this code in `Login.jsx`:

```javascript
// Optional: Send token to backend for verification
const token = await result.user.getIdToken();
await axios.post("http://localhost:8000/api/auth/google", { token });
```

You'll need to implement the backend endpoint to verify the token.</content>
<parameter name="filePath">c:\Users\Lokesh\dpdp-compliance-checker\FIREBASE_SETUP.md