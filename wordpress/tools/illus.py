import os
D=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'own-and-become', '')+'assets/images/'
F='#3D5E4D'; FD='#2C4639'; S='#8BA38B'; SM='#B9CBB6'; SS='#DCE6DA'; T='#EEF2EC'; C='#D4834C'; CD='#B8662F'; CR='#FBFAF6'; SUN='#F3D3B5'
def leaf(x,y,s=1,r=0,fill=S,vein=None,op=1):
    v=f'<path d="M1 -1 L8 -10" stroke="{vein}" stroke-width="{1.2/s:.2f}" stroke-linecap="round" fill="none"/>' if vein else ''
    return f'<g transform="translate({x} {y}) rotate({r}) scale({s})" opacity="{op}"><path d="M0 0C-1-6 3-11 10-12C11-5 7 0 0 0Z" fill="{fill}"/>{v}</g>'
def w(name, vb, body, label=None):
    a = f' role="img" aria-label="{label}"' if label else ' aria-hidden="true"'
    _,_,vw,vh = vb.split()
    open(D+name,'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{vw}" height="{vh}"{a}>{body}</svg>\n')

def figure(x,y,s,body,head):
    # a soft, faceless figure: rounded head + leaf-like body (echoing the logo)
    return f'<g transform="translate({x} {y}) scale({s})"><circle cx="0" cy="-34" r="8.5" fill="{head}"/><path d="M-11 0C-12-14-8-23 0-23C8-23 12-14 11 0Z" fill="{body}"/></g>'

# ---- HERO: arch window, hills, winding path, two people walking together, bending tree
hero = f'''<defs><clipPath id="arch"><path d="M40 600V250A200 200 0 0 1 440 250V600Z"/></clipPath></defs>
<g clip-path="url(#arch)">
<rect width="480" height="600" fill="{T}"/>
<circle cx="318" cy="196" r="52" fill="{SUN}"/>
<circle cx="318" cy="196" r="74" fill="none" stroke="{SUN}" stroke-width="2" opacity=".7"/>
<path d="M40 372C110 330 190 336 255 356C325 378 385 334 440 340V600H40Z" fill="{SS}"/>
<path d="M40 438C130 398 215 418 300 428C362 436 402 410 440 402V600H40Z" fill="{SM}"/>
<path d="M40 500C140 470 250 490 330 500C382 506 420 490 440 486V600H40Z" fill="{S}"/>
<path d="M176 600C214 566 292 556 284 524C277 496 222 492 246 468C262 452 306 446 330 434L338 437C318 450 290 458 280 472C264 494 318 504 320 528C324 562 266 578 292 600Z" fill="{CR}"/>
{figure(256,526,1.3,F,F)}
{figure(285,523,1.2,'#6F8C72','#6F8C72')}
<path d="M120 600C116 540 134 500 126 452C120 414 136 382 162 362" fill="none" stroke="{FD}" stroke-width="8" stroke-linecap="round"/>
<path d="M128 470C112 460 100 448 94 432" fill="none" stroke="{FD}" stroke-width="5" stroke-linecap="round"/>
{leaf(150,370,3.2,-40,F)}{leaf(160,366,3.0,40,S)}{leaf(140,360,2.6,-90,'#5E7F68')}{leaf(166,356,2.3,-10,F)}{leaf(94,436,2.0,-110,S)}{leaf(98,430,1.7,-50,'#5E7F68')}{leaf(182,372,1.8,70,'#5E7F68')}
{leaf(352,476,1.2,-30,F)}{leaf(356,478,1.0,40,SM)}
</g>
<path d="M40 600V250A200 200 0 0 1 440 250V600" fill="none" stroke="{F}" stroke-opacity=".18" stroke-width="2"/>
{leaf(40,560,4.2,-55,S,F)}{leaf(60,572,3.0,-10,F,None)}
{leaf(430,330,3.0,20,F)}{leaf(434,334,2.4,100,S)}
{leaf(78,170,1.5,-70,C)}{leaf(84,166,1.3,10,CD)}'''
w('hero-arch.svg','0 0 480 600',hero,'Illustration: two people walking side by side along a winding path through soft green hills, beside a bending tree')

