const should = require('chai').should();
const zapier = require('zapier-platform-core');

const App = require('../index');
const appTester = zapier.createAppTester(App);

describe('creates.send_whatsapp_message', () => {
  zapier.tools.env.inject();

  it('should throw if no access token is configured', async () => {
    const bundle = {
      authData: {},
      inputData: {
        to: '15551234567',
        message: 'Hello from WhatsApp!',
      },
    };

    let err;
    try {
      await appTester(App.creates.send_whatsapp_message.operation.perform, bundle);
    } catch (e) {
      err = e;
    }

    should.exist(err);
    err.message.should.contain('WhatsApp access token is required');
  });

  it('should throw if no phone number id is configured', async () => {
    const bundle = {
      authData: {
        whatsapp_access_token: 'fake-token',
      },
      inputData: {
        to: '15551234567',
        message: 'Hello from WhatsApp!',
      },
    };

    let err;
    try {
      await appTester(App.creates.send_whatsapp_message.operation.perform, bundle);
    } catch (e) {
      err = e;
    }

    should.exist(err);
    err.message.should.contain('WhatsApp phone number ID is required');
  });
});
