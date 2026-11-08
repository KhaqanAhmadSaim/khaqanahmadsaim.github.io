<?php
/**
 * The setup steps. Each step is idempotent and logs what it did.
 *
 * @package own-and-become-setup
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

/**
 * Run every step. Returns a human-readable log.
 *
 * @return string[]
 */
function ob_setup_run() {
	$log   = array();
	$state = get_option( OB_SETUP_STATE, array() );

	if ( 'own-and-become' !== get_stylesheet() ) {
		return array( 'Stopped: please activate the Own & Become theme first.' );
	}

	ob_setup_settings( $log );
	ob_setup_branding( $state, $log );
	ob_setup_synced( $state, $log );
	ob_setup_form( $state, $log );
	ob_setup_create_pages( $state, $log );
	ob_setup_create_posts( $state, $log );
	ob_setup_navigation( $state, $log );
	ob_setup_template_parts( $state, $log );
	ob_setup_reading( $state, $log );
	ob_setup_seo( $state, $log );
	ob_setup_cleanup( $log );

	update_option( OB_SETUP_STATE, $state, false );
	flush_rewrite_rules();
	$log[] = 'Done. You can now deactivate and delete the “Own & Become Site Setup” plugin.';

	return $log;
}

/**
 * General settings.
 *
 * @param string[] $log Log.
 */
function ob_setup_settings( &$log ) {
	update_option( 'blogname', 'Own & Become' );
	update_option( 'blogdescription', 'Your story. Your pace. Your change.' );
	update_option( 'timezone_string', 'America/Toronto' );
	update_option( 'date_format', 'F j, Y' );
	update_option( 'default_comment_status', 'closed' );
	update_option( 'default_ping_status', 'closed' );
	update_option( 'permalink_structure', '/%postname%/' );
	$GLOBALS['wp_rewrite']->set_permalink_structure( '/%postname%/' );
	$log[] = 'Settings: title, tagline, time zone (Toronto), Post name permalinks, comments off for new content.';
}

/**
 * Copy a file from the theme into the Media Library.
 *
 * @param string $theme_file Path relative to the theme.
 * @param string $title      Attachment title.
 * @param string $alt        Alt text.
 * @return int Attachment ID or 0.
 */
