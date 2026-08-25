# Reference: Gather (try-gather.co) landing page — ground-truth structure audit

I want you to use this as reference material for comparing against / improving my landing page. This is **not** a request to clone Gather — it's a precise, verified record of how a well-built SaaS landing page (Gather, a retreat-booking product) is actually constructed, so you can pull specific ideas that fit my product and brand, and skip the ones that don't.

**Do not visit or re-fetch try-gather.co.** Everything below was already extracted directly from their live `styles.css`, `index.html`, and `script.js` (downloaded and read in full, not eyeballed from screenshots), then corrected after a couple of misreads were caught by live-measuring the actual rendered page. Treat every value below as verified, not estimated. It was captured 2026-08-25 — if a lot of time has passed since then, flag that marketing sites drift and this may be stale before relying on exact pixel values.

Work with me one item at a time on what (if anything) to adopt — don't bulk-implement everything from this doc at once.

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
| Section background (warm off-white) | `#F8F7F4` | Trust bar, "one platform", "why us", "how it works" |
| Footer background (cream) | `#F5EBD6` | Footer shell, stats strip |
| Border/hairline | `#e6e3dd` / `#ece7e1` / `#eee6de` (interchangeable warm grays) | Card borders, dividers |
| Success green | `#2f9e6b` | "Confirmed" / checkmark status pills in mockups |
| Error red | `#b3261e` | Form validation text |

**Note:** no CSS custom-property (`:root { --x }`) token system — every value is a literal hex repeated inline throughout the stylesheet. Colors are consistent by discipline, not variable enforcement.

### Typography
- **Display/UI font:** `'PPNM'` = PP Neue Montreal (Pangram Pangram, **paid/licensed**), self-hosted as `.ttf` files. Both files are declared at `font-weight: 700` only — this typeface is loaded at exactly one weight. Every heading, button, and label uses `font-weight: 700` explicitly.
- **Body font:** `'Helvetica Neue', Arial, sans-serif` — a system font, not custom-loaded.
- **Sizing method:** almost every font-size uses `clamp(min, preferred-vw, max)` — continuous scaling with viewport width, not fixed breakpoint jumps. Example: hero headline `font-size: clamp(34px, 5.4vw, 58px)`.
- **Letter-spacing:** headings use tight negative tracking, `-0.01em` to `-0.04em` (bigger/bolder display numbers trend tighter). Kickers/eyebrows use wide *positive* tracking instead: `letter-spacing: .14em; text-transform: uppercase`.
- **Line-height:** headlines sit at `1.04–1.1`; body copy sits at `1.35–1.65`.

### Spacing / shape scale
- **Section vertical padding:** `clamp(56px, 9vw, 110px)` top/bottom is the standard for full sections.
- **Card border-radius:** large content cards use `clamp(24px, 3vw, 36px)`; smaller cards use `18–22px`; pills/badges use `999px`; buttons use `12–15px`.
- **Card shadow convention:** soft, warm-tinted, large-blur shadows tied to the accent color rather than pure black, e.g. `box-shadow: 0 18px 50px rgba(20,26,26,.05)` for white cards, or `0 16px 30px rgba(150,50,46,.26)` for coral buttons — shadow color is a darkened version of whatever's casting it, not generic black.
- **Container max-width:** `1380px`, with fluid side gutters `clamp(20px, 5vw, 48px)`.

### Buttons
Two states, always: **Primary** (solid coral bg, white text, colored drop shadow) and **Ghost/outline** (white bg, coral text, coral inset ring `box-shadow: inset 0 0 0 2px #E7625B`). On hover they **invert into each other** — primary becomes ghost-styled, ghost becomes primary-styled — plus both lift `transform: translateY(-2px)` on hover. Transition timing is unusually slow/deliberate: `background .6s ease, color .6s ease` (most sites use 0.15–0.3s), giving the color-swap a smooth fade rather than a snap.

---

## 2. Breakpoints actually used

