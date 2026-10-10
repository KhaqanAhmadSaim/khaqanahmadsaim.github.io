<?php
/**
 * Content definitions: pages, menu, posts, form and SEO text.
 *
 * @package own-and-become-setup
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Pages in the sitemap. Content comes from the theme's "Page: …" patterns.
 *
 * @return array[]
 */
function ob_setup_pages() {
	return array(
		array(
			'slug'    => 'home',
			'title'   => 'Home',
			'pattern' => 'page-home',
			'order'   => 0,
			'seo'     => array( 'Online Therapy in Ontario & Across Canada | Own & Become', 'Warm, practical online therapy for teens (14+), adults and couples in Ontario and across Canada, in English, Urdu and Hindi. Book a free 15-minute consult.' ),
		),
		array(
			'slug'    => 'about',
			'title'   => 'About',
			'pattern' => 'page-about',
			'order'   => 10,
			'seo'     => array( 'About Own & Become | Online Psychotherapy Practice in Ontario', 'Own & Become is an Ontario-based online psychotherapy practice. Our approach: own your story, and grow into who you’re choosing to be, at your pace.' ),
		),
		array(
			'slug'    => 'therapist',
			'title'   => 'Meet Your Therapist',
			'pattern' => 'page-therapist',
			'order'   => 20,
			'seo'     => array( 'Ayesha Munawar, Registered Psychotherapist (Qualifying) | Own & Become', 'Meet Ayesha Munawar, RP (Qualifying), MACP. Warm, practical online therapy for anxiety, grief, relationships, self-doubt, pregnancy and postpartum. English, Urdu & Hindi.' ),
		),
		array(
			'slug'    => 'services',
			'title'   => 'Services',
			'pattern' => 'page-services',
			'order'   => 30,
			'seo'     => array( 'Therapy Services: Individual, Couples & Teen | Own & Become', 'Online individual, couples and teen (14+) therapy for people in Ontario and across Canada. Sessions in English, Urdu and Hindi. Free 15-minute consult.' ),
		),
		array(
			'slug'    => 'individual-therapy',
			'parent'  => 'services',
			'title'   => 'Individual Therapy',
			'pattern' => 'page-individual-therapy',
			'order'   => 31,
			'seo'     => array( 'Individual Therapy Online, Ontario & Canada | Own & Become', 'One-on-one online therapy for stress, emotions, grief, life transitions and more. A calm, unhurried space to make sense of things and build practical tools.' ),
		),
		array(
			'slug'    => 'couples-therapy',
			'parent'  => 'services',
			'title'   => 'Couples Therapy',
			'pattern' => 'page-couples-therapy',
			'order'   => 32,
			'seo'     => array( 'Couples & Pre-Marital Therapy Online | Own & Become', 'Online couples therapy and pre-marital support to improve communication, rebuild connection and navigate change together. Ontario and across Canada.' ),
		),
		array(
			'slug'    => 'teen-therapy',
			'parent'  => 'services',
			'title'   => 'Teen Therapy (14+)',
			'pattern' => 'page-teen-therapy',
			'order'   => 33,
			'seo'     => array( 'Teen Therapy Online for Ages 14+ | Own & Become', 'A judgment-free, online space for teens aged 14 and over to talk about stress, emotions, relationships and growing up, at their own pace.' ),
		),
		array(
			'slug'    => 'online-therapy',
			'parent'  => 'services',
			'title'   => 'Online Therapy',
			'pattern' => 'page-online-therapy',
			'order'   => 34,
			'seo'     => array( 'Online Therapy in Ontario & Across Canada | Own & Become', 'Secure video therapy from the comfort of home, for people in Ontario, BC, Alberta, Saskatchewan, Manitoba, New Brunswick, Newfoundland and Labrador and the territories.' ),
		),
		array(
			'slug'    => 'areas-we-support',
			'title'   => 'Areas We Support',
			'pattern' => 'page-areas',
			'order'   => 40,
			'seo'     => array( 'Areas We Support: Stress, Grief, Relationships & More | Own & Become', 'Support for stress, emotions, relationships and family, pregnancy and postpartum, infertility, miscarriage, grief, life transitions and career changes.' ),
		),
		array(
			'slug'    => 'fees',
			'title'   => 'Fees & Insurance',
			'pattern' => 'page-fees',
			'order'   => 50,
			'seo'     => array( 'Fees & Insurance | Own & Become', 'How fees, insurance and benefits work at Own & Become. We talk through costs openly in your free 15-minute consultation.' ),
		),
		array(
			'slug'    => 'how-it-works',
			'title'   => 'How It Works',
			'pattern' => 'page-how-it-works',
			'order'   => 60,
			'seo'     => array( 'How It Works: Getting Started with Therapy | Own & Become', 'Three simple steps: book a free consult, have a conversation, and book your first session. Here’s what to expect before, during and between sessions.' ),
		),
		array(
			'slug'    => 'faq',
			'title'   => 'FAQ',
			'pattern' => 'page-faq',
			'order'   => 70,
			'seo'     => array( 'Therapy FAQ | Own & Become', 'Answers to common questions about therapy at Own & Become: cost, insurance, confidentiality, online sessions, languages, teens and couples.' ),
		),
		array(
			'slug'  => 'resources',
			'title' => 'Resources',
			'order' => 80,
			'seo'   => array( 'Resources & Reflections | Own & Become', 'Gentle reading on starting therapy, small practices for hard days, and reflections on growing through change.' ),
		),
		array(
			'slug'    => 'contact',
			'title'   => 'Contact',
			'pattern' => 'page-contact',
			'order'   => 90,
			'seo'     => array( 'Contact Own & Become | Online Therapy, Ontario', 'Questions about therapy or not sure where to start? Send us a message and we’ll reply within 1–2 business days.' ),
		),
		array(
			'slug'    => 'book',
			'title'   => 'Book a Free Consult',
			'pattern' => 'page-book',
			'order'   => 95,
			'seo'     => array( 'Book a Free 15-Minute Consult | Own & Become', 'Book a free, no-pressure 15-minute consult to ask questions and see whether we’re a good fit. Online therapy in English, Urdu and Hindi.' ),
		),
		array(
			'slug'     => 'privacy-policy',
			'title'    => 'Privacy Policy',
			'pattern'  => 'page-privacy',
			'template' => 'page-no-hero',
			'order'    => 100,
			'seo'      => array( 'Privacy Policy | Own & Become', 'How Own & Become collects, uses and protects your personal information.' ),
		),
		array(
			'slug'     => 'terms',
			'title'    => 'Terms of Use',
			'pattern'  => 'page-terms',
			'template' => 'page-no-hero',
			'order'    => 101,
			'seo'      => array( 'Terms of Use | Own & Become', 'Terms for using the Own & Become website.' ),
		),
		array(
			'slug'     => 'accessibility',
			'title'    => 'Accessibility',
			'pattern'  => 'page-accessibility',
			'template' => 'page-no-hero',
			'order'    => 102,
			'seo'      => array( 'Accessibility Statement | Own & Become', 'Our commitment to an accessible website for everyone, and how to tell us about barriers.' ),
		),
	);
}

