import React, { useEffect, useState } from "react";

/*
  CONFIG: if you run the API elsewhere, change API_BASE
*/
const API_BASE = "http://127.0.0.1:5000";
const TABLES = ["users", "courses", "assignments"];

/* --- small API helpers --- */
async function apiGetAll(table) {
  const res = await fetch(`${API_BASE}/${table}`);
  if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);
  return res.json();
}
async function apiGetOne(table, id) {
  const res = await fetch(`${API_BASE}/${table}/${id}`);
  if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);
  return res.json();
}
async function apiQuery(table, params = {}) {
  const q = new URLSearchParams(params).toString();
  const res = await fetch(`${API_BASE}/${table}?${q}`);
  if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);
  return res.json();
}
async function apiCreate(table, body) {
  const res = await fetch(`${API_BASE}/${table}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);
  return res.json();
}
async function apiPut(table, id, body) {
  // may not be implemented on API — caller handles 404/405
  const res = await fetch(`${API_BASE}/${table}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body)
  });
  if (!res.ok) throw new Error(`${res.status} ${await res.text()}`);
  return res.json();
}

/* --- small components --- */
function TableCard({ table, onOpenAll, onOpenOne, onQuery }) {
  const [items, setItems] = useState(null);
  const [loading, setLoading] = useState(false);
  const [filterText, setFilterText] = useState("");

  useEffect(() => { loadAll(); /* eslint-disable-next-line */ }, [table]);

  async function loadAll() {
    setLoading(true);
    try { setItems(await apiGetAll(table)); }
    catch (e) { setItems({ error: e.message }); }
    finally { setLoading(false); }
  }

  return (
    <div className="card">
      <h3 style={{margin:0, textTransform:"capitalize"}}>{table}</h3>
      <div className="toolbar">
        <button className="button small" onClick={loadAll}>Refresh</button>
        <button className="button small" onClick={() => onOpenAll(table)}>Open all</button>
        <input placeholder="filter key=value" value={filterText} onChange={(e)=>setFilterText(e.target.value)} />
        <button className="button small" onClick={()=>{
          if (!filterText.includes("=")) { alert("use key=value"); return; }
          const [k,v] = filterText.split("=");
          onQuery(table, { [k.trim()]: v.trim() });
        }}>Query</button>
      </div>

      {loading && <div className="note">loading…</div>}
      {items && items.error && <div className="note" style={{color:"red"}}>{items.error}</div>}
      {items && Array.isArray(items) && (
        <div className="list">
          <table style={{width:"100%", borderCollapse:"collapse"}}>
            <thead><tr><th style={{textAlign:"left"}}>id</th><th style={{textAlign:"left"}}>preview</th><th></th></tr></thead>
            <tbody>
              {items.map(it => (
                <tr key={JSON.stringify(it)}>
                  <td style={{padding:"6px 4px", borderTop:"1px solid #eee"}}>{it.id ?? it.user_id ?? it.assignment_id ?? "-"}</td>
                  <td style={{padding:"6px 4px", borderTop:"1px solid #eee"}}>{JSON.stringify(it).slice(0,70)}{JSON.stringify(it).length>70?"...":""}</td>
                  <td style={{padding:"6px 4px", borderTop:"1px solid #eee"}}><button className="button small" onClick={()=>onOpenOne(table, it.id ?? it.assignment_id)}>Open</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

function AllView({ table, onBack }) {
  const [items, setItems] = useState(null);
  useEffect(()=>{ (async ()=>{ try{ setItems(await apiGetAll(table)); } catch(e){ setItems({error:e.message}) } })(); }, [table]);

  return (
    <div>
      <button className="button" onClick={onBack}>Back</button>
      <h2>All: {table}</h2>
      {items && items.error && <div className="note" style={{color:"red"}}>{items.error}</div>}
      {items && !items.error && <pre style={{background:"#fafafa", padding:12, maxHeight:400, overflow:"auto"}}>{JSON.stringify(items, null, 2)}</pre>}
    </div>
  );
}

function SingleView({ table, id, onBack }) {
  const [item, setItem] = useState(null);
  const [editing, setEditing] = useState(false);
  const [jsonText, setJsonText] = useState("");

  useEffect(()=>{ (async ()=>{
    try {
      setItem(await apiGetOne(table, id));
      setJsonText("");
    } catch(e) { setItem({ error: e.message }); }
  })(); }, [table, id]);

  async function save() {
    try {
      const parsed = JSON.parse(jsonText);
      await apiPut(table, id, parsed);
      alert("Saved (server PUT successful)");
      setEditing(false);
      setItem(await apiGetOne(table, id));
    } catch(err) {
      alert("Save failed: " + err.message + "\nNote: if your API doesn't support PUT, you need to add PUT endpoints in service.py");
    }
  }

  return (
    <div>
      <button className="button" onClick={onBack}>Back</button>
      <h2>{table} / {id}</h2>
      {item && item.error && <div className="note" style={{color:"red"}}>{item.error}</div>}
      {item && !editing && <div>
        <pre style={{background:"#fafafa", padding:12}}>{JSON.stringify(item, null, 2)}</pre>
        <div style={{marginTop:8}}>
          <button className="button" onClick={()=>{ setEditing(true); setJsonText(JSON.stringify(item, null, 2)); }}>Edit (raw JSON)</button>
        </div>
      </div>}
      {editing && <div>
        <textarea className="json" value={jsonText} onChange={(e)=>setJsonText(e.target.value)} />
        <div style={{marginTop:8}}>
          <button className="button primary" onClick={save}>Save via PUT</button>{" "}
          <button className="button" onClick={()=>setEditing(false)}>Cancel</button>
        </div>
      </div>}
    </div>
  );
}

function CreateForm({ table, onCreated }) {
  const [text, setText] = useState("{}");

  async function create() {
    try {
      const body = JSON.parse(text);
      const res = await apiCreate(table, body);
      alert("Created: " + JSON.stringify(res));
      onCreated && onCreated(res);
    } catch(e) { alert("Create error: " + e.message); }
  }

  return (
    <div className="card">
      <h4 style={{marginTop:0}}>Create {table}</h4>
      <p className="note">Paste a JSON object matching the table columns (example: <code>{"{ \"username\": \"alice\", \"email\": \"a@b.com\" }"}</code>)</p>
      <textarea className="json" value={text} onChange={(e)=>setText(e.target.value)} />
      <div style={{marginTop:8}}>
        <button className="button primary" onClick={create}>Create</button>
      </div>
    </div>
  );
}

/* --- Main App --- */
export default function App(){
  const [view, setView] = useState({name:"home"});
  const [queryResult, setQueryResult] = useState(null);

  function openAll(table){ setView({name:"all", table}); }
  function openSingle(table, id){ setView({name:"single", table, id}); }
  async function onQuery(table, params){
    try {
      const data = await apiQuery(table, params);
      setQueryResult({table, params, data});
      setView({name:"query"});
    } catch(e){ alert("Query failed: "+e.message); }
  }

  return (
    <div className="container">
      <header className="header">
        <div>
          <h1 style={{margin:0}}>Project 3 — Interactive Client</h1>
          <div className="note">API base: <code>{API_BASE}</code></div>
        </div>
        <div style={{textAlign:"right"}}>
          <div className="note">Tables: {TABLES.join(", ")}</div>
        </div>
      </header>

      {view.name === "home" && (
        <>
          <div className="grid">
            {TABLES.map(t => (
              <div key={t}>
                <TableCard table={t} onOpenAll={openAll} onOpenOne={openSingle} onQuery={onQuery} />
                <div style={{height:12}} />
                <CreateForm table={t} />
              </div>
            ))}
          </div>

          <div style={{marginTop:18}}>
            <p className="note">Tip: Use the create JSON to add rows. Click "Open all" to view entire table or "Open" to view a single record. Edit uses raw JSON and will call PUT (if available).</p>
          </div>
        </>
      )}

      {view.name === "all" && <AllView table={view.table} onBack={()=>setView({name:"home"})} />}
      {view.name === "single" && <SingleView table={view.table} id={view.id} onBack={()=>setView({name:"home"})} />}

      {view.name === "query" && (
        <div>
          <button className="button" onClick={()=>setView({name:"home"})}>Back</button>
          <h2>Query — {queryResult.table}</h2>
          <pre style={{background:"#fafafa", padding:12, maxHeight:400, overflow:"auto"}}>
            {JSON.stringify(queryResult.data, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}