# CoTrader 3000 Landing Page — Design System Reference

Canonical values in use across all 13 pages, verified by direct audit
of the codebase (not aspirational — this is what's actually shipped).

**Important:** this repo has no shared stylesheet. Each of the 13
HTML files is fully self-contained with its own `<style>` block and
duplicated `:root` variables. This document is the closest thing to
a single source of truth — if you change a value, it needs to be
changed in all 13 files by hand (or scripted) to stay in sync.

---

## Colors

### Brand (blue)
| Token | Hex |
|---|---|
| `--blue-50` | `#eff6ff` |
| `--blue-200` | `#bfdbfe` |
| `--blue-600` | `#2563eb` (primary) |
| `--blue-700` | `#1d4ed8` (hover) |
| `--blue-800` | `#1e40af` |

### Semantic
| Token | Hex |
|---|---|
| `--green-50/100/200/500/600/700/800` | `#f0fdf4` `#dcfce7` `#bbf7d0` `#22c55e` `#16a34a` `#15803d` `#166534` |
| `--red-50/200/500/600/700` | `#fef2f2` `#fecaca` `#ef4444` `#dc2626` `#b91c1c` |
| `--amber-50/100/200/500/700/800` | `#fffbeb` `#fef3c7` `#fde68a` `#f59e0b` `#b45309` `#92400e` |

Decorative-only accents (index.html "idea" cards): `--cyan-200 #a5f3fc`, `--violet-200 #ddd6fe`, `--rose-200 #fecdd3`, `--emerald-200 #a7f3d0`.

### Neutrals
| Token | Hex |
|---|---|
| `--ink` / `--gray-900` | `#111827` |
| `--gray-700` | `#1f2937` |
| `--gray-600` | `#374151` |
| `--gray-500` | `#6b7280` |
| `--gray-400` | `#9ca3af` |
| `--gray-300` | `#d1d5db` |
| `--gray-200` | `#e5e7eb` |
| `--gray-100` | `#f3f4f6` |
| `--gray-50` | `#f9fafb` |
| `--white` | `#ffffff` |

### Section backgrounds
- Body sections alternate `var(--white)` / `var(--gray-50)`
- "Premium" dark sections (philosophy, mentorship-teaser, testimonial, footer): `linear-gradient(180deg, var(--ink) 0%, #17263d 100%)`

---

## Typography

**Font:** General Sans (Fontshare CDN), weights 400/500/600/700.
Fallback stack: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif`

```html
<link rel="preconnect" href="https://api.fontshare.com">
<link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=general-sans@400,500,600,700&display=swap">
```

### Type scale
| Element | Size | Weight | Notes |
|---|---|---|---|
| Hero H1 (index.html) | `clamp(42px, 7vw, 76px)` | 800 | line-height 1.0, letter-spacing -0.035em; 34px fixed on mobile |
| Landing-page H1 (FAQ/Blog/Mentorship) | `clamp(34px, 5vw, 50px)` | 800 | letter-spacing -0.03em |
| Article/doc H1 (7 posts + privacy/terms) | `clamp(34px, 5vw, 50px)` | 800 | matches landing-page tier |
| Section H2 (feature-tabs-head, final-cta) | `clamp(30–32px, 4.5–5vw, 44–52px)` | 800 | |
| Feature-tabs panel H3 | `clamp(32px, 4.5vw, 46px)` | 800 | color `--ink` |
| Feature-row H3 | `clamp(24px, 3vw, 34px)` | 800 | color `--blue-600` |
| Eyebrow / section-eyebrow | `12px` | 700 | letter-spacing 0.12em, uppercase, color `--blue-600` |
| Lead/body paragraph | `17px` | 400 | color `--gray-600`, line-height 1.6 |
| Nav links | `15px` | 700 | color `--gray-600` |
| Nav CTA button | `14px` | 700 | |

---

## Layout / spacing

| Context | max-width |
|---|---|
| Base `.wrap` (all pages) | `1360px`, padding `0 24px` |
| Section-scoped (FAQ / Blog listing / Mentorship / Footer) | `1080px` |
| Article/doc reading column | `680px` |

**Breakpoints:** `720px` (nav collapses to hamburger menu), `640px` (section padding tightens, hero/type sizes adjust).

**Section padding:** `96px 0` desktop default, `64px 0` on mobile.

---

## Buttons

| Class | Style |
|---|---|
| `.cta-primary` | bg `--blue-600`, white text, padding `16px 32px`, radius `999px`, font `15px/600`, shadow `0 8px 24px rgba(37,99,235,.28)`. Hover: bg `--blue-700`, `translateY(-2px)`, stronger shadow. |
| `.nav-cta` | bg `--blue-600`, white text, padding `9px 18px`, radius `999px`, font `14px/700` |
| `.cta-outline` | transparent bg, `--blue-600` text, border `1.5px solid --blue-200`, padding `16px 32px`, radius `999px` |
| `.final-cta .cta-primary` (scoped override) | hover hollows to outline instead of darkening (transparent bg, `--blue-600` border+text) |

---

## Header / Footer

**Header:** sticky, `backdrop-filter: blur(12px)`, background `rgba(255,255,255,.85)`, logo height `23px`, nav item gap `26px`. Mobile: hamburger toggle replaces nav, drops down all 5 links + Sign Up.

**Footer:** background gradient (see "Premium" above), wrap capped at `1080px`, grid `1.6fr 1fr 1fr 1fr` with `40px` gap, logo height `26px` (recolored white via `fill` override on the SVG paths — the logo's "T" is a `<polygon>`, not a `<path>`, so any recolor rule must include `polygon` or it silently stays black).

---

## Known deliberate exceptions

- Article/doc pages use a narrower `680px` reading column instead of the `1080px` section width — intentional, long-form text needs a shorter line length.
- The hero and landing-page H1s share the same `clamp(34,5vw,50)` scale as of the last audit; the hero itself goes bigger (`clamp(42,7vw,76)`) since it's the single most prominent headline on the site.

---

*Generated from a full audit of all 13 HTML files. Last verified: this session. If you add a 14th page or change a canonical value, update this file too — it's a snapshot, not enforced by tooling.*