/**
 * Main menu. 'page' items link to pages by slug; children make the dropdown.
 *
 * @return array[]
 */
function ob_setup_menu_items() {
	return array(
		array( 'label' => 'Home', 'page' => 'home' ),
		array( 'label' => 'About', 'page' => 'about' ),
		array(
			'label'    => 'Services',
			'page'     => 'services',
			'children' => array(
				array( 'label' => 'All services', 'page' => 'services' ),
				array( 'label' => 'Individual Therapy', 'page' => 'individual-therapy' ),
				array( 'label' => 'Couples Therapy', 'page' => 'couples-therapy' ),
				array( 'label' => 'Teen Therapy (14+)', 'page' => 'teen-therapy' ),
				array( 'label' => 'Online Therapy', 'page' => 'online-therapy' ),
				array( 'label' => 'Areas We Support', 'page' => 'areas-we-support' ),
				array( 'label' => 'How It Works', 'page' => 'how-it-works' ),
			),
		),
		array( 'label' => 'Therapist', 'page' => 'therapist' ),
		array( 'label' => 'Fees', 'page' => 'fees' ),
		array( 'label' => 'FAQ', 'page' => 'faq' ),
		array( 'label' => 'Resources', 'page' => 'resources' ),
		array( 'label' => 'Contact', 'page' => 'contact' ),
	);
}

/**
 * Synced patterns: edit once, update everywhere.
 *
 * @return array slug => title
 */
