# WH-002B | Visual agent workbench

This is the first native n8n integration, not a general creative agent. Existing WH-001 runner, WH-002 graph, and source assets remain intact.

## Local entry points
- Creative chat: http://127.0.0.1:5678/webhook/nouscera-creative-workbench/chat
- Visual workflow editor: http://127.0.0.1:5678/workflow/NousceraWorkbench01 (local owner setup/sign-in may be required).
- Existing candidates: http://127.0.0.1:8770/compare
- Technical diagnostics: http://127.0.0.1:8765/

The native chat sends an objective to the real local DeepSeek model with scoped governing context. n8n routes its response to an independently allowlisted operation. The operation checks the context hash, refuses changed routes, persists a receipt and supplies direct links. Compare existing candidates, inspect current CP05 readiness, explicitly request a technical replay, or block an unsupported request. No new creative generation or approval. The workflows are actual registered operations, not arbitrary commands. No new media weights downloaded. The model cannot perform visual judgment.

The export nouscera-workbench.n8n.json is versioned. It requires local HTTP Header Auth credential named NOUSCERA local bridge, id NousceraLocalBridge, with a private key held by the bridge. Do not commit or print the key. The private local startup scripts and installation records are on the authorized workstation. n8n 2.20.0 runs isolated because installed Node 22 is incompatible with the latest n8n/Flowise release. n8n is fair-code rather than OSI open source. Docker engine unavailable. Dependency warnings include a deprecated dependency with an advisory: this is a local-only compatibility trial, not a production/security-certified deployment. Loopback bindings, no public tunnel, no arbitrary shell or file-path endpoints. Hosted chat is locally accessible without login; the editor may require initial owner setup. The local bridge opens only registered native masters as verified inspection copies. It does not modify original assets. ComfyUI workflow JSON and native canvas are linked; automatic native workflow import is not implemented. No user-specific account credentials have been created.

Recovery: read the private wh002b CHECKPOINT.md. Start the existing local model if needed, then bridge, then n8n using its isolated environment. Keep the original WH-002 console available for diagnostics. Do not replace the prior harness or change the frozen WH-001 contract merely to mark progress. Do not infer creative readiness. A durable next operation must explicitly reconstruct and verify the hidden paper in Krita/ComfyUI before a new animation.
