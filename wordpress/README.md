# Own & Become: WordPress website

A complete, multi-page website for the Own & Become psychotherapy practice. It's built only with free tools and **WordPress's own block editor**, so every word, image, button, menu item and footer detail can be edited in WordPress without code and without a paid page builder.

**Status: not live.** Installed and set up on the Hostinger staging copy, https://staging.ownandbecome.com (search engines are blocked there). The live ownandbecome.com still shows its Coming Soon page.

## What's in this folder

| Folder | What it is |
|---|---|
| `own-and-become/` | The theme: a child theme of Twenty Twenty-Five (colours, fonts, header, footer, mobile menu, page layouts, ~30 ready-made sections). |
| `own-and-become-setup/` | A **one-time** setup plugin that builds every page, the menu, the contact form, 3 placeholder posts and the settings. Run it once, then delete it. Nothing depends on it afterwards. |
| `dist/` | The two folders above as `.zip` files, ready to upload in WordPress. |
| `tools/` | Optional, historical. Scripts first used to generate the patterns, icons and illustrations. The patterns have since been edited directly (copy changes, photos), so `own-and-become/patterns/` is now the source of truth: don't re-run `tools/patterns.py` over it. |

## Plugins used (all free)

| Plugin | Why |
|---|---|
| **Contact Form 7** | The contact / consult request form. Free, lightweight, no upsells. |
| **Honeypot for Contact Form 7** | Invisible spam protection: no CAPTCHA puzzles for anxious visitors. (Cloudflare Turnstile, which is also free, is built into Contact Form 7 if extra protection is ever needed.) |
| **The SEO Framework** | SEO titles, meta descriptions and the XML sitemap (`/sitemap.xml`). Lightweight, no upsells. |
| **WP Mail SMTP** | Sends website email (the contact form) through the info@ownandbecome.com mailbox at Hostinger, so it reaches the inbox, not Junk. |
| **Flamingo** | Keeps a copy of every contact-form message in the dashboard (**Contact → Flamingo**), including ones flagged as spam, so nothing is lost. |

Everything else is core WordPress: the FAQ uses the built-in **Accordion** block, the menu is a built-in **Navigation** menu, and the fonts (Lora and Nunito Sans) are stored in the theme, so nothing loads from Google.

## How to install (when we're ready, ideally on a Hostinger staging copy first)

1. **Back up** the current site (Hostinger → Websites → Backups).
2. In WordPress: **Plugins → Add New**, install and activate *Contact Form 7*, *Honeypot for Contact Form 7* and *The SEO Framework*.
3. **Appearance → Themes → Add New → Upload Theme**, upload `dist/own-and-become-theme.zip`, then **Activate**. (Twenty Twenty-Five is already installed.)
4. **Plugins → Add New → Upload Plugin**, upload `dist/own-and-become-setup.zip`, activate it.
5. Go to **Tools → Own & Become Setup**, check that every item is ticked, and press **Run setup**.
6. Look through the site. Then **deactivate and delete** the setup plugin.
7. Recommended clean-up: deactivate Elementor, WooCommerce and the Kadence theme if they're no longer used (see the suggestions below).

The setup never overwrites an existing page that has real content or is already published. It only fills in empty, unpublished placeholder pages with the same address (the live site has empty private Home, About, Services, Resources and Contact pages left over from its original setup) and WordPress's untouched sample Privacy Policy, keeping their IDs so links stay valid.

On a site copied from the live one, also deactivate **WooCommerce**: otherwise it adds a shopping-cart and account icon to the header.

## Where to edit things

| To change… | Go to |
|---|---|
| Any page's text, images, buttons, FAQ | **Pages →** the page **→ Edit** |
| Header, info bar (phone, Client Login), footer, contact details, social links | **Appearance → Editor → Patterns → Template parts** (Header / Footer / Mobile menu overlay) |
| Main menu (including the Services dropdown) | **Appearance → Editor → Navigation** |
| Crisis notice, "Get connected" call to action, leaf divider (edit once, updates everywhere) | **Appearance → Editor → Patterns → Own & Become** (synced patterns) |
| Add a section to any page | In the editor: **+ → Patterns → "Own & Become: sections"** |
| Colours and fonts site-wide | **Appearance → Editor → Styles** |
| Form fields and the email address it sends to (info@ownandbecome.com) | **Contact → Contact Forms → Own and Become contact form** (the **Mail** tab) |
| SEO title and description of a page | The page's editor, in the *SEO Framework* box at the bottom |
| Blog posts and categories | **Posts** |

