"""Moodboard (foto preferite salvate nel browser) e pagina 404 'light painting'."""
PATH = {'it': 'moodboard.html', 'en': 'en/moodboard.html'}
TX = {
 'it': dict(mb='Moodboard', save='Aggiungi alla moodboard', saved='Nella moodboard',
   mb_t='La tua moodboard', mb_d='Le foto che hai salvato dal portfolio. Allegale alla richiesta di preventivo oppure condividi il link con il tuo team.',
   empty='La moodboard è vuota. Apri un lavoro e tocca ♡ sulle foto che ti ispirano.', go='Sfoglia i lavori',
   send='Richiedi un preventivo con questa moodboard', share='Copia il link da condividere', copied='Link copiato',
   clear='Svuota', remove='Rimuovi', shared='Moodboard condivisa con te', keep='Salva nella mia moodboard', attached='foto dalla moodboard allegate',
   lp='Pagina non trovata. Intanto, disegna con la luce: muovi il mouse o il dito.', lp_clear='Ricomincia'),
 'en': dict(mb='Moodboard', save='Add to moodboard', saved='In your moodboard',
   mb_t='Your moodboard', mb_d='The photos you saved from the portfolio. Attach them to a quote request or share the link with your team.',
   empty='Your moodboard is empty. Open a project and tap ♡ on the photos that inspire you.', go='Browse the work',
   send='Request a quote with this moodboard', share='Copy shareable link', copied='Link copied',
   clear='Clear', remove='Remove', shared='Moodboard shared with you', keep='Save to my moodboard', attached='photos attached from your moodboard',
   lp='Page not found. Meanwhile, paint with light: move your mouse or finger.', lp_clear='Start again'),
}

def mb_body(lg, up, quote_href, works_href):
    t = TX[lg]
    return f'''<section class="phead">
  <div class="ptitle"><h1>{t['mb_t']}</h1><span class="red" data-mb-count>0</span></div>
  <p class="lead">{t['mb_d']}</p>
</section>
<section class="mbwrap" data-mb-page data-root="{up}" data-remove="{t['remove']}" data-copied="{t['copied']}" data-shared="{t['shared']}">
  <p class="mb-shared label" hidden></p>
  <div class="mbgrid"></div>
  <p class="mb-empty" hidden>{t['empty']} <a class="ul" href="{works_href}">{t['go']} →</a></p>
  <p class="ctas mb-actions" hidden>
    <a class="btn red" href="{quote_href}">{t['send']} →</a>
    <button type="button" class="btn" data-mb-share>{t['share']}</button>
    <button type="button" class="btn" data-mb-keep hidden>{t['keep']}</button>
    <button type="button" class="btn ghost" data-mb-clear>{t['clear']}</button>
  </p>
</section>'''

def nf_body():
    it, en = TX['it'], TX['en']
    return f'''<section class="lp" data-lp>
  <canvas aria-hidden="true"></canvas>
  <div class="lp-txt"><h1>404</h1><p>{it['lp']}<br><span>{en['lp']}</span></p>
  <p class="ctas"><a class="btn" href="/index.html">Home</a><a class="btn ghost" href="/en/index.html">English</a><button type="button" class="btn ghost" data-lp-clear>{it['lp_clear']}</button></p></div>
</section>'''
