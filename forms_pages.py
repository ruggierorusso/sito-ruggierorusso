"""Pagine con moduli: preventivo interattivo, prenotazione ERRE studio, pagina di ringraziamento.

I moduli usano Netlify Forms (attributo data-netlify): Netlify li riconosce al momento della
pubblicazione e inoltra ogni richiesta via email (Netlify → Forms → Form notifications).
"""
import html
E = html.escape

PATHS = {
    'quote': {'it': 'preventivo.html', 'en': 'en/quote.html'},
    'book': {'it': 'prenota-studio.html', 'en': 'en/book-studio.html'},
    'thanks': {'it': 'grazie.html', 'en': 'en/thanks.html'},
}

TX = {
 'it': dict(
   quote='Preventivo', quote_t='Richiedi un preventivo', quote_d='Rispondi a qualche domanda: in due minuti ricevo tutto quello che mi serve per prepararti un preventivo su misura.',
   book='Prenota lo studio', book_t='Prenota ERRE studio', book_d='Richiedi la sala posa per il tuo shooting oppure prenota una sessione con me. Ti confermo disponibilità e dettagli via email.',
   step='Passo', of='di', nextb='Avanti', prevb='Indietro', send='Invia la richiesta', summary='Riepilogo', empty='—',
   q_type='Che tipo di shooting?', types=['Fashion / editoriale', 'Still-life / prodotto', 'Campagna advertising', 'E-commerce', 'Ritratto / personal branding', 'Altro'],
   q_where='Dove?', wheres=['ERRE studio, Barletta', 'In location', 'Da definire insieme'],
   q_qty='Quanti look o prodotti?', qty_u='look / prodotti',
   q_use='Dove userai le immagini?', uses=['Social', 'Sito web / e-commerce', 'Stampa e cataloghi', 'Campagna pubblicitaria', 'Affissioni'],
   q_extra='Ti serve anche…', extras=['Make-up artist', 'Hair stylist', 'Stylist', 'Modella / modello', 'Video e backstage', 'Ritocco avanzato'],
   q_when='Quando?', flex='Date flessibili',
   q_budget='Budget indicativo', budgets=['Fino a 1.000 €', '1.000 – 3.000 €', '3.000 – 7.000 €', 'Oltre 7.000 €', 'Da definire'],
   q_notes='Racconta il progetto', notes_ph='Brand, mood, riferimenti, link a moodboard…',
   q_you='I tuoi contatti', name='Nome e cognome', company='Azienda / brand', email='Email', phone='Telefono',
   consent='Ho letto l\'<a href="{privacy}">informativa privacy</a> e acconsento a essere ricontattato per questa richiesta.',
   b_use='Come vuoi usare lo studio?', b_uses=['Noleggio della sala (con il mio team)', 'Shooting con Ruggiero Russo'],
   b_date='Data', b_slot='Fascia', b_slots=['Mattina', 'Pomeriggio', 'Giornata intera', 'Più giorni'],
   b_people='Quante persone sul set?', b_need='Ti serve…', b_needs=['Luci flash', 'Luci continue', 'Fondali', 'Postazione trucco', 'Assistente di set'],
   thanks_t='Grazie!', thanks_d='La tua richiesta è arrivata. Ti rispondo al più presto, di solito entro un giorno lavorativo.', back_home='Torna al portfolio',
   cta_quote='Richiedi un preventivo', cta_book='Prenota lo studio'),
 'en': dict(
   quote='Quote', quote_t='Request a quote', quote_d='Answer a few questions: in two minutes I get everything I need to prepare a tailored quote.',
   book='Book the studio', book_t='Book ERRE studio', book_d='Request the studio for your own shoot or book a session with me. I will confirm availability and details by email.',
   step='Step', of='of', nextb='Next', prevb='Back', send='Send request', summary='Summary', empty='—',
   q_type='What kind of shoot?', types=['Fashion / editorial', 'Still-life / product', 'Advertising campaign', 'E-commerce', 'Portrait / personal branding', 'Other'],
   q_where='Where?', wheres=['ERRE studio, Barletta', 'On location', 'To be decided together'],
   q_qty='How many looks or products?', qty_u='looks / products',
   q_use='Where will you use the images?', uses=['Social media', 'Website / e-commerce', 'Print and catalogues', 'Advertising campaign', 'Billboards'],
   q_extra='You also need…', extras=['Make-up artist', 'Hair stylist', 'Stylist', 'Model', 'Video and behind the scenes', 'Advanced retouching'],
   q_when='When?', flex='Flexible dates',
   q_budget='Indicative budget', budgets=['Up to €1,000', '€1,000 – 3,000', '€3,000 – 7,000', 'Over €7,000', 'To be defined'],
   q_notes='Tell me about the project', notes_ph='Brand, mood, references, moodboard links…',
   q_you='Your details', name='Full name', company='Company / brand', email='Email', phone='Phone',
   consent='I have read the <a href="{privacy}">privacy policy</a> and agree to be contacted about this request.',
   b_use='How do you want to use the studio?', b_uses=['Studio rental (with my own team)', 'Shoot with Ruggiero Russo'],
   b_date='Date', b_slot='Slot', b_slots=['Morning', 'Afternoon', 'Full day', 'Several days'],
   b_people='How many people on set?', b_need='You need…', b_needs=['Flash lights', 'Continuous lights', 'Backdrops', 'Make-up station', 'Set assistant'],
   thanks_t='Thank you!', thanks_d='Your request has arrived. I will reply as soon as possible, usually within one working day.', back_home='Back to the portfolio',
   cta_quote='Request a quote', cta_book='Book the studio'),
}

def rel(lg, key, up):
    """Link from a page at depth `up` ('' or '../' …) to another site path."""
    return up + PATHS[key][lg]

