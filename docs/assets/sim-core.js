/* HSC Physics 讲解网站 · 动画公共代码（window.Sim）
   从 template_M6T5.html 原样抽出：颜色读取、画图小工具、stage（canvas + 播放按钮 + 自适应宽度）、主循环。
   每页自己的动画写在页面底部的 <script> 里，用法：
     var S=window.Sim, C=S.C, txt=S.txt, ...;
     var st=S.makeStage('sim1',{height:function(w){return w>=640?330:520;}, step:function(dt){...}, draw:function(ctx,W,H){...}});
   - C 里的颜色来自 CSS 变量，主题切换时会自动更新（同一个对象，不要重新赋值）。
   - 主循环只推进“在屏幕里并且在播放”的 stage；prefers-reduced-motion 时默认不自动播放。 */
(function(){
'use strict';
var root=document.documentElement;
var C={};
var KEYS=['bg','stage','surface','ink','muted','line','grid','copper','north','south','force','field','heat','violet','light'];
function readColors(){var cs=getComputedStyle(root);KEYS.forEach(function(k){C[k]=cs.getPropertyValue('--'+k).trim()||'#888888';});}
readColors();
var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var FONT='"IBM Plex Sans","PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans SC",sans-serif';
var MONO='"IBM Plex Mono",ui-monospace,Menlo,monospace';
var MATH='"STIX Two Text","Times New Roman",serif';
var TAU=Math.PI*2;

function rgba(hex,a){var h=String(hex).replace('#','').trim();if(h.length===3)h=h.split('').map(function(x){return x+x;}).join('');var n=parseInt(h,16);if(isNaN(n))return hex;return 'rgba('+((n>>16)&255)+','+((n>>8)&255)+','+(n&255)+','+a+')';}
function txt(ctx,s,x,y,col,size,weight,align,base,family){ctx.font=(weight||500)+' '+(size||13)+'px '+(family||FONT);ctx.fillStyle=col||C.ink;ctx.textAlign=align||'left';ctx.textBaseline=base||'alphabetic';ctx.fillText(s,x,y);}
function seg(ctx,x1,y1,x2,y2,col,w,dash){ctx.strokeStyle=col;ctx.lineWidth=w||1;ctx.setLineDash(dash||[]);ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();ctx.setLineDash([]);}
function arrow(ctx,x1,y1,x2,y2,col,w,head){var dx=x2-x1,dy=y2-y1,len=Math.hypot(dx,dy);if(len<2)return;head=head||9;var ux=dx/len,uy=dy/len;ctx.strokeStyle=col;ctx.fillStyle=col;ctx.lineWidth=w||2.5;ctx.setLineDash([]);ctx.lineCap='round';ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2-ux*head*0.7,y2-uy*head*0.7);ctx.stroke();ctx.lineCap='butt';ctx.beginPath();ctx.moveTo(x2,y2);ctx.lineTo(x2-ux*head-uy*head*0.55,y2-uy*head+ux*head*0.55);ctx.lineTo(x2-ux*head+uy*head*0.55,y2-uy*head-ux*head*0.55);ctx.closePath();ctx.fill();}
function rrect(ctx,x,y,w,h,r){r=Math.max(0,Math.min(r,w/2,h/2));ctx.beginPath();ctx.moveTo(x+r,y);ctx.arcTo(x+w,y,x+w,y+h,r);ctx.arcTo(x+w,y+h,x,y+h,r);ctx.arcTo(x,y+h,x,y,r);ctx.arcTo(x,y,x+w,y,r);ctx.closePath();}
function dot(ctx,x,y,r,fill){ctx.beginPath();ctx.arc(x,y,r,0,TAU);ctx.fillStyle=fill;ctx.fill();}
function ring(ctx,x,y,r,col,w){ctx.beginPath();ctx.arc(x,y,r,0,TAU);ctx.strokeStyle=col;ctx.lineWidth=w;ctx.stroke();}
function pole(ctx,x,y,w,h,label,col){rrect(ctx,x,y,w,h,6);ctx.fillStyle=col;ctx.fill();txt(ctx,label,x+w/2,y+h/2+1,'#ffffff',w<40?16:20,700,'center','middle');}
function wire(ctx,x,y,s,r){dot(ctx,x,y,r,C.surface);ring(ctx,x,y,r,C.copper,3);if(s>0){dot(ctx,x,y,r*0.32,C.ink);}else if(s<0){var d=r*0.46;seg(ctx,x-d,y-d,x+d,y+d,C.ink,2.2);seg(ctx,x-d,y+d,x+d,y-d,C.ink,2.2);}}
function fieldLines(ctx,x0,x1,cy,n,gap){for(var k=-n;k<=n;k++){var y=cy+k*gap;seg(ctx,x0,y,x1-10,y,rgba(C.field,0.65),1.2,[5,6]);arrow(ctx,x1-22,y,x1-4,y,rgba(C.field,1),1.4,7);}}
function hbar(ctx,x,y,w,h,frac,col){rrect(ctx,x,y,w,h,h/2);ctx.fillStyle=rgba(C.muted,0.16);ctx.fill();frac=Math.max(0,Math.min(1,frac));if(frac>0.005){rrect(ctx,x,y,Math.max(h,w*frac),h,h/2);ctx.fillStyle=col;ctx.fill();}}

/* ---------- 网站新加的小工具（样板里没有） ---------- */
function clamp(v,a,b){return Math.max(a,Math.min(b,v));}
function lerp(a,b,t){return a+(b-a)*t;}
/* 可见光波长 (nm) → 近似颜色，用于光谱、双缝、氢光谱线。380–750 nm 以外返回灰色。 */
function lambdaColor(nm,a){var r=0,g=0,b=0;
  if(nm<380||nm>750)return rgba(C.muted,a==null?1:a);
  if(nm<440){r=-(nm-440)/60;b=1;}else if(nm<490){g=(nm-440)/50;b=1;}else if(nm<510){g=1;b=-(nm-510)/20;}
  else if(nm<580){r=(nm-510)/70;g=1;}else if(nm<645){r=1;g=-(nm-645)/65;}else{r=1;}
  var f=nm<420?0.3+0.7*(nm-380)/40:(nm>700?0.3+0.7*(750-nm)/50:1);
  function c(v){return Math.round(255*Math.pow(v*f,0.8));}
  return 'rgba('+c(r)+','+c(g)+','+c(b)+','+(a==null?1:a)+')';}

/* ---------- stage system ---------- */
var stages=[];
function makeStage(id,o){
  var fig=document.getElementById(id);var box=fig.querySelector('.stage-box');var cv=box.querySelector('canvas');var ctx=cv.getContext('2d');
  var s={id:id,fig:fig,box:box,cv:cv,ctx:ctx,W:300,H:200,lw:-1,visible:true,playing:(o.autoplay!==false)&&!reduce,step:o.step,draw:o.draw,height:o.height};
  s.render=function(){ctx.save();s.draw(ctx,s.W,s.H);ctx.restore();};
  s.resize=function(force){var w=Math.round(box.clientWidth)||300;if(w===s.lw&&!force)return;s.lw=w;var h=Math.round(s.height(w));var dpr=Math.min(2,window.devicePixelRatio||1);s.W=w;s.H=h;cv.width=Math.round(w*dpr);cv.height=Math.round(h*dpr);cv.style.height=h+'px';ctx.setTransform(dpr,0,0,dpr,0,0);s.render();};
  var pb=fig.querySelector('[data-play]');
  s.sync=function(){if(pb)pb.textContent=s.playing?'暂停':'播放';};
  s.setPlaying=function(v){s.playing=v;s.sync();};
  if(pb)pb.addEventListener('click',function(){s.setPlaying(!s.playing);});
  s.sync();
  if('ResizeObserver' in window){new ResizeObserver(function(){s.resize(false);}).observe(box);}else{window.addEventListener('resize',function(){s.resize(false);});}
  if('IntersectionObserver' in window){new IntersectionObserver(function(es){es.forEach(function(e){s.visible=e.isIntersecting;});},{rootMargin:'80px'}).observe(fig);}
  stages.push(s);
  s.resize(true);
  return s;
}
function redrawAll(){readColors();stages.forEach(function(s){s.render();});}
try{window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change',redrawAll);}catch(e){}
new MutationObserver(redrawAll).observe(root,{attributes:true,attributeFilter:['data-theme','class','style']});
if(document.fonts&&document.fonts.ready){document.fonts.ready.then(redrawAll);}
function press(btn,on){btn.setAttribute('aria-pressed',on?'true':'false');}

/* ---------- loop ---------- */
var last=performance.now();
function loop(now){var dt=Math.min(0.05,(now-last)/1000);last=now;for(var i=0;i<stages.length;i++){var s=stages[i];if(s.visible&&s.playing){s.step(dt);s.render();}}requestAnimationFrame(loop);}
requestAnimationFrame(loop);

window.Sim={C:C,TAU:TAU,FONT:FONT,MONO:MONO,MATH:MATH,reduce:reduce,stages:stages,
  readColors:readColors,redrawAll:redrawAll,rgba:rgba,txt:txt,seg:seg,arrow:arrow,rrect:rrect,dot:dot,ring:ring,
  pole:pole,wire:wire,fieldLines:fieldLines,hbar:hbar,makeStage:makeStage,press:press,
  clamp:clamp,lerp:lerp,lambdaColor:lambdaColor};
})();