# ---- EMPATHY: a looping line that keeps moving forward and grows into a sprout
emp = f'''<path d="M20 300C70 300 80 230 130 236C186 243 160 314 214 312C262 310 250 238 214 228C178 218 170 286 236 300C300 314 330 250 372 250C410 250 420 214 420 180" fill="none" stroke="{F}" stroke-width="3" stroke-linecap="round" stroke-dasharray="0" />
<path d="M20 300C70 300 80 230 130 236" fill="none" stroke="{SM}" stroke-width="10" stroke-linecap="round" opacity=".45"/>
<circle cx="20" cy="300" r="7" fill="{F}"/>
<path d="M420 182V120" stroke="{F}" stroke-width="3" stroke-linecap="round"/>
{leaf(420,140,3.6,-35,S,F)}{leaf(420,158,3.0,215,F)}{leaf(428,108,1.6,-15,C)}{leaf(433,105,1.2,60,CD)}
<ellipse cx="420" cy="186" rx="44" ry="7" fill="{SS}"/>'''
w('path-sprout.svg','0 0 500 340',emp,'Illustration: a line that loops back on itself a few times, keeps moving forward, and grows into a small sprout')

# ---- TOGETHER: two people sitting on a curved bench under a tree that bends and recovers
tog = f'''<ellipse cx="280" cy="380" rx="250" ry="26" fill="{SS}"/>
<path d="M330 380C318 320 344 270 326 210C316 176 330 136 370 112" fill="none" stroke="{FD}" stroke-width="10" stroke-linecap="round"/>
<path d="M334 262C360 250 382 230 392 204" fill="none" stroke="{FD}" stroke-width="6" stroke-linecap="round"/>
{leaf(370,118,4.4,-40,F)}{leaf(380,112,4.0,40,S)}{leaf(356,108,3.6,-95,'#5E7F68')}{leaf(392,98,3.0,-5,F)}{leaf(394,206,2.6,-20,S)}{leaf(396,200,2.0,60,'#5E7F68')}{leaf(330,130,2.6,-140,S)}{leaf(410,128,2.4,70,'#5E7F68')}
<path d="M120 330C170 344 250 344 300 330" fill="none" stroke="{F}" stroke-width="7" stroke-linecap="round"/>
<path d="M140 336V378M282 336V378" stroke="{F}" stroke-width="6" stroke-linecap="round"/>
{figure(186,330,1.6,F,F)}
{figure(238,330,1.5,'#6F8C72','#6F8C72')}
{leaf(212,262,1.1,-20,C)}{leaf(217,259,0.9,60,CD)}
{leaf(60,370,2.6,-60,S)}{leaf(70,374,2.0,0,F)}'''
w('together.svg','0 0 560 420',tog,'Illustration: two people sitting together on a curved bench beneath a tree, with two small copper leaves between them')

# ---- PORTRAIT placeholder
por = f'''<defs><clipPath id="pa"><path d="M0 500V200A200 200 0 0 1 400 200V500Z"/></clipPath></defs>
<g clip-path="url(#pa)"><rect width="400" height="500" fill="{T}"/>
<circle cx="200" cy="205" r="62" fill="{SS}"/><path d="M80 500C80 380 130 300 200 300S320 380 320 500Z" fill="{SS}"/>
{leaf(312,120,3,-30,S)}{leaf(318,124,2.4,50,SM)}</g>
<text x="200" y="460" text-anchor="middle" font-family="Nunito Sans, Arial, sans-serif" font-size="20" font-weight="700" fill="{F}">[ADD PHOTO OF AYESHA]</text>'''
w('portrait-placeholder.svg','0 0 400 500',por,'Placeholder for a photo of Ayesha Munawar')

