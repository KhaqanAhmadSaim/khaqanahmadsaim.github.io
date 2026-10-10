import os
D=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'own-and-become', '')+'assets/icons/'
F='#3D5E4D'; S='#8BA38B'; SS='#DCE6DA'; C='#D4834C'; CD='#B8662F'
def icon(name, body, vb='0 0 48 48'):
    open(D+name+'.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" fill="none" stroke="{F}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>\n')
LEAF=lambda x,y,s=1,r=0,fill=S,stroke='none': f'<path transform="translate({x} {y}) rotate({r}) scale({s})" d="M0 0C-1-6 3-11 10-12C11-5 7 0 0 0Z" fill="{fill}" stroke="{stroke}"/>'
blob='<path d="M24 5c10 0 19 7 19 18s-8 20-20 20S5 35 5 24 14 5 24 5Z" fill="'+SS+'" stroke="none"/>'
# small decorative
open(D+'leaf-pair.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true"><path d="M11.2 21C6.5 19.6 4.3 14.6 5.6 8.6c4.3 2 6.6 6.6 5.6 12.4Z" fill="{C}"/><path d="M13 19.4c.2-5.6 3.2-9.7 8.2-11-.1 5.8-3.3 9.9-8.2 11Z" fill="{CD}"/></svg>\n')
open(D+'leaf-bullet.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" aria-hidden="true"><path d="M3 17C3 9.2 8 4 17 3c0 8-5 13.4-14 14Z" fill="{S}"/><path d="M4.2 15.8 12.5 7.5" stroke="{F}" stroke-width="1.3" stroke-linecap="round"/></svg>\n')
# UI glyphs (used as CSS masks)
def ui(name, body):
    open(D+'ui-'+name+'.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>\n')
