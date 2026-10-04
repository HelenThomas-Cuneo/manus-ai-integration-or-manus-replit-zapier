const MANUS_API_BASE_URL = 'https://api.manus-ai.com';

const executeTask = (z, bundle) => {
  const { goal, inputs, constraints } = bundle.inputData;

  const promise = z.request({
    url: `${MANUS_API_BASE_URL}/v2/execute`,
    method: 'POST',
    headers: {
      'X-API-Key': bundle.authData.api_key,
      'Content-Type': 'application/json',
    },
    body: {
      goal,
      inputs: inputs || [],
      constraints: constraints || {},
    },
  });

  return promise.then((response) => response.data);
};

module.exports = {
  key: 'execute_task',
  noun: 'Task',

  display: {
    label: 'Execute Task',
    description: 'Executes a task on Manus.ai given a goal, optional inputs and constraints.',
  },

  operation: {
    inputFields: [
      {
        key: 'goal',
        label: 'Goal',
        type: 'string',
        required: true,
        helpText: 'The task goal/description for Manus.ai to execute.',
      },
      {
        key: 'inputs',
        label: 'Inputs',
        type: 'string',
        required: false,
        list: true,
        helpText: 'Optional list of inputs for the task.',
      },
      {
        key: 'constraints',
        label: 'Constraints',
        type: 'string',
        dict: true,
        required: false,
        helpText: 'Optional constraints for the task (e.g. deadline).',
      },
    ],

    perform: executeTask,

    sample: {
      id: '12345',
      status: 'success',
      goal: 'Analyze Q2 sales data and create visualizations',
      result: 'Task completed successfully.',
    },

    outputFields: [
      { key: 'id', label: 'Task ID' },
      { key: 'status', label: 'Status' },
      { key: 'result', label: 'Result' },
    ],
  },
};
