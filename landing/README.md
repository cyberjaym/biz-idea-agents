# RoyaltyStack — Waitlist Landing Page

A single static page for pre-product demand validation. It collects email
signups from digital-download sellers before RoyaltyStack is built. No
backend, no database, no paid service — just `index.html` and `styles.css`.

Copy is taken verbatim from `../ideas/royaltystack/README.md`.

## Files

- `index.html` — the page markup and copy
- `styles.css` — plain CSS, no framework, mobile-friendly

## How the email capture works

The form uses [Netlify Forms](https://docs.netlify.com/forms/setup/), which
is free on Netlify's free tier and requires no separate signup or account
for a service beyond Netlify itself. It works by:

- `<form name="waitlist" data-netlify="true" ...>` — tells Netlify to detect
  and process this form at deploy time.
- A hidden `form-name` input matching the form's `name` — required for
  Netlify's static HTML form detection.
- `netlify-honeypot="bot-field"` plus a hidden `bot-field` input — Netlify's
  built-in spam trap, no extra service needed.

No JavaScript, API keys, or backend code are required for this to work.

## Deploy for free (pick one)

### Option A: Drag-and-drop (no CLI, no account setup beyond a free Netlify account)

1. Go to [app.netlify.com/drop](https://app.netlify.com/drop).
2. Drag the `landing/` folder onto the page.
3. Netlify deploys it instantly on a free `*.netlify.app` URL and
   auto-detects the `waitlist` form.

### Option B: Netlify CLI

```bash
npm install -g netlify-cli
cd landing
netlify deploy --prod
```

Follow the prompts to log in (free account) and create/link a site. Netlify
will publish the current directory and detect the form automatically.

## Where signups show up

After deploy, every submission appears under the site's **Forms** section in
the Netlify dashboard (Site → Forms → waitlist). No database, email service,
or third-party tool is required to view or export them.

## What's intentionally left out

- No analytics or tracking scripts.
- No custom domain setup (use the free `*.netlify.app` subdomain until
  there's demand to justify a domain).
- No thank-you page/redirect — Netlify shows its default success message
  after submission, which is enough for a demand-validation test.