function ob_setup_synced_patterns() {
	return array(
		'crisis-notice' => 'Crisis notice',
		'cta-book'      => 'Call to action: Ready when you are',
		'leaf-divider'  => 'Leaf-curve divider',
	);
}

/**
 * Placeholder notice placed at the top of each sample post.
 *
 * @return string
 */
function ob_setup_post_notice() {
	return '<!-- wp:group {"className":"is-style-card-tint","style":{"spacing":{"padding":{"top":"1rem","bottom":"1rem","left":"1.25rem","right":"1.25rem"}}},"layout":{"type":"default"}} -->
<div class="wp-block-group is-style-card-tint" style="padding-top:1rem;padding-right:1.25rem;padding-bottom:1rem;padding-left:1.25rem"><!-- wp:paragraph -->
<p><mark class="ob-placeholder">[PLACEHOLDER POST: review, rewrite in your own voice, or delete before launch]</mark></p>
<!-- /wp:paragraph --></div>
<!-- /wp:group -->';
}

/**
 * Three placeholder blog posts in editable categories.
 *
 * @return array[]
 */
function ob_setup_posts() {
	$p = static function ( $text ) {
		return "<!-- wp:paragraph -->\n<p>{$text}</p>\n<!-- /wp:paragraph -->";
	};
	$h = static function ( $text ) {
		return "<!-- wp:heading -->\n<h2 class=\"wp-block-heading\">{$text}</h2>\n<!-- /wp:heading -->";
	};
	$list = static function ( $items ) {
		$li = array();
		foreach ( $items as $item ) {
			$li[] = "<!-- wp:list-item -->\n<li>{$item}</li>\n<!-- /wp:list-item -->";
		}
		return "<!-- wp:list {\"className\":\"is-style-leaf-list\"} -->\n<ul class=\"wp-block-list is-style-leaf-list\">" . implode( "\n\n", $li ) . "</ul>\n<!-- /wp:list -->";
	};

	return array(
		array(
			'slug'     => 'what-to-expect-in-your-first-therapy-session',
			'title'    => 'What to expect in your first therapy session',
			'category' => 'Getting Started',
			'image'    => 'post-first-session.png',
			'excerpt'  => 'Nervous about your first session? That’s completely normal. Here’s what usually happens, and why you don’t need to prepare anything.',
			'date'     => '-6 days',
			'content'  => implode(
				"\n\n",
				array(
					ob_setup_post_notice(),
					$p( 'If you’re feeling nervous about your first therapy session, you’re in good company. Many people spend days wondering what they’ll say, or whether they’ll say the “right” thing. The truth is, there is no right thing. A first session is simply a chance to begin.' ),
					$h( 'It’s mostly a conversation' ),
					$p( 'Your therapist will usually ask what’s brought you to therapy now, what’s been happening in your life, and what you’d like to be different. You can share as much or as little as feels comfortable. If something feels too big to talk about yet, it’s okay to say so.' ),
					$h( 'You’ll talk about privacy' ),
					$p( 'Early on, your therapist will explain how your information is kept confidential, and the few situations where they might need to share it, such as a serious risk to someone’s safety. This is a good moment to ask any questions you have.' ),
					$h( 'You can ask questions too' ),
					$list( array( 'How do you usually work with people?', 'How often would we meet?', 'What happens if I don’t know what to talk about?', 'What if I want to pause or stop?' ) ),
					$h( 'You don’t need to prepare' ),
					$p( 'Some people like to jot down a few notes beforehand, and that can help. But you don’t need a plan, a summary of your life, or the perfect words. Showing up is enough.' ),
				)
			),
		),
		array(
			'slug'     => 'am-i-struggling-enough-for-therapy',
			'title'    => 'Am I “struggling enough” for therapy?',
			'category' => 'Reflections',
			'image'    => 'post-struggling-enough.png',
			'excerpt'  => 'Many people wait until things feel unbearable before reaching out. You don’t have to. A gentle reflection on deserving support.',
			'date'     => '-4 days',
			'content'  => implode(
				"\n\n",
				array(
					ob_setup_post_notice(),
					$p( 'It’s one of the most common thoughts people have before they reach out: <em>other people have it worse. I should be able to handle this on my own.</em>' ),
					$p( 'But therapy isn’t only for emergencies. It can be a place to untangle a decision, to grieve something that others don’t see as a loss, to understand why the same argument keeps happening, or simply to feel less alone with what you’re carrying.' ),
					$h( 'Signs it might be worth reaching out' ),
					$list( array( 'You’ve been feeling “not quite yourself” for a while', 'A change, even a happy one, has been harder than you expected', 'The same patterns keep showing up in your relationships', 'You’re coping, but it’s taking everything you have' ) ),
					$h( 'You deserve support, as you are' ),
					$p( 'There’s no threshold you have to cross. If you’re wondering whether therapy could help, that wondering is reason enough to explore it, and a free consult is a low-pressure way to find out.' ),
				)
			),
		),
		array(
			'slug'     => 'a-two-minute-grounding-practice',
			'title'    => 'A two-minute grounding practice for overwhelming moments',
			'category' => 'Tools for Hard Days',
			'image'    => 'post-grounding.png',
			'excerpt'  => 'When your thoughts are racing, a simple practice can help you come back to the present. Try this one wherever you are.',
			'date'     => '-2 days',
			'content'  => implode(
				"\n\n",
				array(
					ob_setup_post_notice(),
					$p( 'When everything feels like too much, it can help to gently bring your attention back to the here and now. This simple practice uses your senses as an anchor. You can do it sitting at your desk, in the car, or lying in bed.' ),
					$h( 'Try the 5-4-3-2-1 practice' ),
					$list( array( 'Notice <strong>5</strong> things you can see', 'Notice <strong>4</strong> things you can feel, like your feet on the floor or the chair beneath you', 'Notice <strong>3</strong> things you can hear', 'Notice <strong>2</strong> things you can smell', 'Notice <strong>1</strong> slow breath, in and out' ) ),
					$p( 'There’s no need to do it perfectly. If your mind wanders, that’s okay; simply come back to the next sense.' ),
					$h( 'A gentle reminder' ),
					$p( 'Grounding practices can help in the moment, but they aren’t a replacement for support. If overwhelming moments are happening often, talking with a therapist can help you understand what’s underneath them.' ),
				)
			),
		),
	);
}

