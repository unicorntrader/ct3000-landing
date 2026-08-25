# Gather Landing Page — Structure Audit

**Source:** https://www.try-gather.co/ (homepage only)
**Method:** Ground-truth extraction — downloaded and read the live `styles.css` (630 lines), `index.html` (547 lines), and `script.js` (417 lines) directly, rather than eyeballing screenshots. Every value below is copied from the real source, not estimated.
**Purpose:** A standalone, reusable reference of how this page is actually built — tokens, section-by-section structure, responsive behavior, and interaction patterns — so it can be compared against any landing page (not just one specific project) or used as a build reference.
**Date captured:** 2026-08-25 (mark down the date when reusing this — marketing sites change).

---

## 1. Design tokens

### Colors
| Token | Hex / value | Used for |
|---|---|---|
| Brand accent (coral) | `#E7625B` | Primary buttons, links, icons, kickers, active states |
| Accent hover-fill (peach) | `#EA8C7E` | Decorative squiggle lines only |
| Ink (near-black text) | `#141A1A` | Headings, primary text |
| Body gray | `#5b6470` / `#5c636a` / `#6b7178` (three near-identical grays used interchangeably by section) | Subheads, body copy |
| Muted gray | `#9aa0a6` | Fine print (plan notes, stat labels) |
| Page background (white) | `#FFFFFF` | Hero, testimonial section, CTA copy area |
| Section background (warm off-white) | `#F8F7F4` | Trust bar, "one platform", "why us", "how it works" (all on the homepage); FAQ and pricing use it too, but see §3.11 — those two aren't on the homepage |
| Footer background (cream) | `#F5EBD6` | Footer shell, stats strip |
| Border/hairline | `#e6e3dd` / `#ece7e1` / `#eee6de` (interchangeable warm grays) | Card borders, dividers |
| Success green | `#2f9e6b` | "Confirmed" / checkmark status pills in mockups |
| Error red | `#b3261e` | Form validation text |

**Note:** there is no CSS custom-property (`:root { --x }`) token system — every value is a literal hex repeated inline throughout the stylesheet. Colors are consistent by convention/discipline, not by variable enforcement.

### Typography
- **Display/UI font:** `'PPNM'` = PP Neue Montreal (Pangram Pangram, **paid/licensed**), self-hosted as `.ttf` files (`/assets/font-01.ttf` regular-style, `/assets/font-02.ttf` italic-style). Both files are declared at `font-weight: 700` — **this typeface is only loaded at one weight (700/Bold).** Every heading, button, and label uses `font-weight: 700` explicitly; there is no 400/500/600 cut of PPNM in use anywhere.
- **Body font:** `'Helvetica Neue', Arial, sans-serif` — a system font, not custom-loaded. Used for all paragraph copy, form fields, footer links.
- **Sizing method:** almost every font-size uses `clamp(min, preferred-vw, max)` — no fixed breakpoint jumps for type, it scales continuously with viewport width. Example: hero headline `font-size: clamp(34px, 5.4vw, 58px)`.
- **Letter-spacing:** headings consistently use tight negative tracking, ranging `-0.01em` (e.g. `.s2-title`) to `-0.04em` (e.g. the big coral stat/score numbers) — not a strict formula, but bigger/bolder display numbers trend tighter than regular headings. Kickers/eyebrows use wide *positive* tracking instead: `letter-spacing: .14em; text-transform: uppercase`.
- **Line-height:** headlines sit at `1.04–1.1`; body copy sits at `1.35–1.65`.

