# Social Plugin — Setup Guide

## Prerequisites

1. **Instagram Business or Creator account**
2. **Meta Developer App** (https://developers.facebook.com/)
3. Python 3.10+

## Step-by-Step Setup

### 1. Create a Meta App

1. Go to https://developers.facebook.com/
2. Create a new app with **Business** type
3. Add the **Instagram** product
4. Select **API setup with Instagram Login** (not the Facebook Login path)

### 2. Add Instagram Accounts as Testers

1. In the app dashboard, go to **App roles > Instagram Testers**
2. Add each Instagram account you want to connect
3. From each Instagram account, accept the tester invitation (Settings > Website permissions > Tester invites)
4. Back in the app dashboard, go to the **Instagram** section and add the accounts

### 3. Enable Webhooks

In the Instagram section of the app, enable webhook subscriptions for each connected account.

### 4. Switch App to Live Mode

This is critical. In Development mode, the comments endpoint returns empty data even when comments exist. Switch the app to **Live mode** in the app dashboard header.

### 5. Generate Tokens via OAuth Flow

The "Generate token" button in the app dashboard generates tokens with limited scopes. You need the full OAuth flow to get tokens with all permissions (especially `instagram_business_manage_comments`).

#### Build the OAuth URL

```
https://www.instagram.com/oauth/authorize?force_reauth=true&client_id={APP_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=instagram_business_basic,instagram_business_manage_messages,instagram_business_manage_comments,instagram_business_content_publish,instagram_business_manage_insights
```

Open this URL in a browser while logged into the target Instagram account. Authorize the app. You will be redirected to your redirect URI with a `?code=` parameter.

#### Exchange Code for Short-Lived Token

```bash
curl -X POST https://api.instagram.com/oauth/access_token \
  -d "client_id={APP_ID}" \
  -d "client_secret={APP_SECRET}" \
  -d "grant_type=authorization_code" \
  -d "redirect_uri={REDIRECT_URI}" \
  -d "code={CODE}"
```

Response includes `access_token` (short-lived) and `user_id` (your IG User ID).

#### Exchange for Long-Lived Token (60 Days)

```bash
curl -s "https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret={APP_SECRET}&access_token={SHORT_LIVED_TOKEN}"
```

This returns a long-lived token valid for 60 days.

### 6. Add to .env

```bash
# App credentials
INSTAGRAM_APP_ID=your_app_id
INSTAGRAM_APP_SECRET=your_app_secret

# Adam's personal account
INSTAGRAM_ACCESS_TOKEN_ACCOUNT_1=your_long_lived_token_here
INSTAGRAM_IG_USER_ID_ACCOUNT_1=your_ig_user_id_here

# {YOUR_COMPANY} account
INSTAGRAM_ACCESS_TOKEN_ACCOUNT_2=your_long_lived_token_here
INSTAGRAM_IG_USER_ID_ACCOUNT_2=your_ig_user_id_here
```

### 7. Token Refresh

Tokens last 60 days. To refresh, re-run the OAuth flow (Step 5) for each account. There is no silent refresh endpoint — user interaction is required.

## Important Gotchas

- **graph.instagram.com** is the correct base URL, NOT graph.facebook.com
- **Bearer header auth** (`Authorization: Bearer {token}`) is required, NOT `access_token` query parameter
- **IGAAS tokens** from the Instagram Login OAuth flow are what you need, NOT EAA-prefixed tokens from the Graph API Explorer
- **Live mode is required** for comments to return data — Development mode returns empty
- **The dashboard "Generate token" button** gives tokens with limited scopes — always use the full OAuth flow

## Required Permissions

| Permission | Purpose |
|------------|---------|
| `instagram_business_basic` | Read profile and media |
| `instagram_business_manage_messages` | Read and send DMs |
| `instagram_business_manage_comments` | Read and reply to comments |
| `instagram_business_content_publish` | Publish content |
| `instagram_business_manage_insights` | Read account insights |

## Adding a New Account

1. Create a folder in `accounts/` with the account key (e.g., `accounts/newaccount/`)
2. Copy `config.json` from an existing account and update:
   - `account_key` — matches the folder name
   - `display_name` — human-readable name
   - `env_token_key`, `env_ig_user_id_key` — unique env var names
   - `crm` — enable/disable CRM integration and set qualify fields
3. Write the strategy documents:
   - `brand-voice.md` — tone, language rules, emoji policy
   - `products.md` — what this account sells/promotes
   - `icp.md` — ideal customer profile
   - `conversation-strategy.md` — the core automation brain (DM flows, comment rules, edge cases)
4. Create a data file at `data/{account_key}/social-data.json` with empty contacts/conversations/comments
5. Run the OAuth flow (Step 5) for the new account and add env vars to `.env`

## Install Dependencies

```bash
pip install -r requirements.txt
```