ui('phone','<path d="M6.6 3.5h2.6l1.4 4-2 1.4a11 11 0 0 0 6.5 6.5l1.4-2 4 1.4v2.6a2 2 0 0 1-2.2 2A16.5 16.5 0 0 1 4.6 5.7a2 2 0 0 1 2-2.2Z"/>')
ui('pin','<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0C18.5 15.4 12 21 12 21Z"/><circle cx="12" cy="10" r="2.3"/>')
ui('chat','<path d="M4 6.5A2.5 2.5 0 0 1 6.5 4h11A2.5 2.5 0 0 1 20 6.5v7a2.5 2.5 0 0 1-2.5 2.5H10l-4.5 4v-4h0A1.5 1.5 0 0 1 4 14.5Z"/>')
ui('lock','<rect x="5" y="10.5" width="14" height="9.5" rx="2.5"/><path d="M8.5 10.5V8a3.5 3.5 0 0 1 7 0v2.5"/>')
# Feature icons
icon('consult', blob+'<path d="M11 13h22a5 5 0 0 1 5 5v9a5 5 0 0 1-5 5H22l-7 6v-6h-4a5 5 0 0 1-5-5v-9a5 5 0 0 1 5-5Z" fill="#fff"/>'+LEAF(17,28,1.05,0,S,F)+f'<path d="M27 21h6M27 25.5h4"/>')
icon('online', blob+'<rect x="9" y="12" width="30" height="20" rx="3" fill="#fff"/><path d="M5 36h38l-2.5 3.5h-33Z" fill="#fff"/>'+f'<path d="M24 29v-6"/>'+LEAF(24,23,0.85,-20,S,F)+LEAF(24,25,0.6,200,C,'none'))
icon('languages', blob+'<path d="M8 12h18a4 4 0 0 1 4 4v7a4 4 0 0 1-4 4h-9l-5 4v-4H8a4 4 0 0 1-4-4v-7a4 4 0 0 1 4-4Z" fill="#fff"/><path d="M30 19h10a4 4 0 0 1 4 4v7a4 4 0 0 1-4 4h-2v4l-5-4h-7a4 4 0 0 1-4-4v-3" fill="'+SS+'"/><path d="M10 18.5h12M10 22.5h8M28 30.5h10"/>')
icon('confidential', blob+'<path d="M24 6l14 5v10c0 9.5-6 16.5-14 20-8-3.5-14-10.5-14-20V11Z" fill="#fff"/>'+LEAF(19,30,1.2,-10,S,F)+'<path d="M19.5 29.5 27 22"/>')
icon('individual', blob+'<circle cx="24" cy="15" r="6" fill="#fff"/><path d="M12 39c0-7.5 5.4-13 12-13s12 5.5 12 13" fill="#fff"/>'+LEAF(31.5,13,0.55,-15,C,'none'))
icon('couples', blob+'<circle cx="17.5" cy="16" r="5.5" fill="#fff"/><circle cx="31" cy="13.5" r="5" fill="'+SS+'"/><path d="M8 39c0-7 4.3-12 10-12 3 0 5.6 1.3 7.4 3.6" fill="#fff"/><path d="M40 37c0-7-3.8-12-9-12-2.8 0-5.2 1.2-7 3.3" fill="'+SS+'"/>'+LEAF(22.5,12.5,0.55,-15,C,'none'))
icon('teen', blob+'<path d="M24 40V22"/>'+LEAF(24,26,1.25,-35,S,F)+LEAF(24,30,1.0,215,'#fff',F)+'<path d="M14 40h20"/><circle cx="35" cy="12" r="3.5" fill="#F3D3B5" stroke="none"/>')
icon('calendar', blob+'<rect x="9" y="11" width="30" height="27" rx="4" fill="#fff"/><path d="M9 19h30M17 7v8M31 7v8"/><path d="m18.5 28.5 4 4 7.5-8"/>')
icon('chat', blob+'<path d="M8 11h20a4 4 0 0 1 4 4v8a4 4 0 0 1-4 4h-8l-6 5v-5H8a4 4 0 0 1-4-4v-8a4 4 0 0 1 4-4Z" fill="#fff"/><path d="M34 20h6a4 4 0 0 1 4 4v8a4 4 0 0 1-4 4h-2v5l-6-5h-6a4 4 0 0 1-4-4v-1" fill="'+SS+'"/><circle cx="12.5" cy="19" r="1.2" fill="'+F+'"/><circle cx="18" cy="19" r="1.2" fill="'+F+'"/><circle cx="23.5" cy="19" r="1.2" fill="'+F+'"/>')
icon('sprout', blob+'<path d="M24 41V23"/>'+LEAF(24,27,1.2,-35,S,F)+LEAF(24,31,1.0,215,'#fff',F)+'<path d="M13 41h22"/>'+LEAF(32,15,0.5,-20,C,'none'))
icon('roots', blob+'<path d="M24 6v18"/>'+LEAF(24,12,0.9,-35,S,F)+'<path d="M8 24h32"/><path d="M24 24c0 6-4 9-9 12M24 24c0 6 4 9 9 12M24 24v15M19 30c-2 1-5 1.5-7 1M29 30c2 1 5 1.5 7 1" />')
icon('path', blob+'<path d="M14 42c0-6 16-6 16-12s-12-6-12-12 7-7 10-8"/><path d="M34 6v10"/><path d="M34 6.5h7l-2 3 2 3h-7" fill="#F3D3B5"/>'+LEAF(10,30,0.75,-60,S,F))
icon('wave', blob+'<path d="M7 19c4-4 7-4 11 0s7 4 11 0 7-4 12 0"/><path d="M7 27c4-4 7-4 11 0s7 4 11 0 7-4 12 0" stroke="'+S+'"/><path d="M11 35c3-2.5 5.5-2.5 8.5 0s5.5 2.5 8.5 0 5.5-2.5 8.5 0" stroke-opacity=".55"/>')
icon('family', blob+'<circle cx="15" cy="16" r="5" fill="#fff"/><circle cx="33" cy="16" r="5" fill="#fff"/><circle cx="24" cy="25" r="3.8" fill="'+SS+'"/><path d="M6 38c0-6 4-10 9-10 2.4 0 4.5.9 6 2.4M42 38c0-6-4-10-9-10-2.4 0-4.5.9-6 2.4"/><path d="M17.5 40c0-4.5 3-7.5 6.5-7.5s6.5 3 6.5 7.5" fill="'+SS+'"/>')
icon('seed', blob+'<path d="M24 42c-7.5 0-12-5-12-11.5S17.5 18 24 18s12 6 12 12.5S31.5 42 24 42Z" fill="#fff"/><path d="M24 18v-5"/>'+LEAF(24,14,0.72,-30,S,F)+LEAF(24,15,0.55,210,C,'none')+'<path d="M17.5 32c1.5 3.2 3.8 4.6 6.5 4.6" stroke="'+S+'"/>')
icon('falling-leaf', blob+LEAF(12,31,1.55,-8,S,F)+'<path d="M12.5 30.5l13.5-13" />'+'<path d="M30 30c3 2 6 6 5 11" stroke-dasharray="2 4"/>'+LEAF(34,40,0.7,40,C,'none'))
icon('heart-leaf', blob+'<path d="M24 39S9 30.5 9 19.5A7.5 7.5 0 0 1 24 15a7.5 7.5 0 0 1 15 4.5C39 30.5 24 39 24 39Z" fill="#fff"/>'+LEAF(24,30,0.95,-35,S,F))
icon('receipt', blob+'<path d="M13 7h22v34l-3.6-2.4L28 41l-4-2.4-4 2.4-3.4-2.4L13 41Z" fill="#fff"/><path d="M18 15h12M18 21h12M18 27h7"/>'+LEAF(29,31,0.7,-30,C,'none'))
icon('book', blob+'<path d="M6 12c6-2 12-1 18 3 6-4 12-5 18-3v25c-6-2-12-1-18 3-6-4-12-5-18-3Z" fill="#fff"/><path d="M24 15v25"/>'+LEAF(12,27,0.7,-30,S,F))
icon('compass', blob+'<circle cx="24" cy="24" r="15" fill="#fff"/><path d="m29.5 18.5-3.4 7.6-7.6 3.4 3.4-7.6Z" fill="'+SS+'"/><path d="M24 9v3M24 36v3M9 24h3M36 24h3"/>')
icon('mail', blob+'<rect x="7" y="12" width="34" height="24" rx="4" fill="#fff"/><path d="m8.5 14 15.5 12 15.5-12"/>')
icon('phone', blob+'<path d="M16 9h4.5l2.4 7-3.5 2.4a19 19 0 0 0 11.2 11.2l2.4-3.5 7 2.4v4.5a3.4 3.4 0 0 1-3.7 3.4C21.5 35.3 12.7 26.5 11.6 12.7A3.4 3.4 0 0 1 15 9Z" fill="#fff"/>')
icon('map', blob+'<path d="M6 13l11-4 14 4 11-4v26l-11 4-14-4-11 4Z" fill="#fff"/><path d="M17 9v26M31 13v26"/><path d="M24 30s-5-4.2-5-8.2a5 5 0 0 1 10 0c0 4-5 8.2-5 8.2Z" fill="'+SS+'"/>')
print(sorted(os.listdir(D)))
