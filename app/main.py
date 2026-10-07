import os,json,re,secrets,hashlib,random,math
from datetime import datetime,timedelta
from functools import wraps
from urllib.request import Request,urlopen
from flask import Flask,render_template,request,redirect,url_for,session,jsonify,flash,send_file
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import create_engine,String,Integer,Boolean,DateTime,Text,ForeignKey,Float,UniqueConstraint,select,func
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,sessionmaker
import qrcode

BASE=os.path.dirname(__file__)
app=Flask(__name__,static_folder='static',template_folder='templates')
app.secret_key=os.getenv('SECRET_KEY','dev-change-this')
DB_URL=os.getenv('DATABASE_URL','sqlite:///english_learning_v4.db')
if DB_URL.startswith('postgres://'): DB_URL=DB_URL.replace('postgres://','postgresql+psycopg://',1)
elif DB_URL.startswith('postgresql://'): DB_URL=DB_URL.replace('postgresql://','postgresql+psycopg://',1)
engine=create_engine(DB_URL,pool_pre_ping=True)
SessionLocal=sessionmaker(bind=engine,expire_on_commit=False)
class Base(DeclarativeBase): pass
class User(Base):
 __tablename__='v4_users'; id:Mapped[int]=mapped_column(primary_key=True); username:Mapped[str]=mapped_column(String(80),unique=True,index=True); password_hash:Mapped[str]=mapped_column(String(255)); display_name:Mapped[str]=mapped_column(String(120),default='Student'); role:Mapped[str]=mapped_column(String(20),default='student'); blocked:Mapped[bool]=mapped_column(Boolean,default=False); selected_level:Mapped[str]=mapped_column(String(10),default=''); recommended_level:Mapped[str]=mapped_column(String(10),default=''); placement_score:Mapped[float]=mapped_column(Float,default=0); ui_lang:Mapped[str]=mapped_column(String(5),default='tg'); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class Book(Base):
 __tablename__='v4_books'; id:Mapped[int]=mapped_column(primary_key=True); level:Mapped[str]=mapped_column(String(10),unique=True); title:Mapped[str]=mapped_column(String(120)); subtitle:Mapped[str]=mapped_column(String(180)); order_no:Mapped[int]=mapped_column(Integer)
class Unit(Base):
 __tablename__='v4_units'; id:Mapped[int]=mapped_column(primary_key=True); book_id:Mapped[int]=mapped_column(ForeignKey('v4_books.id')); number:Mapped[int]=mapped_column(Integer); title:Mapped[str]=mapped_column(String(180)); title_tg:Mapped[str]=mapped_column(String(180)); title_ru:Mapped[str]=mapped_column(String(180)); intro_tg:Mapped[str]=mapped_column(Text); __table_args__=(UniqueConstraint('book_id','number'),)
class Lesson(Base):
 __tablename__='v4_lessons'; id:Mapped[int]=mapped_column(primary_key=True); unit_id:Mapped[int]=mapped_column(ForeignKey('v4_units.id')); number:Mapped[int]=mapped_column(Integer); title:Mapped[str]=mapped_column(String(220)); objective_tg:Mapped[str]=mapped_column(Text); content_json:Mapped[str]=mapped_column(Text); __table_args__=(UniqueConstraint('unit_id','number'),)
class Progress(Base):
 __tablename__='v4_progress'; id:Mapped[int]=mapped_column(primary_key=True); user_id:Mapped[int]=mapped_column(ForeignKey('v4_users.id')); lesson_id:Mapped[int]=mapped_column(ForeignKey('v4_lessons.id')); completed:Mapped[bool]=mapped_column(Boolean,default=False); homework_done:Mapped[bool]=mapped_column(Boolean,default=False); practice_score:Mapped[float]=mapped_column(Float,default=0); speaking_score:Mapped[float]=mapped_column(Float,default=0); updated_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow); __table_args__=(UniqueConstraint('user_id','lesson_id'),)
