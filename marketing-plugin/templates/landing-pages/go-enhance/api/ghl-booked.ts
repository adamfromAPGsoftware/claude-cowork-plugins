import type { VercelRequest, VercelResponse } from "@vercel/node";
import crypto from "crypto";

const PIXEL_ID = process.env.META_PIXEL_ID!;
const ACCESS_TOKEN = process.env.META_CAPI_TOKEN!;
const GHL_WEBHOOK_SECRET = process.env.GHL_WEBHOOK_SECRET;

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
  if (req.method !== "POST") return res.status(405).json({ ok: false });

  // Optional: verify webhook secret
  if (GHL_WEBHOOK_SECRET) {
    const secret = req.headers["x-webhook-secret"] || req.query.secret;
    if (secret !== GHL_WEBHOOK_SECRET) {
      return res.status(401).json({ ok: false, error: "Unauthorized" });
    }
  }

  try {
    const body = req.body ?? {};

    // Log the full GHL payload so we can debug field names
    console.log("GHL webhook body:", JSON.stringify(body, null, 2));

    // GHL webhook payload — extract email/phone
    // GHL may nest these differently; support common formats
    const email =
      body.email ||
      body.contact?.email ||
      body.contact_email ||
      body.data?.email;
    const phone =
      body.phone ||
      body.contact?.phone ||
      body.contact_phone ||
      body.data?.phone;

    // Also extract fbp, ip, userAgent from GHL attribution data
    const attribution = body.contact?.lastAttributionSource || body.contact?.attributionSource || {};
    const fbp = attribution.fbp;
    const fbc = attribution.fbc;
    const ip = attribution.ip;
    const userAgent = attribution.userAgent;
    const firstName = body.first_name;
    const lastName = body.last_name;
    const country = body.country;

    console.log("Extracted email:", email, "phone:", phone, "fbp:", fbp, "ip:", ip);

    if (!email && !phone) {
      return res.status(400).json({ ok: false, error: "No email or phone provided", receivedKeys: Object.keys(body) });
    }

    const em = normEmail(email);
    const ph = normPhone(phone);

    const eventId = `cr_ghl_${Date.now()}_${crypto.randomBytes(6).toString("hex")}`;

    const userData: Record<string, unknown> = {};
    if (em) userData.em = [sha256(em)];
    if (ph) userData.ph = [sha256(ph)];
    if (firstName) userData.fn = [sha256(firstName.trim().toLowerCase())];
    if (lastName) userData.ln = [sha256(lastName.trim().toLowerCase())];
    if (country) userData.country = [sha256(country.trim().toLowerCase())];
    if (fbp) userData.fbp = fbp;
    if (fbc) userData.fbc = fbc;
    if (ip) userData.client_ip_address = ip;
    if (userAgent) userData.client_user_agent = userAgent;

    const payload: Record<string, unknown> = {
      data: [
        {
          event_name: "CompleteRegistration",
          event_time: Math.floor(Date.now() / 1000),
          event_id: eventId,
          action_source: "website",
          user_data: userData,
        },
      ],
      access_token: ACCESS_TOKEN,
    };

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
    return res.status(200).json({
      ok: true,
      fb: json,
      debug: {
        emailFound: !!email,
        phoneFound: !!phone,
        userDataKeys: Object.keys(userData),
      },
    });
  } catch (e: unknown) {
    const message = e instanceof Error ? e.message : "Server error";
    return res.status(500).json({ ok: false, error: message });
  }
}
