# Oxygen Island — Membership & Loyalty Ecosystem
### Spec extension to `CLAUDE.md` (readapted from the generic "premium membership platform" brief)

> **Read `CLAUDE.md` first.** This file extends it. Where they conflict, the real data and design tokens in `CLAUDE.md` win. This document is also written so it can be handed to Claude Code as a build prompt.
>
> **Prime directive (unchanged):** every new feature must feel **native to the existing design system** — same tokens, type (Fraunces/Manrope), spacing, components, dark-lagoon language. Never introduce a second visual identity. Reference `/reference/prototype.html`.

---

## 0. Reality check — read before building

The source brief imagines a Revolut/Stripe-grade cashless + CRM ecosystem. That ambition is right *as a north star*, wrong *as a v1 scope* for this venue. Three hard truths shape the plan:

1. **The venue's real constraint is operations, not software.** Public sentiment is "premium image, neglected reality." A membership program that promises VIP and under-delivers **deepens** that wound. Loyalty is earned by operations, then *sold* by software — never the reverse. Tiers ship only with benefits the venue can actually honor.
2. **A real-money wallet is a regulated financial product in Algeria.** Customer-funded stored value touches SATIM/CIB rails and likely licensing/partnership. **Do not build money top-ups in v1.** v1 loyalty currency = **points** (non-cash, internal), which sidesteps financial regulation entirely. Real-money prepaid is a later, legal-gated phase.
3. **WhatsApp marketing at scale needs the official WhatsApp Business/Cloud API + template approval + opt-in.** Blasting promos from a personal number gets it banned. The CRM is built on the API, with consent capture, from day one of that phase.

**Therefore: points-based loyalty + digital membership card first. Real-money wallet last.**

---

## 1. Architecture of identity (the spine)

`Identity → Membership → Loyalty(points) → [Wallet: later] → CRM → Marketing`

- **Customer profile is the source of truth.** The physical/digital card is just a pointer to it.
- A card holds: Card ID, link to profile, tier, points balance, ( wallet balance — later ), QR token, WhatsApp number, language.
- **Lost card = non-event:** block the card token, keep profile/points/history/balance, issue a new card, relink. Effortless. (The prototype already models card-as-pointer; formalize it.)

---

## 2. Membership tiers `[PROPOSED — owner must confirm benefits are deliverable]`

Keep Silver/Gold/Platinum mechanics, dress them in Oxygen identity. Bilingual labels (FR primary, AR ready).

| Tier | FR / AR | Visual identity | How to reach | Core benefits (deliverable, points-based) |
|---|---|---|---|---|
| **Silver** | Argent / فضي | Aqua foil on abyss, `--lagoon` edge | Free join | 5% spend back as points · member price on Afterwork · birthday drink · digital card |
| **Gold** | Or / ذهبي | Champagne `--gold` foil, brushed | Paid yearly **or** spend threshold | 10% points · **priority booking** · 1 free Afterwork entry/mo · early event access · bed discount |
| **Platinum** | Platine / بلاتيني | Obsidian + pearl, `--gold` hairline | Top spend / invite | 15% points · guaranteed bed/cabana priority · **VIP lounge** · first dibs on event tickets · dedicated WhatsApp concierge · cabana upgrade |

- **Points are loyalty currency**, redeemable for entries, F&B, upgrades — **not** cash, **not** withdrawable. This is the legal-safe engine.
- Card visuals must feel **collectible** (foil/material metaphors via CSS gradients + `--logo` medallion), consistent with the wallet-card component already in the prototype's admin modal.

---

## 3. NEW public page — `Membership / Adhésion` (revenue page)

Goal: **sell memberships + create belonging/FOMO.** Sections:

1. **Hero** — premium 3D-tilt card showcase (CSS transform/parallax, reduced-motion safe), emotional line ("Rejoignez l'île. Pas seulement la plage.").
2. **Comparison** — Silver vs Gold vs Platinum table (benefits, savings, privileges), Gold highlighted.
3. **Exclusive benefits** — discounts, VIP pricing, early access, priority events, birthday rewards, points-back, free gifts.
4. **VIP experiences** — private lounge, priority reservations, early event tickets, meet-the-artist (only if real).
5. **Upgrade journey** — Silver → Gold → Platinum, with the points/threshold path.
6. **CTA** — join/upgrade → reservation-style flow → WhatsApp confirm → card issued.

Build this as a new `#membership` page in the SPA / a `/adhesion` route in production — **first new UI to build**, because it's the only page that directly sells.

---

## 4. WhatsApp CRM ecosystem

