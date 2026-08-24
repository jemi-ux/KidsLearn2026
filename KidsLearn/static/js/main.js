
document.addEventListener("DOMContentLoaded",()=>{
  document.querySelectorAll("[data-progress]").forEach(b=>b.style.width=Math.max(0,Math.min(100,Number(b.dataset.progress||0)))+"%");
  document.querySelectorAll(".option").forEach(o=>o.addEventListener("click",()=>{
    const r=o.querySelector("input"); if(r){r.checked=true;o.parentElement.querySelectorAll(".option").forEach(x=>x.style.borderColor="");o.style.borderColor="#7467e8";}
  }));
  const speech=(text,lang)=>{
    if(!("speechSynthesis" in window)) return;
    speechSynthesis.cancel(); const u=new SpeechSynthesisUtterance(text); u.lang=lang==="en"?"en-US":"fr-FR"; u.rate=.9; speechSynthesis.speak(u);
  };
  document.querySelectorAll("[data-speak]").forEach(b=>b.addEventListener("click",()=>speech(b.dataset.speak,b.dataset.lang||"fr")));
  const game=document.querySelector("[data-letter-game]");
  if(game){
    const letters=["A","B","C","M","L","S"], target=letters[Math.floor(Math.random()*letters.length)];
    game.innerHTML=`<div><div class="muted">Trouve la lettre / Find the letter</div><div class="letter" data-target="${target}">${target}</div><p id="game-feedback"></p></div>`;
    const feedback=game.querySelector("#game-feedback");
    game.querySelector(".letter").onclick=()=>{feedback.textContent="🎉 Bravo ! Great job!"; feedback.style.color="#3d8a58";}
  }
});

// Mini IA : choix du niveau puis avis de l'enfant.
const ai=document.querySelector('[data-ai-widget]');
if(ai){
  const msg=ai.querySelector('#ai-message'), levels=ai.querySelector('[data-ai-level]'), feedback=ai.querySelector('[data-ai-feedback]');
  const post=(data)=>fetch('/api/ai/feedback',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams(data)}).then(r=>r.json());
  ai.querySelectorAll('[data-level]').forEach(b=>b.addEventListener('click',()=>{
    ai.querySelectorAll('[data-level]').forEach(x=>x.disabled=true); const level=b.dataset.level;
    post({level}).then(d=>{msg.textContent=d.message;levels.classList.add('hidden');feedback.classList.remove('hidden');msg.textContent=location.pathname.includes('/en')?msg.textContent:'Quelque chose de simple : est-ce que tu apprécies KidsLearn ?';});
  }));
  ai.querySelectorAll('[data-liked]').forEach(b=>b.addEventListener('click',()=>post({level:'',liked:b.dataset.liked}).then(d=>{msg.textContent=d.message;feedback.innerHTML='<b>⭐ Merci pour ton avis !</b>';feedback.querySelector('b').setAttribute('aria-live','polite');})));
}

