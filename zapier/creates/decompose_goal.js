const MANUS_API_BASE_URL = 'https://api.manus-ai.com';

const decomposeGoal = (z, bundle) => {
  const { goal, context } = bundle.inputData;

  const promise = z.request({
    url: `${MANUS_API_BASE_URL}/v2/decompose`,
    method: 'POST',
    headers: {
      'X-API-Key': bundle.authData.api_key,
      'Content-Type': 'application/json',
    },
    body: {
      goal,
      context: context || '',
    },
  });

  return promise.then((response) => response.data);
};

module.exports = {
  key: 'decompose_goal',
  noun: 'Goal',

  display: {
    label: 'Decompose Goal',
    description: 'Decomposes a complex goal into actionable steps using Manus.ai.',
  },

  operation: {
    inputFields: [
      {
        key: 'goal',
        label: 'Goal',
        type: 'string',
        required: true,
        helpText: 'The goal to decompose into executable steps.',
      },
      {
        key: 'context',
        label: 'Context',
        type: 'text',
        required: false,
        helpText: 'Optional context to help Manus.ai decompose the goal more accurately.',
      },
    ],

    perform: decomposeGoal,

    sample: {
      id: '67890',
      status: 'success',
      goal: 'Plan a marketing campaign for a new product launch',
      steps: ['Define target audience', 'Draft messaging', 'Schedule launch'],
    },

    outputFields: [
      { key: 'id', label: 'Goal ID' },
      { key: 'status', label: 'Status' },
      { key: 'steps[]', label: 'Step' },
    ],
  },
};
