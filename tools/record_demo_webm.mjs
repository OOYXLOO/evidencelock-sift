import fs from "node:fs/promises";
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const root = fileURLToPath(new URL("..", import.meta.url));
const demoPage = path.join(root, "docs", "demo-recording-page.html");
const narration = path.join(root, "docs", "demo-video", "evidencelock-sift-narration.wav");
const output = path.join(root, "docs", "demo-video", "evidencelock-sift-demo.webm");
const viewport = { width: 1280, height: 720 };
const chapterCount = 5;
const holdSeconds = 8;
const fps = 12;
const browserCandidates = [
  process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE,
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
  "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
].filter(Boolean);

async function findBrowserExecutable() {
  for (const candidate of browserCandidates) {
    try {
      await fs.access(candidate);
      return candidate;
    } catch {
      // Try the next browser candidate.
    }
  }
  return undefined;
}

async function readNarrationDataUrl() {
  try {
    const buffer = await fs.readFile(narration);
    return `data:audio/wav;base64,${buffer.toString("base64")}`;
  } catch (error) {
    if (error.code === "ENOENT") return null;
    throw error;
  }
}

async function captureChapterFrames(page) {
  const frames = [];
  const chapters = page.locator(".chapter");
  for (let index = 0; index < chapterCount; index += 1) {
    await chapters.nth(index).click();
    await page.waitForTimeout(250);
    const buffer = await page.screenshot({ fullPage: false, type: "png" });
    frames.push(`data:image/png;base64,${buffer.toString("base64")}`);
  }
  return frames;
}

async function encodeFrames(page, frames, narrationDataUrl) {
  return page.evaluate(
    async ({ frames: frameUrls, narrationDataUrl, width, height, holdSeconds, fps }) => {
      const mimeCandidates = ["video/webm;codecs=vp9", "video/webm;codecs=vp8", "video/webm"];
      const mimeType = mimeCandidates.find((candidate) => MediaRecorder.isTypeSupported(candidate));
      if (!mimeType) throw new Error("No supported MediaRecorder WebM MIME type is available.");

      const canvas = document.createElement("canvas");
      canvas.width = width;
      canvas.height = height;
      const context = canvas.getContext("2d");
      const canvasStream = canvas.captureStream(fps);
      let audioContext = null;
      let narrationSource = null;
      let audioDurationMs = 0;
      let stream = canvasStream;

      if (narrationDataUrl) {
        audioContext = new AudioContext();
        const audioBuffer = await fetch(narrationDataUrl)
          .then((response) => response.arrayBuffer())
          .then((buffer) => audioContext.decodeAudioData(buffer));
        const destination = audioContext.createMediaStreamDestination();
        narrationSource = audioContext.createBufferSource();
        narrationSource.buffer = audioBuffer;
        narrationSource.connect(destination);
        audioDurationMs = audioBuffer.duration * 1000;
        stream = new MediaStream([
          ...canvasStream.getVideoTracks(),
          ...destination.stream.getAudioTracks(),
        ]);
      }

      const chunks = [];
      const recorder = new MediaRecorder(stream, { mimeType, videoBitsPerSecond: 3_500_000 });
      recorder.ondataavailable = (event) => {
        if (event.data && event.data.size > 0) chunks.push(event.data);
      };

      const loadImage = (url) =>
        new Promise((resolve, reject) => {
          const image = new Image();
          image.onload = () => resolve(image);
          image.onerror = () => reject(new Error(`Could not load frame ${url.slice(0, 48)}...`));
          image.src = url;
        });
      const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
      const images = [];
      for (const frameUrl of frameUrls) images.push(await loadImage(frameUrl));

      recorder.start(250);
      if (audioContext) await audioContext.resume();
      if (narrationSource) narrationSource.start();

      const videoDurationMs = images.length * holdSeconds * 1000;
      const totalDurationMs = Math.max(videoDurationMs, audioDurationMs + 750);
      const totalFrames = Math.ceil((totalDurationMs / 1000) * fps);
      const framesPerImage = holdSeconds * fps;

      for (let frame = 0; frame < totalFrames; frame += 1) {
        const image = images[Math.min(Math.floor(frame / framesPerImage), images.length - 1)];
        context.fillStyle = "#eef4f8";
        context.fillRect(0, 0, width, height);
        context.drawImage(image, 0, 0, width, height);
        await wait(1000 / fps);
      }
      await new Promise((resolve) => {
        recorder.onstop = resolve;
        recorder.stop();
      });
      stream.getTracks().forEach((track) => track.stop());
      canvasStream.getTracks().forEach((track) => track.stop());
      if (audioContext) await audioContext.close();
      const blob = new Blob(chunks, { type: mimeType });
      return {
        hasAudio: Boolean(narrationDataUrl),
        mimeType,
        bytes: Array.from(new Uint8Array(await blob.arrayBuffer())),
      };
    },
    { frames, narrationDataUrl, width: viewport.width, height: viewport.height, holdSeconds, fps },
  );
}

async function main() {
  await fs.mkdir(path.dirname(output), { recursive: true });
  const executablePath = await findBrowserExecutable();
  const browser = await chromium.launch({ executablePath, headless: true });
  try {
    const page = await browser.newPage({ viewport });
    await page.goto(pathToFileURL(demoPage).href, { waitUntil: "load" });
    await page.waitForSelector(".chapter");
    const frames = await captureChapterFrames(page);
    const narrationDataUrl = await readNarrationDataUrl();
    const result = await encodeFrames(page, frames, narrationDataUrl);
    await fs.writeFile(output, Buffer.from(result.bytes));
    const stats = await fs.stat(output);
    console.log(JSON.stringify({ output, narration, hasAudio: result.hasAudio, mimeType: result.mimeType, bytes: stats.size }, null, 2));
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
