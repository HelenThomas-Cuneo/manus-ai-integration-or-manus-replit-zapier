# Replit Integration

A Flask-based webhook receiver that integrates with the Manus.ai API and the WhatsApp Business
Cloud API (Meta Graph API).

## Features

- Accept incoming webhooks from external services and trigger Manus.ai tasks
- Execute Manus.ai tasks directly via `/execute`
- Decompose complex goals into actionable steps via `/decompose`
- Receive inbound WhatsApp messages via `/whatsapp/webhook` and optionally forward them to Manus.ai

## Setup

1. **Import to Replit**
   - Import this `replit/` directory as a new Repl (Python).

2. **Configure environment variables** (Replit Secrets, or a local `.env` file copied from
   `.env.example`):

   | Variable | Required | Description |
   |---|---|---|
   | `MANUS_API_KEY` | For `/execute` and `/decompose` | Your Manus.ai API key |
   | `PORT` | No | Port the Flask app listens on (defaults to `5000`) |
   | `WHATSAPP_ACCESS_TOKEN` | For sending WhatsApp messages | Access token for the WhatsApp Business Cloud API |
   | `WHATSAPP_PHONE_NUMBER_ID` | For sending WhatsApp messages | Your WhatsApp Business phone number ID |
   | `WHATSAPP_VERIFY_TOKEN` | For `/whatsapp/webhook` | A secret string you choose and also enter in the Meta App dashboard webhook configuration |

3. **Run**
   - Click the "Run" button, or `python main.py`.

4. **Test**
   ```bash
   python example_usage.py
   ```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service information |
| `/health` | GET | Health check |
| `/webhook` | POST | Receive generic webhooks |
| `/execute` | POST | Execute a Manus.ai task |
| `/decompose` | POST | Decompose a goal into steps |
| `/whatsapp/webhook` | GET | Meta webhook verification handshake |
| `/whatsapp/webhook` | POST | Receive inbound WhatsApp messages |

### WhatsApp Setup (Meta for Developers)

1. Create a Meta App with the **WhatsApp** product added.
2. In **WhatsApp > Configuration**, set the Callback URL to
   `https://your-repl-name.your-username.repl.co/whatsapp/webhook` and the Verify Token to the same
   value as `WHATSAPP_VERIFY_TOKEN`.
3. Subscribe to the `messages` webhook field.
4. Note your **Phone number ID** and generate a **temporary or permanent access token** — set these
   as `WHATSAPP_PHONE_NUMBER_ID` and `WHATSAPP_ACCESS_TOKEN`.

### Example: verification handshake (performed automatically by Meta)

```bash
curl "https://your-repl-name.your-username.repl.co/whatsapp/webhook?hub.mode=subscribe&hub.verify_token=YOUR_VERIFY_TOKEN&hub.challenge=12345"
```

### Example: simulate an inbound WhatsApp message

```bash
curl -X POST https://your-repl-name.your-username.repl.co/whatsapp/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "entry": [{
      "changes": [{
        "value": {
          "messages": [{
            "id": "wamid.example",
            "from": "15551234567",
            "text": {"body": "Hello from WhatsApp!"}
          }]
        }
      }]
    }]
  }'
```

Inbound text messages are optionally forwarded to Manus.ai as a task (when `MANUS_API_KEY` is
configured); otherwise the webhook is simply acknowledged.
