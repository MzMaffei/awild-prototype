// Smoke test: mobile + desktop render, broken images, horizontal overflow, console errors.
const {chromium,devices}=require(process.argv[2]);
const path=require('path');const fs=require('fs');
(async()=>{const b=await chromium.launch();const dir=path.resolve('docs');const shots=path.resolve('_shots');fs.mkdirSync(shots,{recursive:true});
for(const f of fs.readdirSync(dir).filter(x=>x.endsWith('.html'))){
 for(const [n,opt] of [['m',devices['iPhone 13']],['d',{viewport:{width:1366,height:900}}]]){
  const c=await b.newContext(opt);const p=await c.newPage();const errs=[];
  p.on('pageerror',e=>errs.push(String(e)));p.on('response',r=>{if(r.status()>=400)errs.push(r.status()+' '+r.url().slice(0,100))});
  await p.goto('file://'+dir+'/'+f,{waitUntil:'networkidle',timeout:60000}).catch(e=>errs.push(String(e).slice(0,80)));
  await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=600){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,120))}window.scrollTo(0,0)});
  await p.waitForTimeout(1500);
  const r=await p.evaluate(()=>({ov:document.documentElement.scrollWidth-innerWidth,bad:[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src.slice(-60)),h1:document.querySelectorAll('h1').length}));
  console.log(n,f,JSON.stringify(r),errs.slice(0,3).join(' | '));
  if(['index.html','wild-fest.html','protocollo.html'].includes(f)) await p.screenshot({path:`${shots}/${n}-${f}.png`,fullPage:n==='m'?false:false});
  await c.close()}}
await b.close()})()
