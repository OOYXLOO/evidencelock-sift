# Demo Recording

The silent demo video is generated from `docs/demo-recording-page.html`.

Output:

- `docs/demo-video/evidencelock-sift-demo.webm`
- 1280 x 720
- Browser playback verified locally

Run:

```powershell
node tools/record_demo_webm.mjs
```

If Node cannot resolve Playwright in a bundled runtime, set `NODE_PATH` to a Node modules directory that contains `playwright` and `playwright-core`, then rerun the same command.

The generated video is safe to publish because it is rendered from local public project assets only. It does not contain credentials, email, API tokens, private incident data, or payout information.
