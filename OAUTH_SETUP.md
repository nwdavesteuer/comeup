# OAuth Setup Instructions

**⚠️ IMPORTANT: Instagram and Spotify connections are now REQUIRED** to use the platform. You must set up OAuth credentials for both platforms before you can complete onboarding or generate content schedules.

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

**⚠️ IMPORTANT:** Instagram Basic Display API was deprecated in December 2024. You must use **Instagram Graph API** instead, which requires:
- An Instagram **Business** or **Creator** account (not personal)
- The Instagram account linked to a Facebook Page

### Step 1: Convert Your Instagram Account (if needed)

1. **Open Instagram app** on your phone
2. Go to **Settings** → **Account type and tools**
3. Select **Switch to Professional Account**
4. Choose **Business** or **Creator** (Business recommended)
5. **Link to a Facebook Page** (create one if you don't have one)

### Step 2: Set Up Facebook App

1. **Go to Facebook Developers**
   - Visit: https://developers.facebook.com/apps/
   - Log in with your Facebook account

2. **Create an App** (if you haven't already)
   - Click "Create App"
   - Select **"Business"** as the app type (or "Consumer" if Business isn't available)
   - Fill in app details

3. **Add Instagram Graph API Product**
   
   **Option A: From the main dashboard**
   - In your app dashboard, look for a big **"Add Product"** button or **"+"** icon (usually on the left sidebar or top)
   - Click it and search for **"Instagram Graph API"** or **"Instagram"**
   - Click **"Set Up"** or **"Add"** next to Instagram Graph API
   
   **Option B: If you don't see "Add Product"**
   - Go to **Settings** → **Basic** (in the left sidebar)
   - Scroll down to find **"Add Platform"** section
   - Or look for **"Products"** in the left sidebar menu
   
   **Option C: Direct link**
   - Try going directly to: `https://developers.facebook.com/apps/YOUR_APP_ID/instagram-basic-display/`
   - Replace `YOUR_APP_ID` with your actual App ID (found in Settings → Basic)
   
   **What to look for:**
   - The product might be called **"Instagram Graph API"**, **"Instagram"**, or **"Instagram Basic Display"**
   - Even if it says "Basic Display", it should work with Graph API endpoints

4. **Configure OAuth Settings**
   
   **Where to find it:**
   - Look in the left sidebar for **"Instagram Graph API"** or **"Instagram"** (under Products)
   - Click on it, then look for **"Basic Display"** or **"Settings"**
   - You should see a section for **"Valid OAuth Redirect URIs"** or **"OAuth Redirect URIs"**
   
   **If you can't find it:**
   - Try: **Settings** → **Basic** → Scroll down to **"Instagram App ID"** section
   - Or: **Products** → Look for any Instagram-related settings
   - The redirect URI field might be in a different location depending on your app setup
   
   **What to enter:**
   - Add: `http://localhost:8000/api/callback/instagram`
   - Click **"Save Changes"** or **"Add URI"**

5. **Get Your Credentials**
   - **App ID**: Visible in **Settings** → **Basic** (at the top)
   - **App Secret**: In **Settings** → **Basic** → Click **"Show"** next to App Secret

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
- The redirect URIs must match **exactly** what you configure in the OAuth provider (including http vs https, trailing slashes, etc.)
- After OAuth authorization, you will be redirected back to your dashboard automatically
- For production, you'll need to add production redirect URIs in the OAuth provider dashboards
- After adding credentials, **restart your backend server** for changes to take effect

## Troubleshooting

### Instagram redirects to Instagram page instead of your platform

If after authorizing Instagram you're stuck on Instagram's page instead of being redirected back:

1. **Check redirect URI configuration:**
   - Go to Facebook Developer Console > Your App > Instagram Basic Display > Settings
   - Ensure the redirect URI matches **exactly**: `http://localhost:8000/api/callback/instagram` (for development)
   - The URI must match character-for-character including protocol (http/https)

2. **Check app mode:**
   - If your app is in Development mode, only test users can authenticate
   - Add yourself as a test user in the Instagram Basic Display settings

3. **Verify environment variables:**
   - Ensure `INSTAGRAM_REDIRECT_URI` in your `.env` matches the redirect URI in Facebook Developer Console
   - Restart your backend server after changing environment variables

### Facebook can't verify callback URL or verify token

If Facebook shows an error "The callback URL or verify token couldn't be validated":

**For OAuth (What you actually need):**
- You only need to configure the **OAuth Redirect URI** in Instagram Basic Display settings
- Add: `http://localhost:8000/api/callback/instagram` to "Valid OAuth Redirect URIs"
- **You don't need webhooks for basic OAuth** - skip the webhook setup if you're just trying to connect accounts

**If you're setting up webhooks (optional):**
- Facebook can't reach `localhost` URLs from the internet
- For local development, you need to expose your server using a tool like **ngrok**:
  1. Install ngrok: `brew install ngrok` (Mac) or download from https://ngrok.com
  2. Start your backend server: `cd backend && uvicorn main:app --reload`
  3. In another terminal, run: `ngrok http 8000`
  4. Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)
  5. In Facebook Developers, use: `https://abc123.ngrok.io/api/callback/instagram/webhook`
  6. Verify Token: `comeup_instagram_webhook_verify_token_2024`
  7. Make sure your backend server is running when Facebook tries to verify

**Note:** For Instagram Basic Display OAuth, webhooks are **optional**. You only need the OAuth redirect URI to connect accounts.

### Spotify redirect issues

1. **Check redirect URI in Spotify Dashboard:**
   - Go to Spotify Developer Dashboard > Your App > Settings
   - Ensure the redirect URI is added and matches: `http://localhost:8000/api/callback/spotify` (for development)
   - You can add multiple redirect URIs (one for dev, one for production)

2. **Verify environment variables:**
   - Ensure `SPOTIFY_REDIRECT_URI` in your `.env` matches one of the URIs in Spotify Dashboard
   - Restart your backend server after changing environment variables