class Homework(Base):
 __tablename__='v4_homework'; id:Mapped[int]=mapped_column(primary_key=True); user_id:Mapped[int]=mapped_column(ForeignKey('v4_users.id')); lesson_id:Mapped[int]=mapped_column(ForeignKey('v4_lessons.id')); payload_json:Mapped[str]=mapped_column(Text); score:Mapped[float]=mapped_column(Float,default=0); feedback:Mapped[str]=mapped_column(Text,default=''); submitted_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class Placement(Base):
 __tablename__='v4_placement'; id:Mapped[int]=mapped_column(primary_key=True); user_id:Mapped[int]=mapped_column(ForeignKey('v4_users.id')); score:Mapped[float]=mapped_column(Float); level:Mapped[str]=mapped_column(String(10)); answers_json:Mapped[str]=mapped_column(Text); violations:Mapped[int]=mapped_column(Integer,default=0); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class ExamResult(Base):
 __tablename__='v4_exam_results'; id:Mapped[int]=mapped_column(primary_key=True); user_id:Mapped[int]=mapped_column(ForeignKey('v4_users.id')); book_id:Mapped[int]=mapped_column(ForeignKey('v4_books.id')); score:Mapped[float]=mapped_column(Float); grammar:Mapped[float]=mapped_column(Float); vocabulary:Mapped[float]=mapped_column(Float); reading:Mapped[float]=mapped_column(Float); listening:Mapped[float]=mapped_column(Float); writing:Mapped[float]=mapped_column(Float); speaking:Mapped[float]=mapped_column(Float); passed:Mapped[bool]=mapped_column(Boolean); weak_areas:Mapped[str]=mapped_column(Text); created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
class Certificate(Base):
 __tablename__='v4_certificates'; id:Mapped[int]=mapped_column(primary_key=True); user_id:Mapped[int]=mapped_column(ForeignKey('v4_users.id')); book_id:Mapped[int]=mapped_column(ForeignKey('v4_books.id')); certificate_id:Mapped[str]=mapped_column(String(50),unique=True); score:Mapped[float]=mapped_column(Float); revoked:Mapped[bool]=mapped_column(Boolean,default=False); issued_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
Base.metadata.create_all(engine)
LEVELS=[('A0','Starter','Оғози аввал','Начальный',0),('A1','Beginner','Оғозкунанда','Начальный',1),('A2','Elementary','Ибтидоӣ','Элементарный',2),('B1','Pre-Intermediate','Пешмиёна','Средний ниже',3),('B2','Intermediate','Миёна','Средний',4),('C1','Upper-Intermediate','Боломиёна','Выше среднего',5),('C2','Advanced','Пешрафта','Продвинутый',6)]
CONTENT={}
for lv,*_ in LEVELS:
 with open(os.path.join(BASE,'content',lv+'.json'),encoding='utf8') as f: CONTENT[lv]=json.load(f)
