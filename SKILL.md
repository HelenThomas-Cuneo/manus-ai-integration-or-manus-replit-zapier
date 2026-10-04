---
name: manus-whatsapp-integration
description: Send and receive WhatsApp messages on behalf of Manus.ai tasks using the WhatsApp Business Cloud API (Meta Graph API), via either the Replit Flask webhook receiver or the Zapier Platform app in this repository. Use this skill when the user asks to send a WhatsApp message, set up a WhatsApp webhook/inbox, connect WhatsApp to Manus.ai, or automate WhatsApp with Zapier.
---

# Manus WhatsApp Integration

This skill wraps the WhatsApp Business Cloud API (Meta Graph API) integration contained in this
repository, available in two equivalent forms:

- **Replit** (`replit/`): a Flask webhook receiver with a `/whatsapp/webhook` route.
- **Zapier** (`zapier/`): a Zapier Platform CLI app with a `send_whatsapp_message` action and a
  `whatsapp_message_received` trigger.

Both read credentials from environment variables / connection fields — never hardcode a token.

## When to use this skill

- The user wants to **send a WhatsApp message** from an automation or from Manus.ai directly.
- The user wants to **receive inbound WhatsApp messages** and trigger a Manus.ai task from them.
- The user wants to **connect WhatsApp to Zapier** (6,000+ apps) via Manus.ai.
- The user is **setting up the Meta webhook verification handshake** for a WhatsApp Business app.

## Required credentials

| Variable | Description |
|---|---|
| `WHATSAPP_ACCESS_TOKEN` | Access token for the WhatsApp Business Cloud API |
| `WHATSAPP_PHONE_NUMBER_ID` | The phone number ID associated with the WhatsApp Business account |
| `WHATSAPP_VERIFY_TOKEN` | Shared secret used for Meta's webhook verification handshake (Replit only) |
| `MANUS_API_KEY` | Optional. Lets inbound WhatsApp messages be forwarded to Manus.ai as a task |

Get the access token and phone number ID from the [Meta for Developers](https://developers.facebook.com/)
dashboard under your WhatsApp Business app.

## Sending a WhatsApp message (direct Graph API call)

```bash
curl -X POST "https://graph.facebook.com/v19.0/<PHONE_NUMBER_ID>/messages" \
  -H "Authorization: Bearer <WHATSAPP_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "messaging_product": "whatsapp",
    "to": "<RECIPIENT_PHONE_NUMBER>",
    "type": "text",
    "text": {"body": "<MESSAGE_TEXT>"}
  }'
```

## Replit webhook receiver (`replit/main.py`)

- `GET /whatsapp/webhook` — Meta's verification handshake. Respond with `hub.challenge` when
  `hub.verify_token` matches `WHATSAPP_VERIFY_TOKEN`.
- `POST /whatsapp/webhook` — receives inbound WhatsApp messages and, if `MANUS_API_KEY` is set,
  forwards the message text to Manus.ai as a task via `execute_manus_task`.

Setup steps are documented in `replit/README.md`. Deploy by importing `replit/` into Replit,
configuring the four environment variables above as Secrets, and running `main.py`. The resulting
Callback URL to enter in the Meta App dashboard is:

```
https://<your-repl-name>.<your-username>.repl.co/whatsapp/webhook
```

## Zapier app (`zapier/`)

- `creates/send_whatsapp_message.js` — a Zapier action that sends a WhatsApp text message. Inputs:
  `to` (recipient phone number) and `message` (text body). The access token is read only from the
  Zapier connection (`whatsapp_access_token`), never as an action input, per security best
  practice; `phone_number_id` can optionally be overridden per-action.
- `triggers/whatsapp_message_received.js` — a REST Hook trigger that fires a Zap for each inbound
  WhatsApp message.

Setup, authentication fields, and more examples are documented in `zapier/README.md`.

## Notes

- Never hardcode secrets. Always read `WHATSAPP_ACCESS_TOKEN` / `WHATSAPP_PHONE_NUMBER_ID` /
  `WHATSAPP_VERIFY_TOKEN` from environment variables (Replit) or the Zapier connection fields.
- The existing Manus.ai integration (`/execute`, `/decompose`, `execute_task`, `decompose_goal`) is
  unaffected and can be combined with this skill to turn inbound WhatsApp messages into Manus.ai
  tasks.
