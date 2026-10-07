import ast,re,os,json
p=os.path.join(os.path.dirname(__file__),'..','app','main.py'); t=open(p,encoding='utf8').read(); tree=ast.parse(t)
routes=[]
for n in tree.body:
 if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)):
  for d in n.decorator_list:
   if isinstance(d,ast.Call) and isinstance(d.func,ast.Attribute) and d.func.attr in ('route','get','post'):
    routes.append(n.name)
required=['home','login','logout','placement','dashboard','book','lesson','practice','homework','complete','speaking','exam','exam_submit','certificate','verify','qr','ai','admin','add_user','toggle','delete','reset','revoke','user_view','health']
miss=[x for x in required if x not in routes]
assert not miss,miss
print('OK routes:',len(routes))
