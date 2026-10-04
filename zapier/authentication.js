const testAuth = (z, bundle) => {
  // Normally you want to make a request to an endpoint that is either specifically
  // designed to test auth, or one that every user will have access to, such as a
  // "me" or "profile" endpoint.
  const promise = z.request({
    url: 'https://api.manus-ai.com/v2/me',
  });

  // This method can return any truthy value to indicate the credentials are valid.
  // Raise an error to show an error message.
  return promise.then((response) => response.data);
};

module.exports = {
  type: 'custom',

  // Define any fields this app requires. The fields are configured by the user when
  // they set up a connection (authentication) in the Zapier UI.
  fields: [
    {
      key: 'api_key',
      label: 'Manus.ai API Key',
      required: true,
      type: 'string',
      helpText:
        'Your Manus.ai API key. Find it in your Manus.ai account settings. Used as the `X-API-Key` header for all Manus.ai requests.',
    },
    {
      key: 'whatsapp_access_token',
      label: 'WhatsApp Access Token',
      required: false,
      type: 'string',
      helpText:
        'Optional. Access token for the WhatsApp Business Cloud API (Meta Graph API), required only if you use the "Send WhatsApp Message" action or the "New WhatsApp Message Received" trigger. Can also be supplied per-action via input fields.',
    },
    {
      key: 'whatsapp_phone_number_id',
      label: 'WhatsApp Phone Number ID',
      required: false,
      type: 'string',
      helpText:
        'Optional. The phone number ID associated with your WhatsApp Business account. Can also be supplied per-action via input fields.',
    },
  ],

  // The test method allows Zapier to verify that the credentials a user provides are valid.
  test: testAuth,

  // This template string can access all the data returned from the test method. `{{json.X}}`
  // will dump out the value of `X` into the connection label.
  connectionLabel: '{{json.name}}',
};
