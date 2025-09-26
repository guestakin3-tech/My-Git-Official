import React, {useEffect, useState} from 'react';
import axios from 'axios';
export default function App(){
  const [repos, setRepos] = useState([]);
  useEffect(()=>{axios.get('/api/repos/').then(r=>setRepos(r.data)).catch(()=>setRepos([]));},[]);
  return (
    <div style={{fontFamily:'sans-serif', padding:20}}>
      <h1>MyGit (MVP)</h1>
      <p>Simple frontend that lists repos via API (requires logged-in user and auth).</p>
      <ul>
        {repos.length===0 && <li>No repos (or API requires auth)</li>}
        {repos.map(r=>(<li key={r.id}>{r.owner_username}/{r.name} - {r.description}</li>))}
      </ul>
    </div>
  );
}
