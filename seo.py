"""Dati strutturati Schema.org (JSON-LD) per Google."""
import json
STUDIO = {
    'name': 'ERRE studio', 'street': 'Via Patalini 11', 'zip': '76121', 'city': 'Barletta', 'region': 'BT',
    'phone': '+39 389 801 2408', 'site': 'https://errestudiobarletta.it/',
}
SAME_AS = ['https://www.instagram.com/ruggierorussophotography/', 'https://www.facebook.com/ruggiero.russo']
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

def _tag(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '</script>'

def home(domain, lg, cover):
    person = {'@type': 'Person', '@id': domain + '/#ruggiero', 'name': 'Ruggiero Russo',
              'jobTitle': 'Fotografo' if lg == 'it' else 'Photographer', 'url': domain + '/', 'sameAs': SAME_AS,
              'knowsAbout': ['Fashion photography', 'Still-life photography', 'Advertising photography', 'Beauty photography']}
    biz = {'@type': ['ProfessionalService', 'LocalBusiness'], '@id': domain + '/#business',
           'name': 'Ruggiero Russo Photography', 'url': domain + '/', 'image': f'{domain}/img/{cover}',
           'logo': domain + '/assets/logo-full.png', 'email': 'info@ruggierorusso.com', 'telephone': STUDIO['phone'],
           'description': ('Fotografo fashion, still-life e advertising con studio a Barletta (ERRE studio). Shooting in studio e in location per brand e aziende.'
                           if lg == 'it' else 'Fashion, still-life and advertising photographer with a studio in Barletta, Italy (ERRE studio). Studio and on-location shoots for brands.'),
           'address': {'@type': 'PostalAddress', 'streetAddress': STUDIO['street'], 'postalCode': STUDIO['zip'],
                       'addressLocality': STUDIO['city'], 'addressRegion': STUDIO['region'], 'addressCountry': 'IT'},
           'areaServed': ['Puglia', 'Basilicata', 'Italia'], 'founder': {'@id': domain + '/#ruggiero'}, 'sameAs': SAME_AS,
           'openingHoursSpecification': [
               {'@type': 'OpeningHoursSpecification', 'dayOfWeek': DAYS, 'opens': '09:00', 'closes': '13:15'},
               {'@type': 'OpeningHoursSpecification', 'dayOfWeek': DAYS, 'opens': '16:30', 'closes': '19:30'},
               {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Saturday'], 'opens': '09:00', 'closes': '13:15'}],
           'hasOfferCatalog': {'@type': 'OfferCatalog', 'name': 'Servizi' if lg == 'it' else 'Services', 'itemListElement': [
               {'@type': 'Offer', 'itemOffered': {'@type': 'Service', 'name': n}} for n in
               (['Fotografia di moda', 'Fotografia still-life e di prodotto', 'Fotografia pubblicitaria', 'Foto per e-commerce', 'Noleggio sala posa ERRE studio']
                if lg == 'it' else ['Fashion photography', 'Still-life and product photography', 'Advertising photography', 'E-commerce photography', 'ERRE studio rental'])]}}
    site = {'@type': 'WebSite', '@id': domain + '/#website', 'url': domain + '/', 'name': 'Ruggiero Russo Photography',
            'inLanguage': lg, 'publisher': {'@id': domain + '/#business'}}
    return _tag({'@context': 'https://schema.org', '@graph': [person, biz, site]})

def project(domain, lg, url, title, desc, images, crumbs_home, works_label, brand=None, date=None):
    g = {'@type': 'ImageGallery', 'name': title, 'url': url, 'description': desc, 'inLanguage': lg,
         'creator': {'@id': domain + '/#ruggiero'}, 'image': images[:10]}
    if brand: g['about'] = {'@type': 'Brand', 'name': brand}
    bc = {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': 'Ruggiero Russo', 'item': crumbs_home},
        {'@type': 'ListItem', 'position': 2, 'name': works_label, 'item': crumbs_home + '#lavori'},
        {'@type': 'ListItem', 'position': 3, 'name': title, 'item': url}]}
    return _tag({'@context': 'https://schema.org', '@graph': [g, bc]})
