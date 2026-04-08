# Instagram Messaging API Reference

## Base URL

`https://graph.instagram.com/v21.0`

## Authentication

`Authorization: Bearer {token}` header on every request.

Token type: IGAAS tokens obtained via the Instagram API with Instagram Login OAuth flow. These are NOT the EAA-prefixed tokens from Graph API Explorer, and NOT Page Access Tokens.

Do NOT use `access_token` as a query parameter — use the Bearer header.

## Endpoints

### POST /me/messages (or POST /{ig_user_id}/messages)

Send a message to a user.

**Headers:**
```
Authorization: Bearer {INSTAGRAM_ACCESS_TOKEN}
Content-Type: application/json
```

**Body:**
```json
{
  "recipient": { "id": "{IGSID}" },
  "message": { "text": "Hello" }
}
```

**Response:**
```json
{
  "recipient_id": "...",
  "message_id": "..."
}
```

**Requirement:** The recipient must have messaged you first within the last 24 hours.

### GET /{ig_user_id}/conversations

Returns list of conversation threads.

**Headers:**
```
Authorization: Bearer {INSTAGRAM_ACCESS_TOKEN}
```

**Fields:** participants, messages, updated_time

**Pagination:** cursor-based

### GET /{conversation_id}/messages

Returns messages in a thread.

**Headers:**
```
Authorization: Bearer {INSTAGRAM_ACCESS_TOKEN}
```

**Fields:** id, message, from, to, created_time

**Pagination:** cursor-based

## Critical Limitation: User-Initiated Only

You CANNOT message someone who has not messaged you first. This means:

- **Followers who have not DM'd you** — cannot message them
- **People who commented on your post** — cannot DM them (must prompt them to DM you instead)
- **People who liked your post** — cannot message them

The only people you can message are those who:

- DM you directly
- Reply to your Instagram Story
- Message you from a click-to-message ad

There is no workaround. The API enforces this restriction.

## 24-Hour Window

- Can only send messages to users who sent YOU a message in the last 24 hours
- Window resets each time the user sends a new message
- After the window expires, you cannot message them until they re-initiate
- Attempting to message outside the window returns an error

## Rate Limits

- 200 automated DMs per hour per account
- Exceeding pauses automation for 1 hour
- No account ban from official API rate limiting

## Required Permissions

- `instagram_business_basic`
- `instagram_business_manage_messages`

These permissions are granted via the Instagram API with Instagram Login OAuth flow, not via the Facebook Graph API permissions system.
