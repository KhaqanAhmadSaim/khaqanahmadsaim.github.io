<?php
/**
 * Plugin Name:       Own & Become Site Setup
 * Description:       One-time setup for the Own & Become website: creates the pages, menu, synced patterns, contact form, placeholder posts and settings. Run it once from Tools → Own & Become Setup, then deactivate and delete this plugin. Nothing on the site depends on it afterwards.
 * Version:           1.0.0
 * Requires at least: 6.9
 * Requires PHP:      7.4
 * Author:            Own & Become
 * License:           GPL-2.0-or-later
 * Text Domain:       own-and-become-setup
 *
 * @package own-and-become-setup
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'OB_SETUP_STATE', 'ob_setup_state' );

require_once __DIR__ . '/includes/content.php';
require_once __DIR__ . '/includes/runner.php';

/**
 * Admin page: Tools → Own & Become Setup.
 */
function ob_setup_menu() {
	add_management_page(
		__( 'Own & Become Setup', 'own-and-become-setup' ),
		__( 'Own & Become Setup', 'own-and-become-setup' ),
		'manage_options',
		'own-and-become-setup',
		'ob_setup_page'
	);
}
add_action( 'admin_menu', 'ob_setup_menu' );

/**
 * Render the admin page and handle the "Run setup" button.
 */
function ob_setup_page() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}

	$log = null;
	if ( isset( $_POST['ob_setup_run'] ) && check_admin_referer( 'ob_setup_run' ) ) {
		$log = ob_setup_run();
	}

	$checks = ob_setup_checks();
	$ready  = ! in_array( false, wp_list_pluck( $checks, 'ok' ), true );
	$state  = get_option( OB_SETUP_STATE, array() );
	?>
	<div class="wrap">
		<h1><?php esc_html_e( 'Own & Become Setup', 'own-and-become-setup' ); ?></h1>
		<p><?php esc_html_e( 'This builds the full Own & Become website from the theme’s patterns. It is safe to run more than once: anything it already created, or any page that already exists with the same address and has real content, is left untouched. Empty, unpublished placeholder pages with the same address are filled in.', 'own-and-become-setup' ); ?></p>

		<h2><?php esc_html_e( 'Before you start', 'own-and-become-setup' ); ?></h2>
		<table class="widefat striped" style="max-width:760px">
			<tbody>
			<?php foreach ( $checks as $check ) : ?>
				<tr>
					<td style="width:2em"><?php echo $check['ok'] ? '✅' : '⚠️'; ?></td>
					<td><?php echo esc_html( $check['label'] ); ?></td>
				</tr>
			<?php endforeach; ?>
			</tbody>
		</table>

		<h2><?php esc_html_e( 'What this will do', 'own-and-become-setup' ); ?></h2>
		<ul style="list-style:disc;padding-left:1.5em;max-width:760px">
			<li><?php esc_html_e( 'Set the site title, tagline, time zone, permalinks (Post name) and turn off comments for new content.', 'own-and-become-setup' ); ?></li>
			<li><?php esc_html_e( 'Add the logo mark as the Site Logo and the favicon (Site Icon).', 'own-and-become-setup' ); ?></li>
			<li><?php esc_html_e( 'Create synced patterns: Crisis notice, “Ready when you are” call to action, Leaf-curve divider.', 'own-and-become-setup' ); ?></li>
			<li><?php esc_html_e( 'Create the contact form (Contact Form 7 with honeypot spam protection).', 'own-and-become-setup' ); ?></li>
			<li><?php esc_html_e( 'Create every page in the sitemap, the main menu with the Services dropdown, and 3 placeholder blog posts.', 'own-and-become-setup' ); ?></li>
			<li><?php esc_html_e( 'Set Home as the front page and Resources as the blog page, and add SEO titles and descriptions.', 'own-and-become-setup' ); ?></li>
			<li><?php esc_html_e( 'Move the default “Hello world!” post and “Sample Page” to the trash (if present).', 'own-and-become-setup' ); ?></li>
		</ul>

		<?php if ( $log ) : ?>
			<h2><?php esc_html_e( 'Result', 'own-and-become-setup' ); ?></h2>
			<pre style="background:#fff;border:1px solid #ccd0d4;padding:1em;max-width:760px;white-space:pre-wrap"><?php echo esc_html( implode( "\n", $log ) ); ?></pre>
			<p><a class="button" href="<?php echo esc_url( home_url( '/' ) ); ?>"><?php esc_html_e( 'View the site', 'own-and-become-setup' ); ?></a></p>
		<?php endif; ?>

		<form method="post" style="margin-top:1.5em">
			<?php wp_nonce_field( 'ob_setup_run' ); ?>
			<button type="submit" name="ob_setup_run" value="1" class="button button-primary button-hero" <?php disabled( ! $ready ); ?>>
				<?php echo empty( $state ) ? esc_html__( 'Run setup', 'own-and-become-setup' ) : esc_html__( 'Run setup again (fills in anything missing)', 'own-and-become-setup' ); ?>
			</button>
			<?php if ( ! $ready ) : ?>
				<p class="description"><?php esc_html_e( 'Fix the items marked ⚠️ above first.', 'own-and-become-setup' ); ?></p>
			<?php endif; ?>
		</form>
	</div>
	<?php
}

/**
 * Requirements shown on the admin page.
 *
 * @return array[]
 */
function ob_setup_checks() {
	return array(
		array(
			'ok'    => 'own-and-become' === get_stylesheet(),
			'label' => __( 'The “Own & Become” theme is active (Appearance → Themes). Twenty Twenty-Five must be installed too.', 'own-and-become-setup' ),
		),
		array(
			'ok'    => class_exists( 'WPCF7_ContactForm' ),
			'label' => __( 'Contact Form 7 is installed and active.', 'own-and-become-setup' ),
		),
		array(
			'ok'    => function_exists( 'honeypot4cf7_add_form_tag' ),
			'label' => __( 'Honeypot for Contact Form 7 is installed and active (spam protection).', 'own-and-become-setup' ),
		),
		array(
			'ok'    => defined( 'THE_SEO_FRAMEWORK_VERSION' ),
			'label' => __( 'The SEO Framework is installed and active (SEO titles, descriptions and XML sitemap).', 'own-and-become-setup' ),
		),
	);
}