PLACEMENT=[]
# 42 diagnostic items; progressively harder. Answers are indices.
for i,(lv,*_) in enumerate(LEVELS):
 for j in range(6):
  if lv=='A0': q=['Choose the correct form: I ___ Alijon.','Choose the correct word: ___ is my book.','Choose the correct sentence:','Choose the correct meaning of "home".','Choose the correct form: She ___ happy.','Choose the correct question.'][j]; opts=[['am','is','are','be'],['This','These','Those','They'],['I am a student.','I student am.','Am student I.','Student I am a.'],['хона','мактаб','об','дӯст'],['is','are','am','be'],['What is your name?','Your name what?','What your is name?','Name is what your?']][j]
  elif lv=='A1': q=['She ___ to school every day.','We ___ watching a film now.','I ___ yesterday.','There ___ two books on the desk.','I have ___ money.','Which is a comparative?'][j]; opts=[['goes','go','going','gone'],['are','is','am','be'],['visited my friend','visit my friend','visiting my friend','have visit'],['are','is','be','am'],['some','any','many','a'],['better','good','best','well']][j]
  elif lv=='A2': q=['I ___ finished my work.','When I called, she ___ dinner.','If it rains, we ___ home.','You ___ see a doctor if you feel ill.','This is the book ___ I bought.','If I had time, I ___ travel more.'][j]; opts=[['have','has','had','am'],['was cooking','cooked','has cooked','cooks'],['will stay','stayed','stay','would stayed'],['should','can’t','would','mustn’t'],['that','who','where','when'],['would','will','can','am']][j]
  elif lv=='B1': q=['By 8 pm, I ___ my work.','I have lived here ___ 2020.','If I had known, I ___ you.','He said he ___ busy.','The report ___ yesterday.','She is the person ___ helped me.'][j]; opts=[['will have finished','finish','finished','has finish'],['since','for','from','during'],['would have called','will call','call','would call'],['was','is','be','has'],['was published','published','is publish','has publish'],['who','which','where','what']][j]
  elif lv=='B2': q=['If I had studied, I ___ the exam.','Rarely ___ such a clear explanation.','The results are believed ___ accurate.','You ___ have told me earlier.','What I need ___ more time.','The proposal, ___ was revised, passed.'][j]; opts=[['would have passed','will pass','pass','would pass'],['have I heard','I have heard','heard I','I heard have'],['to be','being','be','to being'],['should','might','must','can'],['is','are','be','am'],['which','who','where','what']][j]
  elif lv=='C1': q=['Had I known, I ___ differently.','It is essential that he ___ informed.','The study, ___ carefully designed, is persuasive.','She ___ be right, given the evidence.','Not only ___ the cost high, but it is rising.','The phrase is too informal for an academic ___ .'][j]; opts=[['would have acted','will act','acted','would act'],['be','is','was','being'],['though','which','who','where'],['may','mustn’t','can’t','wouldn’t'],['is','it is','is it','it'],['register','weather','family','street']][j]
  else: q=['Were the premise true, the conclusion ___ follow.','The author’s claim is open to ___ .','Little ___ that the policy would fail.','The evidence ___ the initial hypothesis.','It would be misleading to ___ causation from correlation.','The argument is coherent, ___ several assumptions remain contestable.'][j]; opts=[['would','will','does','has'],['interpretation','interpret','interpreting','interpreted'],['did we expect','we expected','expected we','we did expect'],['corroborates','corroborate','corroborating','has corroborate'],['infer','imply','assume','translate'],['although','because','unless','therefore']][j]
  PLACEMENT.append({'id':len(PLACEMENT),'level':lv,'q':q,'options':opts,'answer':0})

def seed():
 with SessionLocal() as db:
  if db.scalar(select(Book.id).limit(1)): return
  for order,(lv,name,tg,ru,_) in enumerate(LEVELS):
   c=CONTENT[lv]; b=Book(level=lv,title=f'{lv} — {name}',subtitle=f'Original CEFR-aligned {name} course',order_no=order); db.add(b); db.flush()
   for u in c['units']:
    un=Unit(book_id=b.id,number=u['number'],title=u['title'],title_tg=u['title_tg'],title_ru=u['title_ru'],intro_tg=u['intro_tg']); db.add(un); db.flush()
    for l in u['lessons']:
     db.add(Lesson(unit_id=un.id,number=l['number'],title=l['title'],objective_tg=l['objective_tg'],content_json=json.dumps(l,ensure_ascii=False)))
  admin=os.getenv('ADMIN_USERNAME','admin'); pw=os.getenv('ADMIN_PASSWORD','change-me')
  if not db.scalar(select(User).where(User.username==admin)): db.add(User(username=admin,password_hash=generate_password_hash(pw),display_name='Alijon Davlatov',role='admin'))
  db.commit()
seed()
def me():
 uid=session.get('uid')
 if not uid:return None
 with SessionLocal() as db:return db.get(User,uid)
def auth(fn):
 @wraps(fn)
 def w(*a,**kw):
  u=me()
  if not u:return redirect(url_for('login',next=request.path))
  if u.blocked:session.clear();return 'Account blocked',403
  return fn(u,*a,**kw)
 return w