```
max-width: 960px   — hero and "how it works" stack to 1 column
max-width: 900px   — "why us" section stacks to 1 column, CTA band stacks
max-width: 980px   — trust bar starts wrapping (2-across)
max-width: 760px   — nav switches to burger menu, tab-swipe hint appears
max-width: 640px   — footer columns go 2-across
max-width: 560px   — trust bar goes 2-column grid, testimonial card loses max-width, CTA actions stack vertically
prefers-reduced-motion: reduce  — used consistently across every animated section to fully disable motion
```

No `min-width` breakpoints at all — written desktop-first with `max-width` overrides; font-sizes/spacing mostly self-adjust via `clamp()` without even needing a breakpoint.

---

## 3. Section-by-section structure

### 3.1 Header / nav
- `position: fixed`, top:0, full width, `z-index:100`, `rgba(255,255,255,.92)` background + `backdrop-filter: blur(10px)`.
- **Logo shrinks on scroll:** `height:50px` by default, JS adds a `.scrolled` class once `window.scrollY > 12`, CSS shrinks it to `height:35px` over a `.28s` transition. Live, animated, not just a static mobile size.
- Nav links are **absolutely centered** (`left:50%; transform:translateX(-50%)`), independent of the logo/CTA flex flow.
- CTA button exists as **two separate DOM copies** (desktop vs. inside the mobile burger sheet), toggled by CSS display at 760px rather than one button reflowing.
- Mobile burger opens a full-width dropdown sheet (`position:absolute; top:100%`); tapping any link inside auto-closes it.

### 3.2 Hero
**Critical structural point, verified by live measurement (not just reading the CSS):** the hero and the trust bar directly below it are BOTH children of one outer full-viewport flex-column wrapper (`.hero-stage`, `min-height:100vh`, reinforced by JS pinning it to `window.innerHeight`). The hero content has no explicit height of its own — it just fills whatever space is left after the trust bar takes its natural height. This guarantees the trust bar is always visible in the first screen, on any viewport height, by construction — not a coincidence of a particular screen size. **If you build a "hero + trust bar" pattern, the height-reservation math needs to live on the outer wrapper that contains both, not on the hero alone** — a mistake worth avoiding, since it's the exact one made and had to be corrected while building this reference.

Rest of the hero:
- Flex row, copy column ~40% width, image column ~60% — **the image is the majority of the hero's width**, not a small supporting element.
- Headline splits into two `<span>` lines inside one `<h1>`, each independently staggered-animated in (delays `.12s` / `.28s`) — types on line-by-line, not word-by-word.
- Hero image is a single flat `<img>` (`border-radius:22px`), a pre-composited PNG, not a live/interactive component.
- Small decorative illustration + a hand-drawn SVG squiggle line sit in the hero, `pointer-events:none`/`aria-hidden`, pure mood — the squiggle motif repeats near-identically in 4-5 other sections as a consistent "human, not corporate" visual signature.
- Only proof element in the hero itself: 5 star glyphs (literal Unicode ★, not an icon) + "Loved by [X]" text, small, under the CTAs.
- Mobile (≤960px): stacks to a column, copy centers, decorative illustration is hidden entirely (not resized, just cut).

### 3.3 Trust bar
- Own full-bleed background/borders, but structurally nested inside the same height-reserving wrapper as the hero (see 3.2) — not a section that sits *after* the hero's height budget ends.
- Flex row, each item after the first gets a `1px` left border (a vertical divider, not just a gap).
- Icon badge: `40px` circle, `8%`-opacity brand-color tint background, plus a `1.5px` inset ring at `35%` opacity — not just a flat tint, a visible thin outline too.
- Bold label + lighter gray sub-line, tight `2px` gap between them.
- Responsive collapse happens in **two stages**: first wraps to ~2-per-row (divider logic shifts to alternating items), then at the narrowest breakpoint becomes an actual CSS grid (`1fr 1fr`) with `:nth-child` border rules recreating a table-like divider grid.

