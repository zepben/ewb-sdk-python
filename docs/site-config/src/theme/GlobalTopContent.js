import React from 'react';

function GlobalTopContent() {
  return (
    <div style={{ backgroundColor: 'lightyellow', padding: '10px', textAlign: 'center' }}>
      🚨 This is an important announcement! 🚨
      <br/>
      This documentation site is no longer actively maintained. 
      <br/>
      For up-to-date documentation, see the new site at the <a href="https://zepben.github.io/evolve/docs/ewb-sdk-python/">EWB Python SDK</a> page. 
    </div>
  );
}

export default GlobalTopContent;
