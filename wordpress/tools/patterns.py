import sys, os, re
sys.path.insert(0, os.path.dirname(__file__))
from blocks import *

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'own-and-become', '')+'patterns/'
A = lambda f: f'ASSET:{f}'   # replaced with a PHP call to own_and_become_asset()
PH = lambda t: f'<mark class="ob-placeholder">[{t}]</mark>'  # visible placeholder for the owner

PROVINCES = 'Ontario, British Columbia, Alberta, Saskatchewan, Manitoba, New Brunswick, Newfoundland and Labrador, Yukon, the Northwest Territories and Nunavut'

def write(slug, title, content, cats=('own-and-become',), desc='', inserter=True, post_types=None, block_types=None, keywords=None):
    head = ['<?php', '/**', f' * Title: {title}', f' * Slug: own-and-become/{slug}', f' * Categories: {", ".join(cats)}']
    if desc: head.append(f' * Description: {desc}')
    if keywords: head.append(f' * Keywords: {keywords}')
    if post_types: head.append(f' * Post Types: {post_types}')
    if block_types: head.append(f' * Block Types: {block_types}')
    if not inserter: head.append(' * Inserter: no')
    head += [' *', ' * @package own-and-become', ' */', '?>']
    body = re.sub(r'ASSET:([\w\-/\.]+)', lambda m: f"<?php echo own_and_become_asset( '{m.group(1)}' ); ?>", content)
    open(OUT + slug + '.php', 'w').write('\n'.join(head) + '\n' + body + '\n')

def section(inner, bg=None, pad=('70', '70'), cls=None, name=None, wide=True, extra=None):
    a = {'align': 'full', 'style': {'spacing': {'padding': {'top': f'var:preset|spacing|{pad[0]}', 'bottom': f'var:preset|spacing|{pad[1]}'}}}}
    if name: a = {'metadata': {'name': name}, **a}
    if bg: a['backgroundColor'] = bg
    if cls: a['className'] = cls
    if extra: a.update(extra)
    a['layout'] = {'type': 'constrained'}
    if wide:
        inner = group(inner, {'align': 'wide', 'layout': {'type': 'default'}})
    return group(inner, a)

def intro(eyebrow, title, lede=None, center=True, level=2, size=None, width='680px'):
    al = {'align': 'center'} if center else {}
    blocks = [p(eyebrow, {**al, 'className': 'is-style-eyebrow'}) if eyebrow else '',
              heading(title, level, ({'textAlign': 'center'} if center else {}) | ({'fontSize': size} if size else {})),
              p(lede, {**al, 'fontSize': 'large'} if lede else {}) if lede else '']
    return group(J(*blocks), {'style': {'spacing': {'blockGap': '1rem', 'margin': {'bottom': 'var:preset|spacing|50'}}},
                              'layout': {'type': 'constrained', 'contentSize': width, **({} if center else {'justifyContent': 'left'})}})

def icon(name, alt='', size='3rem', cls='ob-icon'):
    return image(A(f'icons/{name}.svg'), alt, {'width': size, 'sizeSlug': 'full', 'className': cls})

def card(inner, tint=False, pad='var:preset|spacing|40', cls='', link=False):
    c = ('is-style-card-tint' if tint else 'is-style-card') + (' ob-card-link' if link else '') + (f' {cls}' if cls else '')
    return group(inner, {'className': c, 'style': {'spacing': {'padding': {'top': pad, 'bottom': pad, 'left': pad, 'right': pad}, 'blockGap': '0.85rem'}, 'dimensions': {'minHeight': '100%'}},
                         'layout': {'type': 'flex', 'orientation': 'vertical', 'justifyContent': 'stretch'}})

def grid(items, min_w='16rem', gap='var:preset|spacing|30', cls=None, cols=None):
    if cols is None:
        cols = len(items) if len(items) <= 4 else 3
    a = {'style': {'spacing': {'blockGap': gap}}, 'layout': {'type': 'grid', 'minimumColumnWidth': min_w, 'columnCount': cols}}
    if cls: a['className'] = cls
    return group(J(*items), a)

def chips(items):
    lis = '\n\n'.join(f'<!-- wp:list-item -->\n<li>{i}</li>\n<!-- /wp:list-item -->' for i in items)
    return f'<!-- wp:list {{"className":"ob-area-chips"}} -->\n<ul class="wp-block-list ob-area-chips">{lis}</ul>\n<!-- /wp:list -->'

def btn_book(text='Book a Free Consult'):
    return button(text, '/book/')

def btn_outline(text, href):
    return button(text, href, {'className': 'is-style-outline'})

def leaf_list(items):
    return ul(items, {'className': 'is-style-leaf-list'})

def page_hero(eyebrow, title, lede, buttons_markup=None, image_markup=None):
    left = J(p(eyebrow, {'className': 'is-style-eyebrow'}), heading(title, 1, {'fontSize': 'xx-large'}), p(lede, {'fontSize': 'large'}), buttons_markup or '')
    if image_markup:
        inner = columns(column(group(left, {'style': {'spacing': {'blockGap': '1.1rem'}}, 'layout': {'type': 'default'}}), {'width': '58%', 'verticalAlignment': 'center'}),
                        column(image_markup, {'width': '42%', 'verticalAlignment': 'center'}),
                        a={'verticalAlignment': 'center', 'style': {'spacing': {'blockGap': {'left': 'var:preset|spacing|60'}}}})
    else:
        inner = group(left, {'style': {'spacing': {'blockGap': '1.1rem'}}, 'layout': {'type': 'constrained', 'contentSize': '720px', 'justifyContent': 'left'}})
    return section(inner, bg='tint', pad=('60', '60'), cls='ob-page-hero', name='Page hero')

def cta():
    return pattern('own-and-become/cta-book')

def crisis():
    return pattern('own-and-become/crisis-notice')

def divider():
    return pattern('own-and-become/leaf-divider')

# =====================================================================
# Small reusable pieces (some become synced patterns in the setup step)
# =====================================================================

CRISIS = group(J(
    p('<strong>If you are in crisis or thinking about suicide</strong>, call or text <a href="tel:988">988</a> (Suicide Crisis Helpline, Canada), call <a href="tel:911">911</a>, or go to your nearest emergency room. This website and our contact form are not monitored for emergencies.', {'style': {'typography': {'fontSize': '1rem'}}})
), {'metadata': {'name': 'Crisis notice'}, 'className': 'ob-crisis', 'style': {'border': {'radius': '14px'}, 'spacing': {'padding': {'top': '1rem', 'bottom': '1rem', 'left': '1.25rem', 'right': '1.25rem'}}, 'elements': {'link': {'color': {'text': 'var:preset|color|primary-deep'}}}},
    'backgroundColor': 'tint', 'textColor': 'contrast', 'layout': {'type': 'default'}})
write('crisis-notice', 'Crisis notice', CRISIS, desc='The 988 / 911 crisis notice shown in the footer and near forms.', keywords='crisis, 988, emergency')

CTA = group(J(
    group(J(
        p('When you’re ready', {'align': 'center', 'className': 'is-style-eyebrow'}),
        heading('Ready when you are.', 2, {'textAlign': 'center', 'style': {'elements': {'link': {'color': {'text': 'var:preset|color|base'}}}}, 'textColor': 'base'}),
        p('A free 15-minute consult is a gentle first step. No pressure and no commitment, just a conversation about what you’re looking for.', {'align': 'center', 'fontSize': 'large'}),
        buttons(button('Book a Free Consult', '/book/', {'backgroundColor': 'base', 'textColor': 'primary-deep', 'style': {'border': {'color': '#FBFAF6'}}}),
                button('Ask a question', '/contact/', {'className': 'is-style-outline', 'textColor': 'base', 'style': {'border': {'color': '#FBFAF6'}}}),
                a={'layout': {'type': 'flex', 'justifyContent': 'center'}}),
    ), {'style': {'spacing': {'blockGap': '1.1rem'}}, 'layout': {'type': 'constrained', 'contentSize': '640px'}}),
), {'metadata': {'name': 'Book a Free Consult call to action'}, 'align': 'full', 'className': 'ob-cta', 'style': {'spacing': {'padding': {'top': 'var:preset|spacing|70', 'bottom': 'var:preset|spacing|70'}}, 'elements': {'link': {'color': {'text': 'var:preset|color|base'}}}},
    'backgroundColor': 'primary-deep', 'textColor': 'base', 'layout': {'type': 'constrained'}})
write('cta-book', 'Call to action: Ready when you are', CTA, desc='Final call to action with the Book a Free Consult button.', keywords='book, consult, cta')

DIV = separator({'className': 'is-style-leaf-curve'})
write('leaf-divider', 'Leaf-curve divider', DIV, desc='A soft divider echoing the copper leaves in the logo.', keywords='divider, separator, leaf')