### 3.4 Tabbed feature section
- Intro block (kicker + h2 + sub) sits above the tabs, independently max-width-constrained from the tab content below.
- Tab buttons live **inside one continuous bordered pill container** (not free-floating), `overflow-x:auto` for mobile scroll, adjacent tabs separated by a `1px` inset box-shadow rather than a gap.
- Active tab: background tint + colored text + a `3px` solid bottom bar via `::after` — a combined tint+underline treatment, not just one.
- **Content switching is not multiple DOM panels.** There is exactly one content panel; clicking a tab mutates its text content and swaps one `<img>`'s `src` via JS, wrapped in a 220ms fade-out → mutate → fade-in. If your product's per-tab content is structurally different per tab (not just swappable text/image), this single-shared-panel approach doesn't map cleanly — decide deliberately whether to adopt the fade-transition idea alone vs. the full DOM-collapse.
- Mobile-only "Swipe to explore →" hint text with an animated arrow, PLUS a separate one-time behavior: on page load, if the tab row's content overflows, it auto-scrolls right 72px then back after a 1s delay — a "look, this scrolls" nudge independent of the static hint text.
- Content panel itself is a 2-column grid (~44% text / ~56% image); on mobile the image is explicitly reordered *above* the text (`order:-1`) even though it's second in the DOM.

### 3.5 "Why us" section
- The entire section is one big white rounded "shell" card sitting on the warm section background — a card-within-a-section, not a flat section.
- 2-column grid, photo and copy nearly evenly split (photo marginally wider).
- Photo is forced to a portrait `aspect-ratio`, `object-fit:cover`, own shadow.
- Copy side: kicker → h2 → sub-paragraph → a short checklist (icon badge + bold label, no description text under each point) → two CTAs (one primary, one ghost).
- **Caution if you inspect a live page yourself for a section like this:** some CSS here (a floating photo-overlay quote card, a small decorative aside image) was fully styled but not actually present in the live HTML — designed but not shipped. Don't assume every selector you find in a stylesheet is currently rendered; cross-check the actual DOM.

### 3.6 "How it works" timeline
- 2-column grid, copy column narrower than the steps column, **copy column is not sticky** — scrolls normally, top-aligned.
- Copy column: kicker, a headline capped at a low character count (`max-width: 12ch`) to force an early, punchy 2-line break, sub-paragraph, one CTA, decorative squiggle.
- Steps column:
  - One continuous vertical rail line (gradient, solid accent fading to ~35% opacity top-to-bottom) runs behind all steps as a single element, not separate segments per step.
  - **Numbered circle badges are vertically centered against each step's own card height** (`position:absolute; top:50%; transform:translateY(-50%)`, relative to the individual step, not a fixed pixel offset) — matters if steps have different content lengths / different card heights, which they typically do.
  - Each step card is a 2-column grid internally: text left, a small distinct "mini" UI mockup right, `align-items:center`. The three mini-mockups are each a genuinely different hand-built micro-UI (not the same template repeated) — e.g. a call-status card, a progress-checklist card, a live-stat-plus-activity-feed card.
  - The whole steps block is a single `IntersectionObserver` target; each step has its own CSS `transition-delay` so they cascade in sequentially from one trigger.

### 3.7 Testimonial / customer story
- Just **one** card shown, not a carousel or grid — centered as the section's sole content block.
- Photo has a floating badge overlaid on it ("Featured story").
- Card content order: stars → bold pull-quote → person row (avatar, name, role/location) → 2 pill tags that encode the *specific result* ("3 → 15 retreats", "Sold out"), not generic category labels.
- A separate animated stats-counter section (count-up numbers) exists fully coded but is currently commented out of the live page — evidence of active iteration, worth knowing as a pattern (build it, then decide later whether to show it) even though it's not live right now.

### 3.8 CTA band
- Top and bottom edges of this section are literal inline `<svg>` wave shapes (a hand-drawn bezier path filled solid brand-color) instead of a straight rectangular color boundary — an organic transition into and out of the colored band. The same wave technique repeats at the footer's top edge.
- 2-column grid, image column the majority.
- A short reassurance list (e.g. "15-minute call", "No hard sell", "Real human support") sits as **plain text, not badges**, positioned *below* the CTA buttons specifically to defuse the anxiety of the highest-friction action on the page.
- A decorative arrow squiggle points toward the photo; dropped entirely on mobile rather than resized.