function ob_setup_import_media( $theme_file, $title, $alt = '' ) {
	$source = get_theme_file_path( $theme_file );
	if ( ! file_exists( $source ) ) {
		return 0;
	}

	// Allow our own logo SVG through for this one upload only (WordPress blocks SVG uploads by default).
	$allow_svg = static function ( $mimes ) {
		$mimes['svg'] = 'image/svg+xml';
		return $mimes;
	};
	add_filter( 'upload_mimes', $allow_svg );
	$upload = wp_upload_bits( basename( $source ), null, file_get_contents( $source ) ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_get_contents_file_get_contents
	remove_filter( 'upload_mimes', $allow_svg );
	if ( ! empty( $upload['error'] ) ) {
		return 0;
	}

	$type = wp_check_filetype( $upload['file'] );
	$mime = $type['type'] ? $type['type'] : ( 'svg' === strtolower( pathinfo( $source, PATHINFO_EXTENSION ) ) ? 'image/svg+xml' : '' );

	$id = wp_insert_attachment(
		array(
			'post_title'     => $title,
			'post_mime_type' => $mime,
			'post_status'    => 'inherit',
		),
		$upload['file']
	);
	if ( ! $id || is_wp_error( $id ) ) {
		return 0;
	}

	require_once ABSPATH . 'wp-admin/includes/image.php';
	if ( 'image/svg+xml' !== $mime ) {
		wp_update_attachment_metadata( $id, wp_generate_attachment_metadata( $id, $upload['file'] ) );
	} else {
		// SVGs have no generated sizes; store the intrinsic size so blocks can lay it out.
		wp_update_attachment_metadata(
			$id,
			array(
				'width'  => 356,
				'height' => 558,
				'file'   => _wp_relative_upload_path( $upload['file'] ),
			)
		);
	}
	if ( $alt ) {
		update_post_meta( $id, '_wp_attachment_image_alt', $alt );
	}
	return (int) $id;
}

/**
 * Site logo and site icon.
 *
 * @param array    $state State.
 * @param string[] $log   Log.
 */
function ob_setup_branding( &$state, &$log ) {
	if ( empty( $state['logo'] ) || ! get_post( $state['logo'] ) ) {
		$state['logo'] = ob_setup_import_media( 'assets/logo/own-and-become-mark.svg', 'Own & Become logo mark', 'Own & Become' );
	}
	if ( $state['logo'] ) {
		update_option( 'site_logo', $state['logo'] );
	}

	if ( empty( $state['icon'] ) || ! get_post( $state['icon'] ) ) {
		$state['icon'] = ob_setup_import_media( 'assets/logo/site-icon-512.png', 'Own & Become site icon', '' );
	}
	if ( $state['icon'] ) {
		update_option( 'site_icon', $state['icon'] );
	}
	$log[] = 'Branding: Site Logo and favicon set from the logo mark.';
}

/**
 * Raw content of one of the theme's patterns.
 *
 * @param string $slug Pattern slug without the theme prefix.
 * @return string
 */
function ob_setup_pattern_content( $slug ) {
	$pattern = WP_Block_Patterns_Registry::get_instance()->get_registered( 'own-and-become/' . $slug );
	return $pattern ? $pattern['content'] : '';
}

/**
 * Replace pattern placeholders with real, editable blocks.
 * Synced patterns become references; everything else is inlined.
 *
 * @param string $content Block markup.
 * @param array  $state   State (synced pattern IDs).
 * @param int    $depth   Recursion guard.
 * @return string
 */
function ob_setup_expand( $content, $state, $depth = 0 ) {
	if ( $depth > 5 ) {
		return $content;
	}
	return preg_replace_callback(
		'#<!-- wp:pattern \{"slug":"own-and-become/([a-z0-9\-]+)"\} /-->#',
		static function ( $m ) use ( $state, $depth ) {
			$slug = $m[1];
			if ( ! empty( $state['synced'][ $slug ] ) ) {
				return '<!-- wp:block {"ref":' . (int) $state['synced'][ $slug ] . '} /-->';
			}
			return ob_setup_expand( ob_setup_pattern_content( $slug ), $state, $depth + 1 );
		},
		$content
	);
}

/**
 * Synced patterns (wp_block posts).
 *
 * @param array    $state State.
 * @param string[] $log   Log.
 */
function ob_setup_synced( &$state, &$log ) {
	$term = term_exists( 'Own & Become', 'wp_pattern_category' );
	if ( ! $term ) {
		$term = wp_insert_term( 'Own & Become', 'wp_pattern_category' );
	}
	$term_id = is_array( $term ) ? (int) $term['term_id'] : 0;

	foreach ( ob_setup_synced_patterns() as $slug => $title ) {
		if ( ! empty( $state['synced'][ $slug ] ) && get_post( $state['synced'][ $slug ] ) ) {
			continue;
		}
		$id = wp_insert_post(
			wp_slash(
				array(
					'post_type'    => 'wp_block',
					'post_status'  => 'publish',
					'post_title'   => $title,
					'post_content' => ob_setup_pattern_content( $slug ),
				)
			),
			true
		);
		if ( ! is_wp_error( $id ) ) {
			$state['synced'][ $slug ] = $id;
			if ( $term_id ) {
				wp_set_object_terms( $id, array( $term_id ), 'wp_pattern_category' );
			}
			$log[] = "Synced pattern created: {$title}";
		}
	}
}

/**
 * Contact Form 7 form.
 *
 * @param array    $state State.
 * @param string[] $log   Log.
 */
function ob_setup_form( &$state, &$log ) {
	if ( ! class_exists( 'WPCF7_ContactForm' ) ) {
		$log[] = 'Skipped contact form: Contact Form 7 is not active.';
		return;
	}
	if ( ! empty( $state['form'] ) && get_post( $state['form'] ) ) {
		return;
	}

	$form  = WPCF7_ContactForm::get_template( array( 'title' => 'Own and Become contact form' ) );
	$props = $form->get_properties();

	$props['form']                         = ob_setup_form_markup();
	$props['mail']['recipient']            = '[_site_admin_email]';
	$props['mail']['subject']              = 'New website enquiry from [your-name]';
	$props['mail']['sender']               = 'Own & Become website <wordpress@' . wp_parse_url( home_url(), PHP_URL_HOST ) . '>';
	$props['mail']['body']                 = ob_setup_form_mail_body();
	$props['mail']['additional_headers']   = 'Reply-To: [your-email]';
	$props['mail_2']['active']             = false;
	$props['messages']['mail_sent_ok']     = 'Thank you for reaching out. We’ll get back to you within 3–5 business days.';
	$props['messages']['validation_error'] = 'A few fields need your attention. Please check the highlighted fields and try again.';
	$props['messages']['mail_sent_ng']     = 'Sorry, something went wrong and your message wasn’t sent. Please try again later, or contact us by phone.';
	$props['messages']['accept_terms']     = 'Please tick the box to confirm you’ve read this note before sending.';
	$props['messages']['spam']             = 'Sorry, your message couldn’t be sent. Please try again, or contact us by phone.';

	$form->set_properties( $props );
	$state['form'] = $form->save();
	$log[]         = 'Contact form created: “Own and Become contact form” (sends to the site admin email for now).';
}

/**
 * Find a page by slug path (e.g. "services/individual-therapy").
 *
 * @param string $path Path.
 * @return WP_Post|null
 */
function ob_setup_page_by_path( $path ) {
	return get_page_by_path( $path, OBJECT, 'page' );
}

/**
 * Whether an existing page is an unused placeholder the setup may fill in.
 *
 * True only for pages that are not published and have no real content (for
 * example the empty private pages a starter template or onboarding wizard
 * leaves behind), or for WordPress's untouched sample Privacy Policy.
 * Published pages and pages with real content are never taken over.
 *
 * @param WP_Post|null $post Page.
 * @return bool
 */
function ob_setup_is_placeholder( $post ) {
	if ( ! $post || ! in_array( $post->post_status, array( 'draft', 'private', 'pending', 'auto-draft' ), true ) ) {
		return false;
	}
	if ( 'privacy-policy' === $post->post_name && false !== strpos( $post->post_content, 'privacy-policy-tutorial' ) ) {
		return true;
	}
	return '' === trim( wp_strip_all_tags( strip_shortcodes( $post->post_content ) ) );
}

/**
 * Pages.
 *
 * @param array    $state State.
 * @param string[] $log   Log.
 */
function ob_setup_create_pages( &$state, &$log ) {
	foreach ( ob_setup_pages() as $page ) {
		$slug   = $page['slug'];
		$parent = ! empty( $page['parent'] ) && ! empty( $state['pages'][ $page['parent'] ] ) ? (int) $state['pages'][ $page['parent'] ] : 0;

		if ( ! empty( $state['pages'][ $slug ] ) ) {
			$known = get_post( $state['pages'][ $slug ] );
			if ( $known && ! ob_setup_is_placeholder( $known ) ) {
				continue;
			}
		}

		$path     = ( $parent ? get_post_field( 'post_name', $parent ) . '/' : '' ) . $slug;
		$existing = ob_setup_page_by_path( $path );
		$content  = ! empty( $page['pattern'] ) ? ob_setup_expand( ob_setup_pattern_content( $page['pattern'] ), $state ) : '';

		$args = array(
			'post_type'      => 'page',
			'post_status'    => 'publish',
			'post_title'     => $page['title'],
			'post_name'      => $slug,
			'post_parent'    => $parent,
			'menu_order'     => $page['order'],
			'post_content'   => $content,
			'comment_status' => 'closed',
			'ping_status'    => 'closed',
		);

		$took_over = false;
		if ( $existing ) {
			// Only fill in unused, unpublished placeholders; never overwrite real content.
			if ( ob_setup_is_placeholder( $existing ) ) {
				$args['ID'] = $existing->ID;
				$took_over  = true;
				// A placeholder left by a page builder would otherwise keep showing the builder's empty layout.
				foreach ( array( '_elementor_edit_mode', '_elementor_data', '_elementor_page_settings', '_elementor_template_type' ) as $key ) {
					delete_post_meta( $existing->ID, $key );
				}
			} else {
				$state['pages'][ $slug ] = $existing->ID;
				$log[]                   = "Page skipped (already exists, left as is): /{$path}/";
				continue;
			}
		}

		$id = wp_insert_post( wp_slash( $args ), true );
		if ( is_wp_error( $id ) ) {
			$log[] = "Page failed: {$page['title']}: " . $id->get_error_message();
			continue;
		}
		if ( ! empty( $page['template'] ) ) {
			update_post_meta( $id, '_wp_page_template', $page['template'] );
		}
		$state['pages'][ $slug ] = $id;
		$log[]                   = ( $took_over ? 'Page filled in (was an empty, unpublished placeholder)' : 'Page created' ) . ": {$page['title']} (/{$path}/)";
	}
}

/**
 * Placeholder posts and their categories.
 *
 * @param array    $state State.
 * @param string[] $log   Log.
 */
function ob_setup_create_posts( &$state, &$log ) {
	foreach ( ob_setup_posts() as $post ) {
		if ( ! empty( $state['posts'][ $post['slug'] ] ) && get_post( $state['posts'][ $post['slug'] ] ) ) {
			continue;
		}
		if ( get_page_by_path( $post['slug'], OBJECT, 'post' ) ) {
			continue;
		}

		$cat = term_exists( $post['category'], 'category' );
		if ( ! $cat ) {
			$cat = wp_insert_term( $post['category'], 'category' );
		}

		$id = wp_insert_post(
			wp_slash(
				array(
					'post_type'      => 'post',
					'post_status'    => 'publish',
					'post_title'     => $post['title'],
					'post_name'      => $post['slug'],
					'post_excerpt'   => $post['excerpt'],
					'post_content'   => $post['content'],
					'post_date'      => gmdate( 'Y-m-d H:i:s', strtotime( $post['date'] ) ),
					'post_category'  => is_array( $cat ) ? array( (int) $cat['term_id'] ) : array(),
					'comment_status' => 'closed',
					'ping_status'    => 'closed',
				)
			),
			true
		);
		if ( is_wp_error( $id ) ) {
			continue;
		}
		$image = ob_setup_import_media( 'assets/images/posts/' . $post['image'], $post['title'], '' );
		if ( $image ) {
			set_post_thumbnail( $id, $image );
		}
		$state['posts'][ $post['slug'] ] = $id;
		$log[]                           = "Placeholder post created: {$post['title']} ({$post['category']})";
	}

	// The default "Uncategorized" category is renamed so it reads well if used.
	$uncat = get_term_by( 'slug', 'uncategorized', 'category' );
	if ( $uncat && 'Uncategorized' === $uncat->name ) {
		wp_update_term( $uncat->term_id, 'category', array( 'name' => 'General', 'slug' => 'general' ) );
	}
}

/**
 * One navigation link block for a page.
 *
 * @param array $item  Menu item.
 * @param array $state State.
 * @return string
 */
function ob_setup_nav_link( $item, $state ) {
	$id   = ! empty( $state['pages'][ $item['page'] ] ) ? (int) $state['pages'][ $item['page'] ] : 0;
	$url  = $id ? wp_make_link_relative( get_permalink( $id ) ) : '/';
	$attr = array(
		'label' => $item['label'],
		'type'  => 'page',
		'id'    => $id,
		'url'   => $url,
		'kind'  => 'post-type',
	);
	if ( ! empty( $item['children'] ) ) {
		$children = array();
		foreach ( $item['children'] as $child ) {
			$children[] = ob_setup_nav_link( $child, $state );
		}
		return '<!-- wp:navigation-submenu ' . wp_json_encode( $attr, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . " -->\n" . implode( "\n", $children ) . "\n<!-- /wp:navigation-submenu -->";
	}
	return '<!-- wp:navigation-link ' . wp_json_encode( $attr, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . ' /-->';
}

/**
 * Main menu (a block "Navigation" menu, editable in Appearance → Editor → Navigation).
 *
 * @param array    $state State.
 * @param string[] $log   Log.
 */
function ob_setup_navigation( &$state, &$log ) {
	if ( ! empty( $state['nav'] ) && get_post( $state['nav'] ) ) {
		return;
	}
	$links = array();
	foreach ( ob_setup_menu_items() as $item ) {
		$links[] = ob_setup_nav_link( $item, $state );
	}
	$id = wp_insert_post(
		wp_slash(
			array(
				'post_type'    => 'wp_navigation',
				'post_status'  => 'publish',
				'post_title'   => 'Main menu',
				'post_content' => implode( "\n", $links ),
			)
		),
		true
	);
	if ( ! is_wp_error( $id ) ) {
		$state['nav'] = $id;
		$log[]        = 'Main menu created with the Services dropdown.';
	}
}

/**
 * Save header, footer and mobile menu as editable template parts that point to
 * the main menu and the synced crisis notice.
 *
 * @param array    $state State.
 * @param string[] $log   Log.
 */
function ob_setup_template_parts( &$state, &$log ) {
	$parts = array(
		'header'       => array( 'Header', WP_TEMPLATE_PART_AREA_HEADER ),
		'footer'       => array( 'Footer', WP_TEMPLATE_PART_AREA_FOOTER ),
		'menu-overlay' => array( 'Mobile menu overlay', defined( 'WP_TEMPLATE_PART_AREA_NAVIGATION_OVERLAY' ) ? WP_TEMPLATE_PART_AREA_NAVIGATION_OVERLAY : 'navigation-overlay' ),
	);
	$theme = get_stylesheet();

	foreach ( $parts as $slug => $info ) {
		$exists = get_block_template( $theme . '//' . $slug, 'wp_template_part' );
		if ( $exists && 'custom' === $exists->source ) {
			continue; // Already customized in the Site Editor: leave it alone.
		}
		$file = get_theme_file_path( "parts/{$slug}.html" );
		if ( ! file_exists( $file ) ) {
			continue;
		}
		$content = file_get_contents( $file ); // phpcs:ignore WordPress.WP.AlternativeFunctions.file_get_contents_file_get_contents
		if ( ! empty( $state['nav'] ) ) {
			$content = str_replace( '<!-- wp:navigation {"className":"ob-main-nav",', '<!-- wp:navigation {"ref":' . (int) $state['nav'] . ',"className":"ob-main-nav",', $content );
		}
		$content = ob_setup_expand( $content, $state );

		$id = wp_insert_post(
			wp_slash(
				array(
					'post_type'    => 'wp_template_part',
					'post_status'  => 'publish',
					'post_name'    => $slug,
					'post_title'   => $info[0],
					'post_content' => $content,
				)
			),
			true
		);
		if ( is_wp_error( $id ) ) {
			continue;
		}
		wp_set_object_terms( $id, $theme, 'wp_theme' );
		wp_set_object_terms( $id, $info[1], 'wp_template_part_area' );
		$log[] = "Template part saved: {$info[0]}";
	}
}

/**
 * Front page, blog page and privacy page.
 *
 * @param array    $state State.
 * @param string[] $log   Log.
 */
function ob_setup_reading( &$state, &$log ) {
	if ( ! empty( $state['pages']['home'] ) ) {
		update_option( 'show_on_front', 'page' );
		update_option( 'page_on_front', (int) $state['pages']['home'] );
	}
	if ( ! empty( $state['pages']['resources'] ) ) {
		update_option( 'page_for_posts', (int) $state['pages']['resources'] );
	}
	if ( ! empty( $state['pages']['privacy-policy'] ) ) {
		update_option( 'wp_page_for_privacy_policy', (int) $state['pages']['privacy-policy'] );
	}
	update_option( 'posts_per_page', 9 );
	$log[] = 'Reading: Home is the front page, Resources is the blog page.';
}

/**
 * SEO titles and descriptions (The SEO Framework).
 *
 * @param array    $state State.
 * @param string[] $log   Log.
 */
function ob_setup_seo( &$state, &$log ) {
	foreach ( ob_setup_pages() as $page ) {
		if ( empty( $state['pages'][ $page['slug'] ] ) || empty( $page['seo'] ) ) {
			continue;
		}
		$id = (int) $state['pages'][ $page['slug'] ];
		if ( ! get_post_meta( $id, '_genesis_title', true ) ) {
			update_post_meta( $id, '_genesis_title', $page['seo'][0] );
			update_post_meta( $id, '_tsf_title_no_blogname', 1 );
		}
		if ( ! get_post_meta( $id, '_genesis_description', true ) ) {
			update_post_meta( $id, '_genesis_description', $page['seo'][1] );
		}
	}

	if ( defined( 'THE_SEO_FRAMEWORK_SITE_OPTIONS' ) ) {
		$options = get_option( THE_SEO_FRAMEWORK_SITE_OPTIONS, array() );
		if ( is_array( $options ) ) {
			$home = ob_setup_pages()[0]['seo'];
			if ( empty( $options['homepage_title'] ) ) {
				$options['homepage_title']   = $home[0];
				$options['homepage_tagline'] = 0;
			}
			if ( empty( $options['homepage_description'] ) ) {
				$options['homepage_description'] = $home[1];
			}
			update_option( THE_SEO_FRAMEWORK_SITE_OPTIONS, $options );
		}
	}
	$log[] = 'SEO: titles and meta descriptions added to every page (The SEO Framework also creates /sitemap.xml).';
}

/**
 * Remove WordPress demo content.
 *
 * @param string[] $log Log.
 */
function ob_setup_cleanup( &$log ) {
	$hello = get_page_by_path( 'hello-world', OBJECT, 'post' );
	if ( $hello && 'publish' === $hello->post_status ) {
		wp_trash_post( $hello->ID );
		$log[] = 'Moved the “Hello world!” demo post to the trash.';
	}
	$sample = get_page_by_path( 'sample-page', OBJECT, 'page' );
	if ( $sample && 'publish' === $sample->post_status ) {
		wp_trash_post( $sample->ID );
		$log[] = 'Moved the “Sample Page” demo page to the trash.';
	}
	$comment = get_comment( 1 );
	if ( $comment && 'https://wordpress.org/' === $comment->comment_author_url ) {
		wp_delete_comment( 1, true );
	}
}
