import requests, json

def capitalize_name( string: str = '' ):
    return ' '.join( tuple( word.capitalize() for word in string.split('_') ) )

cutoff_price = 100
restrict_to_madurai = True
ignore_melees = True
melee_weapons = set( melee.replace( '&', 'and' ) for melee in { 'ack_&_brunt', 'amphis', 'anku', 'ankyros', 'ankyros_prime', 'arca_titron', 'arum_spinosa', 'atterax', 'azothane', 'balla', 'bo', 'bo_prime', 'boltace', 'broken_scepter', 'broken_war', 'cadus', 'cassowar', 'caustacyst', 'ceramic_dagger', 'cerata', 'ceti_lacera', 'cobra_&_crane', 'cobra_&_crane_prime', 'corufell', 'cronus', 'cyath', 'dakra_prime', 'dark_dagger', 'dark_split-sword', 'dark_sword', 'dehtat', 'destreza', 'destreza_prime', 'dex_dakra', 'dokrahm', 'dragon_nikana', 'dual_cleavers', 'dual_ether', 'dual_heat_swords', 'dual_ichor', 'dual_kamas', 'dual_kamas_prime', 'dual_keres', 'dual_keres_prime', 'dual_raza', 'dual_skana', 'dual_zoren', 'edun', 'endura', 'ether_daggers', 'ether_reaper', 'ether_sword', 'falcor', 'fang', 'fang_prime', 'fragor', 'fragor_prime', 'furax', 'furax_wraith', 'galatine', 'galatine_prime', 'galvacord', 'gazal_machete', 'ghoulsaw', 'glaive', 'glaive_prime', 'gram', 'gram_prime', 'guandao', 'guandao_prime', 'gunsen', 'halikar', 'halikar_wraith', 'hate', 'heat_dagger', 'heat_sword', 'heliocor', 'hespar', 'hirudo', 'innodem', 'jat_kittag', 'jat_kusar', 'jaw_sword', 'kama', 'karyst', 'karyst_prime', 'keratinos', 'kesheg', 'kestrel', 'kogake', 'kogake_prime', 'korrudo', 'korumm', 'kreska', 'krohkur', 'kronen', 'kronen_prime', 'kronsh', 'kuva_shildeg', 'lacera', 'lecta', 'lesion', 'machete', 'machete_wraith', 'magistar', 'masseter', 'mewan', 'mios', 'mire', 'mk1-bo', 'mk1-furax', 'nami_skyla', 'nami_skyla_prime', 'nami_solo', 'nepheri', 'nikana', 'nikana_prime', 'ninkondi', 'ninkondi_prime', 'obex', 'ohma', 'okina', 'ooltha', 'orthos', 'orthos_prime', 'orvius', 'pangolin_prime', 'pangolin_sword', 'paracesis', 'pathocyst', 'pennant', 'plague_keewar', 'plague_kripath', 'plasma_sword', 'praedos', 'prisma_dual_cleavers', 'prisma_machete', 'prisma_obex', 'prisma_skana', 'prova', 'prova_vandal', 'pulmonars', 'pupacyst', 'quassus', 'rabvee', 'rakta_dark_dagger', 'reaper_prime', 'redeemer', 'redeemer_prime', 'ripkas', 'rumblejack', 'sampotes', 'sancti_magistar', 'sarofang', 'sarpa', 'scindo', 'scindo_prime', 'scoliac', 'secura_lecta', 'sepfahn', 'serro', 'shaku', 'sheev', 'sibear', 'sigma_&_octantis', 'silva_&_aegis', 'silva_&_aegis_prime', 'skana', 'skana_prime', 'skiajati', 'slaytra', 'stropha', 'sun_&_moon', 'syam', 'sydon', 'synoid_heliocor', 'tatsu', 'tatsu_prime', 'tekko', 'tekko_prime', 'telos_boltace', 'tenet_agendus', 'tenet_exec', 'tenet_grigori', 'tenet_livia', 'tipedo', 'tipedo_prime', 'tonbo', 'twin_basolk', 'twin_krohkur', 'vastilok', 'vaykor_sydon', 'venato', 'venka', 'venka_prime', 'verdilac', 'vericres', 'vitrica', 'volnus', 'volnus_prime', 'war', 'wolf_sledge', 'xoris', 'zenistar' } )
ignore_archguns = True
archguns = { 'cortege', 'corvas', 'cyngas', 'dual decurions', 'fluctus', 'grattler', 'imperator', 'kuva ayanga', 'larkspur', 'mausolon', 'morgha', 'phaedra', 'velocitus' }
ignore_companion_weapons = True
companion_weapons = { 'akaten', 'artax', 'batoten', 'burst laser', 'cryotra', 'deconstructor', 'deth machine rifle', 'helstrum', 'lacerten', 'laser rifle', 'multron', 'stinger', 'sweeper', 'tazicor', 'verglas', 'vulklok' }
desired_positives = ( 'critical_chance', 'critical_damage' )
good_positives = ( 'critical_damage', 'critical_chance', 'multishot', 'toxin_damage', 'heat_damage' )
bad_positives = ( 'zoom', 'projectile_speed', 'ammo_maximum', 'damage_vs_infested', 'damage_vs_corpus', 'damage_vs_grineer', 'impact_damage', 'puncture_damage', 'slash_damage', 'punch_through', r'fire_rate_/_attack_speed', 'status_duration', 'status_chance', 'recoil', 'magazine_capacity', 'reload_speed' )
good_negatives = ( 'zoom', 'projectile_speed', 'ammo_maximum', 'damage_vs_infested', 'damage_vs_corpus', 'impact_damage', 'puncture_damage', 'slash_damage' )
url = r'https://api.warframe.market/v1/auctions/search?type=riven&buyout_policy=direct&positive_stats=' + desired_positives[0] + r'%2C' + desired_positives[1] + ( r'&polarity=madurai' if restrict_to_madurai else '' ) + r'&sort_by=price_asc'