// Trois mini-jeux réellement jouables.
const gameArea=document.querySelector('[data-game-area]');
if(gameArea){
  const lang=gameArea.dataset.lang||'fr'; let score=0;
  const T=(fr,en)=>lang==='fr'?fr:en;
  const renderLetters=()=>{const letters=['A','B','C','D','M','L','S','P'];const target=letters[Math.floor(Math.random()*letters.length)];gameArea.innerHTML=`<h2>🔤 ${T('Trouve la lettre','Find the letter')}: <b>${target}</b></h2><div class="game-grid">${letters.sort(()=>Math.random()-.5).map(x=>`<button class="game-option" data-x="${x}">${x}</button>`).join('')}</div><p class="game-feedback"></p><p class="game-score">⭐ ${T('Score','Score')}: ${score}</p>`;gameArea.querySelectorAll('[data-x]').forEach(b=>b.onclick=()=>{const f=gameArea.querySelector('.game-feedback');if(b.dataset.x===target){score++;f.textContent=T('🎉 Bravo !','🎉 Great job!');f.style.color='#3d8a58';}else{f.textContent=T('Essaie encore !','Try again!');}setTimeout(renderLetters,650);});};
  const renderSyllables=()=>{const items=[['ma','man'],['pa','papa'],['la','lama'],['mi','mimi'],['sa','sac']];const item=items[Math.floor(Math.random()*items.length)];gameArea.innerHTML=`<h2>🧩 ${T('Choisis la syllabe qui commence le mot','Choose the syllable that starts the word')}</h2><div class="word-card">${item[1]}</div><div class="game-grid">${[item[0],['ba','ta','lo','ri'][Math.floor(Math.random()*4)]].sort(()=>Math.random()-.5).map(x=>`<button class="game-option" data-s="${x}">${x}</button>`).join('')}</div><p class="game-feedback"></p>`;gameArea.querySelectorAll('[data-s]').forEach(b=>b.onclick=()=>{const f=gameArea.querySelector('.game-feedback');f.textContent=b.dataset.s===item[0]?T('🎉 Bravo !','🎉 Great job!'):T('Pas tout à fait.','Not quite.');if(b.dataset.s===item[0])score++;setTimeout(renderSyllables,700);});};
  const renderDuo=()=>{const pairs=[['chat','cat'],['chien','dog'],['maison','house'],['livre','book'],['soleil','sun']];const pair=pairs[Math.floor(Math.random()*pairs.length)];const target=pair[0];const opts=[pair[1],pairs[(pairs.indexOf(pair)+1)%pairs.length][1],pairs[(pairs.indexOf(pair)+2)%pairs.length][1]].sort(()=>Math.random()-.5);gameArea.innerHTML=`<h2>🌍 ${T('Trouve le mot anglais','Find the English word')}</h2><div class="word-card">${target}</div><div class="game-grid">${opts.map(x=>`<button class="game-option" data-en="${x}">${x}</button>`).join('')}</div><p class="game-feedback"></p>`;gameArea.querySelectorAll('[data-en]').forEach(b=>b.onclick=()=>{const f=gameArea.querySelector('.game-feedback');if(b.dataset.en===pair[1]){score++;f.textContent=T('🎉 Excellent !','🎉 Excellent!');}else f.textContent=T('Essaie encore !','Try again!');setTimeout(renderDuo,700);});};
  const renderAvatar=()=>{
    const avatars=[['🧒','Explorateur'],['🧑‍🚀','Astronaute'],['🦸','Super-héros'],['🧙','Magicien']];
    const challenges=[
      ['Combien font 2 + 2 ?','What is 2 + 2?',['3','4','5'],'4'],
      ['Quelle lettre vient après A ?','Which letter comes after A?',['B','C','D'],'B'],
      ['Quel est le mot anglais pour « chat » ?','What is the English word for « chat »?',['dog','cat','sun'],'cat'],
      ['Quelle couleur obtient-on avec bleu + jaune ?','What color do blue + yellow make?',['vert / green','rouge / red','rose / pink'],'vert / green']
    ];
    const chosen=localStorage.getItem('kidslearn_avatar')||'🧒';
    const avatarName=avatars.find(a=>a[0]===chosen)?.[1]||'Explorateur';
    const challenge=challenges[Math.floor(Math.random()*challenges.length)];
    gameArea.innerHTML=`<h2>🧑‍🚀 ${T('Aventure Avatar','Avatar Adventure')}</h2>
      <p>${T('Choisis ton avatar, puis réussis le défi pour gagner une étoile !','Choose your avatar, then solve the challenge to earn a star!')}</p>
      <div class="game-grid avatar-choices">${avatars.map(a=>`<button class="game-option avatar-choice ${a[0]===chosen?'selected':''}" data-avatar="${a[0]}">${a[0]}<br><small>${T(a[1],a[1])}</small></button>`).join('')}</div>
      <div class="word-card" style="font-size:3rem">${chosen}</div>
      <h3>${T(challenge[0],challenge[1])}</h3>
      <div class="game-grid">${challenge[2].sort(()=>Math.random()-.5).map(x=>`<button class="game-option" data-answer="${x}">${x}</button>`).join('')}</div>
      <p class="game-feedback"></p><p class="game-score">⭐ ${T('Score','Score')}: ${score}</p>`;
    gameArea.querySelectorAll('[data-avatar]').forEach(b=>b.onclick=()=>{localStorage.setItem('kidslearn_avatar',b.dataset.avatar);renderAvatar();});
    gameArea.querySelectorAll('[data-answer]').forEach(b=>b.onclick=()=>{
      const f=gameArea.querySelector('.game-feedback');
      if(b.dataset.answer===challenge[3]){score++;f.textContent=T('🎉 Bravo ! Ton avatar gagne une étoile !','🎉 Great job! Your avatar earns a star!');f.style.color='#3d8a58';}
      else{f.textContent=T('💪 Essaie encore !','💪 Try again!');f.style.color='#c46b2b';}
      setTimeout(renderAvatar,900);
    });
  };
  const start=(name)=>({letters:renderLetters,syllables:renderSyllables,duo:renderDuo,avatar:renderAvatar}[name]||renderLetters)();
  document.querySelectorAll('[data-game]').forEach(b=>b.addEventListener('click',()=>{document.querySelectorAll('.game-tab').forEach(x=>x.classList.remove('purple','active'));b.classList.add('purple','active');start(b.dataset.game);})); start('letters');
}