### 4.1 Engine (production)
Official **WhatsApp Cloud API**. Store per profile: WhatsApp number, **opt-in status + timestamp**, preferred language (FR/AR), tier. Approved message templates. Respect 24h session windows + consent. No personal-number blasting.

### 4.2 Public-site showcase component `[buildable now as marketing UI]`
A premium **smartphone mockup** on the Membership/Accueil page showing authentic-looking WhatsApp threads with the campaigns below. Pure presentational (no real sending) — it's a sales asset for the owner pitch. Use WhatsApp UI conventions, on-brand framing.

### 4.3 Campaign examples (FR + AR) — Oxygen-tailored
> ⚠️ Do **not** name a real artist unless the booking is confirmed — announcing a real person who isn't coming is false advertising. Use `[Artiste confirmé]` placeholders.

**A — Afterwork Gold (FR)**
🔥 Offre Gold exclusive — aujourd'hui dès 16h. Entrée Afterwork à **2 000 DA** au lieu de 4 000 DA. Réservée aux membres Gold. Réservez avant la fin de la journée.
**A — (AR)** 🔥 عرض حصري لأعضاء Gold — اليوم فقط من الساعة 16:00. دخول الـ Afterwork بـ **2000 دج** بدل 4000 دج. حصري لأعضاء Gold. احجز قبل نهاية اليوم.

**B — Partenaire Heetch (FR)**
🚖 Venez en Heetch aujourd'hui : **−20%** sur la course + une boisson offerte à l'arrivée. Sur présentation de votre carte Oxygen.
**B — (AR)** 🚖 تعال بـ Heetch اليوم: **خصم 20٪** على الرحلة + مشروب مجاني عند الوصول. عند تقديم بطاقة Oxygen.

**C — Événement Platinum (FR)**
🎧 **[Artiste confirmé]** la semaine prochaine à Oxygen Island. Accès prioritaire et billets en avant-première pour les membres Platinum. Réservez avant l'ouverture au public.
**C — (AR)** 🎧 **[الفنان المؤكد]** الأسبوع القادم في Oxygen Island. أولوية الحجز وتذاكر حصرية لأعضاء Platinum قبل الجمهور.

**D — Anniversaire (FR)** 🎂 Joyeux anniversaire de la part d'Oxygen Island ! Votre cadeau membre vous attend : un cocktail offert toute la semaine.
**D — (AR)** 🎂 عيد ميلاد سعيد من Oxygen Island! هديتك كعضو بانتظارك: كوكتيل مجاني طوال الأسبوع.

---

## 5. Customer app (PWA) — UX flows to design/build

Mobile-first. Installable PWA (manifest + service worker; `theme-color #04211d` already set in prototype head).

- **Dashboard** — tier status, points, next reward, upcoming reservation, promos.
- **Digital membership card** — animated card + QR (signed token); "Add to Apple/Google Wallet" (pass generation) as a phase-2 nicety.
- **Points / Rewards** — balance, ledger, redeem catalog (entries, F&B, upgrades).
- **Event tickets** — purchase/priority, QR ticket.
- **Reservations** — reuse the existing devis flow (single entry — see §8).
- **Transaction / experience history** — confirmed visits, points earned/spent.
- **Notifications & promos** — push (web-push) + in-app; tier-targeted.
- **Lost card recovery** — §6.
- **Profile** — language (FR/AR/EN), WhatsApp number, opt-in toggle.

### Lost-card flow (must feel effortless)
Report lost → instantly block old token → balance/points/history preserved (they live on the profile) → issue replacement card + new QR token → relink → confirm via WhatsApp. One screen, two taps.

---

## 6. Business dashboard — extend the existing `Espace Pro`

