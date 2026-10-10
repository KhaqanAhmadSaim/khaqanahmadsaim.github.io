"""Tiny helpers that emit valid core block markup (serialized like the editor does)."""
import json, html as H

def _attrs(a):
    return (' ' + json.dumps(a, separators=(',', ':'), ensure_ascii=False).replace('&','\\u0026').replace('<','\\u003c').replace('>','\\u003e')) if a else ''

def css_val(v):
    if isinstance(v, str) and v.startswith('var:preset|'):
        _, kind, slug = v.split('|')
        return f'var(--wp--preset--{kind}--{slug})'
    return v

def spacing_style(sp, prop):
    out=[]
    for side in ['top','right','bottom','left']:
        if side in sp: out.append(f'{prop}-{side}:{css_val(sp[side])}')
    return out

def style_and_classes(a, link_el=True):
    """Return (classes, styles) the way block supports serialize them."""
    cls=[]; st=[]
    s=a.get('style',{})
    if a.get('textColor'): cls += [f"has-{a['textColor']}-color", 'has-text-color']
    if a.get('backgroundColor'): cls += [f"has-{a['backgroundColor']}-background-color", 'has-background']
    if s.get('color',{}).get('text'): st.append(f"color:{s['color']['text']}"); cls.append('has-text-color')
    if s.get('color',{}).get('background'): st.append(f"background-color:{s['color']['background']}"); cls.append('has-background')
    if link_el and s.get('elements',{}).get('link',{}).get('color'): cls.append('has-link-color')
    if a.get('fontSize'): cls.append(f"has-{a['fontSize']}-font-size")
    if a.get('fontFamily'): cls.append(f"has-{a['fontFamily']}-font-family")
    b=s.get('border',{})
    if b.get('color'): cls.append('has-border-color'); st.append(f"border-color:{b['color']}")
    for side in ['top','right','bottom','left']:
        if side in b:
            for k in ['color','style','width']:
                if k in b[side]: st.append(f"border-{side}-{k}:{css_val(b[side][k])}")
    if b.get('radius'): st.append(f"border-radius:{b['radius']}")
    if b.get('style'): st.append(f"border-style:{b['style']}")
    if b.get('width'): st.append(f"border-width:{b['width']}")
    d=s.get('dimensions',{})
    if d.get('minHeight'): st.append(f"min-height:{d['minHeight']}")
    sp=s.get('spacing',{})
    if 'margin' in sp: st += spacing_style(sp['margin'],'margin')
    if 'padding' in sp: st += spacing_style(sp['padding'],'padding')
    t=s.get('typography',{})
    if t.get('fontSize'): st.append(f"font-size:{t['fontSize']}")
    if t.get('fontStyle'): st.append(f"font-style:{t['fontStyle']}")
    if t.get('fontWeight'): st.append(f"font-weight:{t['fontWeight']}")
    if t.get('lineHeight'): st.append(f"line-height:{t['lineHeight']}")
    if t.get('textTransform'): st.append(f"text-transform:{t['textTransform']}")
    if t.get('letterSpacing'): st.append(f"letter-spacing:{t['letterSpacing']}")
    if s.get('shadow'): pass
    return cls, st

def wrap_attr(base, a, extra_cls=(), link_el=True, skip_style=False):
    cls, st = style_and_classes(a, link_el)
    allc=[base] if base else []
    if a.get('align'): allc.append('align'+a['align'])
    allc += list(extra_cls)
    if a.get('className'): allc.append(a['className'])
    allc += cls
    out=f' class="{" ".join(allc)}"' if allc else ''
    if st and not skip_style: out += f' style="{";".join(st)}"'
    return out

def group(inner, a=None, tag='div'):
    a=dict(a or {})
    if tag!='div': a['tagName']=tag
    a.setdefault('layout',{'type':'constrained'})
    return f'<!-- wp:group{_attrs(a)} -->\n<{tag}{wrap_attr("wp-block-group",a)}>{inner}</{tag}>\n<!-- /wp:group -->'

def J(*blocks):
    return '\n\n'.join(b for b in blocks if b)

def heading(text, level=2, a=None):
    a=dict(a or {})
    if level!=2: a['level']=level
    al=a.get('textAlign')
    extra=[f'has-text-align-{al}'] if al else []
    return f'<!-- wp:heading{_attrs(a)} -->\n<h{level}{wrap_attr("wp-block-heading",a,extra)}>{text}</h{level}>\n<!-- /wp:heading -->'

def p(text, a=None):
    a=dict(a or {})
    al=a.get('align')
    b=dict(a); b.pop('align',None)
    extra=[f'has-text-align-{al}'] if al else []
    w=wrap_attr('',b,extra)
    return f'<!-- wp:paragraph{_attrs(a)} -->\n<p{w}>{text}</p>\n<!-- /wp:paragraph -->'

def button(text, href, a=None):
    a=dict(a or {})
    outer=['wp-block-button']
    if a.get('width'): outer += ['has-custom-width', f"wp-block-button__width-{a['width']}"]
    if a.get('className'): outer.append(a['className'])
    s=a.get('style',{})
    # colours/padding go on the link
    lc, ls = style_and_classes({k:v for k,v in a.items() if k!='className'}, link_el=False)
    if s.get('typography',{}).get('fontSize'): lc.insert(0,'has-custom-font-size')
    link_cls=['wp-block-button__link']+lc+['wp-element-button']
    st=f' style="{";".join(ls)}"' if ls else ''
    return f'<!-- wp:button{_attrs(a)} -->\n<div class="{" ".join(outer)}"><a class="{" ".join(link_cls)}" href="{href}"{st}>{text}</a></div>\n<!-- /wp:button -->'

