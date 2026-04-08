# Instagram Graph API Endpoints — Inbox Collector

## Base URL

```
https://graph.facebook.com/v22.0
```

## Authentication

All requests include the access token as a query parameter or header:
```
?access_token={INSTAGRAM_ACCESS_TOKEN_{KEY}}
```

Required permissions: `instagram_manage_messages`, `instagram_manage_comments`, `pages_manage_metadata`, `pages_read_engagement`

## Endpoints Used

### 1. List DM Conversations
```
GET /{ig-user-id}/conversations
  ?platform=instagram
  &fields=id,updated_time,participants,messages{id,message,from,created_time,attachments}
  &limit=20
Response:
  {
    "data": [
      {
        "id": "t_123456789",
        "updated_time": "2026-04-07T10:30:00+0000",
        "participants": {
          "data": [
            { "id": "17841400123456789", "name": "John Smith", "username": "johnsmith" }
          ]
        },
        "messages": {
          "data": [
            {
              "id": "m_abc123",
              "message": "Hey, I saw your post about AI automation...",
              "from": { "id": "17841400123456789", "name": "John Smith" },
              "created_time": "2026-04-07T10:30:00+0000"
            }
          ]
        }
      }
    ],
    "paging": { "cursors": { "before": "...", "after": "..." }, "next": "..." }
  }
```

### 2. Messages in a Conversation
```
GET /{conversation-id}/messages
  ?fields=id,message,from,created_time,attachments
  &limit=50
Response:
  {
    "data": [
      {
        "id": "m_abc123",
        "message": "Hey, I saw your post...",
        "from": { "id": "17841400123456789", "name": "John Smith" },
        "created_time": "2026-04-07T10:30:00+0000",
        "attachments": {
          "data": [
            { "id": "att_1", "mime_type": "image/jpeg", "size": 45000 }
          ]
        }
      }
    ],
    "paging": { ... }
  }
```

### 3. Recent Media (Posts/Reels)
```
GET /{ig-user-id}/media
  ?fields=id,caption,media_type,timestamp,permalink,like_count,comments_count
  &limit=25
Response:
  {
    "data": [
      {
        "id": "17890012345678901",
        "caption": "5 ways AI can save your business 40 hours a week...",
        "media_type": "VIDEO",
        "timestamp": "2026-04-05T14:00:00+0000",
        "permalink": "https://www.instagram.com/p/ABC123/",
        "like_count": 142,
        "comments_count": 23
      }
    ],
    "paging": { ... }
  }
```

### 4. Comments on a Media Object
```
GET /{media-id}/comments
  ?fields=id,text,from,timestamp,like_count,replies{id,text,from,timestamp}
  &limit=50
Response:
  {
    "data": [
      {
        "id": "17890012345678902",
        "text": "This is exactly what we need! How do I get started?",
        "from": { "id": "17841400987654321", "username": "potential_lead" },
        "timestamp": "2026-04-05T15:30:00+0000",
        "like_count": 3,
        "replies": {
          "data": []
        }
      }
    ],
    "paging": { ... }
  }
```

## Pagination

All list endpoints use cursor-based pagination:
```json
{
  "paging": {
    "cursors": {
      "before": "abc123",
      "after": "def456"
    },
    "next": "https://graph.facebook.com/v22.0/..."
  }
}
```

Follow `paging.next` URL until it no longer appears.

## Rate Limits

- Instagram Graph API: 200 calls per user per hour
- If `error.code` is 4 or 17 → rate limited, back off and retry
- Use `limit` param to reduce number of API calls (fetch more per page)
- Space requests at least 1 second apart for safety

## 24-Hour DM Window

Instagram enforces a 24-hour messaging window for business accounts:
- Window opens when a user sends your account a DM
- You can reply within 24 hours of the user's last message
- After 24 hours, you cannot send a message (only human message tags work)
- The fetch script calculates `window_expires` = message timestamp + 24 hours

## Safety Reminder

**These are the ONLY endpoints this skill uses. All are GET requests.**

Never call:
- POST /{conversation-id}/messages (send DM) — that is Agent 2's job
- POST /{media-id}/comments (reply to comment) — that is Agent 2's job
- DELETE endpoints
- Any endpoint that modifies account state
