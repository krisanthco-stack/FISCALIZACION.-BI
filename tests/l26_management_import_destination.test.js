const test=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const path=require('node:path');

function extractFunction(source,signature){
  const start=source.indexOf(signature);if(start<0)throw new Error(`Missing ${signature}`);
  const open=source.indexOf('{',start);let depth=0,quote=null,escape=false;
  for(let i=open;i<source.length;i++){
    const c=source[i];
    if(quote){if(escape)escape=false;else if(c==='\\')escape=true;else if(c===quote)quote=null;continue;}
    if(c==='"'||c==="'"||c==='`'){quote=c;continue;}
    if(c==='{')depth++;else if(c==='}'&&--depth===0)return source.slice(start,i+1);
  }
  throw new Error('unterminated function');
}

test('Excel/ZIP cargado desde Gestión queda fuera de Trámites activos',()=>{
  const html=fs.readFileSync(path.join(__dirname,'..','index.html'),'utf8');
  const fn=extractFunction(html,"function applyImportDestination(c,destination='tramites')");
  const ctx={structuredClone,normalizeCase:x=>structuredClone(x),Date};
  vm.createContext(ctx);vm.runInContext(fn,ctx);
  const active={id:'a',status:'Asignado',workflow:{stage:'field',history:[]},localBase:{visible:true},importMeta:{source:'excel'}};
  const management=ctx.applyImportDestination(active,'management');
  assert.equal(management.workflow.stage,'completed');
  assert.equal(management.status,'Finalizado');
  assert.equal(management.localBase.visible,false);
  assert.equal(management.importMeta.destinationModule,'management');
  assert.equal(active.workflow.stage,'field','no debe mutar el objeto fuente');
});

test('importación normal de Trámites no fuerza etapa de Gestión',()=>{
  const html=fs.readFileSync(path.join(__dirname,'..','index.html'),'utf8');
  const fn=extractFunction(html,"function applyImportDestination(c,destination='tramites')");
  const ctx={structuredClone,normalizeCase:x=>structuredClone(x),Date};
  vm.createContext(ctx);vm.runInContext(fn,ctx);
  const active={id:'b',status:'Asignado',workflow:{stage:'field',history:[]},localBase:{visible:true}};
  const result=ctx.applyImportDestination(active,'tramites');
  assert.equal(result.workflow.stage,'field');
  assert.equal(result.status,'Asignado');
  assert.equal(result.localBase.visible,true);
});