def service_card(icon_name, title, text, href, link_text='Learn more'):
    return card(J(icon(icon_name), heading(title, 3, {'fontSize': 'large'}), p(text),
                  p(f'<a href="{href}">{link_text}<span class="screen-reader-text"> about {title.lower()}</span> →</a>', {'className': 'ob-stretch', 'style': {'typography': {'fontWeight': '700'}}})), link=True)

write('service-card', 'Service card', service_card('individual', 'Service name', 'One warm sentence about who this is for and how it helps.', '/services/'),
      desc='Layout for a single service card. Duplicate it to add more.', keywords='service, card')

SERVICES = [
    ('individual', 'Individual therapy', 'One-on-one time to slow down, make sense of what you’re carrying, and build tools that fit your real life.', '/services/individual-therapy/'),
    ('couples', 'Couples therapy', 'For partners who want to understand each other again, talk with more care, and move through change together, including pre-marital support.', '/services/couples-therapy/'),
    ('teen', 'Teen therapy (14+)', 'A judgment-free space for teens to talk about stress, emotions, relationships and growing up, at their own pace.', '/services/teen-therapy/'),
    ('online', 'Online therapy', 'Every session happens by video, so support fits around your life, from Ontario to many provinces and territories across Canada.', '/services/online-therapy/'),
]

SERVICES_GRID = grid([service_card(*s) for s in SERVICES], min_w='15rem', cls='ob-reveal-group')

AREAS = [
    ('wave', 'Stress & emotions', ['Stress management', 'Coping skills', 'Emotion regulation', 'Anger management']),
    ('family', 'Relationships & family', ['Marital and pre-marital', 'Family dynamics & relationships', 'Parenting', 'Boundary setting']),
    ('seed', 'Pregnancy & fertility', ['Pregnancy', 'Postpartum depression', 'Infertility', 'Miscarriage']),
    ('falling-leaf', 'Grief & loss', ['Grief', 'Loss', 'Bereavement']),
    ('path', 'Life transitions', ['Life transitions', 'Life coaching']),
    ('compass', 'Career', ['Career guidance', 'Career change', 'Career crisis']),
]

def area_card(ic, title, items, tint=False):
    return card(J(group(J(icon(ic, '', '2.5rem', 'ob-icon ob-icon--sm'), heading(title, 3, {'fontSize': 'large'})),
                        {'style': {'spacing': {'blockGap': '0.75rem'}}, 'layout': {'type': 'flex', 'flexWrap': 'nowrap'}}),
                  chips(items)), tint=tint)

STEPS = [
    ('calendar', 'Book a free consult', 'Choose a time for a free 15-minute call. There’s nothing to prepare and no commitment.'),
    ('chat', 'Have a conversation', 'Share a little about what’s going on and ask anything you like. Together, we’ll see whether we feel like a good fit.'),
    ('sprout', 'Book your first session', 'If it feels right, we’ll book your first session and begin, at a pace that feels right for you.'),
]

def steps_block():
    cols = []
    for i, (ic, t, d) in enumerate(STEPS, 1):
        cols.append(column(J(
            group(J(p(str(i), {'className': 'is-style-step-number'})), {'layout': {'type': 'flex', 'justifyContent': 'center'}}),
            heading(t, 3, {'textAlign': 'center', 'fontSize': 'large'}),
            p(d, {'align': 'center'}))))
    return columns(*cols, a={'className': 'ob-steps ob-reveal-group', 'style': {'spacing': {'blockGap': {'left': 'var:preset|spacing|50', 'top': 'var:preset|spacing|50'}}}})

# FAQ content ----------------------------------------------------------
FAQ = {
 'cost': ('How much does therapy cost?', J(p('We share fees during your free 15-minute consultation, where we can talk openly about what you’re looking for and answer any questions about cost. ' + PH('ADD: sliding-scale or reduced-fee option, if offered')))),
 'insurance': ('Is therapy covered by insurance or workplace benefits?', J(p('Many extended health plans include some coverage for psychotherapy, but every plan is different. We recommend checking with your provider whether sessions with a Registered Psychotherapist (Qualifying) are covered. ' + PH('CONFIRM: whether receipts are issued for benefits claims')))),
 'cancel': ('What is your cancellation policy?', J(p(PH('ADD CANCELLATION POLICY: how much notice is needed to cancel or reschedule, and whether a fee applies')))),
 'length': ('How long does therapy last?', J(p('It’s different for everyone. Some people come for a handful of sessions to work on something specific; others find longer-term support helpful. We’ll check in regularly about how things are going, and you’re always in charge of the pace.'))),
 'right': ('How do I know if therapy is right for me?', J(p('You don’t need to be in crisis, or “struggling enough,” to deserve support. If something feels heavy, confusing or stuck, that’s reason enough to reach out. The free consult is a no-pressure way to find out whether therapy, and this practice, feels right for you.'))),
 'confidential': ('Is what I share kept confidential?', J(p('Yes. What you share in therapy is kept private and stored securely. There are a few limits set by law, for example if there is a serious risk of harm to you or someone else, or if a child may be at risk. We’ll explain these clearly before we begin, so there are no surprises.'))),
 'first': ('What is the first session like?', J(p('The first session is mostly about getting to know you: what’s going on, what you’d like to be different, and what matters to you. You can share as much or as little as feels comfortable. You don’t need the right words or a plan.'))),
 'online': ('Do you offer in-person sessions?', J(p(f'All sessions are currently online by video, so you can join from home or any private space where you feel comfortable. Online therapy is available to people living in {PROVINCES}.'))),
 'consult': ('What happens in the free consult?', J(p('It’s a relaxed 15-minute call. You can share a little about what’s bringing you to therapy, ask questions about how we work, and get a sense of whether it feels like a good fit. There’s no pressure to book anything afterward.'))),
 'language': ('Can I have sessions in Urdu or Hindi?', J(p('Yes. Sessions are available in English, Urdu and Hindi, and you’re welcome to move between languages if that feels more natural. Let us know your preference when you get in touch.'))),
 'teens': ('Can teens book sessions?', J(p('Yes, we work with teens aged 14 and over. A parent or guardian can reach out on a teen’s behalf, or a teen can reach out themselves. ' + PH('CONFIRM: your consent process and what is shared with parents for clients aged 14–17')))),
 'couples': ('Do both partners need to attend couples therapy?', J(p('Couples sessions usually include both partners, and sometimes there’s value in an individual session along the way. If your partner isn’t ready yet, you’re still welcome to start with individual therapy.'))),
 'fit': ('What if it doesn’t feel like a good fit?', J(p('That’s okay, and it’s worth saying out loud. A good fit matters a lot in therapy. We can talk about what isn’t working, adjust our approach, or help you find someone who may be a better match.'))),
 'emergency': ('Can I use the contact form if I’m in crisis?', J(p('Please don’t. Our inbox isn’t monitored around the clock. If you are in crisis or thinking about suicide, call or text <a href="tel:988">988</a>, call <a href="tel:911">911</a>, or go to your nearest emergency room.'))),
 'prepare': ('Do I need to prepare anything?', J(p('Not really. Find a private, comfortable spot, a device with a camera, and a steady internet connection. Some people like to jot down a few thoughts beforehand, but it’s never required.'))),
}

def faq(keys):
    return accordion([FAQ[k] for k in keys])

HOME_FAQ = ['cost', 'insurance', 'first', 'length', 'right', 'confidential', 'online', 'cancel']

# =====================================================================
# Home page sections
# =====================================================================

HERO = section(columns(
    column(group(J(
        p('Online therapy for teens, adults &amp; couples', {'className': 'is-style-eyebrow'}),
        heading('Your story. Your pace. <em>Your change.</em>', 1),
        p(f'Warm, practical online therapy for teens (14+), adults and couples across Canada, in English, Urdu or Hindi. We’ll walk alongside you as you make sense of what feels hard, and grow toward what matters to you.', {'className': 'ob-hero__lede', 'fontSize': 'large'}),
        buttons(btn_book(), btn_outline('Meet Your Therapist', '/therapist/')),
        p('Free 15-minute consult · No pressure, no commitment', {'textColor': 'muted', 'fontSize': 'small'}),
    ), {'style': {'spacing': {'blockGap': '1.25rem'}}, 'layout': {'type': 'default'}}), {'width': '56%', 'verticalAlignment': 'center'}),
    column(image(A('images/hero-arch.svg'), 'Illustration of two people walking side by side along a winding path through soft green hills, beside a tree that bends but keeps growing.', {'sizeSlug': 'full', 'className': 'ob-reveal'}), {'width': '44%', 'verticalAlignment': 'center'}),
    a={'verticalAlignment': 'center', 'style': {'spacing': {'blockGap': {'left': 'var:preset|spacing|60', 'top': 'var:preset|spacing|50'}}}}),
    pad=('60', '60'), cls='ob-hero', name='Hero')
