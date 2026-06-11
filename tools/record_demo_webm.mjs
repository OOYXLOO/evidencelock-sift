import fs from "node:fs/promises";
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const root = fileURLToPath(new URL("..", import.meta.url));
const demoPage = path.join(root, "docs", "demo-recording-page.html");
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

async function encodeFrames(page, frames) {
  return page.evaluate(
    async ({ frames: frameUrls, width, height, holdSeconds, fps }) => {
      const mimeCandidates = ["video/webm;codecs=vp9", "video/webm;codecs=vp8", "video/webm"];
      const mimeType = mimeCandidates.find((candidate) => MediaRecorder.isTypeSupported(candidate));
      if (!mimeType) throw new Error("No supported MediaRecorder WebM MIME type is available.");

      const canvas = document.createElement("canvas");
      canvas.width = width;
      canvas.height = height;
      const context = canvas.getContext("2d");
      const stream = canvas.captureStream(fps);
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
      for (const image of images) {
        for (let frame = 0; frame < holdSeconds * fps; frame += 1) {
          context.fillStyle = "#eef4f8";
          context.fillRect(0, 0, width, height);
          context.drawImage(image, 0, 0, width, height);
          await wait(1000 / fps);
        }
      }
      await new Promise((resolve) => {
        recorder.onstop = resolve;
        recorder.stop();
      });
      stream.getTracks().forEach((track) => track.stop());
      const blob = new Blob(chunks, { type: mimeType });
      return { mimeType, bytes: Array.from(new Uint8Array(await blob.arrayBuffer())) };
    },
    { frames, width: viewport.width, height: viewport.height, holdSeconds, fps },
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
    const result = await encodeFrames(page, frames);
    await fs.writeFile(output, Buffer.from(result.bytes));
    const stats = await fs.stat(output);
    console.log(JSON.stringify({ output, mimeType: result.mimeType, bytes: stats.size }, null, 2));
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
