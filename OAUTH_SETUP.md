# OAuth Setup Instructions

To connect Spotify and Instagram accounts, you need to set up OAuth credentials. Follow these steps:

## Spotify OAuth Setup

1. **Go to Spotify Developer Dashboard**
   - Visit: https://developer.spotify.com/dashboard
   - Log in with your Spotify account

2. **Create an App**
   - Click "Create an app"
   - Fill in:
     - App name: "ComeUp" (or your preferred name)
     - App description: "Music marketing platform"
     - Website: `http://localhost:8000` (for development)
     - Redirect URI: `http://localhost:8000/api/callback/spotify`
     - Accept terms and click "Save"

3. **Get Your Credentials**
   - After creating the app, you'll see:
     - **Client ID** (visible immediately)
     - **Client Secret** (click "Show client secret" to reveal)

4. **Add to .env file**
   - Open the `.env` file in the root directory
   - Add these lines:
   ```
   SPOTIFY_CLIENT_ID=your_client_id_here
   SPOTIFY_CLIENT_SECRET=your_client_secret_here
   SPOTIFY_REDIRECT_URI=http://localhost:8000/api/callback/spotify
   ```

5. **Restart your backend server** after adding the credentials

## Instagram OAuth Setup

1. **Go to Facebook Developers**
   - Visit: https://developers.facebook.com/apps/
   - Log in with your Facebook account

2. **Create an App**
   - Click "Create App"
   - Select "Consumer" as the app type
   - Fill in app details

3. **Add Instagram Basic Display Product**
   - In your app dashboard, find "Add Product"
   - Add "Instagram Basic Display"
   - Configure OAuth redirect URI: `http://localhost:8000/api/callback/instagram`

4. **Get Your Credentials**
   - App ID (visible in app settings)
   - App Secret (in app settings > Basic)

5. **Add to .env file**
   ```
   INSTAGRAM_APP_ID=your_app_id_here
   INSTAGRAM_APP_SECRET=your_app_secret_here
   INSTAGRAM_REDIRECT_URI=http://localhost:8000/api/callback/instagram
   ```

## Quick Setup Command

You can manually edit the `.env` file or use this template:

```bash
# In the project root directory
cat >> .env << 'EOF'
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:8000/api/callback/spotify
INSTAGRAM_APP_ID=your_instagram_app_id_here
INSTAGRAM_APP_SECRET=your_instagram_app_secret_here
INSTAGRAM_REDIRECT_URI=http://localhost:8000/api/callback/instagram
EOF
```

Then replace the placeholder values with your actual credentials.

## Important Notes

- **Never commit your `.env` file to git** (it's already in `.gitignore`)
- The redirect URIs must match exactly what you configure in the OAuth provider
- For production, you'll need to add production redirect URIs in the OAuth provider dashboards
- After adding credentials, **restart your backend server** for changes to take effect