write('hero-home', 'Home: hero', HERO, keywords='hero, header, banner')

REASSURE_ITEMS = [('consult', 'Free 15-minute consult'), ('online', 'Online sessions across Canada'), ('languages', 'English, Urdu &amp; Hindi'), ('confidential', 'A safe, confidential space')]
REASSURE = section(grid([group(J(icon(i, '', '2.75rem', 'ob-icon'), p(t)), {'className': 'ob-reassure__item', 'layout': {'type': 'flex', 'flexWrap': 'nowrap'}}) for i, t in REASSURE_ITEMS],
                        min_w='13rem', gap='var:preset|spacing|30', cls='ob-reassure ob-reveal-group', cols=4),
                   bg='surface', pad=('40', '40'), name='Reassurance row',
                   extra={'style': {'spacing': {'padding': {'top': 'var:preset|spacing|40', 'bottom': 'var:preset|spacing|40'}}, 'border': {'top': {'color': 'var:preset|color|line', 'width': '1px'}, 'bottom': {'color': 'var:preset|color|line', 'width': '1px'}}}})
write('reassurance', 'Home: four reassurance points', REASSURE, keywords='reassurance, features, trust')

EMPATHY = section(columns(
    column(group(J(
        p('You’re not alone in this', {'className': 'is-style-eyebrow'}),
        heading('This isn’t how you thought life would feel.'),
        p('Maybe you’re tired in a way sleep doesn’t fix. Maybe a loss, a new baby, a relationship or a career change has left you feeling unlike yourself. Or maybe nothing is “wrong” enough to explain, and you’re still carrying something heavy.'),
        leaf_list(['Worry that won’t switch off', 'Feeling stuck, flat or overwhelmed', 'Grief that arrives in waves', 'Tension at home or in your relationship', 'Big changes: pregnancy, parenthood, career, identity', 'Saying yes when you mean no']),
        p('You don’t have to be in crisis to deserve support, and you don’t need the right words to begin. <strong>You don’t have to figure it out alone, or all at once.</strong>'),
        buttons(btn_outline('See how we can help', '/areas-we-support/')),
    ), {'style': {'spacing': {'blockGap': '1.15rem'}}, 'layout': {'type': 'default'}}), {'width': '55%', 'verticalAlignment': 'center'}),
    column(J(image(A('images/path-sprout.svg'), 'Illustration of a line that loops back on itself, keeps moving forward, and grows into a small sprout.', {'sizeSlug': 'full', 'className': 'ob-reveal'}),
             p('<em>Healing isn’t a straight line. We’ll go at your pace.</em>', {'align': 'center', 'fontFamily': 'heading', 'fontSize': 'large', 'textColor': 'primary'})),
           {'width': '45%', 'verticalAlignment': 'center'}),
    a={'verticalAlignment': 'center', 'style': {'spacing': {'blockGap': {'left': 'var:preset|spacing|60', 'top': 'var:preset|spacing|50'}}}}),
    name='Empathy')
write('empathy', 'Home: empathy section', EMPATHY, keywords='empathy, struggles')

APPROACHES = 'person-centred and mindfulness-based therapy, Acceptance and Commitment Therapy (ACT), Cognitive Behavioural Therapy (CBT), Internal Family Systems-informed therapy, Emotion-Focused Therapy (EFT) and Solution-Focused Brief Therapy (SFBT)'

OWN_BECOME = section(J(
    intro('Our approach', 'Own your story. <em>Become</em> who you’re choosing to be.', 'Therapy here isn’t about fixing you, because you aren’t broken. It’s a relationship: two people working together, at your pace, through two connected parts.'),
    columns(
        column(J(image(A('images/own-roots.svg'), 'Illustration of a small plant with strong roots.', {'width': '220px', 'sizeSlug': 'full', 'align': 'center'}),
                 heading('Own', 3, {'textAlign': 'center'}),
                 p('Owning your story means looking at what has happened, and what’s happening now, with honesty and self-compassion. We make room for all of it: the hard parts, the proud parts and everything in between, without judgment.', {'align': 'center'})),
               {'className': 'is-style-card', 'style': {'spacing': {'padding': {'top': 'var:preset|spacing|50', 'bottom': 'var:preset|spacing|50', 'left': 'var:preset|spacing|50', 'right': 'var:preset|spacing|50'}}}}),
        column(J(image(A('images/become-growth.svg'), 'Illustration of a young plant growing new leaves.', {'width': '220px', 'sizeSlug': 'full', 'align': 'center'}),
                 heading('Become', 3, {'textAlign': 'center'}),
                 p('Becoming is the growth that follows. Together, we build practical tools and small, doable steps toward the person you’re choosing to be: steadier, more connected, more yourself. Growth is rarely a straight line, and that’s okay.', {'align': 'center'})),
               {'className': 'is-style-card-tint', 'style': {'spacing': {'padding': {'top': 'var:preset|spacing|50', 'bottom': 'var:preset|spacing|50', 'left': 'var:preset|spacing|50', 'right': 'var:preset|spacing|50'}}}}),
        a={'className': 'ob-two-part', 'style': {'spacing': {'blockGap': {'left': 'var:preset|spacing|30', 'top': 'var:preset|spacing|30'}}}}),
    group(J(p(f'Depending on what you need, we draw on {APPROACHES}. Always shaped around you, never one-size-fits-all.', {'align': 'center'}),
            p('<a href="/about/">More about our approach →</a>', {'align': 'center', 'style': {'typography': {'fontWeight': '700'}}})),
          {'style': {'spacing': {'margin': {'top': 'var:preset|spacing|50'}, 'blockGap': '0.75rem'}}, 'layout': {'type': 'constrained', 'contentSize': '720px'}}),
), bg='tint', cls='is-style-section-curve', name='Own and Become approach')
write('own-become', 'Home: Own and Become approach', OWN_BECOME, keywords='approach, own, become')

SERVICES_SECTION = section(J(
    intro('Services', 'Support that meets you where you are', 'All sessions are online, so you can join from home or wherever you feel most at ease.'),
    SERVICES_GRID,
), name='Services')
write('services-cards', 'Home: services cards', SERVICES_SECTION, keywords='services, cards')

AREAS_SECTION = section(J(
    intro('Areas we support', 'Whatever brought you here, it’s welcome here', 'A few of the things people often bring to therapy. If yours isn’t listed, you’re still welcome to reach out.'),
    grid([area_card(*a, tint=True) for a in AREAS], min_w='19rem', cls='ob-reveal-group'),
    buttons(btn_outline('Explore all areas we support', '/areas-we-support/'), a={'layout': {'type': 'flex', 'justifyContent': 'center'}, 'style': {'spacing': {'margin': {'top': 'var:preset|spacing|50'}}}}),
), bg='surface', name='Areas we support')
write('areas-grid', 'Home: areas we support', AREAS_SECTION, keywords='areas, issues, support')

BIO_SHORT = 'Before I was a therapist, I was a daughter, sister, wife, and mother. Those roles taught me about love, loss, and resilience, and how heavy life can feel even in good seasons. I support people through anxiety, grief, relationship challenges, self-doubt, and pregnancy or postpartum changes, with warmth, practical tools, and no pressure to have it all figured out. You don’t have to carry it alone.'

THERAPIST = section(columns(
    column(image(A('images/portrait-placeholder.svg'), 'Placeholder for a photo of Ayesha Munawar, Registered Psychotherapist (Qualifying).', {'sizeSlug': 'full', 'className': 'ob-portrait ob-reveal'}), {'width': '38%', 'verticalAlignment': 'center'}),
    column(group(J(
        p('Meet your therapist', {'className': 'is-style-eyebrow'}),
        heading('Ayesha Munawar'),
        p('<strong>Registered Psychotherapist (Qualifying)</strong><br>Clinic Owner · RP (Qualifying) · MACP', {'textColor': 'primary-deep'}),
        p(PH('ADD: regulatory college and registration number, e.g. College of Registered Psychotherapists of Ontario (CRPO) #'), {'fontSize': 'small'}),
        p(BIO_SHORT),
        p('Sessions in English, Urdu and Hindi', {'className': 'is-style-eyebrow'}),
        buttons(button('Read Ayesha’s story', '/therapist/'), btn_outline('Book a Free Consult', '/book/')),
    ), {'style': {'spacing': {'blockGap': '1rem'}}, 'layout': {'type': 'default'}}), {'width': '62%', 'verticalAlignment': 'center'}),
    a={'verticalAlignment': 'center', 'style': {'spacing': {'blockGap': {'left': 'var:preset|spacing|60', 'top': 'var:preset|spacing|50'}}}}),
    name='Meet your therapist')
