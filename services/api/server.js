import http from 'node:http';
import { evaluateDecision } from '../orchestrator/service.js';
import { appendAudit, getAuditLog } from '../audit/service.js';
import { updateMemoryFromEvent } from '../memory/service.js';

function readJson(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', (c) => (body += c));
    req.on('end', () => { try { resolve(body ? JSON.parse(body) : {}); } catch (e) { reject(e); } });
  });
}

export function createServer() {
  return http.createServer(async (req, res) => {
    try {
      if (req.method === 'POST' && req.url === '/v1/decisions/evaluate') {
        const payload = await readJson(req);
        const decision = evaluateDecision(payload);
        appendAudit({ decisionId: decision.decisionId, employeeId: payload.employeeId, slot: payload.slot, reasonCodes: decision.reasonCodes });
        res.writeHead(200, { 'content-type': 'application/json' });
        return res.end(JSON.stringify(decision));
      }
      if (req.method === 'POST' && req.url === '/v1/events/interactions') {
        const event = await readJson(req);
        const memory = updateMemoryFromEvent(event);
        res.writeHead(202, { 'content-type': 'application/json' });
        return res.end(JSON.stringify({ status: 'accepted', memoryVersion: (memory.memoryVersion || 0) + 1 }));
      }
      if (req.method === 'GET' && req.url === '/v1/audit') {
        res.writeHead(200, { 'content-type': 'application/json' });
        return res.end(JSON.stringify(getAuditLog()));
      }
      res.writeHead(404).end();
    } catch {
      res.writeHead(400).end();
    }
  });
}