# ---- Decorative sprigs
spr = f'''<path d="M30 190C60 150 90 110 150 40" fill="none" stroke="{F}" stroke-width="3" stroke-linecap="round" opacity=".7"/>
{leaf(62,150,3.4,-80,S)}{leaf(66,148,3.0,10,SM)}{leaf(92,112,3.2,-80,S)}{leaf(96,110,2.8,10,SM)}{leaf(122,76,2.8,-75,S)}{leaf(126,74,2.4,15,SM)}{leaf(148,44,2.2,-30,S)}'''
w('leaf-sprig.svg','0 0 200 200',spr)
sprl = spr.replace(S,'#DCE6DA').replace(SM,'#B9CBB6').replace(F,'#DCE6DA')
w('leaf-sprig-light.svg','0 0 200 200',sprl)

# ---- Leaf-curve divider: two paired curves meeting at the logo's copper leaves
div = f'''<path d="M4 20C40 20 60 8 96 10C112 11 120 16 124 19" fill="none" stroke="{S}" stroke-width="2" stroke-linecap="round"/>
<path d="M256 20C220 20 200 8 164 10C148 11 140 16 136 19" fill="none" stroke="{S}" stroke-width="2" stroke-linecap="round"/>
<path d="M4 25C44 27 70 18 100 20C114 21 121 24 125 26M256 25C216 27 190 18 160 20C146 21 139 24 135 26" fill="none" stroke="{F}" stroke-opacity=".35" stroke-width="1.2" stroke-linecap="round"/>
<g transform="translate(130 6) scale(1.1)"><path d="M-1.6 21C-6.3 19.6-8.5 14.6-7.2 8.6c4.3 2 6.6 6.6 5.6 12.4Z" fill="{C}"/><path d="M.2 19.4C.4 13.8 3.4 9.7 8.4 8.4c-.1 5.8-3.3 9.9-8.2 11Z" fill="{CD}"/></g>'''
w('leaf-curve-divider.svg','0 0 260 34',div)

# ---- Winding connector for the 3 steps
win = f'<path d="M2 12C60 2 110 22 170 12S280 2 340 12 450 22 510 12 580 4 598 10" fill="none" stroke="{S}" stroke-width="2" stroke-dasharray="2 7" stroke-linecap="round"/>'
w('winding-line.svg','0 0 600 24',win)

# ---- Own / Become panel art
own = f'''<ellipse cx="120" cy="96" rx="96" ry="10" fill="{SS}"/>
<path d="M120 96V40" stroke="{F}" stroke-width="3" stroke-linecap="round"/>
{leaf(120,58,2.4,-35,S,F)}{leaf(120,66,2.0,215,F)}
<path d="M120 96c0 14-10 22-26 30M120 96c0 14 10 22 26 30M120 96v38M108 112c-8 3-18 4-26 2M132 112c8 3 18 4 26 2M94 126c-6 0-12 2-16 6M146 126c6 0 12 2 16 6" fill="none" stroke="{F}" stroke-width="2.2" stroke-linecap="round" opacity=".8"/>'''
w('own-roots.svg','0 0 240 150',own,'Illustration: a small plant with strong roots')
bec = f'''<ellipse cx="120" cy="132" rx="96" ry="10" fill="{SS}"/>
<path d="M120 132C118 100 126 74 120 44" stroke="{F}" stroke-width="3" stroke-linecap="round" fill="none"/>
{leaf(121,98,3.0,-40,S,F)}{leaf(121,106,2.6,220,F)}{leaf(121,70,2.4,-30,SM,F)}{leaf(121,76,2.0,210,S)}{leaf(122,46,1.4,-15,C)}{leaf(126,43,1.1,60,CD)}'''
w('become-growth.svg','0 0 240 150',bec,'Illustration: a young plant growing new leaves')
print('ok')