Build **on top of** the current dashboard (don't replace it). Add modules:

- **Executive** — revenue, membership growth, active members, event performance, points volume, tier distribution. (Extend current KPI row + 7-day chart.)
- **Membership management** — search member, replace card, upgrade/downgrade tier, block card, restore account.
- **Campaign manager** — create/segment by tier · spend level · visit frequency · birthday · language; preview FR/AR; schedule via Cloud API.
- **WhatsApp automation** — workflows: new-member welcome, birthday reward, event reminder, upgrade offer, win-back. Each with opt-in guard.
- **Analytics** — conversion, campaign performance, open/read rates (from API webhooks), upgrades, revenue attributed, event attendance.

Keep the current visual language: `.panel`, `.kpi`, `.chip`, `.st-*`, wallet-card modal patterns already defined.

---

## 7. Data model — extensions to `CLAUDE.md §6.1`

Add to the existing schema:

```
memberships(id pk, client_id fk, tier enum[silver,gold,platinum], status enum[active,expired],
            started_at, renews_at, source enum[free,paid,threshold,invite])
points_ledger(id pk, client_id fk, delta int, reason enum[earn,redeem,gift,adjust],
              ref_reservation_id fk null, label, created_at)   -- balance = SUM(delta)
campaigns(id pk, name, channel enum[whatsapp,push], segment jsonb, template_id,
          lang enum[fr,ar], status enum[draft,scheduled,sent], scheduled_at, created_by)
campaign_recipients(id pk, campaign_id fk, client_id fk, status enum[queued,sent,delivered,read,failed], sent_at)
wa_optins(id pk, client_id fk, opted_in bool, lang, updated_at)
push_subscriptions(id pk, client_id fk, endpoint, keys jsonb, created_at)
-- LATER (legal-gated): wallet(id pk, client_id fk, balance_da int, ...), wallet_txns(...)
```

- **Points balance is derived** (`SUM(points_ledger.delta)`); cache if needed.
- **Tier is derived or stored** depending on whether it's spend-threshold (derive) or paid (store in `memberships`).
- **Cards** (existing table) get `tier` denormalized for fast card rendering; profile remains source of truth.

---

## 8. The three added requirements (now baked in)

1. **Enhanced code / standards.** Production target: Next.js + TS + Tailwind + Supabase (per `CLAUDE.md §6`), componentized, tokens in one place, RLS on every table, signed QR tokens (not plaintext), a11y (focus rings, ≥44px targets, `prefers-reduced-motion`, ARIA), `loading="lazy"` media, FR/**AR-RTL** scaffolding (`dir` switch). Prototype already upgraded: theme-color, lazy iframe, dedup nav.
2. **Real map — DONE in prototype.** The fake SVG plan is replaced by a live **Google Maps satellite embed** of the venue zone (`q=36.768067,2.9075566&t=k&z=17&output=embed`) + the directions deep link. Production: optionally swap to Google Maps JS API (keyed) for a styled map + custom markers; keep an **owner-supplied illustrated site plan** for internal wayfinding (beach/WC/bar) if desired.
3. **Single reservation entry — DONE in prototype.** Removed the duplicate desktop nav tab; the **"Réserver →" CTA** is the one desktop entry (mobile menu keeps the link since the CTA is hidden on mobile). Production: one canonical `/reservation` route, linked from CTA + offer cards + membership flow.

---

## 9. Build order (phased — ship value, avoid the trap)

| Phase | Scope | Gate |
|---|---|---|
| **1. Foundation** | `CLAUDE.md` MVP: real site (4 pages), reservation→WhatsApp→DB, admin queue/confirm, gift engine. Real Google map ✅. Single reservation entry ✅. | — |
| **2. Membership + Loyalty** | Membership/Adhésion page, tiers, **digital card + signed QR**, **points** ledger, redeem catalog, lost-card flow, member dashboard (PWA shell). | No real money. |
| **3. WhatsApp CRM** | Cloud API integration, opt-in capture, segments, campaign manager, automations, analytics, showcase component live. | Official API + consent. |
| **4. Real-money wallet** | Prepaid balance, top-ups, SATIM/CIB e-paiement, reconciliation. | **Legal/PSP sign-off required.** |
| **5. Polish** | Apple/Google Wallet passes, staff scanner PWA for zones, push, full analytics/export. | Ops commitment for scanners. |

---

## 10. Deliverables (mapped from the brief)

UX architecture · IA · user journeys (join, reserve, redeem, lost-card) · admin flows · wireframes → hi-fi (reuse tokens) · mobile + desktop screens · PWA spec (manifest/SW/push) · component inventory (extend existing) · design-system extensions (tier card materials, points widgets, campaign UI) · WhatsApp CRM · Membership page · microinteractions/empty/success/error states · responsive specs · dev notes. **All within the existing Oxygen visual identity.**

---

## 11. Open decisions blocking this layer (add to `CLAUDE.md §9`)

1. Confirm **tier benefits the venue can actually deliver** (priority, VIP lounge — real or not?).
2. **Paid membership price(s)** + renewal, or spend-threshold tiers only?
3. **Points economics** — earn rate, redemption values (must be margin-safe).
4. Go-ahead on **WhatsApp Cloud API** (Meta Business, verified number, budget)?
5. **Real-money wallet**: pursue at all, and with which PSP? (Triggers legal review.)
6. Confirmed **events/artists** for Platinum early-access (don't announce unconfirmed names).
7. Languages at launch: FR, FR+AR, +EN? (Drives RTL work.)

---

*End of extension. This layer is only worth building once Phase 1 ops + reservation value is real and the owner commits to honoring tier benefits.*
