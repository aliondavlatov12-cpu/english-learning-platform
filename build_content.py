import json,os
ROOT=os.path.join(os.path.dirname(__file__),'..','app','content'); os.makedirs(ROOT,exist_ok=True)
levels={
'A0':('Starter','Оғози аввал','Начальный',['be: am/is/are','subject pronouns','this/that','have got','there is/are','present simple','can/can’t','question words','prepositions','countable nouns','present continuous','review']),
'A1':('Beginner','Оғозкунанда','Начальный',['present simple','be vs do','possessives','frequency adverbs','present continuous','past simple','some/any','comparatives','going to','must/have to','will','review']),
'A2':('Elementary','Ибтидоӣ','Элементарный',['present perfect','past continuous','used to','future forms','first conditional','advice modals','gerunds/infinitives','passive basics','reported speech','relative clauses','second conditional','review']),
'B1':('Pre-Intermediate','Пешмиёна','Средний ниже',['present perfect vs past','past perfect','future continuous','conditionals','probability modals','passive voice','reported speech','relative clauses','gerunds/infinitives','linkers','phrasal verbs','review']),
'B2':('Intermediate','Миёна','Средний',['tense contrast','mixed conditionals','inversion','modal perfects','passive reporting','cleft sentences','participles','noun clauses','advanced relatives','hedging','discourse markers','review']),
'C1':('Upper-Intermediate','Боломиёна','Выше среднего',['complex tense nuance','advanced conditionals','inversion for emphasis','modal nuance','nominalisation','passive reporting','subordination','ellipsis','clefting','hedging','register','review']),
'C2':('Advanced','Пешрафта','Продвинутый',['aspect and stance','complex modality','rhetorical inversion','information structure','dense nominalisation','advanced reporting','ellipsis and substitution','pragmatic conditionals','lexical grammar','cohesion','register','review'])}
themes=['Identity & Introductions','Family & Relationships','Time, Numbers & Routines','Home & Neighbourhood','Food & Healthy Living','Study & Learning','Work & Goals','Travel & Directions','Health & Wellbeing','Shopping & Money','Technology & Media','Culture & Future']
wordbanks={
'A0':[('name','/neɪm/','ном','имя'),('friend','/frend/','дӯст','друг'),('family','/ˈfæm.əl.i/','оила','семья'),('home','/həʊm/','хона','дом'),('food','/fuːd/','хӯрок','еда'),('water','/ˈwɔː.tər/','об','вода'),('school','/skuːl/','мактаб','школа'),('city','/ˈsɪt.i/','шаҳр','город'),('shop','/ʃɒp/','мағоза','магазин'),('weather','/ˈweð.ər/','обу ҳаво','погода'),('music','/ˈmjuː.zɪk/','мусиқӣ','музыка'),('happy','/ˈhæp.i/','хушҳол','счастливый')],
'A1':[('arrive','/əˈraɪv/','расидан','прибывать'),('usually','/ˈjuː.ʒu.ə.li/','одатан','обычно'),('careful','/ˈkeə.fəl/','эҳтиёткор','осторожный'),('healthy','/ˈhel.θi/','солим','здоровый'),('journey','/ˈdʒɜː.ni/','сафар','путешествие'),('ticket','/ˈtɪk.ɪt/','чипта','билет'),('market','/ˈmɑː.kɪt/','бозор','рынок'),('practice','/ˈpræk.tɪs/','машқ','практика'),('decide','/dɪˈsaɪd/','қарор кардан','решать'),('plan','/plæn/','нақша','план'),('enough','/ɪˈnʌf/','кофӣ','достаточно'),('message','/ˈmes.ɪdʒ/','паём','сообщение')],
'A2':[('experience','/ɪkˈspɪə.ri.əns/','таҷриба','опыт'),('improve','/ɪmˈpruːv/','беҳтар кардан','улучшать'),('although','/ɔːlˈðəʊ/','гарчанде','хотя'),('environment','/ɪnˈvaɪ.rən.mənt/','муҳити зист','окружающая среда'),('decision','/dɪˈsɪʒ.ən/','қарор','решение'),('opportunity','/ˌɒp.əˈtʃuː.nə.ti/','имконият','возможность'),('relationship','/rɪˈleɪ.ʃən.ʃɪp/','муносибат','отношение'),('technology','/tekˈnɒl.ə.dʒi/','технология','технология'),('advice','/ədˈvaɪs/','маслиҳат','совет'),('future','/ˈfjuː.tʃər/','оянда','будущее'),('choice','/tʃɔɪs/','интихоб','выбор'),('result','/rɪˈzʌlt/','натиҷа','результат')],
'B1':[('achievement','/əˈtʃiːv.mənt/','дастовард','достижение'),('challenge','/ˈtʃæl.ɪndʒ/','мушкилӣ','вызов'),('reliable','/rɪˈlaɪ.ə.bəl/','боэътимод','надёжный'),('research','/rɪˈsɜːtʃ/','таҳқиқот','исследование'),('career','/kəˈrɪər/','касб','карьера'),('impact','/ˈɪm.pækt/','таъсир','влияние'),('solution','/səˈluː.ʃən/','ҳал','решение'),('benefit','/ˈben.ɪ.fɪt/','фоида','польза'),('evidence','/ˈev.ɪ.dəns/','далел','доказательство'),('approach','/əˈprəʊtʃ/','равиш','подход'),('responsibility','/rɪˌspɒn.səˈbɪl.ə.ti/','масъулият','ответственность'),('confident','/ˈkɒn.fɪ.dənt/','боэътимод ба худ','уверенный')],
'B2':[('perspective','/pəˈspek.tɪv/','дидгоҳ','перспектива'),('consequence','/ˈkɒn.sɪ.kwəns/','оқибат','последствие'),('significant','/sɪɡˈnɪf.ɪ.kənt/','муҳим','значительный'),('sustainable','/səˈsteɪ.nə.bəl/','устувор','устойчивый'),('assumption','/əˈsʌmp.ʃən/','тахмин','предположение'),('controversial','/ˌkɒn.trəˈvɜː.ʃəl/','баҳсбарангез','спорный'),('justify','/ˈdʒʌs.tɪ.faɪ/','асоснок кардан','обосновывать'),('distinguish','/dɪˈstɪŋ.ɡwɪʃ/','фарқ кардан','различать'),('framework','/ˈfreɪm.wɜːk/','чаҳорчӯба','структура'),('allocate','/ˈæl.ə.keɪt/','тақсим кардан','распределять'),('coherent','/kəʊˈhɪə.rənt/','мантиқӣ','связный'),('bias','/ˈbaɪ.əs/','ғараз','предвзятость')],
'C1':[('subtle','/ˈsʌt.əl/','нозук','тонкий'),('ambiguity','/ˌæm.bɪˈɡjuː.ə.ti/','дуқутбӣ будан','двусмысленность'),('implement','/ˈɪm.plɪ.ment/','амалӣ кардан','внедрять'),('compelling','/kəmˈpel.ɪŋ/','боварибахш','убедительный'),('constraint','/kənˈstreɪnt/','маҳдудият','ограничение'),('contemporary','/kənˈtem.pər.ər.i/','муосир','современный'),('critique','/krɪˈtiːk/','танқиди таҳлилӣ','критика'),('infer','/ɪnˈfɜːr/','хулоса баровардан','делать вывод'),('precise','/prɪˈsaɪs/','дақиқ','точный'),('ethical','/ˈeθ.ɪ.kəl/','ахлоқӣ','этический'),('nuance','/ˈnjuː.ɑːns/','нозукии маъно','оттенок'),('credible','/ˈkred.ə.bəl/','эътимодбахш','достоверный')],
'C2':[('epistemic','/ˌep.ɪˈstiː.mɪk/','марбут ба дараҷаи дониш','эпистемический'),('pragmatic','/præɡˈmæt.ɪk/','амалӣ','прагматический'),('concession','/kənˈseʃ.ən/','эътирофи нуқтаи муқобил','уступка'),('rhetoric','/ˈret.ər.ɪk/','санъати сухан','риторика'),('salient','/ˈseɪ.li.ənt/','муҳимтарин','наиболее заметный'),('corroborate','/kəˈrɒb.ə.reɪt/','тасдиқ кардан','подтверждать'),('mitigate','/ˈmɪt.ɪ.ɡeɪt/','коҳиш додан','смягчать'),('premise','/ˈprem.ɪs/','пешфарз/асоси далел','предпосылка'),('discourse','/ˈdɪs.kɔːs/','гуфтор/дискурс','дискурс'),('register','/ˈredʒ.ɪ.stər/','сатҳи услуб','регистр'),('constrain','/kənˈstreɪn/','маҳдуд кардан','ограничивать'),('synthesize','/ˈsɪn.θə.saɪz/','якҷо таҳлил кардан','синтезировать')]
}
def grammar_items(g):
    m={
    'be: am/is/are':('I ___ a student.',['am','is','are','be'],0,'Use am with I.'),
    'subject pronouns':('___ are my friends.',['They','Them','Their','Theirs'],0,'They is the subject pronoun.'),
    'this/that':('___ is my phone here in my hand.',['This','Those','These','They'],0,'This is used for one nearby thing.'),
    'have got':('She ___ got a new book.',['has','have','having','had'],0,'She takes has.'),
    'there is/are':('___ two chairs in the room.',['There are','There is','They are','It is'],0,'Plural chairs take there are.'),
    'present simple':('He ___ English every day.',['studies','study','studying','studied'],0,'Third-person singular takes -s/-ies.'),
    'can/can’t':('I ___ swim, but I cannot drive.',['can','am','have','do'],0,'Can expresses ability.'),
    'question words':('___ do you live?',['Where','Who','Why','When'],0,'Where asks about place.'),
    'prepositions':('The book is ___ the table.',['on','at','to','from'],0,'On is used for a surface.'),
    'countable nouns':('I have two ___.',['books','book','water','rice'],0,'Books is the plural countable noun.'),
    'present continuous':('They ___ dinner now.',['are eating','eat','eats','ate'],0,'Present continuous uses be + -ing.'),
    'present simple':('My brother ___ at six every morning.',['gets up','get up','is getting up','got up'],0,'Habitual actions use present simple.'),
    'be vs do':('___ you like coffee?',['Do','Are','Is','Be'],0,'Do forms present simple questions with like.'),
    'possessives':('This is ___ car.',['my','me','I','mine'],0,'My comes before a noun.'),
    'frequency adverbs':('I ___ walk to school.',['usually','yesterday','now','tomorrow'],0,'Usually expresses frequency.'),
    'past simple':('We ___ the museum yesterday.',['visited','visit','visiting','have visit'],0,'Yesterday signals past simple.'),
    'some/any':('There aren’t ___ apples left.',['any','some','much','a'],0,'Any is common in negatives.'),
    'comparatives':('This book is ___ than that one.',['more interesting','most interesting','interesting','interest'],0,'Comparative form follows than.'),
    'going to':('Look at those clouds. It ___ rain.',['is going to','will to','going','is'],0,'Going to can express a clear prediction from evidence.'),
    'must/have to':('You ___ wear a seat belt; it is required by law.',['have to','might','could','would'],0,'Have to expresses external obligation.'),
    'will':("I think she ___ arrive soon.",['will','is','has','did'],0,'Will is used for a prediction.'),
    'present perfect':('I ___ finished my homework.',['have','has','am','did'],0,'Present perfect uses have/has + past participle.'),
    'past continuous':('At 8 pm, I ___ TV.',['was watching','watched','am watching','have watched'],0,'Past continuous describes an action in progress at a past time.'),
    'used to':('I ___ play outside every day when I was a child.',['used to','use to','am used','would to'],0,'Used to describes a past habit.'),
    'future forms':('This time tomorrow, we ___ to Dushanbe.',['will be travelling','travelled','have travelled','travels'],0,'Future continuous fits an action in progress at a future time.'),
    'first conditional':('If it rains, we ___ at home.',['will stay','would stay','stayed','stay'],0,'First conditional uses present in the if-clause and will in the result.'),
    'advice modals':('You look tired. You ___ take a break.',['should','mustn’t','can’t','would'],0,'Should gives advice.'),
    'gerunds/infinitives':('I enjoy ___ English.',['learning','to learn','learn','learned'],0,'Enjoy is followed by a gerund.'),
    'passive basics':('The letters ___ every morning.',['are delivered','deliver','delivered','are delivering'],0,'Passive uses be + past participle.'),
    'reported speech':('She said that she ___ tired.',['was','is','be','has'],0,'Reported speech commonly backshifts is to was.'),
    'relative clauses':('The woman ___ lives next door is a doctor.',['who','where','when','what'],0,'Who refers to a person.'),
    'second conditional':('If I had more time, I ___ another language.',['would learn','will learn','learned','am learning'],0,'Second conditional uses would + base verb.'),
    'present perfect vs past':('I ___ Paris in 2022.',['visited','have visited','visit','am visiting'],0,'A finished time in 2022 takes past simple.'),
    'past perfect':('When we arrived, the film ___.',['had started','has started','starts','was start'],0,'Past perfect marks the earlier past event.'),
    'future continuous':('At 10 tomorrow, I ___ in a meeting.',['will be sitting','sit','sat','have sat'],0,'Future continuous fits an action in progress at a future time.'),
    'conditionals':('If she studied more, she ___ better results.',['would get','will get','gets','got'],0,'This is a second conditional pattern.'),
    'probability modals':('He isn’t answering. He ___ be asleep.',['might','mustn’t','wouldn’t','can’t to'],0,'Might expresses possibility.'),
    'passive voice':('The bridge ___ last year.',['was built','built','has build','was building'],0,'Passive past simple uses was/were + past participle.'),
    'linkers':('The task was difficult; ___, we finished it.',['however','because','unless','despite of'],0,'However links a contrast between clauses.'),
    'phrasal verbs':('Please ___ the form before Friday.',['fill in','fill at','fill to','fill on'],0,'Fill in means complete a form.'),
    'tense contrast':('She ___ here since 2020.',['has worked','worked','is working','had work'],0,'Since 2020 connects past to present.'),
    'mixed conditionals':('If I had taken the job, I ___ in London now.',['would be','will be','am','would have'],0,'Mixed conditional links past condition with present result.'),
    'inversion':('Rarely ___ such a clear result.',['do we see','we see','see we','we do see'],0,'Negative adverbial inversion uses auxiliary before subject.'),
    'modal perfects':('She isn’t here. She ___ have missed the train.',['may','should','mustn’t','can'],0,'May have expresses past possibility.'),
    'passive reporting':('The policy ___ to have reduced costs.',['is believed','believes','is believing','believed is'],0,'Passive reporting uses is believed + to-infinitive.'),
    'cleft sentences':('___ I need is a quiet room.',['What','Which','Who','Where'],0,'What-cleft highlights the thing needed.'),
    'participles':('___ by the evidence, the team changed its plan.',['Convinced','Convince','Convincing','Was convince'],0,'A participle clause can give the reason/state.'),
    'noun clauses':('We need to decide ___ the proposal is practical.',['whether','who','where','what'],0,'Whether introduces an embedded yes/no question.'),
    'advanced relatives':('The project, ___ results were impressive, won an award.',['whose','who','where','what'],0,'Whose shows possession in a relative clause.'),
    'hedging':('The result ___ suggest a small improvement.',['may','definitely must','cannot possibly','always'],0,'May is an appropriate hedge.'),
    'discourse markers':('The evidence is limited. ___, the pattern is interesting.',['Nevertheless','Because','Unless','Therefore of'],0,'Nevertheless marks contrast.'),
    'complex tense nuance':('By the time she arrived, we ___ for an hour.',['had been waiting','waited','have waited','are waiting'],0,'Past perfect continuous emphasizes duration before a past point.'),
    'advanced conditionals':('Had I known, I ___ differently.',['would have acted','will act','acted','would act'],0,'Inverted third conditional uses had + would have.'),
    'inversion for emphasis':('Not only ___ the cost high, but it is rising.',['is','it is','is it','it'],0,'Not only at the start triggers inversion.'),
    'modal nuance':('Given the evidence, she ___ be right.',['may','mustn’t','can’t','wouldn’t'],0,'May expresses a considered possibility.'),
    'nominalisation':('The committee ___ a decision yesterday.',['made','decisioned','making','has make'],0,'Made is the correct verb with the noun decision.'),
    'subordination':('___ the weather was poor, the event continued.',['Although','Because of','Despite','Unless'],0,'Although introduces a subordinate contrast clause.'),
    'ellipsis':('A: I can swim. B: So ___.',['can I','I can','am I','I am'],0,'So + auxiliary + subject forms agreement.'),
    'clefting':('___ was the timing that caused the problem.',['It','There','What','Which'],0,'It-cleft emphasizes the element after was.'),
    'register':('Which is most appropriate in a formal report?',['The results indicate a significant trend.','The results are kinda cool.','The results are super good.','The results rock.'],0,'Formal academic register uses precise neutral language.'),
    'aspect and stance':('The author ___ appears to assume that demand will rise.',['seems to','is definitely','must to','has to be'],0,'Seems to signals cautious stance.'),
    'complex modality':('The findings ___ have been affected by sampling bias.',['may','mustn’t','wouldn’t','cannot to'],0,'May have expresses a cautious past possibility.'),
    'rhetorical inversion':('Never ___ such a striking result before.',['have I seen','I have seen','seen I have','I seen have'],0,'Never at the start triggers inversion.'),
    'information structure':('It was the final paragraph ___ changed my view.',['that','who','where','what'],0,'It-cleft uses that for the focused thing.'),
    'dense nominalisation':('The rapid ___ of the policy created uncertainty.',['implementation','implement','implemented','implementing'],0,'Implementation is the noun form.'),
    'advanced reporting':('The study is reported ___ shown a consistent effect.',['to have','having to','to has','have'],0,'Reported + to have + participle is correct.'),
    'ellipsis and substitution':('I can finish it today, and she can ___.',['too','so','do','be'],0,'Too substitutes for agreement here.'),
    'pragmatic conditionals':('If you could send the file today, ___ be helpful.',['that would','that will','it is','there is'],0,'This conditional politely makes a request.'),
    'lexical grammar':('The evidence strongly ___ the conclusion.',['supports','supporting','support','has support'],0,'Evidence takes the singular verb supports.'),
    'cohesion':('The first study was small. ___, the second used a larger sample.',['By contrast','Because','Unless','Despite'],0,'By contrast creates a clear comparison.'),
    }
    if g in m:return [m[g]]
    return [(f'Which sentence uses {g} correctly?',[f'The researcher uses {g} accurately in context.','The researcher use no grammar in context.','Grammar are only for titles.','The sentence have no structure.'],0,'The first sentence is the only grammatically acceptable option.')]
