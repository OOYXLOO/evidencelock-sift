# EvidenceLock SIFT Video Upload Pack

Use this pack for the required public demo video upload. FIND EVIL's official rules require a public YouTube, Vimeo, or Youku video with audio narration; do not use the raw GitHub WebM as the official Devpost video field.

Narrated source video:

```text
docs/demo-video/evidencelock-sift-demo.webm
```

Public raw backup/source link, not the official Devpost video field:

```text
https://raw.githubusercontent.com/OOYXLOO/evidencelock-sift/main/docs/demo-video/evidencelock-sift-demo.webm
```

Embedded playback page:

```text
https://ooyxloo.github.io/evidencelock-sift/demo.html
```

## Upload Settings

- Visibility: unlisted or public. Do not use private, because judges must be able to view it without logging in.
- Audience: not made for kids.
- License: standard platform license is fine.
- Comments: optional.
- Monetization: off.
- Thumbnail: use `docs/proof-card.png` if the host allows a custom thumbnail.
- Description links: include the judge hub, repo, judge pack, and smoke test.
- Audio: verify the narration is audible before submitting.

## Title

```text
EvidenceLock SIFT: Verifier-First Protocol SIFT Triage Demo
```

## Description

```text
EvidenceLock SIFT is a verifier-first DFIR triage agent pattern for the FIND EVIL! hackathon. It lets an agent move quickly through evidence collection and report drafting, but blocks confirmed conclusions unless they are tied to evidence references, tool-call IDs, verifier correction, and integrity hashes.

Judge hub:
https://ooyxloo.github.io/evidencelock-sift/

Repository:
https://github.com/OOYXLOO/evidencelock-sift

Judge pack:
https://github.com/OOYXLOO/evidencelock-sift/blob/main/docs/judge_pack.md

Smoke test:
https://github.com/OOYXLOO/evidencelock-sift/blob/main/tools/judge_smoke_test.py

Honest scope: synthetic Windows EVTX-style vertical slice, no real victim data, no live full-disk SIFT workstation claim, no external LLM/API key required for the demo.
```

## Tags

```text
DFIR, incident response, SANS SIFT, Protocol SIFT, MCP, AI agent, verifier, evidence, security, hackathon
```

## Upload Checks

- The hosted video URL opens in a logged-out browser.
- The host does not require a password, account membership, or age gate.
- The video plays from the first frame and is not still processing.
- The narration audio is present and understandable.
- The title does not claim live SIFT workstation execution or real victim evidence.
- The description includes the honest scope boundary.
- The Devpost video field accepts the hosted URL.
- `https://ooyxloo.github.io/evidencelock-sift/demo.html` remains in the project links even after the hosted URL is accepted.

## If WebM Upload Fails

If the host refuses WebM, use a local screen recorder or video editor to export the same `docs/demo-recording-page.html` playback to MP4 with the same narration. Keep the same title, description, and honest-scope language above. Do not add private desktop, email, account, API key, payout, bank, tax, KYC, or identity-document footage.
