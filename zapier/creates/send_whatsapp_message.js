const WHATSAPP_API_BASE_URL = 'https://graph.facebook.com/v19.0';

const sendWhatsappMessage = (z, bundle) => {
  const { to, message, phone_number_id } = bundle.inputData;

  // The access token is a sensitive credential and is intentionally only read
  // from the connection (bundle.authData), never collected as a per-action
  // input field. The phone number ID is not sensitive, so it can optionally be
  // overridden per-action if a Zap needs to send from a different number.
  const accessToken = bundle.authData.whatsapp_access_token;
  const phoneNumberId = phone_number_id || bundle.authData.whatsapp_phone_number_id;

  if (!accessToken) {
    throw new z.errors.Error(
      'A WhatsApp access token is required. Set it on the connection or provide it as an input field.',
      'InvalidAccessTokenError',
      400
    );
  }

  if (!phoneNumberId) {
    throw new z.errors.Error(
      'A WhatsApp phone number ID is required. Set it on the connection or provide it as an input field.',
      'InvalidPhoneNumberIdError',
      400
    );
  }

  const promise = z.request({
    url: `${WHATSAPP_API_BASE_URL}/${phoneNumberId}/messages`,
    method: 'POST',
    headers: {
      Authorization: `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
    body: {
      messaging_product: 'whatsapp',
      to,
      type: 'text',
      text: { body: message },
    },
  });

  return promise.then((response) => response.data);
};

module.exports = {
  key: 'send_whatsapp_message',
  noun: 'WhatsApp Message',

  display: {
    label: 'Send WhatsApp Message',
    description: 'Sends a text message via the WhatsApp Business Cloud API (Meta Graph API).',
  },

  operation: {
    inputFields: [
      {
        key: 'to',
        label: 'Recipient Phone Number',
        type: 'string',
        required: true,
        helpText:
          'The recipient phone number in international format without a leading "+" (e.g. 15551234567).',
      },
      {
        key: 'message',
        label: 'Message',
        type: 'text',
        required: true,
        helpText: 'The text message body to send.',
      },
      {
        key: 'phone_number_id',
        label: 'WhatsApp Phone Number ID',
        type: 'string',
        required: false,
        helpText:
          'Optional. Overrides the Phone Number ID configured on the connection, if you need to send from a different number.',
      },
    ],

    perform: sendWhatsappMessage,

    sample: {
      messaging_product: 'whatsapp',
      messages: [{ id: 'wamid.example' }],
    },

    outputFields: [
      { key: 'messaging_product', label: 'Messaging Product' },
      { key: 'messages[]id', label: 'Message ID' },
    ],
  },
};