for level,(name,tg,ru,grams) in levels.items():
 units=[]
 for ui,theme in enumerate(themes,1):
  lessons=[]
  for li in range(1,5):
   g=grams[ui-1]; title=f'{theme} — Lesson {li}'; words=[]
   bank=wordbanks[level]
   for j,(w,ipa,tt,rr) in enumerate(bank): words.append({'w':w,'ipa':ipa,'tg':tt,'ru':rr,'pos':'word','ex':f'The lesson uses the word {w} naturally in context.'})
   reading=f'This original {level} reading explores {theme.lower()}. Learners meet the target vocabulary in a practical context, identify the main idea, notice details, and connect the topic to their own lives. The lesson also revisits {g} through meaningful examples and short comprehension tasks.'
   listening=f'Listen to a short original dialogue about {theme.lower()}. Notice key vocabulary, the target grammar, and the speaker\'s main point. Then repeat two useful sentences aloud.'
   ex=[]
   for gq in grammar_items(g):
    q,opts,ans,why=gq; ex.append({'skill':'grammar','q':q,'options':opts,'answer':ans,'why':why})
   ex += [
    {'skill':'vocabulary','q':f'Which word best fits the theme {theme}?','options':[bank[0][0],'zzzzword','notaword','qwerty'],'answer':0,'why':f'{bank[0][0]} is a target word for this lesson.'},
    {'skill':'vocabulary','q':f'What is the Tajik meaning of {bank[1][0]}?','options':[bank[1][2],'машина','китоб','рӯз'],'answer':0,'why':f'{bank[1][0]} means {bank[1][2]}.'},
    {'skill':'reading','q':'What is the main purpose of the reading?','options':[f'To understand practical ideas about {theme.lower()}.','To memorise random numbers.','To study a different language.','To avoid the topic.'],'answer':0,'why':'The passage develops the unit theme.'},
    {'skill':'listening','q':'What should the learner listen for first?','options':['The main idea and key details','Every sound separately','Only the title','Nothing; listening is optional'],'answer':0,'why':'Listening for gist and details builds comprehension.'},
    {'skill':'use','q':'Which action best supports active learning?','options':['Use a target word in your own sentence','Copy without understanding','Skip practice','Memorise only the unit number'],'answer':0,'why':'Producing language helps consolidate learning.'},
    {'skill':'meaning','q':'What should you do after making a mistake?','options':['Read the feedback, correct it, and try again','Stop learning','Delete the lesson','Ignore the answer'],'answer':0,'why':'Correction and retry turn mistakes into learning.'},
    {'skill':'reading','q':'Which detail is supported by the passage?','options':[f'The theme is explored through practical language and examples.','The passage contains no English.','The topic is unrelated to the unit.','The text is only a list of numbers.'],'answer':0,'why':'The reading explicitly develops the unit theme.'}
   ]
   hw={'vocabulary':f'Write 5 original sentences using five target words from {theme}.','grammar':f'Write 5 sentences using {g}.','listening':'Listen to the lesson audio twice and write three key ideas you understood.','writing':f'Write 80–150 words about {theme}. Use at least four target words.','speaking':f'Speak for 60–90 seconds about {theme}; use the target grammar and vocabulary.'}
   lessons.append({'number':li,'title':title,'objective_tg':f'Пас аз ин дарс шумо метавонед дар бораи {theme.lower()} фикр ва маълумоти худро равшантар баён кунед ва {g}-ро истифода баред.','vocab':words,'grammar':{'title':g,'explain_en':f'{g} helps learners express meaning accurately in the context of {theme.lower()}. Study the examples, notice the form, and then produce your own sentences.','explain_tg':f'Ин қоида барои баёни маъно дар мавзӯи {theme.lower()} истифода мешавад. Мисолҳоро бинед, сохторро дарк кунед ва баъд ҷумлаҳои худро созед.','explain_ru':f'Эта грамматика помогает точно выражать смысл в теме {theme.lower()}. Изучите примеры и создайте собственные предложения.','rules':[f'Use the target form consistently: {g}.','Keep normal English word order in statements.','Check the verb form before submitting an answer.'],'examples':[{'en':f'I practise English through {theme.lower()}.','tg':f'Ман тавассути {theme.lower()} забони англисиро машқ мекунам.'},{'en':'I check my answer and try again.','tg':'Ман ҷавобамро месанҷам ва боз кӯшиш мекунам.'},{'en':'Clear examples make grammar easier.','tg':'Мисолҳои равшан грамматикаро осонтар мекунанд.'},{'en':'Practice turns knowledge into a skill.','tg':'Машқ донишро ба малака табдил медиҳад.'}]},'reading':{'title':f'Reading: {theme}','text':reading,'questions':[{'q':'What is the main idea?','options':['Practical understanding of the theme','Random facts','A different topic','No clear idea'],'answer':0},{'q':'What should the learner notice?','options':['Vocabulary and grammar in context','Only punctuation','Only names','Nothing specific'],'answer':0}], 'summary_tg':f'Матн ба мавзӯи {theme.lower()} ва истифодаи забони англисӣ дар ҳолати воқеӣ бахшида шудааст.'},'listening':{'title':f'Listening: {theme}','script':listening,'questions':[{'q':'What is the first listening goal?','options':['Understand the main idea','Translate every word','Memorise punctuation','Ignore the speaker'],'answer':0},{'q':'What should you do next?','options':['Repeat useful sentences','Stop immediately','Skip practice','Only read the title'],'answer':0}]},'speaking':{'prompt':f'Talk for 60–90 seconds about {theme}. Use at least three target words and the target grammar.','target_words':[w[0] for w in bank[:5]]},'writing':{'prompt':f'Write 80–150 words about {theme}. Give one example and use at least four target words.','min_words':40},'homework':hw,'exercises':ex})
  units.append({'number':ui,'title':theme,'title_tg':theme,'title_ru':theme,'intro_tg':f'Шумо метавонед дар бораи {theme.lower()} бо ҷумлаҳои амалӣ суҳбат ва навиштан кунед.','lessons':lessons})
 out={'level':level,'name':name,'units':units}
 json.dump(out,open(os.path.join(ROOT,level+'.json'),'w'),ensure_ascii=False,indent=2)
print('built',len(levels),'levels,',len(levels)*12*4,'lessons')
