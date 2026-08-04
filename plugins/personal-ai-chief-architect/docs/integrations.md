# Integration contract

The package defines an integration boundary, not a bundled credential broker. Configure reviewed MCP servers/adapters for:

| Service | Role | Default access | Sensitive writes |
|---|---|---|---|
| Telegram | conversation channel | receive, draft | send message |
| Gmail | inbox and threads | read | send/archive/delete |
| Google Calendar | agenda and meeting context | read | create/update/cancel |
| Google Drive | document storage | read | create/update/delete |
| GitHub | engineering source | read, draft branch/PR | push, submit, merge |

Required environment variables are named in `.mcp.json`. Use a dedicated service account or OAuth client with the smallest scopes, rotate tokens, and keep `.env` outside git. The included adapter is deliberately non-networking until replaced and reviewed.
