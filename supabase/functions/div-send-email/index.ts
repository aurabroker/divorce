import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "jsr:@supabase/supabase-js@2";

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Accept",
};

function esc(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

async function sendEmail(apiKey: string, payload: object): Promise<boolean> {
  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    console.error("Resend error:", await res.text());
  }
  return res.ok;
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: CORS });
  }

  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "Method not allowed" }), {
      status: 405,
      headers: { ...CORS, "Content-Type": "application/json" },
    });
  }

  let body: Record<string, string>;
  try {
    body = await req.json();
  } catch {
    return new Response(JSON.stringify({ error: "Invalid JSON" }), {
      status: 400,
      headers: { ...CORS, "Content-Type": "application/json" },
    });
  }

  const imie      = (body.imie      || "").trim();
  const telefon   = (body.telefon   || "").trim();
  const email     = (body.email     || "").trim();
  const temat     = (body.temat     || "").trim();
  const wiadomosc = (body.wiadomosc || "").trim();
  const domain    = (body.domain    || "").trim();
  const district  = (body.district  || "").trim();

  if (!imie || !telefon || !temat) {
    return new Response(JSON.stringify({ error: "Brak wymaganych pól" }), {
      status: 400,
      headers: { ...CORS, "Content-Type": "application/json" },
    });
  }

  // Zapis do bazy
  const supabase = createClient(
    Deno.env.get("SUPABASE_URL")!,
    Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!,
  );
  const { error: dbError } = await supabase.from("div_leads").insert({
    imie,
    telefon,
    email:     email     || null,
    temat,
    wiadomosc: wiadomosc || null,
    domain:    domain    || null,
    district:  district  || null,
    source_url: req.headers.get("referer") || null,
  });
  if (dbError) console.error("DB insert error:", dbError.message);

  const apiKey = Deno.env.get("div_RESEND_API_KEY")!;
  const sourceDomain = domain || "rozwod.waw.pl";

  // ── 1. Powiadomienie do kancelarii ──────────────────────────
  const rows = [
    ["Imię",        imie],
    ["Telefon",      telefon],
    ...(email     ? [["E-mail",       email]]     : []),
    ["Temat",       temat],
    ...(wiadomosc ? [["Wiadomość", wiadomosc]] : []),
    ...(district  ? [["Lokalizacja",  district]]  : []),
    ["Źródło",        sourceDomain],
  ]
    .map(([label, val]) =>
      `<tr><td style="padding:6px 16px 6px 0;font-weight:600;color:#555;white-space:nowrap;">${esc(label)}:</td>` +
      `<td style="padding:6px 0;">${esc(val)}</td></tr>`
    )
    .join("");

  const notifHtml = `<!DOCTYPE html><html><body style="font-family:sans-serif;font-size:15px;color:#222;max-width:600px;margin:0 auto;padding:24px;">
<h2 style="margin-bottom:4px;color:#1a3a5e;">Nowe zapytanie</h2>
<p style="margin-top:0;color:#666;font-size:13px;">Kancelaria Adwokacka Magdalena Idzik-Cieśla</p>
<table style="border-collapse:collapse;margin-top:16px;">${rows}</table>
<hr style="margin:24px 0;border:none;border-top:1px solid #eee;">
<p style="font-size:12px;color:#999;">Formularz na ${esc(sourceDomain)}</p>
</body></html>`;

  const notifOk = await sendEmail(apiKey, {
    from: "formularz@rozwod.waw.pl",
    to: ["kancelaria@idzik.org.pl"],
    subject: `Nowe zapytanie z ${sourceDomain} — ${temat}`,
    html: notifHtml,
    ...(email ? { reply_to: email } : {}),
  });

  if (!notifOk) {
    return new Response(JSON.stringify({ error: "Błąd wysyłki" }), {
      status: 500,
      headers: { ...CORS, "Content-Type": "application/json" },
    });
  }

  // ── 2. Potwierdzenie do klienta (jeśli podał e-mail) ────────
  if (email) {
    const confirmHtml = `<!DOCTYPE html>
<html lang="pl">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f5f5f5;font-family:'Helvetica Neue',Helvetica,Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#f5f5f5;padding:32px 16px;">
  <tr><td align="center">
    <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:#fff;border-radius:8px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.08);">

      <!-- Nagłówek -->
      <tr><td style="background:#8B5E1A;padding:28px 40px;">
        <p style="margin:0;color:rgba(255,255,255,.75);font-size:12px;letter-spacing:.08em;text-transform:uppercase;">Kancelaria Adwokacka</p>
        <h1 style="margin:4px 0 0;color:#fff;font-size:20px;font-weight:600;">Magdalena Idzik&#8209;Cieśla</h1>
      </td></tr>

      <!-- Treść -->
      <tr><td style="padding:36px 40px;">
        <h2 style="margin:0 0 12px;font-size:22px;color:#1a1a1a;">Dziękujemy, ${esc(imie)}!</h2>
        <p style="margin:0 0 20px;font-size:15px;line-height:1.7;color:#444;">
          Twoje zgłoszenie dotarło do naszej kancelarii.
          Oddzwonimy do Ciebie w ciągu <strong>2 godzin</strong> w dni robocze (8:00&#8211;18:00).
        </p>

        <!-- Podsumowanie zgłoszenia -->
        <table width="100%" cellpadding="0" cellspacing="0"
               style="background:#f9f6f1;border-radius:6px;padding:20px;margin-bottom:28px;font-size:14px;color:#333;">
          <tr><td style="padding:4px 0;"><strong>Temat:</strong></td><td style="padding:4px 0;">${esc(temat)}</td></tr>
          <tr><td style="padding:4px 0;"><strong>Telefon:</strong></td><td style="padding:4px 0;">${esc(telefon)}</td></tr>
          ${wiadomosc ? `<tr><td style="padding:4px 0;vertical-align:top;"><strong>Wiadomość:</strong></td><td style="padding:4px 0;">${esc(wiadomosc)}</td></tr>` : ""}
        </table>

        <p style="margin:0 0 8px;font-size:15px;line-height:1.7;color:#444;">
          Jeśli chcesz przyspieszyć kontakt, zadzwoń bezpośrednio:
        </p>
        <a href="tel:+48605089552"
           style="display:inline-block;background:#8B5E1A;color:#fff;text-decoration:none;
                  padding:12px 28px;border-radius:6px;font-size:15px;font-weight:600;
                  margin-bottom:28px;">
          &#128222; 605&#160;089&#160;552
        </a>

        <p style="margin:0;font-size:13px;color:#888;line-height:1.6;">
          Prosimy nie odpowiadać na tę wiadomość &#8212; skrzynka nie jest monitorowana.
          W sprawach pilnych proszę dzwonić lub pisać na
          <a href="mailto:kancelaria@idzik.org.pl" style="color:#8B5E1A;">kancelaria@idzik.org.pl</a>.
        </p>
      </td></tr>

      <!-- Stopka -->
      <tr><td style="background:#f0ebe0;padding:20px 40px;border-top:1px solid #e8e0d0;">
        <p style="margin:0;font-size:12px;color:#888;line-height:1.7;">
          <strong style="color:#555;">Kancelaria Adwokacka Magdalena Idzik-Cieśla</strong><br>
          ul. Bolkowska 2A/28, 01-466 Warszawa<br>
          <a href="https://${esc(sourceDomain)}" style="color:#8B5E1A;text-decoration:none;">${esc(sourceDomain)}</a>
        </p>
      </td></tr>

    </table>
  </td></tr>
</table>
</body></html>`;

    await sendEmail(apiKey, {
      from: "kancelaria@rozwod.waw.pl",
      to: [email],
      subject: "Potwierdzenie zgłoszenia — Kancelaria Idzik-Cieśla",
      html: confirmHtml,
    });
  }

  return new Response(JSON.stringify({ ok: true }), {
    status: 200,
    headers: { ...CORS, "Content-Type": "application/json" },
  });
});