write('therapist-card', 'Home: meet your therapist', THERAPIST, keywords='therapist, team, bio')

STEPS_SECTION = section(J(
    intro('Getting started', 'How to get started', 'Reaching out is often the hardest part. The next steps are simple, and you can go at your own pace.'),
    steps_block(),
    buttons(btn_book(), btn_outline('How it works', '/how-it-works/'), a={'layout': {'type': 'flex', 'justifyContent': 'center'}, 'style': {'spacing': {'margin': {'top': 'var:preset|spacing|50'}}}}),
), bg='tint', name='How to get started')
write('steps', 'Home: how to get started (3 steps)', STEPS_SECTION, keywords='steps, process, getting started')

FEES_SUMMARY = section(group(columns(
    column(icon('receipt', '', '3.5rem'), {'width': '5rem'}),
    column(group(J(
        heading('Fees &amp; insurance', 2, {'fontSize': 'x-large'}),
        p('We’ll walk you through fees, session options and questions about benefits during your free consultation, so you have the full picture before you decide anything. Many extended health plans include psychotherapy; we recommend checking your coverage.'),
        p(PH('ADD: sliding-scale or reduced-fee option, if offered') + ' ' + PH('CONFIRM: receipts for insurance claims'), {'fontSize': 'small'}),
    ), {'style': {'spacing': {'blockGap': '0.85rem'}}, 'layout': {'type': 'default'}})),
    column(buttons(btn_outline('Fees &amp; insurance details', '/fees/')), {'width': '16rem', 'verticalAlignment': 'center'}),
    a={'style': {'spacing': {'blockGap': {'left': 'var:preset|spacing|40', 'top': 'var:preset|spacing|30'}}}}),
    {'className': 'is-style-card', 'style': {'spacing': {'padding': {'top': 'var:preset|spacing|50', 'bottom': 'var:preset|spacing|50', 'left': 'var:preset|spacing|50', 'right': 'var:preset|spacing|50'}}}, 'layout': {'type': 'default'}}),
    pad=('60', '60'), name='Fees summary')
write('fees-summary', 'Home: fees summary', FEES_SUMMARY, keywords='fees, insurance, cost')

FAQ_HOME = section(columns(
    column(group(J(
        p('Questions', {'className': 'is-style-eyebrow'}),
        heading('Things people often ask'),
        p('It’s normal to have questions before starting therapy. Here are a few answers. If yours isn’t here, just ask during your free consult.'),
        p('<a href="/faq/">See all questions →</a>', {'style': {'typography': {'fontWeight': '700'}}}),
    ), {'style': {'spacing': {'blockGap': '1rem'}}, 'layout': {'type': 'default'}}), {'width': '36%'}),
    column(faq(HOME_FAQ), {'width': '64%'}),
    a={'style': {'spacing': {'blockGap': {'left': 'var:preset|spacing|60', 'top': 'var:preset|spacing|40'}}}}),
    name='FAQ')
write('faq-home', 'Home: FAQ accordion', FAQ_HOME, keywords='faq, questions, accordion')

HOME = J(pattern('own-and-become/hero-home'), pattern('own-and-become/reassurance'), pattern('own-and-become/empathy'),
         pattern('own-and-become/own-become'), pattern('own-and-become/services-cards'), pattern('own-and-become/areas-grid'),
         pattern('own-and-become/therapist-card'), pattern('own-and-become/steps'), pattern('own-and-become/fees-summary'),
         pattern('own-and-become/faq-home'), cta())
write('page-home', 'Page: Home', HOME, cats=('own-and-become-pages',), post_types='page', block_types='core/post-content')

# =====================================================================
# Inner pages
# =====================================================================

def two_col(left, right, lw='50%', rw='50%', align='center', gap='60'):
    return columns(column(left, {'width': lw, 'verticalAlignment': align}), column(right, {'width': rw, 'verticalAlignment': align}),
                   a={'verticalAlignment': align, 'style': {'spacing': {'blockGap': {'left': f'var:preset|spacing|{gap}', 'top': 'var:preset|spacing|50'}}}})

def stack(*b, gap='1.1rem'):
    return group(J(*b), {'style': {'spacing': {'blockGap': gap}}, 'layout': {'type': 'default'}})

def prose(*b):
    return section(group(J(*b), {'style': {'spacing': {'blockGap': '1.25rem'}}, 'layout': {'type': 'constrained', 'contentSize': '720px'}}), wide=False, name='Text')

# ---------- About
ABOUT = J(
    page_hero('About Own &amp; Become', 'A quiet place to grow through what’s hard', 'Own &amp; Become is an online psychotherapy practice based in Ontario, offering warm, practical support to teens (14+), adults and couples across Canada.'),
    section(two_col(
        image(A('images/together.svg'), 'Illustration of two people sitting together on a bench beneath a tree, with two small copper leaves between them.', {'sizeSlug': 'full', 'className': 'ob-reveal'}),
        stack(p('Why “Own &amp; Become”', {'className': 'is-style-eyebrow'}),
              heading('Not fixing a person. Walking alongside them.'),
              p('The name holds the heart of our work. <strong>Own</strong> is about owning your story, with honesty and self-compassion. <strong>Become</strong> is about growing into who you’re choosing to be. Together, they stand for resilience: not fixing a person, but walking alongside them as they grow through difficulty.'),
              p('Our logo shows two figures leaning toward each other to form a single leaf, with a small new leaf growing between them. That’s how we see therapy: a relationship built on trust and shared effort, where something new can grow.'),
              p(PH('ADD: a few sentences about the practice in your own words, e.g. why you started it and who you hope to help'))),
        lw='45%', rw='55%'), name='Our story'),
    section(J(
        intro('What we stand for', 'Our mission and values', None),
        card(J(heading('Our mission', 3, {'fontSize': 'large'}),
               p(PH('PLACEHOLDER MISSION, to be finalised') + ' To offer warm, practical and culturally responsive therapy that helps people own their stories and grow into who they’re choosing to be.')), tint=False),
        spacer('var:preset|spacing|30'.replace('var:preset|spacing|30', '1.5rem')),
        grid([card(J(icon(i, '', '2.5rem', 'ob-icon ob-icon--sm'), heading(t, 3, {'fontSize': 'large'}), p(d)), tint=True) for i, t, d in [
            ('couples', 'Connected', 'Therapy is a relationship. We listen closely and work together, side by side.'),
            ('roots', 'Grounded', 'Calm, steady and practical, with tools you can use in everyday life.'),
            ('sprout', 'Growing', 'Change happens gradually and in its own shape. Every small step counts.'),
            ('heart-leaf', 'Respectful', 'Every culture, faith, identity and family is welcome here, without judgment.')]], min_w='14rem', cls='ob-reveal-group'),
        p(PH('PLACEHOLDER VALUES, to be finalised. Edit or replace these four cards.'), {'align': 'center', 'fontSize': 'small', 'style': {'spacing': {'margin': {'top': 'var:preset|spacing|30'}}}}),
    ), bg='tint', cls='is-style-section-curve', name='Mission and values'),
    section(J(
        intro('How we work', 'Approaches, explained simply', 'We don’t follow one rigid method. We draw on several well-established approaches and shape them around you.'),
        grid([card(J(heading(t, 3, {'fontSize': 'large'}), p(d))) for t, d in [
            ('Person-centred', 'You’re the expert on your own life. Sessions follow what matters most to you, with warmth and without judgment.'),
            ('Mindfulness-based', 'Gentle ways to notice what’s happening in your body and mind, so you can feel a little steadier in the moment.'),
            ('Acceptance and Commitment Therapy (ACT)', 'Making room for difficult thoughts and feelings while taking steps toward what you truly value.'),
            ('Cognitive Behavioural Therapy (CBT)', 'Noticing patterns in thoughts and habits, and practising new, more helpful ways of responding.'),
            ('Internal Family Systems-informed', 'Getting curious, with compassion, about the different “parts” of you, like the worried part or the critical part.'),
            ('Emotion-Focused Therapy (EFT)', 'Understanding emotions and working with them, in yourself and in your relationships, rather than against them.'),
            ('Solution-Focused Brief Therapy (SFBT)', 'Focusing on your strengths, what’s already working, and the small changes that make a real difference.')]], min_w='18rem', cls='ob-reveal-group'),
    ), name='Approaches'),
    section(group(J(
        icon('heart-leaf', '', '3.25rem'),
        heading('Everyone is welcome here', 2, {'fontSize': 'x-large'}),
        p('We welcome people of all genders, sexual orientations, cultures, faiths, abilities, body sizes and family structures. We work in English, Urdu and Hindi, and we bring curiosity and respect to the cultural, spiritual and family contexts that shape your story.'),
        p(PH('ADD: any specific communities you serve or would like to highlight'), {'fontSize': 'small'}),
    ), {'className': 'is-style-card-tint', 'style': {'spacing': {'padding': {'top': 'var:preset|spacing|50', 'bottom': 'var:preset|spacing|50', 'left': 'var:preset|spacing|50', 'right': 'var:preset|spacing|50'}, 'blockGap': '1rem'}}, 'layout': {'type': 'constrained', 'contentSize': '720px'}}),
        pad=('20', '70'), name='Inclusion'),
    cta())
