import type { VercelRequest, VercelResponse } from "@vercel/node";
import crypto from "crypto";

const PIXEL_ID = process.env.META_PIXEL_ID!;
const ACCESS_TOKEN = process.env.META_CAPI_TOKEN!;

function sha256(value: string): string {
  return crypto.createHash("sha256").update(value).digest("hex");
}

function normEmail(email?: string) {
  if (!email) return undefined;
  return email.trim().toLowerCase();
}

function normPhone(phone?: string) {
  if (!phone) return undefined;
  return phone.replace(/[^\d]/g, "");
}

export default async function handler(req: VercelRequest, res: VercelResponse) {
  // CORS headers
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST") return res.status(405).json({ ok: false });

  try {
    const { eventName, eventId, email, phone, fbp, fbc, userAgent } =
      req.body ?? {};

    if (!eventName || !eventId) {
      return res.status(400).json({ ok: false, error: "Missing eventName/eventId" });
    }

    // Get IP from Vercel headers (more reliable than client-sent)
    const ip =
      (req.headers["x-forwarded-for"] as string)?.split(",")[0]?.trim() ||
      req.socket?.remoteAddress;

    const em = normEmail(email);
    const ph = normPhone(phone);

    const userData: Record<string, unknown> = {};
    if (em) userData.em = [sha256(em)];
    if (ph) userData.ph = [sha256(ph)];
    if (fbp) userData.fbp = fbp;
    if (fbc) userData.fbc = fbc;
    if (ip) userData.client_ip_address = ip;
    if (userAgent) userData.client_user_agent = userAgent;

    const payload: Record<string, unknown> = {
      data: [
        {
          event_name: eventName,
          event_time: Math.floor(Date.now() / 1000),
          event_id: eventId,
          event_source_url: req.headers.referer || undefined,
          action_source: "website",
          user_data: userData,
        },
      ],
      access_token: ACCESS_TOKEN,
    };

    // Include test code if provided (for Meta Test Events tab)
    if (process.env.META_TEST_EVENT_CODE) {
      payload.test_event_code = process.env.META_TEST_EVENT_CODE;
    }

    const url = `https://graph.facebook.com/v21.0/${PIXEL_ID}/events`;
    const fbRes = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const json = await fbRes.json();
    return res.status(200).json({ ok: true, fb: json });
  } catch (e: unknown) {
    const message = e instanceof Error ? e.message : "Server error";
    return res.status(500).json({ ok: false, error: message });
  }
}
