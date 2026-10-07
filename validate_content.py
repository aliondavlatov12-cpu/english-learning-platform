import json,glob,sys,os
root=os.path.join(os.path.dirname(__file__),'..','app','content'); problems=[]
for f in glob.glob(os.path.join(root,'*.json')):
 try:d=json.load(open(f,encoding='utf8'))
 except Exception as e: problems.append(f'{f}: invalid JSON {e}'); continue
 if set(d)!= {'level','name','units'}: problems.append(f'{f}: root keys')
 for u in d.get('units',[]):
  for k in ['number','title','title_tg','title_ru','intro_tg','lessons']:
   if k not in u: problems.append(f'{f}: unit missing {k}')
  if len(u.get('lessons',[]))!=4: problems.append(f'{f}: unit {u.get("number")} must have 4 lessons')
  for l in u.get('lessons',[]):
   for k in ['number','title','objective_tg','vocab','grammar','reading','listening','speaking','writing','homework','exercises']:
    if k not in l: problems.append(f'{f}: lesson missing {k}')
   if len(l.get('vocab',[]))!=12: problems.append(f'{f}: vocab count')
   if len(l.get('exercises',[]))<8: problems.append(f'{f}: exercise count')
   for v in l.get('vocab',[]):
    if not all(v.get(x) for x in ['w','ipa','tg','ru','ex']): problems.append(f'{f}: bad vocab')
if problems:
 print('\n'.join(problems)); print(f'{len(problems)} problems'); sys.exit(1)
print('0 problems')
