/**
 * Own & Become: tiny progressive enhancements. No dependencies.
 * 1. Header gets a soft border once the page scrolls.
 * 2. Elements with .ob-reveal fade in gently (skipped for reduced motion).
 * 3. Essential-cookies notice, dismissed once per browser.
 */
( function () {
	'use strict';

	var doc = document.documentElement;
	var reduceMotion = window.matchMedia && window.matchMedia( '(prefers-reduced-motion: reduce)' ).matches;

	// 1. Header state
	var header = document.querySelector( '.wp-site-blocks > header' ) || document.querySelector( '.ob-site-header' );
	if ( header ) {
		var onScroll = function () {
			header.classList.toggle( 'is-scrolled', window.scrollY > 8 );
		};
		onScroll();
		window.addEventListener( 'scroll', onScroll, { passive: true } );
	}

	// 2. Gentle reveal on scroll
	if ( ! reduceMotion && 'IntersectionObserver' in window ) {
		var items = document.querySelectorAll( '.ob-reveal, .ob-reveal-group > *' );
		if ( items.length ) {
			items.forEach( function ( el ) {
				el.classList.add( 'ob-reveal' );
			} );
			doc.classList.add( 'ob-motion' );
			var io = new IntersectionObserver( function ( entries ) {
				entries.forEach( function ( entry ) {
					if ( entry.isIntersecting ) {
						entry.target.classList.add( 'is-visible' );
						io.unobserve( entry.target );
					}
				} );
			}, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 } );
			items.forEach( function ( el ) {
				io.observe( el );
			} );
		}
	}

	// 3. Cookie notice
	var notice = document.querySelector( '.ob-cookie' );
	if ( notice ) {
		var KEY = 'ob-cookie-notice-dismissed';
		var dismissed = false;
		try {
			dismissed = window.localStorage.getItem( KEY ) === '1';
		} catch ( e ) {}

		if ( ! dismissed ) {
			notice.classList.add( 'is-visible' );
			notice.setAttribute( 'role', 'region' );
			notice.setAttribute( 'aria-label', 'Cookie notice' );
		}

		notice.addEventListener( 'click', function ( event ) {
			var button = event.target.closest( '.wp-block-button__link' );
			if ( ! button || button.getAttribute( 'href' ) !== '#ok' ) {
				return;
			}
			event.preventDefault();
			notice.classList.remove( 'is-visible' );
			try {
				window.localStorage.setItem( KEY, '1' );
			} catch ( e ) {}
		} );
	}
}() );