def buttons(*btns, a=None):
    a=dict(a or {})
    return f'<!-- wp:buttons{_attrs(a)} -->\n<div{wrap_attr("wp-block-buttons",a)}>{chr(10).join([""]) if False else ""}' + '\n\n'.join(btns) + '</div>\n<!-- /wp:buttons -->'

def image(src, alt, a=None, caption=None):
    a=dict(a or {})
    cls=['wp-block-image']
    if a.get('align'): cls.append('align'+a['align'])
    if a.get('sizeSlug'): cls.append('size-'+a['sizeSlug'])
    if a.get('width') or a.get('height'): cls.append('is-resized')
    if a.get('className'): cls.append(a['className'])
    st=[]
    if a.get('width'): st.append(f"width:{a['width']}")
    if a.get('height'): st.append(f"height:{a['height']}")
    elif a.get('width'): st.append("height:auto")
    if a.get('aspectRatio'): st.append(f"aspect-ratio:{a['aspectRatio']}")
    if a.get('scale'): st.append(f"object-fit:{a['scale']}")
    sty=f' style="{";".join(st)}"' if st else ''
    cap=f'<figcaption class="wp-element-caption">{caption}</figcaption>' if caption else ''
    return f'<!-- wp:image{_attrs(a)} -->\n<figure class="{" ".join(cls)}"><img src="{src}" alt="{H.escape(alt, quote=True)}"{sty}/>{cap}</figure>\n<!-- /wp:image -->'

def columns(*cols, a=None):
    a=dict(a or {})
    extra=[]
    if a.get('isStackedOnMobile') is False: extra.append('is-not-stacked-on-mobile')
    if a.get('verticalAlignment'): extra.append('are-vertically-aligned-'+a['verticalAlignment'])
    return f'<!-- wp:columns{_attrs(a)} -->\n<div{wrap_attr("wp-block-columns",a,extra)}>' + '\n\n'.join(cols) + '</div>\n<!-- /wp:columns -->'

def column(inner, a=None):
    a=dict(a or {})
    extra=[]
    if a.get('verticalAlignment'): extra.append('is-vertically-aligned-'+a['verticalAlignment'])
    w=wrap_attr('wp-block-column',a,extra)
    if a.get('width'):
        if ' style="' in w: w=w.replace(' style="',f' style="flex-basis:{a["width"]};',1)
        else: w+=f' style="flex-basis:{a["width"]}"'
    return f'<!-- wp:column{_attrs(a)} -->\n<div{w}>{inner}</div>\n<!-- /wp:column -->'

def ul(items, a=None):
    a=dict(a or {})
    lis='\n\n'.join(f'<!-- wp:list-item -->\n<li>{i}</li>\n<!-- /wp:list-item -->' for i in items)
    return f'<!-- wp:list{_attrs(a)} -->\n<ul{wrap_attr("wp-block-list",a)}>{lis}</ul>\n<!-- /wp:list -->'

def separator(a=None):
    a=dict(a or {})
    return f'<!-- wp:separator{_attrs(a)} -->\n<hr{wrap_attr("wp-block-separator",a,["has-alpha-channel-opacity"])}/>\n<!-- /wp:separator -->'

def spacer(h):
    return f'<!-- wp:spacer {{"height":"{h}"}} -->\n<div style="height:{h}" aria-hidden="true" class="wp-block-spacer"></div>\n<!-- /wp:spacer -->'

def pattern(slug):
    return f'<!-- wp:pattern {{"slug":"{slug}"}} /-->'

def html_block(s):
    return f'<!-- wp:html -->\n{s}\n<!-- /wp:html -->'

def shortcode(s):
    return f'<!-- wp:shortcode -->\n{s}\n<!-- /wp:shortcode -->'

def quote(text, cite=None, a=None):
    a=dict(a or {})
    c=f'<cite>{cite}</cite>' if cite else ''
    return f'<!-- wp:quote{_attrs(a)} -->\n<blockquote{wrap_attr("wp-block-quote",a)}>' + p(text) + f'{c}</blockquote>\n<!-- /wp:quote -->'

def accordion(items, a=None):
    """items: list of (question, answer_blocks_markup)."""
    a=dict(a or {})
    out=[]
    for q,ans in items:
        out.append(
            '<!-- wp:accordion-item -->\n<div class="wp-block-accordion-item">'
            f'<!-- wp:accordion-heading -->\n<h3 class="wp-block-accordion-heading has-icon has-icon-right"><button type="button" class="wp-block-accordion-heading__toggle"><span class="wp-block-accordion-heading__toggle-title">{q}</span><span class="wp-block-accordion-heading__toggle-icon" aria-hidden="true">+</span></button></h3>\n<!-- /wp:accordion-heading -->\n\n'
            f'<!-- wp:accordion-panel -->\n<div role="region" class="wp-block-accordion-panel">{ans}</div>\n<!-- /wp:accordion-panel --></div>\n<!-- /wp:accordion-item -->')
    return f'<!-- wp:accordion{_attrs(a)} -->\n<div role="group"{wrap_attr("wp-block-accordion",a)}>' + '\n\n'.join(out) + '</div>\n<!-- /wp:accordion -->'
