const API_URL = 'https://renewwise-backend.onrender.com'; // change to your backend
document.getElementById('apiUrl').textContent = API_URL;

async function checkHealth(){
  const el=document.getElementById('health');
  try{
    const res=await fetch(API_URL+'/api/health');
    const d=await res.json();
    el.textContent='API OK: '+(d.status||'ok'); el.className='health ok';
  }catch{ el.textContent='API unreachable'; el.className='health fail'; }
}
async function loadDocs(){
  const list=document.getElementById('docsList');
  try{
    const res=await fetch(API_URL+'/api/documents');
    const docs=await res.json();
    if(!docs.length){list.textContent='No docs yet';return;}
    list.innerHTML=docs.map(x=>`<div class="doc"><span>${x.name||x.filename}</span><small>${x.status||'authorized'}</small></div>`).join('');
  }catch{ list.textContent='Could not load /api/documents - check backend routes'; }
}
async function upload(){
  const f=document.getElementById('fileInput').files[0];
  const s=document.getElementById('uploadStatus');
  if(!f){s.textContent='Pick a file';return;}
  const fd=new FormData(); fd.append('file',f);
  s.textContent='Uploading...';
  try{
    const res=await fetch(API_URL+'/api/documents/upload',{method:'POST',body:fd});
    const d=await res.json(); s.textContent='Success: '+JSON.stringify(d).slice(0,100); loadDocs();
  }catch(e){ s.textContent='Failed - your backend may use /api/upload'; }
}
document.getElementById('uploadBtn').onclick=upload;
document.getElementById('refreshBtn').onclick=loadDocs;
checkHealth(); loadDocs();
