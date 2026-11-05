<?php
/**
 * Own & Become theme functions.
 *
 * Kept deliberately small: styles, one tiny script, block style
 * variations and pattern categories. All content lives in the editor.
 *
 * @package own-and-become
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'OWN_AND_BECOME_VERSION', '1.0.0' );

/**
 * Front-end styles and the small motion/cookie-notice script.
 */
function own_and_become_enqueue_assets() {
	wp_enqueue_style(
		'own-and-become',
		get_stylesheet_uri(),
		array(),
		OWN_AND_BECOME_VERSION
	);

	wp_enqueue_script(
		'own-and-become',
		get_theme_file_uri( 'assets/js/own-and-become.js' ),
		array(),
		OWN_AND_BECOME_VERSION,
		array(
			'in_footer' => true,
			'strategy'  => 'defer',
		)
	);
}
add_action( 'wp_enqueue_scripts', 'own_and_become_enqueue_assets' );

/**
 * Same styles inside the block editor, so editing looks like the site.
 */
function own_and_become_editor_styles() {
	add_editor_style( 'style.css' );
}
add_action( 'after_setup_theme', 'own_and_become_editor_styles' );

/**
 * Block style variations: pick them from the "Styles" panel of a block.
 */
function own_and_become_block_styles() {
	$styles = array(
		'core/paragraph' => array(
			'eyebrow'     => __( 'Eyebrow label', 'own-and-become' ),
			'step-number' => __( 'Step number', 'own-and-become' ),
		),
		'core/group'     => array(
			'card'          => __( 'Card', 'own-and-become' ),
			'card-tint'     => __( 'Card (sage tint)', 'own-and-become' ),
			'section-curve' => __( 'Curved top edge', 'own-and-become' ),
		),
		'core/column'    => array(
			'card'      => __( 'Card', 'own-and-become' ),
			'card-tint' => __( 'Card (sage tint)', 'own-and-become' ),
		),
		'core/separator' => array(
			'leaf-curve' => __( 'Leaf curve', 'own-and-become' ),
		),
		'core/list'      => array(
			'leaf-list' => __( 'Leaf bullets', 'own-and-become' ),
		),
		'core/image'     => array(
			'arch' => __( 'Arch', 'own-and-become' ),
			'soft' => __( 'Soft corners', 'own-and-become' ),
		),
	);

	foreach ( $styles as $block => $variations ) {
		foreach ( $variations as $name => $label ) {
			register_block_style(
				$block,
				array(
					'name'  => $name,
					'label' => $label,
				)
			);
		}
	}
}
add_action( 'init', 'own_and_become_block_styles' );

/**
 * Pattern categories so the practice's own sections are easy to find.
 */
function own_and_become_pattern_categories() {
	register_block_pattern_category(
		'own-and-become',
		array(
			'label'       => __( 'Own & Become: sections', 'own-and-become' ),
			'description' => __( 'Sections designed for the Own & Become website.', 'own-and-become' ),
		)
	);
	register_block_pattern_category(
		'own-and-become-pages',
		array(
			'label'       => __( 'Own & Become: full pages', 'own-and-become' ),
			'description' => __( 'Complete page layouts for the Own & Become website.', 'own-and-become' ),
		)
	);
}
add_action( 'init', 'own_and_become_pattern_categories', 9 );

/**
 * Hide Twenty Twenty-Five's demo patterns (books, podcasts, events) from the
 * inserter so only on-brand patterns show up. Core and our own patterns stay.
 */
function own_and_become_unregister_parent_patterns() {
	$registry = WP_Block_Patterns_Registry::get_instance();
	foreach ( $registry->get_all_registered() as $pattern ) {
		if ( 0 === strpos( $pattern['name'], 'twentytwentyfive/' )
			&& ! preg_match( '#/(hidden-|template-|comments|post-navigation|more-posts|binding-)#', $pattern['name'] ) ) {
			unregister_block_pattern( $pattern['name'] );
		}
	}
}
add_action( 'init', 'own_and_become_unregister_parent_patterns', 20 );

/**
 * Small helper for patterns: URL of a theme image or icon.
 *
 * @param string $file Path relative to the theme's assets folder.
 * @return string
 */
function own_and_become_asset( $file ) {
	return esc_url( get_theme_file_uri( 'assets/' . ltrim( $file, '/' ) ) );
}

/**
 * Contact Form 7: the form markup already uses its own paragraphs and
 * fieldsets, so stop CF7 from adding extra <p>/<br> tags around them.
 */
add_filter( 'wpcf7_autop_or_not', '__return_false' );

/**
 * Contact Form 7: only load its scripts and styles on pages that contain a form.
 *
 * @return bool
 */
function own_and_become_page_has_form() {
	$post = get_post();
	return is_singular() && $post && ( has_shortcode( $post->post_content, 'contact-form-7' ) || has_block( 'contact-form-7/contact-form-selector', $post ) );
}
add_filter( 'wpcf7_load_js', 'own_and_become_page_has_form' );
add_filter( 'wpcf7_load_css', 'own_and_become_page_has_form' );

/**
 * The Fees page was folded into the FAQ: send old /fees/ links to the
 * FAQ's "Fees & insurance" section (only when no page exists there).
 */
function own_and_become_redirect_fees() {
	if ( ! is_404() ) {
		return;
	}
	$path = trim( (string) wp_parse_url( $_SERVER['REQUEST_URI'] ?? '', PHP_URL_PATH ), '/' ); // phpcs:ignore WordPress.Security.ValidatedSanitizedInput
	if ( in_array( $path, array( 'fees', 'fees-insurance' ), true ) ) {
		wp_safe_redirect( home_url( '/faq/#fees' ), 301 );
		exit;
	}
}
add_action( 'template_redirect', 'own_and_become_redirect_fees' );