write('page-about', 'Page: About', ABOUT, cats=('own-and-become-pages',), post_types='page', block_types='core/post-content')

# ---------- Therapist
BIO_FULL = [
    'Before I was a therapist, I was a daughter, sister, wife, and mother. Those roles taught me about love, loss, patience, and resilience. They also showed me that life can be complicated, even in the moments meant to bring joy.',
    'I work with people through the seasons that feel heavy, uncertain, or lonely: anxiety, grief, relationship struggles, self-doubt, pregnancy and postpartum changes, or simply feeling stuck. You don’t need the right words or a clear plan to begin. Here, you can exhale.',
    'Together, we’ll make sense of what brought you here and build practical tools for change, at a pace that feels right for you. I bring warmth, curiosity, and compassion to every session, and I believe everyone has strength and the capacity to grow, even when it’s hard to see.',
    'It’s a privilege to be invited into your story. My promise is a relationship built on trust, honesty, and real human connection.',
]
GLANCE = [
    ('couples', 'Works with', 'Teens (14+), adults and couples'),
    ('languages', 'Languages', 'English, Urdu and Hindi'),
    ('online', 'Sessions', 'Online by video, across Ontario and much of Canada'),
    ('sprout', 'Often supports', 'Anxiety, grief and loss, relationship challenges, self-doubt, pregnancy and postpartum changes, life and career transitions'),
    ('book', 'Approaches', 'Person-centred, mindfulness-based, ACT, CBT, IFS-informed, EFT and SFBT'),
    ('confidential', 'Registration', 'RP (Qualifying), MACP. ' + PH('ADD: regulatory college, registration number and clinical supervisor details, if applicable')),
]
THERAPIST_PAGE = J(
    section(two_col(
        stack(p('Meet your therapist', {'className': 'is-style-eyebrow'}),
              heading('Ayesha Munawar', 1, {'fontSize': 'xx-large'}),
              p('<strong>Registered Psychotherapist (Qualifying)</strong><br>Clinic Owner · RP (Qualifying) · MACP', {'fontSize': 'large', 'textColor': 'primary-deep'}),
              p(PH('ADD: regulatory college and registration number'), {'fontSize': 'small'}),
              p('“You don’t need the right words or a clear plan to begin. Here, you can exhale.”', {'fontFamily': 'heading', 'fontSize': 'x-large', 'textColor': 'burgundy', 'style': {'typography': {'fontStyle': 'italic', 'lineHeight': '1.35'}}}),
              buttons(btn_book(), btn_outline('Ask a question', '/contact/'))),
        image(A('images/portrait-placeholder.svg'), 'Placeholder for a photo of Ayesha Munawar.', {'sizeSlug': 'full', 'className': 'ob-portrait'}),
        lw='58%', rw='42%'), bg='tint', pad=('60', '60'), cls='ob-page-hero', name='Therapist hero'),
    section(two_col(
        stack(heading('A little about me', 2, {'fontSize': 'x-large'}), *[p(t) for t in BIO_FULL], p('— Ayesha', {'fontFamily': 'heading', 'fontSize': 'large', 'textColor': 'primary', 'style': {'typography': {'fontStyle': 'italic'}}})),
        stack(*[group(J(icon(i, '', '2.5rem', 'ob-icon ob-icon--sm'), stack(p(f'<strong>{t}</strong>', {'textColor': 'primary-deep', 'style': {'spacing': {'margin': {'bottom': '0'}}}}), p(d, {'fontSize': 'small'}), gap='0.15rem')),
                        {'style': {'spacing': {'blockGap': '0.9rem'}}, 'layout': {'type': 'flex', 'flexWrap': 'nowrap', 'verticalAlignment': 'top'}}) for i, t, d in GLANCE],
              gap='1.35rem'),
        lw='58%', rw='42%', align='top'), name='Biography'),
    section(group(J(heading('Education &amp; training', 2, {'fontSize': 'x-large'}),
                    p(PH('ADD: degrees, training and professional memberships exactly as they should appear')),
                    ), {'className': 'is-style-card', 'style': {'spacing': {'padding': {'top': 'var:preset|spacing|50', 'bottom': 'var:preset|spacing|50', 'left': 'var:preset|spacing|50', 'right': 'var:preset|spacing|50'}, 'blockGap': '1rem'}}, 'layout': {'type': 'constrained', 'contentSize': '720px'}}),
            pad=('20', '70'), name='Credentials'),
    cta())
write('page-therapist', 'Page: Meet Your Therapist', THERAPIST_PAGE, cats=('own-and-become-pages',), post_types='page', block_types='core/post-content')

# ---------- Services overview
SERVICES_PAGE = J(
    page_hero('Services', 'Online therapy for teens, adults and couples', 'Every person and every relationship is different. Here’s how we can work together, all from the comfort and privacy of your own space.', buttons(btn_book())),
    section(J(intro(None, 'Ways we can work together', None), SERVICES_GRID), name='Services'),
    section(two_col(
        stack(heading('Not sure which is right for you?', 2, {'fontSize': 'x-large'}),
              p('That’s completely normal. Many people aren’t sure where to start. In your free 15-minute consult, we can talk through what’s going on and figure out together what kind of support makes sense.'),
              buttons(btn_book(), btn_outline('See areas we support', '/areas-we-support/'))),
        image(A('images/path-sprout.svg'), '', {'sizeSlug': 'full'}), lw='55%', rw='45%'), bg='tint', cls='is-style-section-curve', name='Not sure'),
    cta())
write('page-services', 'Page: Services', SERVICES_PAGE, cats=('own-and-become-pages',), post_types='page', block_types='core/post-content')

def service_page(eyebrow_title, title, lede, who_title, who, like_title, like_paras, topics, extra_sections=(), faq_keys=()):
    details = card(J(heading('Session details', 3, {'fontSize': 'large'}),
                     ul(['<strong>Format:</strong> online, by video', f'<strong>Languages:</strong> English, Urdu or Hindi', '<strong>Session length:</strong> ' + PH('ADD SESSION LENGTH'), '<strong>Fees:</strong> shared in your free consult'], {'className': 'is-style-leaf-list'}),
                     buttons(btn_book())), tint=True)
    parts = [
        page_hero(eyebrow_title, title, lede, buttons(btn_book(), btn_outline('How it works', '/how-it-works/'))),
        section(two_col(stack(heading(who_title, 2, {'fontSize': 'x-large'}), leaf_list(who)), details, lw='58%', rw='42%', align='top'), name='Who it is for'),
        section(group(J(heading(like_title, 2, {'fontSize': 'x-large'}), *[p(t) for t in like_paras], heading('Things we might explore', 3, {'fontSize': 'large'}), chips(topics), p('<a href="/areas-we-support/">See all areas we support →</a>', {'style': {'typography': {'fontWeight': '700'}}})),
                        {'style': {'spacing': {'blockGap': '1.2rem'}}, 'layout': {'type': 'constrained', 'contentSize': '760px'}}), bg='tint', cls='is-style-section-curve', wide=False, name='What sessions are like'),
        *extra_sections,
    ]
    if faq_keys:
        parts.append(section(group(J(heading('Questions about ' + title.lower(), 2, {'fontSize': 'x-large'}), faq(faq_keys)), {'style': {'spacing': {'blockGap': '1.5rem'}}, 'layout': {'type': 'constrained', 'contentSize': '760px'}}), wide=False, name='Questions'))
    parts.append(cta())
    return J(*parts)

write('page-individual-therapy', 'Page: Individual therapy', service_page(
    'Services · Individual therapy', 'Individual therapy',
    'A private, unhurried space that’s just for you: to slow down, make sense of what you’re carrying, and build tools that fit your real life.',
    'Who it’s for', ['Adults, and teens 14 and over, who feel stuck, overwhelmed or unlike themselves', 'Anyone going through a big change, loss or season of uncertainty', 'People who want to understand their patterns and treat themselves with more kindness', 'First-timers who aren’t sure therapy is “for them” yet'],
    'What sessions are like', ['Sessions are a conversation, not an interrogation. We’ll start with what feels most pressing to you and go from there. Some sessions are about making sense of feelings and experiences; others are about practical tools for the week ahead.', 'You’re in charge of the pace. We’ll check in about what’s helpful, and adjust as you grow.'],
    ['Stress management', 'Coping skills', 'Emotion regulation', 'Anger management', 'Boundary setting', 'Grief and loss', 'Pregnancy and postpartum', 'Life transitions', 'Career change'],
    faq_keys=['first', 'length', 'confidential']), cats=('own-and-become-pages',), post_types='page', block_types='core/post-content')

