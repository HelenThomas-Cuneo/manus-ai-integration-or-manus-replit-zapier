# Zapier Integration

A Zapier Platform CLI app that integrates **Manus.ai** and the **WhatsApp Business Cloud API**
(Meta Graph API), enabling:

- Triggering Manus.ai tasks and goal decomposition from 6,000+ apps
- Receiving notifications when a Manus.ai task completes
- Sending WhatsApp messages from any Zap
- Triggering Zaps when a new WhatsApp message is received

## Actions (Creates)

| Key | Label | Description |
|---|---|---|
| `execute_task` | Execute Task | Executes a Manus.ai task given a goal, optional inputs and constraints. |
| `decompose_goal` | Decompose Goal | Decomposes a complex goal into actionable steps using Manus.ai. |
| `send_whatsapp_message` | Send WhatsApp Message | Sends a text message via the WhatsApp Business Cloud API. |

## Triggers

| Key | Label | Description |
|---|---|---|
| `task_completed` | Task Completed | Fires when a Manus.ai task finishes executing (REST Hook). |
| `whatsapp_message_received` | New WhatsApp Message Received | Fires when a new inbound WhatsApp message is received (REST Hook). |

## Authentication

Custom auth with the following fields:

| Field | Required | Description |
|---|---|---|
| `api_key` | Yes | Your Manus.ai API key, sent as the `X-API-Key` header. |
| `whatsapp_access_token` | No | Access token for the WhatsApp Business Cloud API. Required only to use `send_whatsapp_message`. |
| `whatsapp_phone_number_id` | No | Your WhatsApp Business phone number ID. Required only to use `send_whatsapp_message`, can be overridden per-action. |

No secrets are hardcoded anywhere in this app — all tokens are supplied via the Zapier connection
(`bundle.authData`) or, for non-sensitive values like the phone number ID, optionally via
per-action input fields.

## Setup

1. **Install dependencies**
   ```bash
   cd zapier/
   npm install
   ```

2. **Configure environment** (for local testing only; real credentials are entered by end users
   when they connect the Zapier integration)
   ```bash
   cp .env.example .env
   # Edit .env with your Manus.ai API key and/or WhatsApp credentials
   ```

3. **Test**
   ```bash
   npm test
   ```

4. **Validate** (structural + integration checks)
   ```bash
   npx zapier validate
   ```

5. **Register / deploy** (requires a Zapier Developer account)
   ```bash
   npx zapier login
   npx zapier register "Manus.ai Integration"
   npx zapier push
   ```

## WhatsApp Setup

1. Obtain a WhatsApp Business Cloud API access token and phone number ID from the
   [Meta for Developers](https://developers.facebook.com/) dashboard.
2. When connecting this integration in Zapier, fill in the optional `whatsapp_access_token` and
   `whatsapp_phone_number_id` connection fields.
3. Use the **Send WhatsApp Message** action in any Zap, providing the recipient's phone number and
   message text.
4. To trigger Zaps on inbound WhatsApp messages, use the **New WhatsApp Message Received** trigger.
   Inbound delivery requires your own webhook receiver (see `../replit/README.md`) configured in
   the Meta App dashboard, forwarding matching payloads to the Zap's hook URL.

### Example: send a WhatsApp message directly against the Graph API (for reference/testing)

```bash
curl -X POST "https://graph.facebook.com/v19.0/<PHONE_NUMBER_ID>/messages" \
  -H "Authorization: Bearer <WHATSAPP_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "messaging_product": "whatsapp",
    "to": "15551234567",
    "type": "text",
    "text": {"body": "Hello from Manus.ai + Zapier!"}
  }'
```
