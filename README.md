# Manus.ai Integration Template

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Node.js 18+](https://img.shields.io/badge/node-18+-green.svg)](https://nodejs.org/)

A comprehensive template for integrating **Manus.ai** autonomous agent with **Replit** and **Zapier**. This repository provides ready-to-use code, configurations, and documentation to help you quickly build automation workflows powered by Manus.ai.

## 📋 Overview

This template includes two complete integration solutions:

### 🔧 Replit Integration
A Flask-based webhook receiver that can:
- Accept incoming webhooks from external services
- Execute Manus.ai tasks via API
- Decompose complex goals into actionable steps
- Deploy instantly on Replit with automatic scaling

### ⚡ Zapier Integration
A Zapier Platform CLI app that enables:
- Triggering Manus.ai tasks from 6,000+ apps
- Receiving notifications when tasks complete
- Building complex automation workflows
- No-code integration with popular tools

## 🚀 Quick Start

### Prerequisites

- **Manus.ai API Key** - [Request access](https://manus.im/)
- **Replit Account** - [Sign up](https://replit.com/) (for Replit integration)
- **Zapier Developer Account** - [Sign up](https://developer.zapier.com/) (for Zapier integration)

### Replit Integration

1. **Import to Replit**
   - Fork or import the `replit/` directory into Replit
   - Or click: [![Run on Replit](https://replit.com/badge/github/your-repo)](https://replit.com/)

2. **Configure Environment**
   - Add `MANUS_API_KEY` in Replit Secrets
   - Set `PORT` (optional, defaults to 5000)

3. **Run**
   - Click the "Run" button
   - Your webhook receiver is now live!

4. **Test**
   ```bash
   python example_usage.py
   ```

### Zapier Integration

1. **Install Dependencies**
   ```bash
   cd zapier/
   npm install
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your MANUS_API_KEY
   ```

3. **Register with Zapier**
   ```bash
   zapier login
   zapier register "Manus.ai Integration"
   ```

4. **Test**
   ```bash
   npm test
   ```

5. **Deploy**
   ```bash
   zapier push
   ```

## 📁 Repository Structure

```
manus-integration-template/
├── replit/                      # Replit integration
│   ├── main.py                 # Flask webhook receiver
│   ├── requirements.txt        # Python dependencies
│   ├── .replit                 # Replit configuration
│   ├── replit.nix             # Nix environment
│   ├── .env.example           # Environment template
│   ├── example_usage.py       # Usage examples
│   └── README.md              # Replit documentation
│
├── zapier/                      # Zapier integration
│   ├── index.js                # Main entry point
│   ├── authentication.js       # Auth configuration
│   ├── creates/                # Zapier actions
│   │   ├── execute_task.js    # Execute task action
│   │   ├── decompose_goal.js  # Decompose goal action
│   │   └── send_whatsapp_message.js  # Send WhatsApp message action
│   ├── triggers/               # Zapier triggers
│   │   ├── task_completed.js  # Task completion trigger
│   │   └── whatsapp_message_received.js  # Inbound WhatsApp message trigger
│   ├── test/                   # Test files
│   ├── package.json            # Node.js dependencies
│   ├── .env.example           # Environment template
│   └── README.md              # Zapier documentation
│
└── README.md                    # This file
```

## 🔌 API Endpoints

### Replit Webhook Receiver

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Service information |
| `/health` | GET | Health check |
| `/webhook` | POST | Receive webhooks |
| `/execute` | POST | Execute Manus.ai task |
| `/decompose` | POST | Decompose goal |
| `/whatsapp/webhook` | GET | Meta WhatsApp webhook verification handshake |
| `/whatsapp/webhook` | POST | Receive inbound WhatsApp messages |

### Example Request

```bash
curl -X POST https://your-repl.repl.co/execute \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Analyze Q2 sales data and create visualizations",
    "inputs": ["sales_data.csv"],
    "constraints": {"deadline": "2024-12-31T23:59:59"}
  }'
```

### Example: Send a WhatsApp Message (Graph API)

```bash
curl -X POST "https://graph.facebook.com/v19.0/<PHONE_NUMBER_ID>/messages" \
  -H "Authorization: Bearer <WHATSAPP_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "messaging_product": "whatsapp",
    "to": "15551234567",
    "type": "text",
    "text": {"body": "Hello from Manus.ai!"}
  }'
```

## 💬 WhatsApp Integration

Both halves of this template support WhatsApp Business Cloud API (Meta Graph API) messaging:

- **Replit**: `/whatsapp/webhook` handles Meta's verification handshake (`GET`) and inbound
  messages (`POST`), optionally forwarding received text to Manus.ai.
- **Zapier**: the `send_whatsapp_message` action sends messages, and the
  `whatsapp_message_received` trigger fires Zaps on inbound messages.

Required environment variables:

| Variable | Used by | Description |
|---|---|---|
| `WHATSAPP_ACCESS_TOKEN` | Replit | Access token for the WhatsApp Business Cloud API |
| `WHATSAPP_PHONE_NUMBER_ID` | Replit | Your WhatsApp Business phone number ID |
| `WHATSAPP_VERIFY_TOKEN` | Replit | Secret string used for the Meta webhook verification handshake |

The Zapier app does not use environment variables for these — instead, users enter
`whatsapp_access_token` and `whatsapp_phone_number_id` as optional fields when connecting the
integration (see [`zapier/README.md`](./zapier/README.md)).

## 🎯 Use Cases

### 1. Automated Report Generation
Trigger Manus.ai to generate weekly reports from multiple data sources, then automatically email them to stakeholders.

### 2. Customer Support Automation
Use webhooks to capture support tickets, analyze them with Manus.ai, and draft intelligent responses.

### 3. Content Creation Pipeline
Automate content generation for blogs, social media, and newsletters based on form submissions or scheduled triggers.

### 4. Data Analysis Workflows
Schedule regular data analysis tasks that pull from databases, analyze trends, and create visualizations.

### 5. WhatsApp-Driven Automation
Receive inbound WhatsApp messages, forward them to Manus.ai for analysis or response drafting, and
send WhatsApp replies — all from a single Zap.

## 🛠️ Configuration

### Environment Variables

#### Replit
```bash
MANUS_API_KEY=your_api_key_here
PORT=5000
WHATSAPP_ACCESS_TOKEN=your_whatsapp_access_token_here
WHATSAPP_PHONE_NUMBER_ID=your_whatsapp_phone_number_id_here
WHATSAPP_VERIFY_TOKEN=a_shared_secret_you_choose_for_webhook_verification
```

#### Zapier
```bash
MANUS_API_KEY=your_api_key_here
```
Zapier does not use environment variables for WhatsApp; `whatsapp_access_token` and
`whatsapp_phone_number_id` are entered as optional connection fields when the integration is
connected inside Zapier.

### Manus.ai API Configuration

- **Base URL**: `https://api.manus-ai.com`
- **Authentication**: API Key (Header: `X-API-Key`)
- **Rate Limits**: 500 req/min (Enterprise tier)
- **Compliance**: GDPR, HIPAA modes available

## 📚 Documentation

For detailed setup instructions, API reference, and troubleshooting:

- **[Integration Guide](./INTEGRATION_GUIDE.md)** - Complete walkthrough
- **[Replit README](./replit/README.md)** - Replit-specific docs
- **[Zapier README](./zapier/README.md)** - Zapier-specific docs

### External Resources

- [Manus.ai API Documentation](https://manus-ai.com/api-docs)
- [Replit Documentation](https://docs.replit.com/)
- [Zapier Developer Platform](https://developer.zapier.com/)

## 🧪 Testing

### Replit
```bash
python example_usage.py
```

### Zapier
```bash
npm test
zapier validate
```

## 🐛 Troubleshooting

### Common Issues

**Authentication Errors (401)**
- Verify API key is correctly set in environment variables
- Confirm API key is valid and not expired

**Rate Limit Exceeded (429)**
- Implement exponential backoff
- Consider upgrading subscription tier
- Batch requests when possible

**Webhook Not Receiving Data**
- Ensure Replit app is running
- Verify webhook URL is correct
- Test with curl or Postman

**Zapier Integration Not Appearing**
- Run `zapier integrations` to verify
- Try `zapier push` again
- Check for validation errors with `zapier validate`

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Manus.ai](https://manus.im/) - Autonomous AI agent platform
- [Replit](https://replit.com/) - Cloud development environment
- [Zapier](https://zapier.com/) - Automation platform

## 📞 Support

For questions or issues:

- **Manus.ai Support**: [help.manus.im](https://help.manus.im)
- **GitHub Issues**: [Create an issue](https://github.com/your-repo/issues)

## 🔗 Links

- [Manus.ai Website](https://manus.im/)
- [Manus.ai API Docs](https://manus-ai.com/api-docs)
- [Replit Platform](https://replit.com/)
- [Zapier Developer Platform](https://developer.zapier.com/)

---

**Built with ❤️ by the Manus.ai Community**

*Last Updated: October 13, 2025*