write('page-couples-therapy', 'Page: Couples therapy', service_page(
    'Services · Couples therapy', 'Couples therapy',
    'A calm, collaborative space for partners to understand each other again, communicate with more care, and navigate change together.',
    'Who it’s for', ['Couples who keep having the same painful argument', 'Partners feeling distant, disconnected or more like roommates', 'Couples navigating big changes: a new baby, infertility, loss, a move or a career shift', 'Engaged or newly committed couples who want a strong foundation (pre-marital support)', 'Couples navigating family expectations and different cultural or faith backgrounds'],
    'What sessions are like', ['Couples sessions are a shared space where each person gets to be heard. The goal isn’t to decide who’s right; it’s to understand the pattern you’re caught in and find new ways of reaching each other.', 'We’ll work on communication, emotional connection and practical agreements, at a pace that feels safe for both of you.'],
    ['Marital and pre-marital', 'Communication', 'Family dynamics &amp; relationships', 'Parenting together', 'Boundary setting', 'Infertility', 'Pregnancy and postpartum', 'Grief and loss'],
    faq_keys=['couples', 'length', 'cost']), cats=('own-and-become-pages',), post_types='page', block_types='core/post-content')

TEEN_EXTRA = section(two_col(
    card(J(icon('teen', '', '2.75rem'), heading('For teens', 3, {'fontSize': 'large'}),
           p('This is your space. You can talk about school, friends, family, identity, stress, or anything else on your mind, and you don’t have to have it all figured out. We’ll go at your pace, and you’ll always know what stays private and what doesn’t.'))),
    card(J(icon('family', '', '2.75rem'), heading('For parents and guardians', 3, {'fontSize': 'large'}),
           p('It can be hard to watch your teen struggle. We work with teens directly while respecting your role in their life. We’ll talk with you at the start about how we’ll communicate and what confidentiality looks like.'),
           p(PH('CONFIRM: your consent and confidentiality process for clients aged 14–17'), {'fontSize': 'small'})), tint=True),
    align='top', gap='30'), name='For teens and parents')
write('page-teen-therapy', 'Page: Teen therapy (14+)', service_page(
    'Services · Teen therapy (14+)', 'Teen therapy (14+)',
    'A judgment-free space for teens aged 14 and over to talk about stress, emotions, relationships and growing up, at their own pace.',
    'Who it’s for', ['Teens 14 and over who feel anxious, low, angry or overwhelmed', 'Teens dealing with stress at school, with friends or at home', 'Teens going through change: moving, family changes, loss', 'Teens who want to understand themselves and their emotions better'],
    'What sessions are like', ['Sessions are relaxed and conversational. We might talk, try simple tools for big feelings, or work through a situation that’s been on your mind. There’s no right or wrong way to use the time.', 'Everything is online, so you can join from a private, comfortable spot at home.'],
    ['Stress management', 'Coping skills', 'Emotion regulation', 'Anger management', 'Family dynamics &amp; relationships', 'Boundary setting', 'Grief and loss', 'Career guidance'],
    extra_sections=(TEEN_EXTRA,), faq_keys=['teens', 'confidential', 'first']), cats=('own-and-become-pages',), post_types='page', block_types='core/post-content')

ONLINE_EXTRA = section(J(
    intro('Getting ready', 'What you’ll need', None),
    grid([card(J(icon(i, '', '2.75rem'), heading(t, 3, {'fontSize': 'large'}), p(d))) for i, t, d in [
        ('confidential', 'A private space', 'Somewhere you can talk freely without being overheard: a bedroom, a parked car, a quiet office. Headphones can help.'),
        ('online', 'A device and connection', 'A phone, tablet or computer with a camera and a steady internet connection. You’ll get a secure link before your session.'),
        ('heart-leaf', 'A few quiet minutes', 'If you can, give yourself a moment before and after to settle in and to land gently afterwards.')]], min_w='16rem', cls='ob-reveal-group'),
    p(PH('CONFIRM: the video platform used (for example, Jane’s secure telehealth) and what clients receive before each session'), {'align': 'center', 'fontSize': 'small', 'style': {'spacing': {'margin': {'top': 'var:preset|spacing|30'}}}}),
), name='What you need')
ONLINE_AREAS = section(group(J(
    icon('map', '', '3rem'),
    heading('Where we can see clients', 2, {'fontSize': 'x-large'}),
    p('Online sessions are available to people living in:'),
    chips(['Ontario', 'British Columbia', 'Alberta', 'Saskatchewan', 'Manitoba', 'New Brunswick', 'Newfoundland and Labrador', 'Yukon', 'Northwest Territories', 'Nunavut']),
    p(PH('CONFIRM: that your registration and insurance allow you to practise in each listed province and territory'), {'fontSize': 'small'})),
    {'className': 'is-style-card', 'style': {'spacing': {'padding': {'top': 'var:preset|spacing|50', 'bottom': 'var:preset|spacing|50', 'left': 'var:preset|spacing|50', 'right': 'var:preset|spacing|50'}, 'blockGap': '1rem'}}, 'layout': {'type': 'constrained', 'contentSize': '720px'}}),
    pad=('20', '70'), name='Service area')
write('page-online-therapy', 'Page: Online therapy', service_page(
    'Services · Online therapy', 'Online therapy',
    'Every session happens by video, so you can get support from the privacy of your own space, without commuting, waiting rooms or rushing across town.',
    'Why people choose online therapy', ['It fits around work, school, parenting and busy weeks', 'You can talk from a space where you already feel safe', 'Support is available across many provinces and territories, including smaller and remote communities', 'It’s easier to keep going during a move, a new baby or a hard season'],
    'What it’s like', ['Online sessions work much like sessions in a room: we talk, reflect and practise tools together. Many people find it easier to open up from home.', 'At the start, we’ll confirm where you are joining from and a backup way to reach you if the connection drops.'],
    ['Individual therapy', 'Couples therapy', 'Teen therapy (14+)', 'Sessions in English, Urdu or Hindi'],
    extra_sections=(ONLINE_EXTRA, ONLINE_AREAS), faq_keys=['online', 'prepare', 'confidential']), cats=('own-and-become-pages',), post_types='page', block_types='core/post-content')

# ---------- Areas we support
AREAS_DESC = {
    'Stress & emotions': 'When feelings run high, or shut down entirely, we can build ways to steady yourself and respond rather than react.',
    'Relationships & family': 'For the relationships that matter most, and the patterns, expectations and boundaries that come with them.',
    'Pregnancy & fertility': 'Gentle support through trying to conceive, pregnancy, loss and the early months of parenthood.',
    'Grief & loss': 'Room to grieve in your own way and time, whether the loss is recent or from long ago.',
    'Life transitions': 'Moves, milestones, identity shifts and new chapters, even the ones you chose, can be harder than expected.',
    'Career': 'Clarity and steadiness when work feels uncertain, unfulfilling or like it’s asking too much.',
}
AREAS_PAGE = J(
    page_hero('Areas we support', 'Whatever brought you here, it’s welcome here', 'These are some of the things people bring to therapy. You don’t need to fit neatly into a category. Many people come with a mix of things, or simply a feeling that something needs to change.'),
    section(grid([card(J(group(J(icon(i, '', '2.75rem'), heading(t.replace('&', '&amp;'), 2, {'fontSize': 'large'})), {'style': {'spacing': {'blockGap': '0.85rem'}}, 'layout': {'type': 'flex', 'flexWrap': 'nowrap'}}),
                             p(AREAS_DESC[t]), chips(items))) for i, t, items in AREAS], min_w='20rem', cls='ob-reveal-group'), name='Areas'),
    section(two_col(
        stack(heading('Don’t see what you’re looking for?', 2, {'fontSize': 'x-large'}),
              p('Ayesha also often supports people with anxiety, self-doubt and feeling stuck. If you’re not sure whether we can help, reach out. If we’re not the right fit, we’ll do our best to point you toward someone who is.'),
              buttons(btn_book(), btn_outline('Contact us', '/contact/'))),
        image(A('images/become-growth.svg'), '', {'sizeSlug': 'full', 'width': '320px', 'align': 'center'}), lw='60%', rw='40%'), bg='tint', cls='is-style-section-curve', name='Not listed'),
    cta())
write('page-areas', 'Page: Areas we support', AREAS_PAGE, cats=('own-and-become-pages',), post_types='page', block_types='core/post-content')

