<?php
/**
 * Title: Service card
 * Slug: own-and-become/service-card
 * Categories: own-and-become
 * Description: Layout for a single service card. Duplicate it to add more.
 * Keywords: service, card
 *
 * @package own-and-become
 */
?>
<!-- wp:group {"className":"is-style-card ob-card-link","style":{"spacing":{"padding":{"top":"var:preset|spacing|40","bottom":"var:preset|spacing|40","left":"var:preset|spacing|40","right":"var:preset|spacing|40"},"blockGap":"0.85rem"},"dimensions":{"minHeight":"100%"}},"layout":{"type":"flex","orientation":"vertical","justifyContent":"stretch"}} -->
<div class="wp-block-group is-style-card ob-card-link" style="min-height:100%;padding-top:var(--wp--preset--spacing--40);padding-right:var(--wp--preset--spacing--40);padding-bottom:var(--wp--preset--spacing--40);padding-left:var(--wp--preset--spacing--40)"><!-- wp:image {"width":"3rem","sizeSlug":"full","className":"ob-icon"} -->
<figure class="wp-block-image size-full is-resized ob-icon"><img src="<?php echo own_and_become_asset( 'icons/individual.svg' ); ?>" alt="" style="width:3rem;height:auto"/></figure>
<!-- /wp:image -->

<!-- wp:heading {"fontSize":"large","level":3} -->
<h3 class="wp-block-heading has-large-font-size">Service name</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>One warm sentence about who this is for and how it helps.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph {"className":"ob-stretch","style":{"typography":{"fontWeight":"700"}}} -->
<p class="ob-stretch" style="font-weight:700"><a href="/services/">Learn more<span class="screen-reader-text"> about service name</span> →</a></p>
<!-- /wp:paragraph --></div>
<!-- /wp:group -->
