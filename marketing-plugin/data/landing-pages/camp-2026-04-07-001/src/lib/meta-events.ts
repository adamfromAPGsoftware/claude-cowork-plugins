function getCookie(name: string): string | undefined {
  const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
  return match ? decodeURIComponent(match[2]) : undefined;
}

function generateEventId(prefix: string): string {
  return `${prefix}_${Date.now()}_${Math.random().toString(16).slice(2)}`;
}

interface TrackEventOptions {
  eventName: "Lead" | "CompleteRegistration";
  email?: string;
  phone?: string;
}

export function trackMetaEvent({ eventName, email, phone }: TrackEventOptions) {
  const eventId = generateEventId(eventName.toLowerCase());

  // 1) Browser Pixel (with eventID for dedup)
  window.fbq?.("track", eventName, {}, { eventID: eventId });

  // 2) Server CAPI
  fetch("/api/meta-capi", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      eventName,
      eventId,
      email,
      phone,
      fbp: getCookie("_fbp"),
      fbc: getCookie("_fbc"),
      userAgent: navigator.userAgent,
    }),
  }).catch(() => {
    // CAPI failure shouldn't break the user experience
  });
}