def admin_only(fn):
 @wraps(fn)
 def w(u,*a,**kw):
  if u.role!='admin':return 'Forbidden',403
  return fn(u,*a,**kw)
 return w
def progress(db,uid,lid):
 p=db.scalar(select(Progress).where(Progress.user_id==uid,Progress.lesson_id==lid))
 if not p:p=Progress(user_id=uid,lesson_id=lid);db.add(p);db.flush()
 return p
def score_text(text,targets=()):
 words=set(re.findall(r"[a-zA-Z']+",(text or '').lower())); t=set(re.findall(r"[a-zA-Z']+",' '.join(targets).lower()))
 if not words:return 0
 return round(min(100,(len(words& t)/max(1,min(5,len(t)))*70)+(min(len(words),120)/120*30)),1)
@app.context_processor
def common(): return {'me':me(),'levels':LEVELS,'year':datetime.utcnow().year}
@app.route('/')
def home():return render_template('home.html')
@app.route('/login',methods=['GET','POST'])
def login():
 if request.method=='POST':
  with SessionLocal() as db:
   u=db.scalar(select(User).where(User.username==request.form.get('username','').strip()))
   if u and not u.blocked and check_password_hash(u.password_hash,request.form.get('password','')):
    session['uid']=u.id; return redirect(url_for('placement') if not u.recommended_level else url_for('dashboard'))
  flash('Номи корбар ё парол нодуруст аст','error')
 return render_template('login.html')
@app.route('/logout')
def logout():session.clear();return redirect(url_for('home'))
@app.route('/set-lang/<lang>')
def set_lang(lang):
 if lang not in {'tg','ru','en'}: lang='tg'
 session['lang']=lang
 if session.get('uid'):
  with SessionLocal() as db:u=db.get(User,session['uid']);u.ui_lang=lang;db.commit()
 return redirect(request.referrer or url_for('home'))
@app.route('/placement',methods=['GET','POST'])
@auth
def placement(u):
 if request.method=='GET': return render_template('placement.html',questions=PLACEMENT)
 answers=request.form.get('answers','')
 try: amap=json.loads(answers)
 except: amap={}
 correct=sum(1 for q in PLACEMENT if str(amap.get(str(q['id']),''))==str(q['answer']))
 pct=round(correct/len(PLACEMENT)*100,1); idx=min(6,max(0,int(correct/6))) ; level=LEVELS[idx][0]
 with SessionLocal() as db:
  user=db.get(User,u.id);user.recommended_level=level;user.selected_level=level;user.placement_score=pct;db.add(Placement(user_id=u.id,score=pct,level=level,answers_json=answers,violations=int(request.form.get('violations',0) or 0)));db.commit()
 return render_template('placement_result.html',score=pct,level=level,level_name=LEVELS[idx][1])
@app.post('/api/placement/violation')
@auth
def violation(u):return jsonify(ok=True)
@app.route('/dashboard')
@auth
def dashboard(u):
 with SessionLocal() as db:
  books=db.scalars(select(Book).order_by(Book.order_no)).all(); done=db.scalar(select(func.count(Progress.id)).where(Progress.user_id==u.id,Progress.completed==True)) or 0; hw=db.scalar(select(func.count(Homework.id)).where(Homework.user_id==u.id)) or 0; exams=db.scalars(select(ExamResult).where(ExamResult.user_id==u.id).order_by(ExamResult.created_at.desc())).all(); certs=db.scalars(select(Certificate).where(Certificate.user_id==u.id,Certificate.revoked==False)).all()
 return render_template('dashboard.html',books=books,done=done,hw=hw,exams=exams,certs=certs,placement=u.placement_score,recommended=u.recommended_level)