### Spacing / shape scale
- **Section vertical padding:** `clamp(56px, 9vw, 110px)` top/bottom is the standard for most full sections, including two (`.faq`, `.pricing`) that aren't actually on the homepage — see §3.11. On-homepage sections using this value: `.s3`, `.how`, `.tst`.
- **Card border-radius:** large content cards (`.s2-shell`, `.s3-body`) use `clamp(24px, 3vw, 36px)`; smaller cards (`.how-card`, `.insight`, `.plan`) use `18–22px`; pills/badges use `999px` (full round); buttons use `12–15px`.
- **Card shadow convention:** soft, warm-tinted, large-blur shadows tied to the accent color rather than pure black, e.g. `box-shadow: 0 18px 50px rgba(20,26,26,.05)` for white cards on the warm background, or `0 16px 30px rgba(150,50,46,.26)` for coral buttons (shadow color ≈ a darkened version of the accent, not generic black).
- **Container max-width:** `1380px` (wider than CT3000's `1080px`), with fluid side gutters `clamp(20px, 5vw, 48px)`.

### Buttons (3 near-duplicate systems: `.pbtn`, `.b2`, `.plan-btn` — same visual language, different sizes per section)
- **Primary:** solid coral bg, white text, colored drop shadow. Hover → **inverts**: white bg, coral text, coral inset ring (`box-shadow: inset 0 0 0 2px #E7625B`), no more drop shadow.
- **Ghost/outline:** white bg, coral text, coral inset ring by default. Hover → **inverts the other way**: solid coral bg, white text, drop shadow appears.
- Both button styles also `transform: translateY(-2px)` on hover (lift effect).
- Transition timing is unusually slow/deliberate: `background .6s ease, color .6s ease` (most other sites use 0.15–0.3s) — the color-swap feels smooth/fade-y rather than snappy.

---

## 2. Breakpoints actually used

```
max-width: 960px   — hero, trust bar wrap-start, "how it works" stacks to 1 column
max-width: 900px    — "why us" section stacks to 1 column, CTA band stacks
max-width: 980px    — trust bar starts wrapping (2-across)
max-width: 760px    — nav switches to burger menu, tab-swipe hint appears
max-width: 720px    — (empty/reserved rule, unused)
max-width: 640px    — footer columns go 2-across, cookie banner insets shrink
max-width: 560px    — trust bar goes 2-column grid, testimonial card loses max-width, CTA actions stack vertically
prefers-reduced-motion: reduce  — used consistently across every animated section to fully disable motion
```

No `min-width` breakpoints at all — everything is written desktop-first with `max-width` overrides, and font-sizes/spacing mostly self-adjust via `clamp()` without needing a breakpoint at all.

---

## 3. Section-by-section structure

### 3.1 Header / nav (`.topnav`)
- **Position:** `fixed` (not sticky) top:0, full width, `z-index:100`.
- **Background:** `rgba(255,255,255,.92)` + `backdrop-filter: blur(10px)`.
- **Height/logo:** logo image `height:50px` by default. **On scroll (`window.scrollY > 12`), a `.scrolled` class is added via JS and the logo shrinks to `height:35px`** with a `.28s` transition — a live, animated size change, not a static mobile-only shrink.
- **Nav links:** absolutely centered (`left:50%; transform:translateX(-50%)`), independent of the logo/CTA flex flow — links are dead-center of the header regardless of logo or button width.
- **CTA button:** separate desktop (`topnav-cta-desktop`) vs mobile (`topnav-cta-mobile`, inside the burger menu) — two DOM copies of the same button, toggled by CSS display at 760px, not one button that reflows.
- **Mobile (≤760px):** burger icon appears (3-line). Only `span:first-child` and `span:last-child` get an explicit `[aria-expanded="true"]` transform (`translateY(4.8px) rotate(45deg)` / `translateY(-4.8px) rotate(-45deg)`), forming an X from the outer two bars; the CSS read from the live stylesheet has no explicit rule for the middle span, so confirm its exact behavior visually before relying on this detail. Nav links become a full-width dropdown sheet below the header (`position:absolute; top:100%`), closed by default, opened by toggling `.open` class. Tapping any link inside auto-closes the sheet.

### 3.2 Hero (`.hero-stage` > `.hero` + `.trustbar`)
- **Critical structural point, verified by live measurement, not just reading the CSS:** `.hero-stage` is the *true* full-viewport box — it wraps **both** `.hero` and `.trustbar` as flex-column children (`display:flex; flex-direction:column`), NOT just `.hero` alone. `.hero` has no explicit height of its own; it just fills whatever space is left after `.trustbar` takes its natural height. This means the trust bar is *always* visible in the first screen, guaranteed, regardless of hero content length — it isn't a coincidence of a tall viewport. (Confirmed live: at a 1215px-tall viewport, trust bar bottom sits at exactly 1215px — flush, zero scroll.) Don't skip straight to `.hero`'s own CSS when rebuilding this — the height-reservation logic lives one level up, on `.hero-stage`.
- **Full-viewport intent:** `.hero-stage { min-height: 100vh; min-height: 100dvh }`, AND reinforced by JS: `setH()` explicitly sets `stage.style.minHeight = window.innerHeight + 'px'` on load/resize/orientationchange — belt-and-suspenders against mobile browser chrome resize bugs.
- **Layout:** `.hero-grid` is a `flex` row, `justify-content:space-between`, copy column flex-basis 40%, image column 60% — **image is the majority of the hero's width**, not a supporting side element.
- **Headline:** two `<span>` lines (`.l1`/`.l2`) inside one `<h1>`, each independently staggered-animated in (`animation-delay: .12s` / `.28s`) — the headline visually types on line-by-line, not word-by-word or all-at-once.
- **Hero image:** single `<img>`, `border-radius:22px`, no card/frame — just a rounded-corner photo/mockup composite baked into one PNG asset (`hero-visual.png`). Not a live component like CT3000's phone mockup.
- **Extra decorative layer:** a small illustrated "traveller" character image (`.hero-traveller`, absolutely positioned bottom-left of the hero, hidden below 960px) and a hand-drawn SVG squiggle line (`.hero-flourish`, bottom-right, opacity .95) — these are **pure decoration, `pointer-events:none`, `aria-hidden`**, contributing nothing functionally, purely mood/personality.
- **Social proof line:** 5 star glyphs (★★★★★, literal Unicode characters, not an image/icon) + "Loved by retreat hosts" text, small, directly under the CTA buttons — the *only* proof element in the hero itself.
- **Mobile (≤960px):** grid stacks to column, copy becomes centered (`text-align:center`), image caps at `640px` and centers, the decorative traveller image is hidden entirely (`display:none`) — one whole decorative asset is simply cut on mobile rather than resized.

### 3.3 Trust bar (`.trustbar`)
- **Container:** full-bleed `<section>` (own background `#F8F7F4`, `border-top`/`border-bottom` 1px hairlines), a *sibling* of `.hero` in the markup — but both are children of `.hero-stage`, which is what actually reserves the height (see §3.2). Don't build this as a section that sits *after* the hero's height budget ends; build it as a co-tenant *inside* the same viewport-height wrapper.
- **Layout:** `flex; justify-content:space-between`, 5 items, **each item after the first gets a `1px` left border** (`.trustbar-item + .trustbar-item`) — a vertical divider between items instead of a gap/whitespace-only separation.
- **Icon badge:** `40px` circle, `background: rgba(231,98,91,.08)` (8% coral tint), plus an **inset ring** `box-shadow: inset 0 0 0 1.5px rgba(231,98,91,.35)` (35% coral) — so the badge isn't just a flat tinted fill, it has a visible thin coral outline too. Icon itself `20×20px`, `stroke-width:1.7`.
- **Copy:** bold label (PPNM 700) + lighter gray sub-line (Helvetica), stacked tightly (`gap:2px`).
- **Responsive collapse (two stages, not one):**
  - ≤980px: wraps to ~2-per-row (`flex:1 1 46%`), left-border divider removed, replaced by border only on even-indexed items.
  - ≤560px: becomes an actual **CSS grid**, `grid-template-columns: 1fr 1fr`, with borders now conditionally applied via `:nth-child(even)` (left border) and `:nth-child(n+3)` (top border) — recreating a table-like grid of dividers, not just stacking.

### 3.4 "One platform" tabbed feature section (`.s3`, id `#features`)
- **Intro block:** kicker + `<h2>` + sub-paragraph, left-aligned, max-width constrained independent of the tab content below.
- **Tab row:** `.tabrow` is a bordered white pill-shaped container (`border-radius:14px`) holding all 5 tab buttons *inside itself* — the tabs are not free-floating buttons, they share one continuous bounding box with `overflow-x:auto` for horizontal scroll on mobile, and `1px inset box-shadow` between adjacent tabs (not a gap).
- **Active tab state:** `background: rgba(231,98,91,.08)` (8% coral tint) + coral text + a `::after` pseudo-element `3px` solid coral bar along the bottom edge — like an underline/tab-indicator combined with a background tint, not just one or the other.
- **Content switching:** **not 5 separate DOM panels** (unlike CT3000's approach) — there is exactly **one** `.s3-body` panel, and clicking a tab **mutates its text content and image `src` via JS** (`label.textContent=...`, `img.src=...`). A `.is-fading` class triggers a 220ms opacity/translateY fade-out, content swaps, then fades back in. This is meaningfully different from a show/hide-multiple-panels pattern — there's only ever one panel in the DOM.
- **Swipe hint:** a text hint ("Swipe to explore →") appears **only ≤720px**, with an animated arrow (`translateX` loop) — explicitly telling mobile users the tab row scrolls horizontally.
- **First-load nudge:** on page load, JS checks if the tab row's content overflows its visible width (`scrollWidth > clientWidth + 12`) and if so, **auto-scrolls it right 72px then back to 0** after a 1s delay — a one-time "look, this scrolls" hint animation, independent of the static swipe-hint text.
- **Layout of the content panel itself:** 2-column grid (`minmax(0,.9fr) minmax(0,1.15fr)`) — text ~44% width, image ~56%, image column wins the majority.
- **Mobile (≤900px):** grid stacks to 1 column, and **the image is reordered above the text** (`.s3-visual { order: -1 }`) — visual comes first on mobile even though it's second in the DOM/desktop layout.

### 3.5 "Why Gather" section (`.s2`)
- **Whole section is a single big white rounded "shell" card** (`.s2-shell`, `border-radius: clamp(24px,3vw,36px)`) sitting on top of the warm section background — not a flat section, a card-within-a-section.
- **Layout:** 2-column grid, photo left (`minmax(0,1.05fr)`), copy right (`minmax(0,1fr)`) — nearly even split, photo column marginally wider.
- **Photo treatment:** forced `aspect-ratio: 4/5` (portrait), `object-fit:cover`, own shadow. **Important:** the CSS also fully styles a floating photo-overlay quote card (`.s2-quote`, bottom-right of the image, serif quotation mark + italic pull-quote) and a small decorative aside image beside the photo (`.s2-aside`) — but **neither element exists in the current live HTML**. This is the same "built but not currently deployed" pattern as the stats counter and footer social row (§3.7, §3.9) — worth knowing the design intent existed, but don't describe it as visible on the page today.
- **Copy side:** kicker → `<h2>` → sub-paragraph → a 3-item checklist (`.s2-points`, each row `border-top`, icon badge + bold text, no description text under each point — label-only) → 2 CTAs (primary "Book a call" + ghost "Read the FAQs").
- **Decorative squiggle:** another hand-drawn SVG line (`.s2-flourish`), positioned `top:-20px; right:-44px` relative to the shell card — bleeds slightly outside the card's own edge rather than being contained inside it.
- **Mobile (≤900px):** stacks to 1 column; since `.s2-aside` isn't in the HTML at all, its `display:none` rule at this breakpoint is currently a no-op.

### 3.6 "How it works" (`.how`, id `#how`) — the timeline section
This is the section you specifically asked about earlier — here's its exact structure:
- **Layout:** 2-column grid `minmax(0,.85fr) minmax(0,1.25fr)` — left column (copy) is narrower than the right column (steps), and **not sticky** — `align-items:start`, no `position:sticky` anywhere in `.how-copy`'s CSS. (CT3000's current build made this column sticky; Gather's does not — it just scrolls normally, top-aligned.)
- **Left column:** kicker, `<h2>` (max `12ch` — forces an early line-break for a punchy 2-line headline), sub-paragraph, one "Book a call" button, and a decorative squiggle underneath.
- **Right column — the numbered step list:**
  - `.how-rail`: a single continuous vertical line (`2px` wide, `linear-gradient(180deg, #E7625B 0%, rgba(231,98,91,.35) 100%)` — solid coral fading to 35% coral top-to-bottom) positioned absolutely at `left:19px`, running from `top:28px` to `bottom:28px` of the whole step list — one gradient line behind all 3 steps, not separate segments.
  - `.how-num`: the numbered circle (`38×38px`, solid coral, white bold number) is positioned `absolute; left:-28px; top:50%; transform:translateY(-50%)` **relative to each individual step article** — i.e. **already vertically centered against that step's own card height**, exactly the fix you just asked me to make on CT3000.
  - `.how-card`: white card, `border-radius:18px`, 2-column grid inside itself (`minmax(0,1.05fr) minmax(140px,.9fr)`) — text left, a small mockup ("mini") card right, `align-items:center` (confirms the vertical-centering approach).
  - Each step's "mini" mockup (`.how-mini`) is a distinct hand-built micro-UI: step 1 is a call-status card, step 2 is a browser-chrome-style progress/checklist card, step 3 is a live stat + activity-feed + inline SVG line-chart card. All three are visually different components, not the same template reused 3x.
  - **Stagger animation:** the whole `.how-steps` block is one `IntersectionObserver` target (not each step individually) — when the block enters view, `.in` is added, and each `.how-step` has its own CSS `transition-delay` (`.06s`, `.16s`, `.26s` for steps 2/3/4 — note: CSS is written for up to 4 steps even though only 3 exist in the HTML) so they cascade in one after another despite firing from a single observer trigger.
- **Mobile (≤960px):** grid stacks to 1 column, card's internal 2-column layout also stacks to 1 column. At ≤560px specifically, the rail and numbers both shrink and shift left (`num: 34px, left:-24px`; `rail: left:16px`) to match tighter padding.

### 3.7 Customer stories (`.tst`)
- Just **one** testimonial card shown (not a carousel/grid) — `max-width:420px`, `border: 1.5px solid` the coral accent (a colored border, not just a shadow), single column, effectively centered as the section's sole content block after the heading.
- **Photo:** `aspect-ratio:16/11`, has a floating badge overlaid top-left ("Featured story").
- **Quote card:** stars (★ unicode again) → bold pull-quote → person row (circular avatar, name, role/location) → 2 pill tags summarizing the outcome ("3 → 15 retreats", "Sold out") — the tags encode the *result*, not generic category labels.
- A stats-counter section (`.stats`, count-up animated numbers) exists in the CSS/JS but is **commented out in the live HTML** ("Stats strip hidden 7 Jul 2026 ... may return later") — worth knowing it was tested and pulled, not that it doesn't exist as a pattern.

### 3.8 CTA band (`.cta`)
- **Wave dividers:** top and bottom of this section are literal inline `<svg>` wave shapes (`viewBox="0 0 1440 64"`, a hand-drawn bezier path filled solid coral) acting as organic section transitions instead of a straight rectangular color block boundary. Same technique repeats at the footer's top edge (cream-colored wave into the footer).
- **Background:** solid coral (`#E7625B`) shell between the two waves.
- **Layout:** 2-column grid, copy `.9fr` / photo `1.2fr` — again image column is the majority.
- **Trust list:** 3 inline icon+text items ("15-minute call", "No hard sell", "Real human support") — **plain text list, not badges/pills**, `rgba(255,255,255,.9)` on the coral background, positioned *below* the CTA buttons, not above them.
- **Decorative arrow squiggle** pointing toward the photo, `position:absolute`, hidden ≤900px.
- **Mobile (≤900px):** stacks to 1 column, the decorative arrow is dropped entirely.

### 3.9 Footer (`.ftr`)
- Same wave-divider technique at the top (cream color, transitioning from the white page background into the footer's cream `#F5EBD6` shell).
- **Layout:** 2-column grid, brand block `1.35fr` / link columns `1.4fr`.
- **Brand block:** logo (`height:56px`, bigger than the header's 50px), kicker, `<h2>`-level tagline ("Run retreats, not admin."), one-line description, email link, decorative squiggle, and a **social row that is `display:none` by default** (`.ftr-social { display:none }` — present in HTML/CSS, coded, but switched off — same "built but currently hidden" pattern as the stats section).
- **Link columns:** 3 columns (Explore / Resources / Legal), each link has a small trailing arrow glyph that **animates `translateX(3px)` on hover** — a "nudge forward" micro-interaction on every single footer link, not just CTAs.
- **Legal bar:** company registration number + copyright, a "Made with retreat hosts" heart-icon line, and legal links — all in one flex row that wraps to stacked on mobile.
- **Mobile (≤640px):** the 3 link columns become a 2-column grid, with the 3rd column (Legal) forced to span both (`grid-column:1/-1`).

### 3.10 Contact modal
- Triggered by the hero's "Get in touch" ghost button (not a page navigation — `aria-haspopup="dialog"`).
- Standard centered modal, backdrop click or Escape key both close it, focus returns to the triggering element on close (`lastFocus.focus()`) — proper focus management.
- Client-side validation (regex email check, required-field checks) before a `fetch('/api/contact')` POST; a honeypot field (`.contact-hp`, visually hidden, `tabindex="-1"`) is included purely to catch spam bots.

### 3.11 Sections styled in `styles.css` but **not present anywhere in the homepage HTML**
Cross-checked every `<section>` tag against every top-level CSS block — these two are real, fully-built components, but they render on a *different* page (most likely `/faq` and/or a dedicated pricing page — the nav links to `/faq` as its own URL), not embedded in the homepage scroll. Don't describe them as part of the homepage flow:
- **`.pricing`** — 2 plan cards (`max-width:880px`, side-by-side grid). Featured plan gets a thicker 2px coral border, bigger shadow, and a floating badge pill that pulses twice on scroll-into-view (`animation: badgePulse 1.8s ease-in-out .5s 2` — plays exactly twice, then stops). Cards animate in with opacity/translateY **and** a scale (`translateY(24px) scale(.96)` → none).
- **`.faq`** — native `<details>/<summary>` elements (accessible/semantic), but JS still hijacks open/close to animate height smoothly (340ms, measures `scrollHeight` then animates to it) since raw `<details>` can't do that natively. Plus-icon rotates 45° into an X when open.

If you re-audit `/faq` or another Gather page directly, use the same download-and-read method as §0 — don't assume these match the homepage's exact spacing scale even though they share the same stylesheet.

---

## 4. Interaction & animation inventory

| Pattern | Trigger | Notes |
|---|---|---|
| `.reveal` fade-up | `IntersectionObserver`, threshold 0.25, `rootMargin: 0px 0px -10% 0px` | Generic — applied to most section headings site-wide |
| How-it-works steps cascade | One `IntersectionObserver` (threshold 0.2) on the parent, CSS `transition-delay` per child | Steps 2/3/4 delayed .06s/.16s/.26s (note: CSS supports a 4th step that doesn't exist yet) |
| Pricing cards — **not on homepage, see §3.11** | `IntersectionObserver` (threshold 0.2), fade+scale | — |
| Testimonial card | `IntersectionObserver` (threshold 0.3) | Single card only |
| Health-score chart — **not on homepage** (no `#health-score` element in the live HTML; likely another page) | Scroll-position check on every `scroll` event (not IO) | Bars grow via CSS var `--h`, count-up number via `setInterval` (42 steps, 22ms each ≈ 924ms) |
| Stats counters (on homepage, but currently commented out) | Same scroll-check pattern as health-score | Count-up via `setInterval`, same 42-step timing |
| Nav logo shrink | `scroll` event, `scrollY > 12` threshold | 50px → 35px, `.28s` transition |
| Tab content swap | Click | 220ms fade-out → content mutate → fade-in; single shared DOM panel, not multiple panels |
| Tab-row first-load hint | `setTimeout` 1000ms after page load, only if content overflows | Auto-scrolls 72px right then back, once |
| FAQ accordion — **not on homepage, see §3.11** | Click | JS-animated height on native `<details>`, 340ms |
| Footer link arrows | CSS `:hover` | `translateX(3px)` nudge per link |
| All buttons | CSS `:hover` | Fill/outline color inversion + `translateY(-2px)` lift, `.6s` transition |
| `prefers-reduced-motion: reduce` | Media query, checked in both CSS and JS | Every single animation above has an explicit disabled/instant-state fallback — this is handled thoroughly, not an afterthought |

---

## 5. "Curiosity hooks" / conversion devices

These are the copy and layout tricks doing persuasion work, independent of visual styling:

1. **Specific, odd numbers over round ones:** "44 / 44 sold", "3 → 15 retreats" — precise, slightly unusual numbers read as more real/credible than "100% booked" or "5x growth".
2. **Named, located social proof:** "Marnie Rays · Surf retreats · Ericeira, Portugal" — a real-sounding name + niche + place, not "Sarah T., verified customer".
3. **Live-feeling mockups instead of static screenshots:** the how-it-works "mini" cards show *in-progress* states (a progress bar at 80%, an activity feed with relative micro-events, a small live-looking line chart) rather than a finished dashboard screenshot — implies motion/activity even in a static image.
4. **Two-step proof stacking:** trust bar (immediate, skimmable) → tabbed feature depth (for people who want detail) → "why us" emotional/origin story → timeline (process de-risking) → single strong testimonial (social proof) → CTA. Pricing and FAQ (objection-handling) are **not embedded in this homepage scroll at all** — they live on separate dedicated pages linked from the nav (`/faq`, likely a pricing page too) — so the homepage itself stays a pure proof-then-ask funnel with the call-booking CTA as the only homepage destination, and objection-handling is one click away rather than scrolled past.
5. **"Book a call" as the primary CTA everywhere, not "Sign up" or "Start free trial":** every single primary button on the page says "Book a call" (or a minor variant) — zero self-serve signup path is offered anywhere on the homepage. The only alternate action is "Get in touch" (a form) or a secondary link ("Read the FAQs", "See how Gather works").
6. **Reassurance micro-copy placed immediately next to the highest-friction CTA:** the final CTA band's 3-item trust list ("15-minute call", "No hard sell", "Real human support") exists specifically to defuse the anxiety of booking a sales call — it doesn't appear anywhere else on the page.
7. **Hand-drawn squiggle SVGs as a repeated visual signature:** the same loose, organic bezier-curve line motif (`#E7625B`/`#EA8C7E` stroke, `stroke-linecap:round`) appears near-identically in the hero, "why us", "how it works", CTA, and footer sections — a consistent "human, not corporate" visual signature repeated 5 times, always `pointer-events:none`/`aria-hidden` (decoration only, never competing for attention/interaction).
8. **Things that are built but intentionally switched off:** both the animated stats counter section and the footer's social-links row are fully coded and styled but currently disabled (commented out / `display:none`) — evidence of active A/B-style iteration rather than a finished, static page.

---

## 6. Explicit differences from CT3000's current build (for the comparison pass)

Noting only structural/behavioral facts, not opinions — decide what's worth adopting separately:

- Gather's container is **1380px** max-width vs CT3000's **1080px**.
- Gather's headline/UI font is a **paid, single-weight (700 only)** font; CT3000 uses free General Sans at 400–700 (see `feedback_no_ai_contrastive_tics`-adjacent fix already made: CT3000 was incorrectly requesting weight 800, now corrected to 700).
- Gather's nav is `position:fixed` + a **live logo-shrink-on-scroll** effect; CT3000's header is `position:sticky` with no logo resize.
- Gather's tab section swaps **one shared panel's content via JS**; CT3000 renders **all 5 panels in the DOM** and toggles visibility.
- Gather's "how it works" left column is **not sticky**; CT3000's current build made it `position:sticky`.
- Gather's trust bar and hero are both children of one `.hero-stage` flex-column wrapper, guaranteeing the trust bar is visible with zero scroll; CT3000's `.hero-stage` now reproduces this exact mechanism (fixed after an initial build that put the trust bar in its own section outside the hero's height budget, which needed a scroll to reach).
- Gather uses **organic SVG wave dividers** between colored sections; CT3000 uses hard rectangular section boundaries throughout.
- Gather's numbered step badges are **already vertically centered per-card** (`top:50%`) — this was the exact bug just fixed on CT3000.
- Gather has **zero self-serve/free-trial path** — 100% call-booking funnel; CT3000's primary CTA is "Start free trial".

---

*This document should be re-verified against the live site before reuse if more than a few weeks have passed — marketing sites iterate. To refresh: `curl -s https://www.try-gather.co/ -o index.html`, `curl -s https://www.try-gather.co/assets/styles.css -o styles.css`, `curl -s https://www.try-gather.co/assets/script.js -o script.js`, then re-read.*
