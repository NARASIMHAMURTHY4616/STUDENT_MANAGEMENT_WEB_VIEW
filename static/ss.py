/* ===== GLOBAL ===== */
body {
    margin: 0;
    font-family: 'Segoe UI', sans-serif;
    background: linear-gradient(135deg, green, dodgerblue, blue);
    min-height: 100vh;
    color: white;
    font-size: 16px;
}
/* ===== NAVBAR ===== */
nav {
    background: rgba(15,23,42,0.75);
    backdrop-filter: blur(12px);
    padding: 15px 30px;
    display: flex;
    gap: 15px;
    justify-content: center;
}
nav a { color:#fef3c7; text-decoration:none; font-weight:600; padding:8px 16px; border-radius:10px; transition:0.3s;}
nav a:hover {background: rgba(251,191,36,0.25); color:#fff;}

/* ===== CARDS ===== */
.container, .content-card {
    background: rgba(255,255,255,0.25);
    backdrop-filter: blur(18px);
    padding: 35px;
    border-radius: 22px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.35);
    max-width: 900px; width:100%;
    animation: slideUp 0.6s ease;
}

/* ===== LISTS AS CARDS ===== */
ul.marks li {background:#22c55e;color:#052e16; padding:10px 15px; margin:10px 0; border-radius:12px;}
ul.attendance li {background:#3b82f6;color:#fff; padding:10px 15px; margin:10px 0; border-radius:12px;}
ul.connections li {background:#f59e0b;color:#1e293b; padding:10px 15px; margin:10px 0; border-radius:12px;}

/* ===== BUTTONS ===== */
button { width:100%; padding:14px; background: linear-gradient(135deg,#f59e0b,#fbbf24); border:none; color:#1e293b; font-size:16px; font-weight:bold; border-radius:14px; cursor:pointer; transition:0.3s;}
button:hover {transform:translateY(-2px); box-shadow:0 10px 25px rgba(251,191,36,0.6);}

/* ===== DASHBOARD FLOATING CARDS ===== */
.dashboard { display:grid; grid-template-columns: repeat(auto-fit,minmax(180px,1fr)); gap:20px; margin-top:30px; }
.dash-card { padding:20px; border-radius:20px; text-align:center; font-weight:bold; color:#1e293b; background:linear-gradient(135deg,#fbbf24,#f59e0b); text-decoration:none; transition:0.3s;}
.dash-card:hover {transform:translateY(-8px); box-shadow:0 15px 35px rgba(251,191,36,0.7);}
#abs{ 
border : 5 px solid linear-gradient(45deg,red,black,transparent);
background:linear-gradinet(45deg,transparent,black,red);
}

/* ===== ANIMATION ===== */
@keyframes slideUp { from{opacity:0; transform:translateY(30px);} to{opacity:1; transform:translateY(0);} }
