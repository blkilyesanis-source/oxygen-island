# Oxygen Island — Reservation & Loyalty Platform
### Project Context for Claude Code (handoff document)

> **What this is:** the build context for turning the existing single-file HTML prototype into a real, production reservation + admin platform for *Oxygen Island*, a premium artificial-beach club near Algiers. Built by **Numidea Labs** (agency) for the venue owner.
>
> **How to use this file:** drop it in the repo root (rename to `CLAUDE.md` so Claude Code auto-loads it). Keep the prototype HTML in `/reference/prototype.html` — it is the **visual source of truth**. This doc is the **spec**; the prototype is the **render**.
>
> **Golden rule:** prices, menu, and the brand asset are real where marked `[REAL]` and provisional where marked `[CONFIRM]`. Do **not** invent commercial numbers. Anything `[CONFIRM]` must be verified with the owner before launch.

---

## 0. TL;DR — what to build

A bilingual-ready (FR-first) web app with two surfaces:

1. **Public site** (4 pages): présentation, offres, restauration/menu, réservation. Premium dark-lagoon aesthetic. The reservation page is a live **devis builder** → submits via WhatsApp deep link → persists to DB → issues a **QR pass**.
2. **Admin "Espace Pro"** (auth-gated): live reservation queue, confirm action, an **upsell engine** (≥ 20 000 DA → free gift), KPIs, and a **rechargeable client card / loyalty wallet** with spend history and per-card QR.

The prototype already demonstrates the full UX and the client↔admin loop using in-memory JS. Production = same UX, real backend, real persistence, real auth.

---

## 1. Business context (why this exists)

**The venue.** Oxygen Island — Algiers' **first artificial beach** (opened 2023), a man-made lagoon + pools + bar/DJ set inside the **forêt de Bouchaoui, Chéraga**. Sells *a premium day*, not a product. Revenue = footfall × spend-per-head, with F&B and VIP/bed/event packages as the margin engine. Strong organic TikTok/Instagram reach; near-zero CAC.

**The strategic thesis (drives every product decision).**
- The brand **outruns the operation**: hype is high, delivery (cleanliness, service, pricing transparency) lags. Public reviews trend toward *"premium image, neglected reality, cash-machine, no reinvestment."*
- The venue is **100% dependent on Instagram** — an account it doesn't own — and on **manual DM/WhatsApp** handling. Demand isn't the problem; **systems** are.
- Therefore the platform's job is **not** "a pretty website." It is: stop revenue leaking from unanswered DMs, **own the client data** (de-risk Instagram), raise **panier moyen** via in-flow upsell, and give the owner **visibility + control** without being the bottleneck. The admin dashboard *is* the product; the public site is the funnel into it.

**Implication for Claude Code:** when trade-offs arise, favor the features that produce **owned client data + owner visibility + upsell** over cosmetic polish. The dashboard's "confirm → card updates" loop is the core value, not the hero animation.

---

## 2. Real data — single source of truth

Seed the DB / config from this section.

### 2.1 Identity & contact `[REAL]`
| Field | Value |
|---|---|
| Name | Oxygen Island |
| Tagline (local) | *« Le lagon caché au cœur de la forêt de Bouchaoui »* |
| Positioning | 1ʳᵉ plage artificielle d'Alger · depuis 2023 |
| Address | Forêt de Bouchaoui (Bouchaoui 3), Chéraga, Alger 16084, Algérie |
| Coordinates | `36.768067, 2.9075566` |
| Phones | 0660 05 65 83 (main), 0560 34 34 22, 0560 71 09 27 |
| WhatsApp (intl) | `213660056583` |
| Email | contact@oxygen-island.com |
| Instagram | https://www.instagram.com/oxygenisland |
| Facebook | https://www.facebook.com/profile.php?id=61575716741025 |
| Hours | Daily 10:00–19:30 · Afterwork from 16:00 · Friday kids' shows |
| Domain (likely) | oxygen-island.com `[CONFIRM]` |

### 2.2 Offers — "La Journée" `[REAL — 2025 grid, re-confirm before launch]`
| Offer | Price (DZD) | Unit |
|---|---|---|
| Accès individuel | 8 500 | per person |
| Formule couple | 10 000 | per 2 |
| Enfant | 4 000 | per child |
| Bed (2 pers.) | 20 000 | per bed |
| Afterwork (from 16:00) | 4 000 | per person |

