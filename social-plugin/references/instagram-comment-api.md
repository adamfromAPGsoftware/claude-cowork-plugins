# Instagram Comment API Reference

## Base URL

`https://graph.instagram.com/v21.0`

## Authentication

`Authorization: Bearer {token}` header on every request.

Token type: IGAAS tokens obtained via the Instagram API with Instagram Login OAuth flow. Do NOT use `access_token` as a query parameter — use the Bearer header.

## Endpoints

### GET /me/media (or GET /{ig_user_id}/media)

Returns list of recent media (posts, Reels, carousels).

**Headers:**
```
Authorization: Bearer {INSTAGRAM_ACCESS_TOKEN}
```

**Fields:** id, caption, media_type, timestamp, permalink

**Pagination:** cursor-based

### GET /{media_id}/comments

Returns comments on a media object.

**Headers:**
```
Authorization: Bearer {INSTAGRAM_ACCESS_TOKEN}
```

**Fields:** id, text, timestamp, username

**Pagination:** cursor-based

### POST /{comment_id}/replies

Post a reply to a comment.

**Headers:**
```
Authorization: Bearer {INSTAGRAM_ACCESS_TOKEN}
Content-Type: application/json
```

**Body:**
```json
{
  "message": "Your reply text here"
}
```

**Response:**
```json
{
  "id": "..."
}
```

## Required Permissions

- `instagram_business_basic`
- `instagram_business_manage_comments`

These permissions are granted via the Instagram API with Instagram Login OAuth flow.

## Notes

- **App must be in Live mode for comments to return data.** In Development mode, the comments endpoint returns empty results even when comments exist on the post. This is a known Meta behaviour — switch the app to Live mode to fix it.
- Comments on Reels use the same endpoints
- No documented rate limit for comment replies, but pace to avoid looking automated
- Can also hide/delete comments (not used in this plugin)
