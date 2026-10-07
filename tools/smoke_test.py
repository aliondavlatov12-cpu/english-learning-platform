import os,json,glob,ast
root=os.path.join(os.path.dirname(__file__),'..')
main=open(os.path.join(root,'app','main.py'),encoding='utf8').read(); ast.parse(main)
levels=['A0','A1','A2','B1','B2','C1','C2']; lessons=0; units=0; vocab=0; exercises=0
for lv in levels:
 d=json.load(open(os.path.join(root,'app','content',lv+'.json'),encoding='utf8')); assert d['level']==lv and len(d['units'])==12
 units+=len(d['units'])
 for u in d['units']:
  assert len(u['lessons'])==4
  for l in u['lessons']:
   lessons+=1; vocab+=len(l['vocab']); exercises+=len(l['exercises'])
   assert len(l['vocab'])==12 and len(l['exercises'])>=8
   for v in l['vocab']: assert v['ipa'].startswith('/') and v['ipa'].endswith('/')
assert lessons==336 and units==84 and vocab==4032 and exercises>=2688
for path in glob.glob(os.path.join(root,'app','templates','*.html')): assert '{%' in open(path,encoding='utf8').read() or '{{' in open(path,encoding='utf8').read()
print(f'OK: {lessons} lessons, {units} units, {vocab} vocabulary, {exercises} lesson exercises; Python AST valid.')