### 2.3 Offers — "Événements & Privatisation" `[REAL categories, pricing = sur devis]`
`Anniversaire` · `Soirée DJ / Événement` · `Journée privée — Particuliers` · `Journée privée — Entreprises` (séminaires, team-building, afterworks corporate). All quote-based; capture: type, date, headcount, organisation (if corporate), free-text project.

### 2.4 Menu `[ITEMS real-ish, PRICES illustrative — CONFIRM]`
Categories confirmed from listings: **Burgers & Grillades, Sushis, Boissons & Rafraîchissements, Desserts**. Sample items used in prototype (replace prices): Burger maison 1 500, Assiette grillades 2 500, Tacos poulet 1 300, California roll 1 600, Plateau sushi 24p 3 800, Cocktail signature 1 200, Jus frais 800, Soda 400, Eau 200, Glace 600, Salade de fruits 650.

### 2.5 Gift / upsell rule `[PROPOSED — owner sign-off needed]`
Config-driven: **`gift_threshold_da = 20000`**, **`gift_label = "Cocktail signature offert"`**. When a day-reservation total ≥ threshold → gift unlocked (per the rule; consider per-guest scaling). Below threshold → show the gap nudge on the client devis *and* a "propose +X DA" recommendation in the admin queue.

### 2.6 Loyalty tiers `[PROPOSED]`
By cumulative seasonal spend (DZD): `Découverte < 20 000` · `Argent 20 000–49 999` · `Or 50 000–99 999` · `Platine ≥ 100 000`. Tiers are derived, not stored.

### 2.7 Brand asset — logo ⚠️
The owner's logo is **illustrated raster art** (palms/island/sun, bubble "OXYGEN Island" wordmark) on a **white background**. In the prototype it's cleaned (Windows watermark removed), trimmed, compressed to JPEG, and embedded once as a CSS variable `--logo` (data URI), displayed inside white circular "medallion" chips so the white background reads as intentional.
- **Production need:** request a **vector (SVG) and/or transparent-PNG** version, ideally a **horizontal lockup + a mark-only** variant, so it can sit on dark surfaces and scale crisp. If unavailable, scope a small **logo cleanup/vectorization** task (good cheap trust-builder for the pitch).
- **Design tension (intentional):** the logo is playful/cartoon; the site is premium/restrained. Treatment = "jewel in a premium setting" — show the mark sparingly with breathing room; do **not** let cartoon-tropical styling take over the UI.

---

## 3. The prototype (current state)

- **Location:** `/reference/prototype.html` (single self-contained file, ~140 KB incl. embedded logo).
- **Stack:** vanilla HTML + CSS + JS. One CDN dep: `qrcodejs` (QR generation). Fonts: Google Fonts (Fraunces + Manrope). No backend; all state in-memory (resets on reload).
- **Structure:** SPA-style page switcher (`go(id)` toggles `.page.live`). Pages: `#accueil`, `#offres`, `#restauration`, `#reservation`, `#admin`. Two modals: `#passModal` (client reservation QR), `#cardModal` (admin wallet card).
- **Client↔admin loop:** `sendWhatsApp()` builds a `wa.me` message, opens it, then `pushReservation(info)` injects the reservation into the admin queue (`reservations[]`), and `showPass()` renders the client QR. Admin `confirmRes()` posts spend to the matching card and recomputes tier.
- **Known prototype shortcuts (to replace in prod):** in-memory arrays seeded with mock data; `prompt()` for recharge; QR encodes a plain text summary (not a signed token); WhatsApp is one-way deep link; reviews + KPIs + 7-day fill chart are seeded/mock.

Treat the prototype as the **definitive UX + copy + visual reference**. Re-implement, don't re-imagine.

---

## 4. Product spec — features

### 4.1 Public site — pages
1. **Accueil:** cinematic hero (animated lagoon/caustics + palm SVG), logo medallion, real tagline + "depuis 2023" stats, "Notre Histoire" block, **6 univers cards** (Plage artificielle, Beds & lounge, Soirées DJ & afterwork, Anniversaires & spectacles, Privatisation & entreprises, Restauration — each with an inline SVG icon, **no emoji as structural icons**), **site plan** (custom SVG map: lagon, beds, bar/DJ, restaurant, WC, accueil, admin, parking), **itinéraire** (Google Maps directions deep link to coords), **avis feed** + "laisser un avis" form.
2. **Offres:** two groups — *La Journée* (priced cards, "Ajouter au devis") and *Événements & Privatisation* (sur-devis cards → route to reservation in event mode). Transparent pricing; "no hidden fees" framing.
3. **Restauration:** menu by category, each item has a "+" to add to the devis.
4. **Réservation:** Journée/Événement segmented toggle. Journée: date, guests, name, phone, quick-pick offers, items carried from menu. Événement: type, date, headcount, organisation, project textarea. Sticky **devis** panel: live line items, live total (DZD), gift nudge, WhatsApp submit.

