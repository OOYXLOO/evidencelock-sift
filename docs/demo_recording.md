# Demo Recording

The silent demo video is generated from `docs/demo-recording-page.html`.

Output:

- `docs/demo-video/evidencelock-sift-demo.webm`
- 1280 x 720
- Browser playback verified locally
- Hosted-provider copy is in `docs/video_upload_pack.md`

Run:

```powershell
node tools/record_demo_webm.mjs
```

If Node cannot resolve Playwright in a bundled runtime, set `NODE_PATH` to a Node modules directory that contains `playwright` and `playwright-core`, then rerun the same command.

The generated video is safe to publish because it is rendered from local public project assets only. It does not contain credentials, email, API tokens, private incident data, or payout information.

If Devpost requires a YouTube, Vimeo, or Youku URL instead of a raw GitHub WebM, use `docs/video_upload_pack.md` for the exact title, description, tags, upload settings, logged-out checks, and MP4 fallback.