@app.route('/book/<int:bid>')
@auth
def book(u,bid):
 with SessionLocal() as db:
  b=db.get(Book,bid); units=db.scalars(select(Unit).where(Unit.book_id==bid).order_by(Unit.number)).all(); rows=[]
  for un in units: rows.append((un,db.scalars(select(Lesson).where(Lesson.unit_id==un.id).order_by(Lesson.number)).all()))
  done={p.lesson_id for p in db.scalars(select(Progress).where(Progress.user_id==u.id,Progress.completed==True)).all()}
 return render_template('book.html',book=b,rows=rows,done=done)
@app.route('/lesson/<int:lid>')
@auth
def lesson(u,lid):
 with SessionLocal() as db:
  l=db.get(Lesson,lid)
  if not l:return 'Not found',404
  p=progress(db,u.id,lid); content=json.loads(l.content_json); last=db.scalar(select(Homework).where(Homework.user_id==u.id,Homework.lesson_id==lid).order_by(Homework.submitted_at.desc()))
  db.commit()
 return render_template('lesson.html',lesson=l,c=content,p=p,last=last)
@app.post('/lesson/<int:lid>/practice')
@auth
def practice(u,lid):
 with SessionLocal() as db:
  l=db.get(Lesson,lid);c=json.loads(l.content_json); ex=c['exercises']; correct=sum(1 for i,e in enumerate(ex) if request.form.get(f'e{i}')==str(e['answer'])); sc=round(correct/len(ex)*100,1);p=progress(db,u.id,lid);p.practice_score=sc;p.updated_at=datetime.utcnow();db.commit()
 flash(f'Practice: {sc}/100','ok');return redirect(url_for('lesson',lid=lid))
@app.post('/lesson/<int:lid>/homework')
@auth
def homework(u,lid):
 with SessionLocal() as db:
  l=db.get(Lesson,lid);c=json.loads(l.content_json); payload={k:request.form.get(k,'').strip() for k in ['vocabulary','grammar','listening','writing','speaking']}; targets=[v['w'] for v in c['vocab']]; scores=[score_text(payload['vocabulary'],targets),score_text(payload['grammar'],[c['grammar']['title']]),score_text(payload['listening'],targets),score_text(payload['writing'],targets),score_text(payload['speaking'],targets)]; sc=round(sum(scores)/5,1);p=progress(db,u.id,lid);p.homework_done=True;db.add(Homework(user_id=u.id,lesson_id=lid,payload_json=json.dumps(payload,ensure_ascii=False),score=sc,feedback='Five homework sections received. Review the lowest-scoring section and resubmit for practice.'));db.commit()
 flash(f'Homework: {sc}/100','ok');return redirect(url_for('lesson',lid=lid))
@app.post('/lesson/<int:lid>/complete')
@auth
def complete(u,lid):
 with SessionLocal() as db:p=progress(db,u.id,lid);p.completed=True;p.updated_at=datetime.utcnow();db.commit()
 return redirect(url_for('lesson',lid=lid))
@app.post('/api/speaking/<int:lid>')
@auth
def speaking(u,lid):
 d=request.get_json(silent=True) or {}; heard=d.get('heard',''); target=d.get('target',''); a=set(re.findall(r"[a-z']+",target.lower()));b=set(re.findall(r"[a-z']+",heard.lower()));sc=round(len(a&b)/max(1,len(a))*100,1)
 with SessionLocal() as db:p=progress(db,u.id,lid);p.speaking_score=sc;p.updated_at=datetime.utcnow();db.commit()
 return jsonify(score=sc,feedback='Great match — repeat once more for fluency.' if sc>=85 else 'Good attempt — listen again and repeat the difficult words.' if sc>=60 else 'Keep practising: listen, speak slowly, then try again.')