### 4.2 Reservation / devis flow
Client composes devis → submit. Submit must: (a) persist reservation + items, (b) generate a unique `ref` (e.g., `OXI-XXXXX`), (c) notify the venue (phase 1: `wa.me` prefilled message; phase 2: WhatsApp Cloud API template + dashboard realtime), (d) issue a QR pass to the client, (e) appear in the admin queue as `pending`.

### 4.3 Gift / upsell engine
Pure function of total vs `gift_threshold_da`. Surfaces in **two places**: client devis (live "plus que X DA…" / "débloqué") and admin queue (per-row recommendation chip). Config-driven so the owner can change threshold/label without a deploy.

### 4.4 QR pass
Issued on submit (or on confirm — decide, see §9). Encodes a **signed token** resolving to the reservation (ref, client, date, guests, items, total/sur-devis). Staff scan to validate at entry/zones (phase 3 scanner PWA). Prototype encodes plain text — **upgrade to signed token** (JWT or HMAC'd opaque id) in prod.

### 4.5 Loyalty card / rechargeable wallet
On first confirmed reservation, issue a **card** (number + QR token) tied to the client. Card holds: **balance** (rechargeable), **cumulative spend** (→ tier), **experience history** (one entry per confirmed visit: date, label, amount). Admin can **recharge** (credit) and view the wallet card (front + QR + history). ⚠️ See §8 on stored-value regulation — treat balance as **prepaid credit usable on-site**, not a general wallet, and confirm legal basis before enabling top-ups with real money.

### 4.6 Admin "Espace Pro" dashboard
Auth-gated. Components: **4 KPIs** (pending / confirmed / revenu confirmé / remplissage du jour), **incoming-requests queue** (client, ref/date/guests, total, upsell reco, status, action), **Confirmer** action (pending→confirmed, posts spend to card), **7-day fill chart**, **client cards grid** (tier, balance, cumulative, → wallet modal with QR + history + recharge). Realtime-friendly (new reservations should appear without manual refresh).

### 4.7 Maps
- **Itinerary:** `https://www.google.com/maps/dir/?api=1&destination=36.768067,2.9075566` (opens directions from user location). Keep as deep link; optionally embed Google Maps JS later.
- **Site plan:** hand-drawn **SVG** in the prototype (not a real map). Keep as a styled SVG/illustrated plan, or replace with a designed plan from the owner. Labels: lagon, beds, bar/DJ, restaurant, WC, accueil, admin, parking.

### 4.8 Reviews feed
Manual reviews (site form → moderation → publish) + intended **import from Google/Instagram/Facebook** for credibility. Prototype reviews are placeholder personas — do **not** ship fabricated reviews; wire real sources or owner-supplied testimonials. Doubles as an owner feedback channel ("voice of customer" → optimize ops).

---

## 5. Design system

Port these tokens verbatim (CSS vars from the prototype `:root`):

```css
--abyss:#04211d; --abyss-2:#072b26; --ink:#03110f;     /* forest-night backgrounds */
--lagoon:#19c2b1; --lagoon-deep:#0a6b62; --lagoon-glow:#3fe6d4; /* aqua signature */
--sand:#ece0c8; --sand-dim:#b9b09b;                    /* warm light text */
--gold:#cba85a; --amber:#e9a23b;                       /* premium accent + logo sun */
--mist:#f3f8f6; --line:rgba(236,224,200,.14);
--r:18px; --shadow:0 30px 80px -30px rgba(0,0,0,.7);
```

- **Type:** Display = **Fraunces** (serif, optical sizing, characterful). Body/UI = **Manrope**. Eyebrow labels = uppercase, tracked.
- **Signature elements:** animated lagoon caustics/ripple in hero; palm-silhouette SVG; gold-hairline white "medallion" for the logo; "tide line" gradient dividers.
- **Motion:** 150–350 ms transitions; full `prefers-reduced-motion` reset already in prototype — preserve it.
- **A11y baseline (already in prototype, keep/extend):** `:focus-visible` rings, ≥44–46 px touch targets, `Escape` closes modals, ARIA labels on icon-only controls, **SVG icons (never emoji) as structural icons**, contrast on dark backgrounds.
- **Responsive:** desktop-first, single-column collapse < 900 px / < 620 px; sticky devis becomes static on mobile.
- **Currency:** display as **DA** (local usage) / DZD; `Intl.NumberFormat('fr-DZ')`, space thousands.

**Recommended:** if using Tailwind, map these to CSS variables + a small `tailwind.config` theme extension rather than hardcoding hex. Keep a single tokens file as source of truth.

---

## 6. Recommended production architecture

> Opinionated default — adjust to team preference. Chosen for fast delivery in the Algeria context.

- **Frontend:** Next.js (App Router) + TypeScript + Tailwind. Componentize the prototype's pages; keep it a marketing-site-quality front with an authed `/admin` area.
- **Backend/DB:** **Supabase** (Postgres + Auth + Realtime + Row-Level Security). Realtime powers the live admin queue. Auth gates `/admin` (staff only).
- **QR:** server-issued signed token (HMAC or short-lived JWT) → `qr` rendered client-side. A `/p/[token]` route resolves a pass for staff.
- **WhatsApp:**
  - *Phase 1 (now):* `wa.me/213660056583?text=…` deep link (zero cost, already working).
  - *Phase 2:* **WhatsApp Cloud API** for two-way + confirmation templates + owner notifications. Needs a Meta Business + verified number — **scope and cost-check**.
- **Payments / recharge (Algeria-specific):**
  - *Phase 1:* cashless concept only — admin recharges card manually (record-keeping), no online money movement.
  - *Phase 3:* online pay via **SATIM / CIB e-paiement** (and possibly Edahabia). ⚠️ Stored-value/prepaid balances may carry **regulatory/licensing** obligations — get legal confirmation before enabling customer-funded top-ups. Until then, treat "balance" as venue-issued credit reconciled on-site.
- **Hosting:** Vercel (front) + Supabase (data). Confirm domain (oxygen-island.com).
- **i18n:** FR primary. Architect for **AR** (RTL) and **EN** even if launching FR-only.

### 6.1 Data model (Postgres / Supabase)

```
clients(id pk, name, phone, email, created_at)
cards(id pk, client_id fk, card_number unique, qr_token unique, balance_da int default 0,
      status enum[active,blocked] default active, created_at)
card_transactions(id pk, card_id fk, type enum[recharge,debit,credit_gift],
      amount_da int, label, created_by, created_at)
offers(id pk, slug unique, category enum[journee,event], name, description,
      price_da int null,  -- null = sur devis
      unit, active bool default true, sort int)
menu_items(id pk, category, name, description, price_da int, active bool, sort int)
reservations(id pk, ref unique, client_id fk, type enum[jour,event],
      date date, guests int, status enum[pending,confirmed,cancelled] default pending,
      total_da int default 0, gift_unlocked bool default false,
      source enum[site,whatsapp,phone] default site, created_at)
reservation_items(id pk, reservation_id fk, kind enum[offer,menu], name, qty int,
      unit_price_da int, subtotal_da int)
event_requests(id pk, reservation_id fk, event_type, organisation, headcount int, message)
passes(id pk, reservation_id fk, qr_token unique, status enum[valid,used,void],
      issued_at, redemptions jsonb)  -- [{zone, at}]
reviews(id pk, client_id fk null, author_name, source enum[site,google,instagram,facebook],
      rating int, body, status enum[pending,published] default pending, created_at)
staff(id pk = auth.uid, name, role enum[owner,staff])  -- via Supabase auth
settings(key pk, value jsonb)  -- gift_threshold_da, gift_label, hours, etc.
```

- **Derived, not stored:** client cumulative spend (sum of confirmed reservation totals) and tier (function of spend). Cache if needed.
- **RLS:** public read on `offers`/`menu_items`/published `reviews`; insert on `reservations`/`reviews`(pending) for anon; everything else staff-only.

### 6.2 Key flows
- **Submit reservation (anon):** upsert client by phone → insert reservation + items (+ event_requests) → compute `gift_unlocked` → issue pass token → return ref+token → fire wa.me. Realtime row triggers admin queue.
- **Confirm (staff):** set `confirmed` → upsert card for client → `card_transactions(credit history)` + recompute spend/tier → if gift, log it.
- **Recharge (staff):** `card_transactions(recharge)` → `cards.balance_da += amount`.

---

## 7. Build roadmap & acceptance

**Phase 0 — Scaffold.** Next.js+TS+Tailwind+Supabase repo; tokens ported; brand assets in; prototype in `/reference`. ✅ when `/` renders Accueil with real tokens/fonts and `/admin` is route-gated.

**Phase 1 — MVP (the prototype, made real).** Public 4 pages reading offers/menu from DB; devis builder; wa.me submit; reservation+items persisted; admin auth + dashboard (queue, confirm, KPIs); gift engine (client + admin); reviews (manual + moderation). ✅ when a real submit appears in the dashboard and confirm changes status server-side.

**Phase 2 — Loyalty.** Card issuance on confirm; signed QR pass (`/p/[token]`); tiers; admin recharge + wallet modal + history. ✅ when confirming a reservation creates/updates a card with a scannable pass and visible history.

**Phase 3 — Scale.** Online payments (SATIM/CIB) [legal-gated]; WhatsApp Cloud API notifications; staff scanner PWA for zone validation; social reviews import; analytics/export. ✅ per sub-feature.

---

## 8. Constraints, non-goals, risks

- **Don't oversell the site as fixing operations.** Cleanliness/service are the venue's real weakness; this platform measures and de-risks, it doesn't mop floors. Keep owner expectations honest.
- **Stored-value/payments = regulatory.** Do not ship customer-funded wallet top-ups without legal sign-off (SATIM/CIB rules, prepaid-instrument licensing). Phase-gate it.
- **QR-as-wallet at zones needs staff + scanners.** It implies operational discipline the venue may lack — ship the scanner PWA only when the owner commits to the process. Phase 3.
- **Seasonality:** summer-concentrated demand; the dashboard should still be useful off-season (events, corporate, memberships).
- **Don't fabricate:** prices `[CONFIRM]`, menu prices, and reviews must be real before launch. Placeholder reviews and illustrative prices are prototype-only.
- **Logo:** raster/white-bg only today; needs vector for dark surfaces (see §2.7).

---

## 9. Open decisions (need owner/Numidea input)

1. Confirm 2025 **prices** + provide **real menu prices**.
2. **Gift rule:** flat ≥20 000 DA, or per-guest? Which gift?
3. QR pass issued **on submit** (optimistic) or **on confirm** (verified)? (Recommend: lightweight pre-pass on submit, validated pass on confirm.)
4. **Guest checkout only**, or client accounts/login?
5. **Languages** at launch: FR only, or FR+AR(+EN)?
6. **WhatsApp:** stay on deep links, or invest in Cloud API?
7. **Payments:** which provider, and do they want online prepay / card recharge at all in v1?
8. **Domain/hosting** + **vector logo** availability.
9. Real **site plan** from owner, or keep illustrated SVG?

---

## 10. Commercial context (Numidea Labs)

Numidea Labs is the agency pitching this. The sell to the owner is **value, not features**: convert more DMs into bookings, own client data (de-risk Instagram), raise panier moyen via in-flow upsell, and give the owner control/visibility ("croissance portée par des systèmes, pas par des personnes"). The prototype + this dashboard are the **demo that closes** — the killer moment is making the owner click **Confirmer** and watch a client card update. A French value-only **proposal booklet** is a pending deliverable; its spine: *"votre image dépasse votre opération → voici comment vous mesurez et fermez l'écart."*

---

## 11. Appendix — prototype file map & migration notes

**Prototype internals (for reference when porting):**
- `go(id)` — page switcher → becomes Next.js routes/segments.
- `devis[]` + `renderDevis()` — devis state → React state/store; nudge logic = gift engine.
- `sendWhatsApp()` — builds wa.me text + `pushReservation()` → becomes a server action (persist) + notification + optimistic UI.
- `reservations[]`, `cards[]`, `fill7[]` (admin script) — seeded in-memory → DB tables (§6.1) + Realtime.
- `confirmRes()`, `recharge()`, `openCard()`, `tierOf()` — admin logic → server actions + RLS.
- `passModal` / `cardModal` + `qrcodejs` — keep UX; swap plain-text QR for **signed token**.
- CSS `:root` tokens + `.medallion`/`--logo` — port to tokens file; replace data-URI logo with proper asset pipeline.

**Migration order:** tokens → layout/nav → public pages (static from DB) → reservation submit (persist + wa.me) → admin auth + queue + confirm → cards/passes → payments/notifications.

---

*End of context. Keep this file current as decisions in §9 are resolved.*