auction_data = json.loads( requests.get( url ).text )

noteworthy_auctions = []
for auction in auction_data['payload']['auctions']:
    if auction['owner']['status'] == 'offline': continue
    price = auction['buyout_price']
    if price > cutoff_price: continue
    weapon_name = auction['item']['weapon_url_name']
    if ignore_melees            and weapon_name in melee_weapons    : continue
    if ignore_archguns          and weapon_name in archguns         : continue
    if ignore_companion_weapons and weapon_name in companion_weapons: continue
    p1, p2, p3, n1 = ( 'none', 'none', 'none', 'none' )
    for idx, att in enumerate( auction['item']['attributes'] ):
        if   idx == 0:
            p1 = att['url_name']
        elif idx == 1:
            p2 = att['url_name']
        elif idx == 2 and att['positive']:
            p3 = att['url_name']
        else:
            n1 = att['url_name']
    positives = ( p1, p2 ) + ( ( p3, ) if p3 != 'none' else tuple() )
    negative = n1 if n1 != 'none' else False
    bad_riven = False
    for att in positives:
        if att not in good_positives: bad_riven = True; break
    if bad_riven: continue
    if negative:
        if negative not in good_negatives: bad_riven = True
    if bad_riven: continue
    attributes = '\tPositive Attributes: ' + ', '.join( capitalize_name( att ) for att in positives ) + ( ( '\n\tNegative Attributes: ' + capitalize_name( n1 ) ) if n1 else '' )
    riven_name = f"{ ' '.join( tuple( word.capitalize() for word in weapon_name.split('_') ) ).replace(' And ',' and ') } { auction['item']['name'].capitalize() }"
    seller_ign = auction['owner']['ingame_name']
    dm = f'\tDirect Message: /w { seller_ign } Hi. I would like to buy your { riven_name } riven mod for { price }:platinum:.'
    noteworthy_auctions.append( f'\tPrice: { price }\n\tWeapon: { capitalize_name( weapon_name ) }\n{ attributes }\n{ dm }' )
if len( noteworthy_auctions ):
    noteworthy_auctions.sort( key = lambda x: int( x.split('\n',1)[0].split(' ',1)[1] ) )
    print( 'The following noteworthy auctions have been found:\n\n' + '\n\n'.join( noteworthy_auctions ) )
else:
    print( 'No auctions of note have been found.' )