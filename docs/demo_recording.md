# Demo Recording

The narrated demo video is generated from `docs/demo-recording-page.html`. If `docs/demo-video/evidencelock-sift-narration.wav` exists, `tools/record_demo_webm.mjs` muxes that audio into the WebM.

Output:

- `docs/demo-video/evidencelock-sift-demo.webm`
- 1280 x 720
- audio narration required for the final hosted YouTube/Vimeo/Youku upload
- Browser playback verified locally
- Hosted-provider copy is in `docs/video_upload_pack.md`

Run:

```powershell
node tools/record_demo_webm.mjs
```

Narration checklist:

- Keep the finished hosted video under five minutes.
- Show terminal execution or command/output snapshots.
- Include the self-correction sequence: unsafe draft rejected, corrected report accepted, manifest verifies.
- Verify audio is audible after upload in a logged-out browser.

If Node cannot resolve Playwright in a bundled runtime, set `NODE_PATH` to a Node modules directory that contains `playwright` and `playwright-core`, then rerun the same command.

The generated video is safe to publish because it is rendered from local public project assets only. It does not contain credentials, email, API tokens, private incident data, or payout information.

The official Devpost video field should use a public YouTube, Vimeo, or Youku URL. Use `docs/video_upload_pack.md` for the exact title, description, tags, upload settings, logged-out checks, and MP4 fallback.