# ---------- Fees
FEES_PAGE = J(
    page_hero('Fees &amp; insurance', 'Clear, honest conversations about cost', 'Cost is one of the most common worries about starting therapy. We’d rather talk about it openly, so you can make the choice that’s right for you.'),
    section(J(intro(None, 'How fees work', None), grid([
        card(J(icon('consult', '', '2.75rem'), heading('Fees are shared in your free consult', 3, {'fontSize': 'large'}),
               p('During your free 15-minute consultation, we’ll go over session fees and options and answer any questions, before you commit to anything.'))),
        card(J(icon('heart-leaf', '', '2.75rem'), heading('Reduced-fee options', 3, {'fontSize': 'large'}),
               p(PH('ADD: whether you offer a sliding scale or a limited number of reduced-fee spots, and how to ask about them. Remove this card if not offered.'))), tint=True),
        card(J(icon('receipt', '', '2.75rem'), heading('Insurance &amp; benefits', 3, {'fontSize': 'large'}),
               p('Many extended health and workplace benefit plans include some coverage for psychotherapy. Coverage varies, so we recommend checking with your provider whether services by a Registered Psychotherapist (Qualifying) are covered.'),
               p(PH('CONFIRM: whether receipts are provided for benefits claims, and whether direct billing is available'), {'fontSize': 'small'}))),
    ], min_w='17rem', cls='ob-reveal-group')), name='Fees overview'),
    section(group(J(
        heading('Good to know', 2, {'fontSize': 'x-large'}),
        ul(['<strong>Session length:</strong> ' + PH('ADD SESSION LENGTH(S)'),
            '<strong>Payment:</strong> ' + PH('ADD accepted payment methods and when payment is taken'),
            '<strong>Cancellations:</strong> ' + PH('ADD CANCELLATION POLICY: notice period and any fee'),
            '<strong>Questions to ask your insurer:</strong> Is psychotherapy covered? Does my plan cover a Registered Psychotherapist (Qualifying)? How much is covered per session and per year? Do I need a doctor’s referral?'],
           {'className': 'is-style-leaf-list'})),
        {'style': {'spacing': {'blockGap': '1.2rem'}}, 'layout': {'type': 'constrained', 'contentSize': '760px'}}), bg='tint', cls='is-style-section-curve', wide=False, name='Good to know'),
    section(group(J(heading('Questions about fees', 2, {'fontSize': 'x-large'}), faq(['cost', 'insurance', 'cancel'])), {'style': {'spacing': {'blockGap': '1.5rem'}}, 'layout': {'type': 'constrained', 'contentSize': '760px'}}), wide=False, name='Fee questions'),
    cta())
write('page-fees', 'Page: Fees & insurance', FEES_PAGE, cats=('own-and-become-pages',), post_types='page', block_types='core/post-content')

# ---------- How it works
HOW_PAGE = J(
    page_hero('How it works', 'Getting started, one gentle step at a time', 'Reaching out can feel like a big step. Here’s exactly what happens, so there are no surprises.', buttons(btn_book())),
    section(J(intro(None, 'Three simple steps', None), steps_block()), name='Three steps'),
    section(J(
        intro('What to expect', 'Before, during and between sessions', None),
        grid([card(J(heading(t, 3, {'fontSize': 'large'}), *[p(x) for x in d])) for t, d in [
            ('Before your first session', ['You’ll receive a secure link to complete intake and consent forms, and to share anything you’d like us to know ahead of time.', PH('CONFIRM: intake process and forms (for example, via Jane)')]),
            ('Your first session', ['We’ll get to know each other, talk about what brought you here, and what you’d like to be different. We’ll also go over privacy and the limits of confidentiality.']),
            ('Ongoing sessions', ['We’ll work together on what matters most to you, using approaches that suit you. We’ll check in regularly about what’s helping and what to adjust.']),
            ('Between sessions', ['Sometimes there’s a small practice or reflection to try during the week. It’s always an invitation, never homework you can fail.'])]], min_w='16rem', cls='ob-reveal-group'),
    ), bg='tint', cls='is-style-section-curve', name='What to expect'),
    section(two_col(
        stack(heading('Online sessions, made simple', 2, {'fontSize': 'x-large'}),
              p('All sessions happen by video. You’ll need a private space, a device with a camera, and a steady internet connection. That’s it.'),
              p('<a href="/services/online-therapy/">Learn more about online therapy →</a>', {'style': {'typography': {'fontWeight': '700'}}})),
        stack(heading('Your privacy', 2, {'fontSize': 'x-large'}),
              p('What you share in therapy stays private, with a few limits required by law that we’ll explain clearly before we begin. Your records are kept securely.'),
              p('<a href="/privacy-policy/">Read our Privacy Policy →</a>', {'style': {'typography': {'fontWeight': '700'}}})),
        align='top', gap='60'), name='Online and privacy'),
    cta())
write('page-how-it-works', 'Page: How it works', HOW_PAGE, cats=('own-and-become-pages',), post_types='page', block_types='core/post-content')

# ---------- FAQ page
FAQ_GROUPS = [('Getting started', ['right', 'consult', 'first', 'prepare', 'fit']),
              ('Fees &amp; insurance', ['cost', 'insurance', 'cancel']),
              ('Sessions', ['online', 'length', 'language', 'teens', 'couples']),
              ('Privacy &amp; safety', ['confidential', 'emergency'])]
FAQ_PAGE = J(
    page_hero('FAQ', 'Questions people often ask', 'It’s completely normal to have questions before starting therapy. If yours isn’t answered here, you’re welcome to ask during your free consult or send us a message.'),
    section(group(J(*[J(heading(t, 2, {'fontSize': 'x-large', 'style': {'spacing': {'margin': {'top': 'var:preset|spacing|50'}}}}), faq(k)) for t, k in FAQ_GROUPS]),
                  {'style': {'spacing': {'blockGap': '1.25rem'}}, 'layout': {'type': 'constrained', 'contentSize': '800px'}}), wide=False, pad=('40', '70'), name='Questions'),
    cta())
write('page-faq', 'Page: FAQ', FAQ_PAGE, cats=('own-and-become-pages',), post_types='page', block_types='core/post-content')

# ---------- Contact form section
FORM = J(
    p('Please don’t include sensitive or detailed health information in this form. We’ll talk about the details together, privately.', {'className': 'ob-hint', 'fontSize': 'small', 'textColor': 'muted'}),
    group(shortcode('[contact-form-7 title="Own and Become contact form"]'), {'className': 'ob-form', 'layout': {'type': 'default'}}),
)
CONTACT_DETAILS = stack(
    heading('Get in touch', 2, {'fontSize': 'x-large'}),
    *[group(J(icon(i, '', '2.5rem', 'ob-icon ob-icon--sm'), stack(p(f'<strong>{t}</strong>', {'textColor': 'primary-deep'}), p(d, {'fontSize': 'small'}), gap='0.1rem')),
            {'style': {'spacing': {'blockGap': '0.9rem'}}, 'layout': {'type': 'flex', 'flexWrap': 'nowrap', 'verticalAlignment': 'top'}}) for i, t, d in [
        ('phone', 'Phone', '<a href="tel:+10000000000">[ADD PHONE]</a>'),
        ('mail', 'Email', '<a href="#add-email">[ADD EMAIL]</a>'),
        ('calendar', 'Hours', PH('ADD HOURS')),
        ('map', 'Where we are', 'Based in Ontario. Online sessions across Ontario, BC, Alberta, Saskatchewan, Manitoba, New Brunswick, Newfoundland and Labrador, Yukon, NWT and Nunavut.'),
        ('languages', 'Languages', 'English, Urdu and Hindi')]],
    p('We’ll get back to you within 1–2 business days.', {'textColor': 'muted', 'fontSize': 'small'}),
    crisis(), gap='1.25rem')
write('contact-form', 'Contact form with details', section(two_col(CONTACT_DETAILS, card(J(heading('Send us a message', 2, {'fontSize': 'x-large'}), FORM)), lw='40%', rw='60%', align='top'), name='Contact'), keywords='contact, form')

CONTACT_PAGE = J(
    page_hero('Contact', 'Let’s talk', 'Have a question, or not sure where to start? Send us a message. There’s no wrong way to reach out.'),
    pattern('own-and-become/contact-form'),
    section(group(J(icon('confidential', '', '3rem'), heading('A note on privacy', 2, {'fontSize': 'x-large'}),
                    p('Messages sent through this form are delivered by email and are not part of a clinical record. To protect your privacy, please keep your message brief and avoid sharing detailed health information. We’ll discuss the details with you directly.')),
                  {'className': 'is-style-card-tint', 'style': {'spacing': {'padding': {'top': 'var:preset|spacing|50', 'bottom': 'var:preset|spacing|50', 'left': 'var:preset|spacing|50', 'right': 'var:preset|spacing|50'}, 'blockGap': '1rem'}}, 'layout': {'type': 'constrained', 'contentSize': '720px'}}),
            pad=('20', '70'), name='Privacy note'),
)
write('page-contact', 'Page: Contact', CONTACT_PAGE, cats=('own-and-become-pages',), post_types='page', block_types='core/post-content')

