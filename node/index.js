"use strict";

/**
 * FuseIQ Agent SDK — Connect any AI agent to FuseIQ in 3 lines.
 *
 * Usage:
 *   const { FuseIQAgent } = require('@fuseiq/agent-sdk');
 *   const agent = new FuseIQAgent({ apiKey: 'fk_live_xxx', name: 'My Agent' });
 *   await agent.heartbeat('online');
 */

const https = require('https');
const http = require('http');

class FuseIQAgent {
  /**
   * @param {Object} options
   * @param {string} options.apiKey - API key from fuseiq.io/settings/api-keys
   * @param {string} options.name - Display name in dashboard
   * @param {string} [options.agentId] - Stable ID for reconnection
   * @param {string} [options.framework='Custom'] - Agent framework name
   * @param {string} [options.baseUrl='https://fuseiq.io'] - API endpoint
   */
  constructor(options) {
    if (!options || !options.apiKey) {
      throw new Error('apiKey is required. Get one at fuseiq.io/settings/api-keys');
    }
    if (!options.name) {
      throw new Error('name is required');
    }

    this.apiKey = options.apiKey;
    this.name = options.name;
    this.agentId = options.agentId || crypto.randomUUID();
    this.framework = options.framework || 'Custom';
    this.baseUrl = (options.baseUrl || 'https://fuseiq.io').replace(/\/$/, '');
  }

  /**
   * Send a heartbeat to update agent status in the dashboard.
   * @param {'online'|'idle'|'busy'|'offline'} status - Agent status
   * @param {Object} [options]
   * @param {string} [options.task] - Current task description
   * @param {Object} [options.metadata] - Additional data
   * @returns {Promise<Object>}
   */
  async heartbeat(status = 'online', options = {}) {
    const payload = JSON.stringify({
      agent_name: this.name,
      status,
      framework: this.framework,
      metadata: {
        agent_id: this.agentId,
        task: options.task || '',
        ...(options.metadata || {}),
      },
    });

    for (let attempt = 0; attempt < 3; attempt++) {
      try {
        const resp = await this._request('/api/external/heartbeat', payload);
        return resp;
      } catch (err) {
        if (attempt === 2) return { success: false, error: err.message };
        await new Promise(r => setTimeout(r, 1000 * Math.pow(2, attempt)));
      }
    }
  }

  /**
   * Send a log message for this agent.
   * @param {string} message - Log line text
   * @returns {Promise<Object>}
   */
  async log(message) {
    const payload = JSON.stringify({
      agent_name: this.name,
      metadata: {
        agent_id: this.agentId,
        log: message,
      },
    });

    try {
      return await this._request('/api/external/heartbeat', payload);
    } catch (err) {
      return { success: false, error: err.message };
    }
  }

  _request(path, payload) {
    return new Promise((resolve, reject) => {
      const url = new URL(path, this.baseUrl);
      const transport = url.protocol === 'https:' ? https : http;

      const req = transport.request(
        url,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'x-api-key': this.apiKey,
            'User-Agent': 'fuseiq-agent-sdk/0.1.0',
            'Content-Length': Buffer.byteLength(payload),
          },
        },
        (res) => {
          let data = '';
          res.on('data', chunk => data += chunk);
          res.on('end', () => {
            try {
              resolve(JSON.parse(data));
            } catch {
              resolve({ success: false, error: 'Invalid response' });
            }
          });
        }
      );

      req.on('error', reject);
      req.write(payload);
      req.end();
    });
  }
}

module.exports = { FuseIQAgent };
