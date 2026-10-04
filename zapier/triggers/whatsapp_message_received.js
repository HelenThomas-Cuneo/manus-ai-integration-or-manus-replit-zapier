const subscribeHook = (z, bundle) => {
  // WhatsApp Business Cloud API webhooks are configured once, at the Meta App
  // level (Callback URL + Verify Token) - Meta does not support per-Zap target
  // URLs the way a typical REST Hook provider does. We record bundle.targetUrl
  // here so it can be wired up to whatever fan-out mechanism your webhook
  // receiver uses (e.g. a subscribers list consulted by /whatsapp/webhook); no
  // outbound call is required to "subscribe" on the WhatsApp Cloud API itself.
  return Promise.resolve({
    id: bundle.targetUrl,
    target_url: bundle.targetUrl,
  });
};

const unsubscribeHook = (z, bundle) => {
  // Mirrors performSubscribe: there is nothing to call on the WhatsApp Cloud
  // API side to "unsubscribe" a single Zap, since the webhook is configured
  // once at the Meta App level. Resolve so Zapier can clean up its own state.
  return Promise.resolve({ id: bundle.subscribeData && bundle.subscribeData.id });
};

const extractMessages = (payload) => {
  // Flattens the WhatsApp Cloud API's nested entry/changes/value structure into
  // a flat list of simple message objects Zapier can map fields from.
  const messages = [];

  if (!payload || !Array.isArray(payload.entry)) {
    return messages;
  }

  payload.entry.forEach((entry) => {
    (entry.changes || []).forEach((change) => {
      const value = change.value || {};
      (value.messages || []).forEach((message) => {
        messages.push({
          id: message.id,
          from: message.from,
          timestamp: message.timestamp,
          type: message.type,
          text: message.text && message.text.body,
        });
      });
    });
  });

  return messages;
};

const getWhatsappMessageReceived = (z, bundle) => {
  if (bundle.cleanedRequest) {
    // bundle.cleanedRequest is either the raw Meta webhook payload (if forwarded
    // as-is) or an already-flattened message (if the upstream webhook receiver
    // forwards one message per call). Handle both shapes.
    if (bundle.cleanedRequest.entry) {
      return extractMessages(bundle.cleanedRequest);
    }
    return [bundle.cleanedRequest];
  }

  // Fallback for "test this step": nothing to poll for since WhatsApp has no
  // list endpoint for historical inbound messages, so return an empty sample set.
  return [];
};

module.exports = {
  key: 'whatsapp_message_received',
  noun: 'WhatsApp Message',

  display: {
    label: 'New WhatsApp Message Received',
    description:
      'Triggers when a new inbound WhatsApp message is received via the WhatsApp Business Cloud API webhook.',
  },

  operation: {
    type: 'hook',

    performSubscribe: subscribeHook,
    performUnsubscribe: unsubscribeHook,
    perform: getWhatsappMessageReceived,
    performList: getWhatsappMessageReceived,

    sample: {
      id: 'wamid.example',
      from: '15551234567',
      timestamp: '1700000000',
      type: 'text',
      text: 'Hello from WhatsApp!',
    },

    outputFields: [
      { key: 'id', label: 'Message ID' },
      { key: 'from', label: 'Sender Phone Number' },
      { key: 'timestamp', label: 'Timestamp' },
      { key: 'type', label: 'Message Type' },
      { key: 'text', label: 'Message Text' },
    ],
  },
};