@app.route('/exam/<int:bid>')
@auth
def exam(u,bid):
 with SessionLocal() as db:
  b=db.get(Book,bid); lessons=db.scalars(select(Lesson).join(Unit,Lesson.unit_id==Unit.id).where(Unit.book_id==bid)).all(); pool=[]
  for l in lessons:
   c=json.loads(l.content_json)
   for e in c['exercises']:
    if e['skill'] in {'grammar','vocabulary','reading','listening'}: pool.append(e)
  random.Random(u.id+bid).shuffle(pool); pool=pool[:24]
 return render_template('exam.html',book=b,questions=pool,writing=f'Write 120–180 words about what you learned in {b.level}. Give reasons and examples.',speaking=f'Speak for 90 seconds about your progress in {b.level}.')
@app.post('/api/exam/<int:bid>')
@auth
def exam_submit(u,bid):
 d=request.get_json(silent=True) or {};answers=d.get('answers',{});writing=d.get('writing','');speaking=d.get('speaking','')
 with SessionLocal() as db:
  b=db.get(Book,bid); lessons=db.scalars(select(Lesson).join(Unit,Lesson.unit_id==Unit.id).where(Unit.book_id==bid)).all();pool=[]
  for l in lessons:
   for e in json.loads(l.content_json)['exercises']:
    if e['skill'] in {'grammar','vocabulary','reading','listening'}:pool.append(e)
  random.Random(u.id+bid).shuffle(pool);pool=pool[:24]; buckets={k:[0,0] for k in ['grammar','vocabulary','reading','listening']}
  for i,e in enumerate(pool): buckets[e['skill']][1]+=1; buckets[e['skill']][0]+=answers.get(str(i))==e['answer']
  vals={k:round((v[0]/v[1])*100,1) if v[1] else 0 for k,v in buckets.items()}; ws=min(100,score_text(writing,[b.level.lower()])+20); ss=min(100,score_text(speaking,[b.level.lower()])+20); score=round(sum(vals.values())/4*.7+ws*.15+ss*.15,1); passed=score>=70; weak=[k.title() for k,v in vals.items() if v<70]+(['Writing'] if ws<70 else [])+(['Speaking'] if ss<70 else []); weak=', '.join(weak) or 'No major weak area detected';r=ExamResult(user_id=u.id,book_id=bid,score=score,grammar=vals['grammar'],vocabulary=vals['vocabulary'],reading=vals['reading'],listening=vals['listening'],writing=ws,speaking=ss,passed=passed,weak_areas=weak);db.add(r);db.flush();cert=None
  if passed:
   cert=Certificate(user_id=u.id,book_id=bid,certificate_id=f'EL-{datetime.utcnow().year}-{secrets.token_hex(5).upper()}',score=score);db.add(cert);db.flush()
  db.commit()
 return jsonify(score=score,passed=passed,weak_areas=weak,certificate_id=cert.certificate_id if cert else None,result_id=r.id)
@app.route('/certificate/<int:cid>')
@auth
def certificate(u,cid):
 with SessionLocal() as db:
  c=db.get(Certificate,cid)
  if not c or c.revoked or (c.user_id!=u.id and u.role!='admin'):return 'Not found',404
  return render_template('certificate.html',cert=c,book=db.get(Book,c.book_id),owner=db.get(User,c.user_id))
@app.route('/verify/<certid>')
def verify(certid):
 with SessionLocal() as db:
  c=db.scalar(select(Certificate).where(Certificate.certificate_id==certid)); valid=bool(c and not c.revoked); return render_template('verify.html',valid=valid,certid=certid,cert=c,book=db.get(Book,c.book_id) if c else None,owner=db.get(User,c.user_id) if c else None)
@app.route('/certificate/<int:cid>/qr.png')
@auth
def qr(cid):
 with SessionLocal() as db:
  c=db.get(Certificate,cid)
  if not c:return 'Not found',404
  if c.user_id!=u.id and u.role!='admin':return 'Forbidden',403
  img=qrcode.make(url_for('verify',certid=c.certificate_id,_external=True));path=f'/tmp/{c.certificate_id}.png';img.save(path);return send_file(path,mimetype='image/png')