def _choices(kind, name, opts, required=False):
    req = ' required' if required and kind == 'radio' else ''
    return '<div class="opts">' + ''.join(
        f'<label class="opt"><input type="{kind}" name="{name}" value="{E(o)}"{req if i == 0 else ""}><span>{E(o)}</span></label>'
        for i, o in enumerate(opts)) + '</div>'

def _contact(t, privacy_href):
    return f'''<div class="grid2">
  <label class="fld"><span>{t['name']} *</span><input name="nome" autocomplete="name" required></label>
  <label class="fld"><span>{t['company']}</span><input name="azienda" autocomplete="organization"></label>
  <label class="fld"><span>{t['email']} *</span><input type="email" name="email" autocomplete="email" required></label>
  <label class="fld"><span>{t['phone']}</span><input type="tel" name="telefono" autocomplete="tel"></label>
</div>
<label class="consent"><input type="checkbox" name="privacy" value="accettata" required><span>{t['consent'].format(privacy=privacy_href)}</span></label>'''

def _form(name, action, steps, t, extra_attrs=''):
    n = len(steps)
    fs = ''.join(f'''<fieldset class="step" data-step="{i + 1}">
  <legend><span class="label">{t['step']} {i + 1} {t['of']} {n}</span>{E(title)}</legend>
  {content}
</fieldset>''' for i, (title, content) in enumerate(steps))
    return f'''<form class="wizard" name="{name}" method="POST" action="{action}" data-netlify="true" netlify-honeypot="bot-field"{extra_attrs}>
  <input type="hidden" name="form-name" value="{name}">
  <p class="hp"><label>Non compilare: <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
  <div class="progress" aria-hidden="true"><span></span></div>
  {fs}
  <div class="wnav">
    <button type="button" class="btn ghost" data-prev>← {t['prevb']}</button>
    <button type="button" class="btn" data-next>{t['nextb']} →</button>
    <button type="submit" class="btn red" data-send>{t['send']}</button>
  </div>
</form>'''

def quote_body(lg, up):
    t = TX[lg]
    priv = up + ('privacy.html' if lg == 'it' else 'en/privacy.html')
    steps = [
        (t['q_type'], _choices('radio', 'tipo', t['types'], True)),
        (t['q_where'], _choices('radio', 'luogo', t['wheres'], True) +
            f'<label class="fld range"><span>{t["q_qty"]}</span><input type="range" name="quantita" min="1" max="50" value="6"><output>6</output> <small>{t["qty_u"]}</small></label>'),
        (t['q_use'], _choices('checkbox', 'utilizzo', t['uses']) + f'<h3 class="sub">{t["q_extra"]}</h3>' + _choices('checkbox', 'extra', t['extras'])),
        (t['q_when'], f'''<div class="grid2"><label class="fld"><span>{t['q_when']}</span><input type="date" name="data"></label>
<label class="consent inline"><input type="checkbox" name="date_flessibili" value="sì"><span>{t['flex']}</span></label></div>
<h3 class="sub">{t['q_budget']}</h3>''' + _choices('radio', 'budget', t['budgets']) +
            f'<label class="fld"><span>{t["q_notes"]}</span><textarea name="note" rows="4" placeholder="{E(t["notes_ph"])}"></textarea></label>'),
        (t['q_you'], _contact(t, priv)),
    ]
    action = '/' + PATHS['thanks'][lg]
    return f'''<section class="phead">
  <div class="ptitle"><h1>{t['quote_t']}</h1><span class="red">{t['quote']}</span></div>
  <p class="lead">{t['quote_d']}</p>
</section>
<section class="formwrap">
  {_form('preventivo', action, steps, t)}
  <aside class="summary" aria-live="polite"><p class="label">{t['summary']}</p><dl data-summary data-empty="{t['empty']}"></dl></aside>
</section>'''

def book_body(lg, up, studio_img):
    t = TX[lg]
    priv = up + ('privacy.html' if lg == 'it' else 'en/privacy.html')
    steps = [
        (t['b_use'], _choices('radio', 'uso', t['b_uses'], True)),
        (t['b_date'], f'<div class="grid2"><label class="fld"><span>{t["b_date"]} *</span><input type="date" name="data" required></label>'
            f'<label class="fld"><span>{t["b_people"]}</span><input type="number" name="persone" min="1" max="30" value="3"></label></div>'
            f'<h3 class="sub">{t["b_slot"]}</h3>' + _choices('radio', 'fascia', t['b_slots'], True) +
            f'<h3 class="sub">{t["b_need"]}</h3>' + _choices('checkbox', 'attrezzatura', t['b_needs']) +
            f'<label class="fld"><span>{t["q_notes"]}</span><textarea name="note" rows="3"></textarea></label>'),
        (t['q_you'], _contact(t, priv)),
    ]
    action = '/' + PATHS['thanks'][lg]
    return f'''<section class="phead">
  <div class="ptitle"><h1>{t['book_t']}</h1><span class="red">Barletta (BT)</span></div>
  <p class="lead">{t['book_d']}</p>
</section>
<section class="formwrap">
  {_form('prenota-studio', action, steps, t)}
  <aside class="summary"><img src="{up}img/{studio_img}" alt="ERRE studio" loading="lazy"><p class="label">{t['summary']}</p><dl data-summary data-empty="{t['empty']}"></dl></aside>
</section>'''

def thanks_body(lg, up):
    t = TX[lg]
    home = up + ('index.html' if lg == 'it' else 'en/index.html')
    return f'''<section class="nf"><h1>{t['thanks_t']}</h1><p>{t['thanks_d']}</p><a class="ul" href="{home}">{t['back_home']} →</a></section>'''