/**
 * Contact Form 7 form markup (fields from the brief).
 *
 * @return string
 */
function ob_setup_form_markup() {
	return <<<'FORM'
<div class="ob-row ob-row--2">
<p class="ob-field"><label for="ob-name">Your name <span class="ob-hint">Required</span></label>[text* your-name id:ob-name autocomplete:name]</p>
<p class="ob-field"><label for="ob-email">Email <span class="ob-hint">Required</span></label>[email* your-email id:ob-email autocomplete:email]</p>
</div>
<p class="ob-field"><label for="ob-phone">Phone <span class="ob-hint">Optional, if you’d prefer a call back</span></label>[tel your-phone id:ob-phone autocomplete:tel]</p>
<fieldset>
<legend class="ob-legend">What can we help with?</legend>
[radio reason use_label_element default:1 "A free 15-minute consult" "Booking an appointment" "A general question"]
</fieldset>
<fieldset>
<legend class="ob-legend">Preferred format <span class="ob-hint">All sessions are currently online.</span></legend>
[radio format use_label_element default:1 "Online (video)" "No preference"]
</fieldset>
<fieldset>
<legend class="ob-legend">Preferred language</legend>
[radio language use_label_element default:1 "English" "Urdu" "Hindi" "No preference"]
</fieldset>
<fieldset>
<legend class="ob-legend">Times that usually suit you <span class="ob-hint">Choose any that apply</span></legend>
[checkbox times use_label_element "Weekday mornings" "Weekday afternoons" "Weekday evenings" "Weekends"]
</fieldset>
<p class="ob-field"><label for="ob-message">A short message <span class="ob-hint">Please don’t include sensitive or detailed health information here.</span></label>[textarea your-message id:ob-message x4 maxlength:1500]</p>
[honeypot ob-website-url]
<p class="ob-field">[acceptance ob-consent] I understand this form is not for emergencies, and that my details will only be used to respond to my enquiry. [/acceptance]</p>
<p>[submit "Send message"]</p>
FORM;
}

/**
 * Email the form sends.
 *
 * @return string
 */
function ob_setup_form_mail_body() {
	return "Name: [your-name]\nEmail: [your-email]\nPhone: [your-phone]\n\nWhat can we help with: [reason]\nPreferred format: [format]\nPreferred language: [language]\nTimes that suit: [times]\n\nMessage:\n[your-message]\n\n--\nSent from the contact form on [_site_title] ([_site_url])";
}