**Booking (Jane):** every "Book a Free Consult" button (header, mobile menu, home, service pages, footer and the shared "Get connected" box) links straight to the Jane booking page, https://ownandbecome.janeapp.com. The `/book/` page stays as a short "what to expect" page with a **Book on Jane** button and the contact form for people who prefer to send a message. If the Jane address ever changes, search the editor for `janeapp.com`. There's no Client Login link: clients sign in through Jane.

**Fees:** there is no separate Fees page. Fees, the sliding scale, insurance, translation cost, payment and cancellation are answered in the FAQ's **Fees & insurance** section (`/faq/#fees`), and old `/fees/` links redirect there. The sliding scale is also on the Services page.

**Contact details:** phone 705-770-2733 and info@ownandbecome.com appear in the header, mobile menu, footer and contact section.

## Photos

The section photos are royalty-free from [Pexels](https://www.pexels.com/license/) (free for commercial use, no credit required), cropped and stored in `own-and-become/assets/images/photos/`. On the site they live in the Media Library, so any of them can be swapped in the page editor.

| File | Where | Pexels photo |
|---|---|---|
| `hero-armchair.jpg` | Home, top (arch frame) | [40059237](https://www.pexels.com/photo/40059237/) |
| `not-alone-plant.jpg` | Home, “This isn’t how you thought life would feel” | [20643351](https://www.pexels.com/photo/20643351/) |
| `own-soil.jpg` | Home, “Own” card | [31374933](https://www.pexels.com/photo/31374933/) |
| `become-fern.jpg` | Home, “Become” card | [13079522](https://www.pexels.com/photo/13079522/) |
| `about-hands.jpg` | About | [6134941](https://www.pexels.com/photo/6134941/) |
| `online-session.jpg` | Services, “Not sure” section | [8473914](https://www.pexels.com/photo/8473914/) |
| `areas-fern.jpg` | Areas We Support, “Not listed” section | [18189850](https://www.pexels.com/photo/18189850/) |

The therapist portrait on the live pages is uploaded in WordPress (Media Library); the theme file is only a placeholder.

## Spam protection & email

- **Where messages go:** the contact form sends to **info@ownandbecome.com** (Contact → Contact Forms → Own and Become contact form → Mail). Press Reply to answer the visitor.
- **Sending:** WP Mail SMTP (Settings → WP Mail SMTP) uses `smtp.hostinger.com`, SSL, port 465, username info@ownandbecome.com. The mailbox **password must be entered there** (it is never stored in this repository). Use *Email Test* on that page to check.
- **Bots:** an invisible honeypot field. For stronger protection add **Cloudflare Turnstile** (free): create a Turnstile widget for the domain at dash.cloudflare.com, then paste the Site Key and Secret Key in **Contact → Integration → Cloudflare Turnstile**. It's added to the form automatically.
- **Sales pitches:** phrases such as "SEO services", "link building", "first page of Google" are listed in **Settings → Discussion → Disallowed Comment Keys**. Matching form messages are treated as spam: not emailed, but kept in **Contact → Flamingo → Inbound Messages → Spam**. Glance at that list now and then and click *Not spam* if a real enquiry was caught. Edit the list there (one phrase per line).
- **Emails sent straight to info@:** in Hostinger webmail, *Settings → Filters*: add a rule "if Subject or Body contains SEO services / backlinks / lead generation / web design services → move to folder *Sales pitches*", and block persistent senders with *Block sender*.

## Placeholders

Anything still to fill in shows up on the site highlighted in yellow, as **[ADD …]** or **[CONFIRM …]**. Search the editor for `[ADD` and `[CONFIRM`.