@app.post('/api/ai-teacher')
@auth
def ai(u):
 d=request.get_json(silent=True) or {}; key=os.getenv('OPENROUTER_API_KEY');
 if not key:return jsonify(answer='AI Teacher is optional. Add OPENROUTER_API_KEY in Render to activate it.')
 prompt=d.get('message',''); model=os.getenv('OPENROUTER_MODEL','google/gemini-2.0-flash-exp:free'); body=json.dumps({'model':model,'messages':[{'role':'system','content':'You are a patient English teacher. Explain simply, correct mistakes, and adapt to CEFR level. Support Tajik, Russian and English.'},{'role':'user','content':prompt}]}).encode(); req=Request('https://openrouter.ai/api/v1/chat/completions',data=body,headers={'Authorization':'Bearer '+key,'Content-Type':'application/json','HTTP-Referer':request.host_url})
 try:
  with urlopen(req,timeout=30) as r: out=json.loads(r.read().decode()); return jsonify(answer=out['choices'][0]['message']['content'])
 except Exception as e:return jsonify(answer='AI Teacher is temporarily unavailable.',error=str(e)),200
@app.route('/admin')
@auth
@admin_only
def admin(u):
 with SessionLocal() as db:
  users=db.scalars(select(User).order_by(User.created_at.desc())).all();books=db.scalars(select(Book).order_by(Book.order_no)).all();certs=db.scalars(select(Certificate).order_by(Certificate.issued_at.desc()).limit(50)).all();stats={'users':len(users),'lessons':db.scalar(select(func.count(Lesson.id))) or 0,'certificates':db.scalar(select(func.count(Certificate.id))) or 0,'exams':db.scalar(select(func.count(ExamResult.id))) or 0}
 return render_template('admin.html',users=users,books=books,certs=certs,stats=stats)
@app.post('/admin/users/add')
@auth
@admin_only
def add_user(u):
 username=request.form.get('username','').strip();pw=request.form.get('password','');name=request.form.get('display_name','Student').strip()
 if not username or len(pw)<6:return 'Username and password(6+) required',400
 with SessionLocal() as db:
  if db.scalar(select(User).where(User.username==username)):return 'Username already exists',409
  db.add(User(username=username,password_hash=generate_password_hash(pw),display_name=name));db.commit()
 return redirect(url_for('admin'))
@app.post('/admin/users/<int:uid>/toggle')
@auth
@admin_only
def toggle(u,uid):
 with SessionLocal() as db:x=db.get(User,uid);x.blocked=not x.blocked;db.commit()
 return redirect(url_for('admin'))
@app.post('/admin/users/<int:uid>/delete')
@auth
@admin_only
def delete(u,uid):
 with SessionLocal() as db:x=db.get(User,uid);db.delete(x);db.commit()
 return redirect(url_for('admin'))
@app.post('/admin/users/<int:uid>/reset')
@auth
@admin_only
def reset(u,uid):
 new=request.form.get('password','')
 if len(new)<6:return 'Password must be 6+',400
 with SessionLocal() as db:x=db.get(User,uid);x.password_hash=generate_password_hash(new);db.commit()
 return redirect(url_for('admin'))
@app.post('/admin/certificate/<int:cid>/revoke')
@auth
@admin_only
def revoke(u,cid):
 with SessionLocal() as db:x=db.get(Certificate,cid);x.revoked=True;db.commit()
 return redirect(url_for('admin'))
@app.route('/admin/user/<int:uid>')
@auth
@admin_only
def user_view(u,uid):
 with SessionLocal() as db:
  x=db.get(User,uid); ps=db.scalars(select(Progress).where(Progress.user_id==uid)).all(); ex=db.scalars(select(ExamResult).where(ExamResult.user_id==uid)).all(); cs=db.scalars(select(Certificate).where(Certificate.user_id==uid)).all()
 return render_template('user_view.html',user=x,progress=ps,exams=ex,certs=cs)
@app.get('/health')
def health():return jsonify(status='ok',version='V4',lessons=336,levels=7)
if __name__=='__main__':app.run(host='0.0.0.0',port=int(os.getenv('PORT',5000)),debug=False)
