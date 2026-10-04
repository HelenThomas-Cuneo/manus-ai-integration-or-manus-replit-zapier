const should = require('chai').should();
const zapier = require('zapier-platform-core');

const App = require('../index');
const appTester = zapier.createAppTester(App);

describe('triggers.whatsapp_message_received', () => {
  zapier.tools.env.inject();

  it('should flatten a raw WhatsApp Cloud API payload into message objects', async () => {
    const bundle = {
      cleanedRequest: {
        entry: [
          {
            changes: [
              {
                value: {
                  messages: [
                    {
                      id: 'wamid.example',
                      from: '15551234567',
                      timestamp: '1700000000',
                      type: 'text',
                      text: { body: 'Hello from WhatsApp!' },
                    },
                  ],
                },
              },
            ],
          },
        ],
      },
      inputData: {},
    };

    const results = await appTester(
      App.triggers.whatsapp_message_received.operation.perform,
      bundle
    );

    results.should.be.an('array');
    results.length.should.equal(1);
    results[0].id.should.equal('wamid.example');
    results[0].from.should.equal('15551234567');
    results[0].text.should.equal('Hello from WhatsApp!');
  });

  it('should return an empty array when testing without live data', async () => {
    const bundle = { inputData: {} };

    const results = await appTester(
      App.triggers.whatsapp_message_received.operation.performList,
      bundle
    );

    results.should.deep.equal([]);
  });

  it('performSubscribe should resolve with the target URL as the hook id', async () => {
    const bundle = {
      targetUrl: 'https://hooks.zapier.com/hooks/standard/123/abc',
      inputData: {},
    };

    const result = await appTester(
      App.triggers.whatsapp_message_received.operation.performSubscribe,
      bundle
    );

    result.id.should.equal(bundle.targetUrl);
  });
});