# ---------- Book page (single place to swap in Jane later)
BOOK_PAGE = J(
    page_hero('Book a free consult', 'A gentle first step', 'A free, no-pressure 15-minute call to talk about what’s going on, ask questions and see whether we’re a good fit.'),
    section(two_col(
        stack(heading('What to expect', 2, {'fontSize': 'x-large'}),
              leaf_list(['A relaxed 15-minute conversation by phone or video', 'Share as much or as little as you like', 'Ask anything about how therapy works, fees or availability', 'No commitment: you decide afterwards, in your own time']),
              group(J(heading('Online booking', 3, {'fontSize': 'large'}),
                      p('Online booking through Jane is coming soon. For now, send us a message with a few times that suit you and we’ll reply within 1–2 business days to find a time.'),
                      p(PH('WHEN READY: replace this box with a “Book on Jane” button linking to your Jane booking page'), {'fontSize': 'small'})),
                    {'className': 'is-style-card-tint', 'style': {'spacing': {'padding': {'top': 'var:preset|spacing|40', 'bottom': 'var:preset|spacing|40', 'left': 'var:preset|spacing|40', 'right': 'var:preset|spacing|40'}, 'blockGap': '0.75rem'}}, 'layout': {'type': 'default'}}),
              crisis()),
        card(J(heading('Request your free consult', 2, {'fontSize': 'x-large'}), FORM)), lw='42%', rw='58%', align='top'), name='Book'),
)
write('page-book', 'Page: Book a free consult', BOOK_PAGE, cats=('own-and-become-pages',), post_types='page', block_types='core/post-content')

# ---------- Legal pages (simple template shows the title)
def legal(intro_text, sections):
    out = [group(J(p(PH('LEGAL TEXT REQUIRED: this page is a structured placeholder. Have it reviewed and completed by a qualified professional before launch.')),), {'className': 'is-style-card-tint', 'style': {'spacing': {'padding': {'top': '1rem', 'bottom': '1rem', 'left': '1.25rem', 'right': '1.25rem'}}}, 'layout': {'type': 'default'}}),
           p(intro_text), p('<em>Last updated: ' + PH('ADD DATE') + '</em>', {'fontSize': 'small'})]
    for t, body in sections:
        out.append(heading(t, 2, {'fontSize': 'x-large'}))
        out += [p(b) for b in body]
    return J(*out)

PRIVACY = legal('Own &amp; Become respects your privacy. This policy explains what personal information we collect through this website and our services, why we collect it, and how we protect it, in line with Canada’s Personal Information Protection and Electronic Documents Act (PIPEDA) and applicable provincial health privacy laws, such as Ontario’s Personal Health Information Protection Act (PHIPA).', [
    ('Who we are', ['Own &amp; Become is an online psychotherapy practice based in Ontario. ' + PH('ADD: legal business name and mailing address'), 'Privacy officer: ' + PH('ADD: name and contact details of the person responsible for privacy')]),
    ('Information we collect', ['<strong>Through our contact form:</strong> your name, email address, phone number (optional), the reason for your enquiry, your preferred times and language, and your message.', '<strong>When you book or attend sessions:</strong> information you provide for intake, consent, scheduling, billing and clinical records. ' + PH('CONFIRM: these are stored in Jane (or your chosen practice-management system), and link to its privacy policy'), '<strong>Website data:</strong> basic technical information, such as your browser type and pages visited, which our hosting provider may log for security. ' + PH('CONFIRM: whether any analytics tools are used')]),
    ('How we use your information', ['To respond to your enquiry, schedule appointments, provide therapy services, process payments, meet our professional and legal obligations, and keep our website secure. We do not sell your personal information.']),
    ('Consent', ['By contacting us, you consent to us using your information to respond to you. You may withdraw consent at any time, subject to legal and professional record-keeping requirements. ' + PH('ADD: details')]),
    ('How we protect your information', [PH('ADD: safeguards, e.g. encrypted systems, secure practice-management software, restricted access, secure devices')]),
    ('How long we keep information', [PH('ADD: retention periods for enquiries and for clinical records, in line with your regulatory college’s requirements')]),
    ('Service providers', ['We use trusted service providers to run this website and our practice, which may include our web host (Hostinger), our practice-management and video platform ' + PH('CONFIRM: Jane'), ' and our email provider ' + PH('ADD') + '. Some providers may store data outside your province or outside Canada. ' + PH('CONFIRM: data locations')]),
    ('Cookies', ['This website uses only essential cookies and similar technologies needed for it to work, such as remembering that you’ve dismissed the cookie notice. We do not use advertising or tracking cookies. ' + PH('UPDATE this section if you add analytics, embedded videos or other third-party tools')]),
    ('Your rights', ['You may ask to access or correct the personal information we hold about you, and ask questions or raise concerns about how it is handled. Contact our privacy officer at ' + PH('ADD EMAIL') + '. You also have the right to complain to the Office of the Privacy Commissioner of Canada or the Information and Privacy Commissioner of Ontario.']),
    ('Changes to this policy', ['We may update this policy from time to time. The “last updated” date above shows when it last changed.']),
])
write('page-privacy', 'Page: Privacy Policy (placeholder)', PRIVACY, cats=('own-and-become-pages',), post_types='page', block_types='core/post-content')

TERMS = legal('These terms explain how you may use the Own &amp; Become website. By using this website, you agree to them.', [
    ('Information only, not therapy', ['Content on this website is general information. It is not therapy, medical advice, diagnosis or treatment, and reading it does not create a therapeutic relationship.']),
    ('Emergencies', ['This website and our contact form are not monitored for emergencies. If you are in crisis or thinking about suicide, call or text 988, call 911, or go to your nearest emergency room.']),
    ('Booking and services', ['Therapy services are provided under a separate informed-consent agreement that you’ll review before your first session. ' + PH('ADD: link or reference to client agreement, if appropriate')]),
    ('Links to other websites', ['We may link to other websites, such as our booking platform. We are not responsible for their content or privacy practices.']),
    ('Intellectual property', ['The Own &amp; Become name, logo, text and illustrations on this website belong to Own &amp; Become and may not be copied without permission.']),
    ('Limitation of liability', [PH('ADD: limitation of liability wording reviewed by a legal professional')]),
    ('Governing law', ['These terms are governed by the laws of Ontario and the federal laws of Canada that apply there. ' + PH('CONFIRM')]),
    ('Contact', ['Questions about these terms? Email ' + PH('ADD EMAIL') + '.']),
])
write('page-terms', 'Page: Terms of Use (placeholder)', TERMS, cats=('own-and-become-pages',), post_types='page', block_types='core/post-content')

ACCESS = J(
    p('Own &amp; Become is committed to making this website welcoming and usable for everyone, including people with disabilities. We aim to meet the Web Content Accessibility Guidelines (WCAG) 2.2 at Level AA, consistent with the Accessibility for Ontarians with Disabilities Act (AODA).'),
    heading('What we’ve done', 2, {'fontSize': 'x-large'}),
    ul(['Text and background colours chosen for strong contrast', 'A clear heading structure and descriptive link text', 'Visible focus outlines so the site can be used with a keyboard', 'Text descriptions (alt text) for meaningful images', 'Labelled form fields with clear error messages', 'Gentle motion only, which switches off if your device is set to reduce motion', 'A layout that adapts to phones, tablets and larger screens, and to text zoom'], {'className': 'is-style-leaf-list'}),
    heading('Ongoing work', 2, {'fontSize': 'x-large'}),
    p('Accessibility is ongoing work. Some third-party tools, such as our booking platform, are managed by other companies, and we’ll work with them where we can.'),
    heading('Feedback and alternative formats', 2, {'fontSize': 'x-large'}),
    p('If you have difficulty using any part of this website, or would like information in another format, please contact us at ' + PH('ADD EMAIL') + ' or <a href="tel:+10000000000">[ADD PHONE]</a>. We’ll do our best to help, and we welcome your feedback.'),
    p('<em>Last reviewed: ' + PH('ADD DATE') + '</em>', {'fontSize': 'small'}),
)
write('page-accessibility', 'Page: Accessibility statement', ACCESS, cats=('own-and-become-pages',), post_types='page', block_types='core/post-content')

print('patterns written:', len(os.listdir(OUT)))