### 3.9 Footer
- Same wave-divider technique at its top edge, transitioning from the page background into the footer's own background color.
- 2-column grid: brand block (logo, larger than the header's own logo, kicker, h2-level tagline, one-line description, email, decorative squiggle) / link columns.
- A social-links row exists in the HTML/CSS but is `display:none` by default — another "built but switched off" element, same pattern as the stats counter.
- Every footer link has a small trailing arrow that nudges `translateX(3px)` on hover — a micro-interaction applied to plain text links, not just CTAs.
- Legal bar (registration number, copyright, a small "made with" line, legal links) wraps to stacked on mobile.

### 3.10 Contact modal
- Triggered by a secondary hero button (not a page navigation), `aria-haspopup="dialog"`.
- Standard centered modal: backdrop click or Escape both close it, focus returns to the triggering element on close — proper focus management.
- Client-side validation before a `fetch()` POST; includes a visually-hidden honeypot field purely to catch spam bots.

### 3.11 A caution about auditing any live page yourself
Two whole sections (pricing, FAQ) were fully styled in the shared stylesheet but **not present anywhere in this page's actual HTML** — they render on a different page that shares the same stylesheet file. If you inspect a live competitor page for reference the way this document was built, always cross-check which CSS selectors actually appear as real elements in that specific page's HTML — don't assume a class existing in the stylesheet means it's rendered on the page you're looking at.

---

## 4. Interaction & animation inventory

| Pattern | Trigger | Notes |
|---|---|---|
| Generic fade-up on section headings | `IntersectionObserver`, threshold 0.25 | Applied broadly, site-wide |
| Timeline steps cascade | One `IntersectionObserver` on the parent, CSS `transition-delay` per child | Steps stagger in sequentially from a single trigger |
| Testimonial card fade-in | `IntersectionObserver`, threshold 0.3 | Single card only |
| Nav logo shrink | `scroll` event, `scrollY > 12` threshold | Animated size change, `.28s` transition |
| Tab content swap | Click | 220ms fade-out → content mutate → fade-in; single shared DOM panel |
| Tab-row first-load hint | `setTimeout` 1000ms after page load, only if content overflows | Auto-scrolls right then back, once, in addition to a persistent static swipe hint |
| Footer link arrows | CSS `:hover` | `translateX(3px)` nudge per link |
| All buttons | CSS `:hover` | Fill/outline inversion + lift, unusually slow `.6s` transition |
| `prefers-reduced-motion: reduce` | Media query, checked in both CSS and JS | Every animation has an explicit disabled/instant-state fallback — handled thoroughly, not an afterthought |

---

## 5. "Curiosity hooks" / conversion devices (copy and structure tricks, independent of visual styling)

1. **Specific, odd numbers over round ones** — precise, slightly unusual numbers ("44 / 44 sold", "3 → 15") read as more real/credible than round percentages.
2. **Named, located social proof** — a real-sounding name + specific niche + specific place, not "verified customer".
3. **Live-feeling mockups instead of static screenshots** — in-progress states (a progress bar mid-fill, a relative-time activity feed, a small live-looking chart) imply motion/activity even in a static image.
4. **Proof-then-ask funnel structure with objection-handling deliberately left off the homepage scroll** — trust signals → feature depth → origin story → process de-risking → one strong testimonial → CTA. Pricing and FAQ live on separate linked pages rather than being scrolled past, so the homepage stays a pure funnel and objection-handling is one click away rather than in the main scroll.
5. **One consistent primary CTA phrase across the entire page** — every primary button uses the same action phrase; there's no split-attention between two different CTA labels doing the same job.
6. **Reassurance micro-copy placed immediately next to the single highest-friction CTA on the page**, nowhere else — it exists specifically to defuse that one moment of hesitation, not as generic trust-building repeated everywhere.
7. **A repeated hand-drawn decorative motif** used as a consistent brand signature across otherwise-unrelated sections, always non-interactive/decorative-only.
8. **Evidence of active iteration** — components that are fully built and styled but currently switched off (commented out or `display:none`) rather than deleted, suggesting an A/B or "not ready yet" workflow rather than a static, finished page.

---

*Use this to compare against my actual landing page section-by-section and suggest what's worth adapting — matched to my product and brand, not copied verbatim. Ask me before implementing anything; go one item at a time.*
