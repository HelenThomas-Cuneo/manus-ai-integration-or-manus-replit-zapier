const subscribeHook = (z, bundle) => {
  // In a REST Hook subscription, Zapier passes along a URL that is a unique hook
  // for this specific Zap. Manus.ai is asked to call that URL whenever a task completes.
  const promise = z.request({
    url: 'https://api.manus-ai.com/v2/hooks/subscribe',
    method: 'POST',
    headers: {
      'X-API-Key': bundle.authData.api_key,
      'Content-Type': 'application/json',
    },
    body: {
      target_url: bundle.targetUrl,
      event: 'task.completed',
    },
  });

  return promise.then((response) => response.data);
};

const unsubscribeHook = (z, bundle) => {
  const hookId = bundle.subscribeData.id;

  const promise = z.request({
    url: `https://api.manus-ai.com/v2/hooks/${hookId}`,
    method: 'DELETE',
    headers: {
      'X-API-Key': bundle.authData.api_key,
    },
  });

  return promise.then((response) => response.data);
};

const getTaskCompleted = (z, bundle) => {
  // Zapier will call this function for both subscription notifications (via the
  // inbound webhook payload in bundle.cleanedRequest) and in a "test this step" context.
  if (bundle.cleanedRequest) {
    // This should emit an array of objects.
    return [bundle.cleanedRequest];
  }

  // If someone clicks "test this step", this fallback lets them pull recent task
  // completions so the REST Hook payload can be confirmed/mapped.
  const promise = z.request({
    url: 'https://api.manus-ai.com/v2/tasks',
    params: { status: 'completed', limit: 3 },
    headers: {
      'X-API-Key': bundle.authData.api_key,
    },
  });

  return promise.then((response) => response.data.tasks || []);
};

module.exports = {
  key: 'task_completed',
  noun: 'Task',

  display: {
    label: 'Task Completed',
    description: 'Triggers when a Manus.ai task finishes executing.',
  },

  operation: {
    type: 'hook',

    performSubscribe: subscribeHook,
    performUnsubscribe: unsubscribeHook,
    perform: getTaskCompleted,

    // In cases where Zapier needs to show users a list of sample results, the
    // sample can come from performList (polling fallback) rather than live data.
    performList: getTaskCompleted,

    sample: {
      id: '12345',
      status: 'completed',
      goal: 'Analyze Q2 sales data and create visualizations',
      result: 'Task completed successfully.',
      completed_at: '2024-01-01T00:00:00.000Z',
    },

    outputFields: [
      { key: 'id', label: 'Task ID' },
      { key: 'status', label: 'Status' },
      { key: 'goal', label: 'Goal' },
      { key: 'result', label: 'Result' },
      { key: 'completed_at', label: 'Completed At' },
    ],
  },
};
