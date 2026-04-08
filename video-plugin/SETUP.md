# Video Plugin — Setup

## Required Credentials

### DeepGram (Transcription)
1. Sign up at https://deepgram.com
2. Create an API key with pre-recorded transcription access
3. Add to `.env` as `DEEPGRAM_API_KEY`

### OpenRouter (Visual Analysis)
1. Get an OpenRouter API key from https://openrouter.ai/keys
2. Used for vision model access (e.g. Gemini 2.5 Flash) for video frame analysis
3. Add to `.env` as `OPENROUTER_API_KEY`

### Hera Video (Motion Graphics)
1. Sign up at https://hera.video
2. Create an API key
3. Add to `.env` as `HERA_API_KEY`

### Supabase Storage (Reference Image Hosting)
1. Create a Supabase project at https://supabase.com
2. Add `SUPABASE_URL` and `SUPABASE_SERVICE_KEY` to `.env`
3. Used to host reference images for Hera Video API calls

## System Dependencies

- **FFmpeg** — `brew install ffmpeg` (must support arnndn filter for audio denoising)
- **Node.js** — Required for TypeScript tooling (`npx tsx`)
- **Python 3** — Required for Silero VAD (`pip3 install silero-vad`)

## Project Structure

Videos are processed within CCS project folders:
```
content/projects/{project-slug}/video-editor/
  video-ingest/     <- Drop raw 4K video files here
  raw/              <- Registry YAMLs (proxy/raw mappings)
  analysis/         <- Audio analysis, transcripts, visual analysis JSONs
  clips/            <- Clipped video files
  storyboard/       <- Storyboard documents
  broll/            <- Extracted B-roll clips
  motion-graphics/  <- Generated Hera MG clips
```
