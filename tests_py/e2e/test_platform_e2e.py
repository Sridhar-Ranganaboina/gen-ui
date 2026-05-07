import json
import os
import unittest
import urllib.request
from threading import Thread
from services_py.api import create_server

class TestPlatformE2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['GENUI_API_TOKEN'] = 'dev-token'
        cls.server = create_server(0)
        cls.thread = Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        host, port = cls.server.server_address
        if host == '0.0.0.0':
            host = '127.0.0.1'
        cls.base = f"http://{host}:{port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def _post(self, path, payload, token='dev-token'):
        req = urllib.request.Request(
            self.base + path,
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
            method="POST",
        )
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())

    def _get(self, path, token='dev-token'):
        req = urllib.request.Request(self.base + path, headers={"Authorization": f"Bearer {token}"})
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())

    def test_health_readiness(self):
        with urllib.request.urlopen(self.base + '/healthz') as r:
            self.assertEqual(r.status, 200)
        with urllib.request.urlopen(self.base + '/readyz') as r:
            self.assertEqual(r.status, 200)

    def test_auth_required(self):
        with self.assertRaises(Exception):
            self._get('/v1/audit', token='wrong-token')

    def test_decision_event_audit_memory(self):
        req = {"appId":"employee-portal","channel":"web","surface":"employee-dashboard","slot":"dashboard-hero","employeeId":"E999","context":{"roleContext":{"isManager":False}}}
        status, decision = self._post('/v1/decisions/evaluate', req)
        self.assertEqual(status, 200)
        self.assertIn('decisionId', decision)

        status, _ = self._post('/v1/events/interactions', {"eventType":"dismiss","employeeId":"E999","slot":"dashboard-hero","timestamp":"2026-05-05T00:00:00Z","candidateId":decision['candidateId']})
        self.assertEqual(status, 202)

        status, memory = self._get('/v1/memory/E999')
        self.assertEqual(status, 200)
        self.assertIn(decision['candidateId'], memory['behavioralMemory']['recentDismissedCards'])

        status, audits = self._get(f"/v1/audit?decisionId={decision['decisionId']}")
        self.assertEqual(status, 200)
        self.assertEqual(len(audits), 1)

if __name__ == '__main__':
    unittest.main()
