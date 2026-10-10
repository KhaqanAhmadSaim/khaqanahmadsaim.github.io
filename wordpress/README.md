# Own & Become: WordPress website

A complete, multi-page website for the Own & Become psychotherapy practice. It's built only with free tools and **WordPress's own block editor**, so every word, image, button, menu item and footer detail can be edited in WordPress without code and without a paid page builder.

**Status: not live.** Nothing here has been installed on ownandbecome.com yet.

## What's in this folder

| Folder | What it is |
|---|---|
| `own-and-become/` | The theme: a child theme of Twenty Twenty-Five (colours, fonts, header, footer, mobile menu, page layouts, ~30 ready-made sections). |
| `own-and-become-setup/` | A **one-time** setup plugin that builds every page, the menu, the contact form, 3 placeholder posts and the settings. Run it once, then delete it. Nothing depends on it afterwards. |
| `dist/` | The two folders above as `.zip` files, ready to upload in WordPress. |
| `tools/` | Optional. Scripts used to generate the patterns, icons and illustrations. Not needed to run or edit the site. |

## Plugins used (all free)

| Plugin | Why |
|---|---|
| **Contact Form 7** | The contact / consult request form. Free, lightweight, no upsells. |
| **Honeypot for Contact Form 7** | Invisible spam protection: no CAPTCHA puzzles for anxious visitors. (Cloudflare Turnstile, which is also free, is built into Contact Form 7 if extra protection is ever needed.) |
| **The SEO Framework** | SEO titles, meta descriptions and the XML sitemap (`/sitemap.xml`). Lightweight, no upsells. |

Everything else is core WordPress: the FAQ uses the built-in **Accordion** block, the menu is a built-in **Navigation** menu, and the fonts (Lora and Nunito Sans) are stored in the theme, so nothing loads from Google.

## How to install (when we're ready, ideally on a Hostinger staging copy first)

1. **Back up** the current site (Hostinger → Websites → Backups).
2. In WordPress: **Plugins → Add New**, install and activate *Contact Form 7*, *Honeypot for Contact Form 7* and *The SEO Framework*.
3. **Appearance → Themes → Add New → Upload Theme**, upload `dist/own-and-become-theme.zip`, then **Activate**. (Twenty Twenty-Five is already installed.)
4. **Plugins → Add New → Upload Plugin**, upload `dist/own-and-become-setup.zip`, activate it.
5. Go to **Tools → Own & Become Setup**, check that every item is ticked, and press **Run setup**.
6. Look through the site. Then **deactivate and delete** the setup plugin.
7. Recommended clean-up: deactivate Elementor, WooCommerce and the Kadence theme if they're no longer used (see the suggestions below).

The setup never overwrites an existing page with the same address. It only replaces WordPress's untouched draft Privacy Policy page.

## Where to edit things

| To change… | Go to |
|---|---|
| Any page's text, images, buttons, FAQ | **Pages →** the page **→ Edit** |
| Header, info bar (phone, Client Login), footer, contact details, social links | **Appearance → Editor → Patterns → Template parts** (Header / Footer / Mobile menu overlay) |
| Main menu (including the Services dropdown) | **Appearance → Editor → Navigation** |
| Crisis notice, "Ready when you are" call to action, leaf divider (edit once, updates everywhere) | **Appearance → Editor → Patterns → Own & Become** (synced patterns) |
| Add a section to any page | In the editor: **+ → Patterns → "Own & Become: sections"** |
| Colours and fonts site-wide | **Appearance → Editor → Styles** |
| Form fields and the email address it sends to | **Contact → Contact Forms → Own and Become contact form** (the **Mail** tab) |
| SEO title and description of a page | The page's editor, in the *SEO Framework* box at the bottom |
| Blog posts and categories | **Posts** |

**Swapping in Jane later:** every "Book a Free Consult" button points to one page, `/book/`. When the Jane booking link is ready, edit just that page (replace the "Online booking" box with a button to Jane). Nothing else needs to change. Also update the **Client Login** link in the header and the mobile menu.

## Placeholders

Anything still to fill in shows up on the site highlighted in yellow, as **[ADD …]** or **[CONFIRM …]**. Search the editor for `[ADD` and `[CONFIRM`.
