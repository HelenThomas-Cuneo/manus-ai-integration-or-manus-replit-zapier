const authentication = require('./authentication');

const executeTask = require('./creates/execute_task');
const decomposeGoal = require('./creates/decompose_goal');
const sendWhatsappMessage = require('./creates/send_whatsapp_message');

const taskCompleted = require('./triggers/task_completed');
const whatsappMessageReceived = require('./triggers/whatsapp_message_received');

const addBearerHeader = (request, z, bundle) => {
  // Attach the Manus.ai API key header automatically to every outbound request
  // unless the request already defines its own headers (e.g. WhatsApp requests,
  // which use a different auth scheme).
  if (bundle.authData.api_key && !request.headers['X-API-Key']) {
    request.headers['X-API-Key'] = bundle.authData.api_key;
  }
  return request;
};

module.exports = {
  // This is just a shorthand to reference the installed dependencies you have.
  // Zapier will need to know this to allow for pre-installed dependencies to be
  // used with your app.
  version: require('./package.json').version,
  platformVersion: require('zapier-platform-core').version,

  authentication: authentication,

  beforeRequest: [addBearerHeader],

  afterResponse: [],

  resources: {},

  triggers: {
    [taskCompleted.key]: taskCompleted,
    [whatsappMessageReceived.key]: whatsappMessageReceived,
  },

  // If you want your creates to show up, you'll need to define them here.
  creates: {
    [executeTask.key]: executeTask,
    [decomposeGoal.key]: decomposeGoal,
    [sendWhatsappMessage.key]: sendWhatsappMessage,
  },

  searches: {},
};
