import re
text = """
¶1 dra: mu:l hut zəkh gəkhuləmt rándolf kartərn di vindərləkhə shtut, in dra: mu:l iz er avékgəkhàpt gəvurn bəshas er iz nokh gəblibm shtayn of dər hoykhər terásə ibər ir. gants guldn in libləkh hut zi gəsarfənt in dər shkiə, mit moyərn, bòtay-mikdú:shəm, kòlonádəs, in gəboygənə brikn fin gəudərtn mírmlshtayn, fontánən mit zilbərnə basáynən fin prìzmátishə shpritsn in bərákhvəsdikə pletsər in pàrfumírtə gertnər, in braytə gasn vus marshírn tsvishn tsartə baymər in kvàyt-balúdənə urnəs in hélfandbàynərnə státuəs in shtrálndikə rayən; bəshas of shtútsikə ikúsn of tsofn hubm zəkh gədrapət ráyənshikhtn fin roytə dekhər in altə farshpítstə dákhshpitsn vus baháltn klaynə shtegləkh fin grúzikə bríkshtaynər. siz gəveyn ə fibər fin di getər; ə tri:ə fin hímlishə trimáytn in ə trask fin ímshtàrbikə tatsn. mistéryə iz arímgəhùngən arím ir vi khmarəs arím ə fàntástishn ìmbazíkhtn bark; in bays kartər iz gəshtanən un utəm in fil mit vártink kíkndik ibər yenəm balùstradírtn pàrapét, hut tsi im ó:fgəshvebt di rírndikà:t in shpánink fin ə kimàt-farshvíndənəm zaykhər, dər váytik fin farlóyrənə zakhn, in dus ó:frègndikə bàdérfənish tsi gəfinən an urt inəm zəku:rn far vus hut ə mu:l gəhat ə gəváldikn in bərìmoy-shel-óylamdikn farném.
¶2 er hut gəvist az far im iz ir batá:t ə mu:l gəveyn of zikhər dər hekhstər; khotsh in velkhn tsikl udər gilgəl hut er zi gəkent, udər tsi in khuləm tsi vakh, hut er nisht gəkent dərkenən. ímklur hut zi ó:fgərifn á:nblikn fin ə va:tər fargésənər ershtər yigənt, ven vindər in hanúə zenən gəlign in dər gantsər mistéryə fin teyk, in kayú:r in farnákht hubm dest gla:khn aró:sgəshpànt nəvíish tsim ná:gərikn klank fin litnyəs in gəzank; féə-toyərn vus zay farmákhn zəkh nisht tsi vá:tərdikə in fàrkhídəshndikə múfsim. ubər yedə nakht bays er iz gəshtanən of yenər hoykhər mirmlənər terásə mit di tshikávə urnəs in dər ó:sgəshnitstər paréntshə, in avékgəkìkt ibər yenər á:ngəshtiltər shkíə-shtut fin sháynka:t in ímèrdishər ìmanénts, hut er gəfilt dem tsvank fin di tìránishə getər fin khuləm; va:l bəshím-oyfm hut er nisht gəkent avék fin yenəm dərhoybm urt, udər aróp di braytə mirmlənə trep anídərgəvùrfm únsòyfik aróp tsim urt vi yenə gasn fin eltərn kishəf zenən gəlign ó:sgəshprayt in tsi im gəvinkn.
¶3 ven dus dritə mu:l hut er zəkh ó:fgəvekt mit yenə gurns nokh nisht arópgəgàngən in yenə á:ngəshtiltə shkíə-gasn nokh nisht adórəkhgəgàngən, hut er lank in erntst tfilə gətun di farbúrgənə getər fin khuləm vus dimən kapríznə ibər di khmarəs of ìmbakánt kádas inəm kaltn vístənish vi kayn mentsh tret nisht. ubər di getər hubm nisht gəshikt kayn entfər in nisht gəvizn kayn óplus, in zay hubm nisht gəgeybm kayn simn az zay hubm im nóysə-khayn gəveyn ven er hut zay mispáləl gəveyn in khuləm, in zəkh gəvundn tsi zay mit kurbúnəs dorəkh di babérdltə pristərs nasht in káman-tàn, veməns hayl-háykhl mit za:n flámənza:l ligt nisht tsi va:t fin di toyərn fin dər vakhər velt. əs hut zəkh níshmer gədakht az mə hut mistámə ímgìntsik gəhert za:nə tfiləs, va:l afílə nokh dər ershtər fin zay hut er kayn mu:l nisht dərzeyn di vindərləkhə shtut; eləháy di dra: á:nblikn fin dər va:tns zenən gəveyn stam tuəsn udər farzéyns, in əgeygn epəs ə farbúrgənəm plan udər vélənish fin di getər.
¶4 sof-kl-sóf hut kartər, shlaf mit bénkənish far yenə glímtsərndikə shkíə-gasn in kríptishə bark-shtáygn tsvishn fàrtsá:tikə bakákhltə dekhər, in nisht bikhóyləs sa: shlófndik sa: vakh zay avéktsitrà:bm fin za:nə gədankən, úngənimən ə hakhlótə tsi gayn mit draystə takhnínəm vìahín kayn mentsh iz friər nisht gəgangən, in zəkh dərveygn adórəkhtsigàyn dorəkh di á:zikə midbúryəs dorəkhn fíntstərnish tsim urt vi kádas dus ìmbakántə, farshláyərt in khmarəs in bakráynt mit shtern vus zay ken mən zəkh nisht fórshteln, halt bəsóydik in bà:nákhtik dem óniksənəm shlus fin di groysə.
¶5 in la:khtn dreml iz er arópgəgàngən di zíbətsik trepləkh tsi dər flámənhayl in hut gəshmiəst mikóyəkh dem dúzikn plan mit di babérdltə pristərs nasht in káman-tàn. in di pristərs hubm gəshuklt di pskhènt-trúgndikə kep in ə naydər gətin az svult za:n dər toyt fin dər nəshumə za:nər. zay hubm im íbərgəgeybm az di groysə hubm shoyn bavízn zayər rotsn, in az siz nisht zay nikhə az mən zul zay bàléstikn mit tsìshtáyikə takhnínəm. zay hubm im oykh dərmunt az nisht nur iz kayn mentsh kayn mu:l nisht gəveyn in kádas dem ìmbakántn, nur oykh hut kayn mentsh kayn mu:l nisht khoyshəd gəveyn in velkhn tayl fin khaləl ken əs lign; tsi əs iz in di khúləm-lendər arím indzər velt, tsi in yenə vus ringlən arím an imgərékhəntn bagláytər fin fómalhàut udər àldəbarán. oyb in indzər khúləm-lant, ken mən əs megləkh dərgraykhn; ubər nur dra: far fil mentshləkhə nəshuməs zint tsa:t hut zəkh úngəhoybm zenən ə mu:l aríbər in tsirík di shvartsə gútlùzikə ópgrintn kayn andərə khúləm-lendər, in fin yenə dra: zenən tsvay tsiríkgəkìmən gants məshigə. sə zenən gəveyn in azélkhə nəsiəs úrtikə sakúnəs un ə shi:ər; dərtsi nokh yenə ó:ftràysləndikə sòf-sakúnə vus zi bebət nisht-gədákht mikhíts dem kəsáydərdikn véltal, vìahín dərgraykhn nisht kayn khalóyməs; yenər letstər àmórfishər farfál fin dər samə nídrikstər bəhulə vus zi lestərt in bilblt ba:m tsentər finəm gantsn áyn-sof—dər ímgvìlikər dèmon-súltan àzatós, vus dem numən za:nəm dərveygn zəkh nisht kayn leftsn tsi redn bəkúl-roym, in vus er grizhət híngərik in ìmbanémləkhə, ìmbalóykhtənə kamərn mikhíts dər tsa:t in mitn fardíshətn ó:frègndikn klapm fin nívzədikə poykn in dem dinəm, mònotónishn pkhik fin farshúltənə flaytn tsi velkhn paskídnə klapm in fa:fm tantsn paméləkh, imgəlímpərt, in àbzúrdish di samə hekhstə imgəháyərə getər, di blində, shtímluzə, khóyshəkhdikə in sáykhlluzə andərə getər vus zayər nəshumə in shtafét iz dər kríkhndikər kháos nyàrlasótep.
¶6 fin di dúzikə zakhn iz kartər gəvurnt gəvurn fin di pristərs nasht in káman-tàn in dər flámənhayl, ubər fíndəstveygn hut er úngənimən ə hakhlótə tsi gəfinən di getər of ìmbakánt kádas inəm kaltn vístənish, vi əs zul nisht za:n, in tsi bakímən fin zay dus bilt in zaykhər in miklət fin dər vindərləkhər shkíə-shtut. er hut gəvist az za:n nəsiə vult za:n ó:stərlish in lank, in az di groysə vultn za:n əgeygn ir; ubər zá:əndik alt inəm lant fin khalóyməs hut er zəkh farlúzt of ə sakh nitsləkhə zikhróynəs in takhbíləs zəkh tsi helfn. iz, béytndik ə gəzèygninks-brú:khə fin di pristərs in pìkáykhish íbərklèrndik veygn za:n veyk, iz er arópgəgàngən ə draystər di zibn hindərt trep tsim toyər fin tifərn dreml, in zəkh gəluzt in veyk ará:n dorəkhn fàrkíshiftn valt.
¶7 in di tunéln fin yenəm fardráytn valt, vus za:nə nídrikə gìgántishə dembm farvíkln mátsndikə tsva:gn in glantsn fíntstərha:t mit dər fòsforəstsénts fin ó:stərlishə shvéml-gəviksn, voynən di zugn di gànáyvishə in sóydəsdikə; vus vaysn ə sakh farnépltə soydəs fin dər khúləm-velt in ə pur fin dər vakhər velt, va:l dər valt in tsvay ertər rirt di méntshnlendər, khotsh sə vult za:n an ímglik tsi zugn vi. gəvisə imdərklértə shmiəs, gəshéənishn, in fàrshvíndingən pasírn tsvishn mentshn vi di zugn hubm ə tsítrit, in siz git az zay kenən nisht vandərn va:t mikhítsn lant fin khalóyməs. ubər ibər di neəntərə tayln fin dər khúləm-velt bavégn zay zəkh fra:, arímflàtərndik ahín in ahér klayn in broyn in imgəzéyn, in tsiríktrùgndik pikántə ma:nsəs kəday fàrkíshift tsi farbréngən di shuən arím zayərə háymfa:ərn inəm valt vus zay hubm im lip. sruv fin zay voynən in nurəs, ubər ə tayl bavóynən di shtamən fin di groysə baymər; in khotsh zay nern zəkh sruv mit shvéml-gəviksn, mirmlt mən az zay hubm oykh ə gistl far flaysh, tsi gàshmíəsdik tsi rìkhníəsdik, va:l of zikhər zenən ə sakh bàlay-khalóyməs ará:ngəkìmən in yenəm valt ará:n in zenən nisht aró:s. kartər hut níshmer nisht moyrə gəhat, va:l er iz gəveyn an altər bàl-khalóyməs in hut zəkh ó:sgəlernt zayərə flátərndikə shprakh in gəshlusn ə sakh ópmakhn mit zay; nokh gəfinən mit zayər hilf di prákhtfilə shtut kèləfáis in ùs-nárgay hintər di tànaryánər berk, vi sə hersht dus halbə yur dər groysər kínik kuránəs, ə mentsh vemən er hut im gəkent intər an andər numən inəm lebm. kuránəs iz gəveyn di áyntsikə nəshumə vus iz gəfurn in di shtèrn-ópgrintn ará:n in tsiríkgəkìmən rayn fin shigóyən.
¶8 zəkh adórəkhshlènglndik itst dorəkh di nídrikə fòsforəstséntə dórəkhgangən tsvishn yenə rízikə shtamən, hut kartər gəmakht flátərndikə klangən inəm shtaygər fin di zugn, in zəkh alə vaylə tsígəhert tsi sə vultn za:n óprufm. er hut gədenkt epəs ə durf fin di bàshéfənishn noənt tsim tsentər valt, vi sə dərtsaylt veygn eltərə in nokh shoyn lank fargésənə gróylikə á:nvoynərs ə kra:z groysə mókhikə shtaynər vus iz ə mu:l gəveyn ə polyánə; in tsi dem dúzikn plats hut er zəkh tsígəa:lt. er hut núkhgəshpirt za:n veyk mit di grotéskə shvéml-gəviksn, vus hubm shténdik ó:sgəzeyn alts besər gənert, vus neəntər mən kimt tsim məùyámdikn kra:z vi eltərə yayshn hubm gətantst in makrəv gəveyn kurbúnəs. sof-kl-sóf hut dus gresərə likht fin yenə gədikhtərə shvéml-gəviksn o:fgədəkt ə bayzə grinə in gruə imgəháyərikà:t vus shtoyst zəkh aró:f dorəkhn váld-dakh mikhítsn óygngraykh. siz gəveyn dər noəntstər finəm groysn rink shtaynər, in kartər hut gəvist az er iz gəveyn noənt tsin zúg-durf. baná:ət za:n flátərndikn klank, hut er gədúldik gəvart; in er iz mit dər tsa:t balóynt gəvurn mit an á:ndrik fin ə sakh oygn vus zay bakíkn im. sə zenən gəveyn di zugn, va:l mə zet zayərə məshí:nədikə oygn lank aydər mən ken dərzeyn zayərə klaynə fífikə broynə kontúrn.
¶9 aró:s hubm zay gəgimzhət fin fartá:ətə norəs in stélnikə-bàymər biz di gantsə kòym-balóykhtənə gegənt hut mit zay gəshviblt in gəgriblt. etləkhə fin di vildərə hubm zəkh imá:ngənəm fartshépət in kartərn in aynər hut im afílə ə knip hadkə inəm oyər gətin; ubər balt hubm zayərə eltərə á:ngətsamt ut di héfkərdikə nəshuməs. dər khakhúməm-rùt, dərkénəndik dem gast, hut úngəbutn ə kérbis gəyoyrtn suk fin ə farsháydəvətn boym nisht vi di andərə, vus iz ó:sgəvaksn fin ə zoymən vus emətsər of dər ləvunə hut arópgəvùrfm; in bays kartər hut im gətrinkn mit tsərəmonyə hut zəkh úngəhoybm ə gur ó:stərlishər dórəkhshmiəs. di zugn hubm, tsim badóyərn, nisht gəvist vi ligt di shpits kádas, in zay hubm nisht gəkent afílə zugn tsi dus kaltə vístənish iz in indzər khúləm-velt tsi in an andər. shmiəs veygn di groysə zenən gəkimən in gla:khər mus fin alə ríkhtingən; in mə hut nur gəkent zugn az mən vult zay gikhər zeyn of hoykhə bárgshpitsn aydər in telər, va:l of azélkhə shpitsn tantsn zay mit bénkənish ven di ləvunə shtayt fin oybm in di vulkns dərintər.
¶10 iz aynər ə zayər bayúrtər zug hut dərmunt ə zakh vus di andərə hubm nisht gəhert fin ir, in hut gəzukt az in últar, hintərn ta:kh skay, iz nokh farblíbm dər letstər èkzemplár fin yenə ìmbanémləkhə altə pnakótər ksav-yádn gəmakht fin vakhə mentshn in fargésənə tsófndikə malkhísn in ará:ngətrùgn inəm lant fin khalóyməs ven di húrikə kànibálishə gnofkəs zenən báygəkimən òlasóə, mit ir sakh bòtay-mikdóshəm, in gətayt alə gibóyrəm finəm lant lómar. yenə ksav-yádn, hut er gəzukt, hubm dərtsaylt ə sakh veygn di getər, in akhíts dem, zenən mentshn gəveyn in últar vus hubm gəzeyn di simúnəm fin di getər, in afílə an altər pristər aynər vus hut aró:fgəklètərt of ə groysn bark kəday zay tsi dərzeyn bays zay tantsn in dər ləvúnə-sha:n. er iz dórəkhgəfaln, khotsh za:n bagláytər iz matslíəkh gəveyn in iz númənluz ímgəkimən.
¶11 iz rándolf kartər hut gədankt di zugn, vus hubm bəshúləmdik gəflatərt in im gəgeybm nokh ə kérbis va:n mìttsinémən mit zəkh, in zəkh gəluzt in veyk ará:n dorəkhn fòsforəstséntn valt tsi dər andərər za:t, vi əs flist aróp dər víkhərndikər skay fin di ikúsn fin leríən, in háseg in nir in últar bashprénklən dem playn. hintər im, gànáyvish in imgəzáyn, zenən gəkrokhn ə pur fin di ná:gərikə zugn, va:l zay hubm khayshək gəhat zəkh tsi dərvisn vus zul pasírn mit im, in tsirìktsitrúgn di legéndə tsi zayər fulk. di imgəháyərə dembm hubm zəkh fàrgədíkhtikt bays er hut zəkh íntərgəshtipt va:tər finəm durf, in er hut sharf arímgəkìkt far ə gəvisn plats vi zay vultn epəs shitərər vern, shtáyəndik gur toyt udər góysəsdik tsvishn di ìmnatírləkh gədikhtə shvéml-gəviksn in dem fóylndikn shiml in mashəvátə kletsər fin zayərə gəfalənə bridər durt vult er zəkh sharf ópgəkert in ə za:t, mákhmas dem az ba: yenəm urt likt ə mákhtikə shtaynərnə táfliə of dər válddil; in di vus hubm zəkh dərvekt tsìtsigáyn tsi ir zugn az zi trukt an a:zərnəm ring dra: fis di brayt. zəkh dərmunt inəm àrkháishn kra:z fin groysə mókhikə shtaynər, in far vus er iz efshər ó:fgəshtelt gəvurn, shteln di zugn zəkh nisht op lebm yenər braytər táfliə mit ir rízədikn ring, va:l zay khapm zəkh az alts vus iz fargésn miz lav-dáfkə toyt za:n, in zay vultn nisht gəvult zen di táfliə zəkh ó:fhaybm pàvú:liə in bazákht.
"""
def analyze_accents():
    # Mapping accented vowels to their plain counterparts for correction formatting
    vowel_unaccent_map = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'à': 'a', 'è': 'e', 'ì': 'i', 'ò': 'o', 'ù': 'u',
        'a': 'a', 'e': 'e', 'i': 'i', 'o': 'o', 'u': 'u'
    }
    
    acute_accents = set("áéíóú")
    grave_accents = set("àèìòù")
    
    rules_text = {
        1: "Rule 1: A word with one vowel does not have accents on the vowel.",
        2: "Rule 2: A word with two vowels has accents on one vowel.",
        3: "Rule 3: A word with three or more vowels has an acute accent on one vowel and a grave on another."
    }
    
    # Tracking violations by rule to group and order
    violations = {1: [], 2: [], 3: []}
    
    paragraphs = text.strip().split('¶')
    
    # Regex designed to match fully connected words containing valid letters, accents, schwas, colons, and hyphens.
    word_pattern = re.compile(r'[a-zA-Záéíóúàèìòùə:\-]+')
    
    for p in paragraphs:
        if not p.strip():
            continue
            
        section_match = re.match(r'^(\d+)', p.strip())
        if not section_match:
            continue
            
        section_num = f"¶{section_match.group(1)}"
        words = word_pattern.findall(p)
        
        for word in words:
            # Extract just the targeted vowels (schwa `ə` is ignored per the rules)
            vowels_in_word = [char.lower() for char in word if char.lower() in vowel_unaccent_map]
            num_v = len(vowels_in_word)
            
            if num_v == 0:
                continue
                
            num_acute = sum(1 for v in vowels_in_word if v in acute_accents)
            num_grave = sum(1 for v in vowels_in_word if v in grave_accents)
            
            # Check Rule 1: One vowel = 0 accents
            if num_v == 1:
                if num_acute + num_grave > 0:
                    corrected = "".join(vowel_unaccent_map.get(c.lower(), c) if c.lower() in vowel_unaccent_map else c for c in word)
                    violations[1].append((section_num, word, corrected))
                    
            # Check Rule 2: Two vowels = exactly 1 accent
            elif num_v == 2:
                if num_acute + num_grave != 1:
                    # Correction cannot be unambiguously determined for 0 or >1 accents
                    violations[2].append((section_num, word, ""))
                    
            # Check Rule 3: Three or more vowels = exactly 1 acute AND exactly 1 grave
            else:
                if num_acute != 1 or num_grave != 1:
                    # Correction cannot be unambiguously determined 
                    violations[3].append((section_num, word, ""))
                    
    # Output Results
    for rule_num in [1, 2, 3]:
        if violations[rule_num]:
            print(f"\n--- Violations for {rules_text[rule_num]} ---")
            print(f"{'Section':<8} | {'Word':<25} | {'Correct Form':<25}")
            print("-" * 65)
            for sec, word, corr in violations[rule_num]:
                print(f"{sec:<8} | {word:<25} | {corr:<25}")
if __name__ == "__main__":
    analyze_accents()