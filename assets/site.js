
(function(){
  const faqItems=[...document.querySelectorAll('.faq details')];
  faqItems.forEach(d=>d.addEventListener('toggle',()=>{
    if(d.open) faqItems.forEach(o=>{if(o!==d)o.open=false});
  }));
const form=document.getElementById('projectForm');
  if(form){
    form.addEventListener('submit',function(e){
      e.preventDefault();
      const type=form.querySelector('[name="type"]')?.value||'';
      const details=form.querySelector('[name="details"]')?.value||'';
      const budget=form.querySelector('[name="budget"]')?.value||'';
      const timing=form.querySelector('[name="timing"]')?.value||'';
      const lang=document.documentElement.lang||'fr';
      const headers={fr:'Bonjour MAQTA, je souhaite discuter d’un projet.',en:'Hello MAQTA, I would like to discuss a project.',ar:'مرحبًا MAQTA، أرغب في مناقشة مشروع.'};
      const labels={fr:['Type','Détails','Budget','Délai'],en:['Type','Details','Budget','Timing'],ar:['نوع المشروع','التفاصيل','الميزانية','الموعد']};
      const l=labels[lang]||labels.fr;
      let msg=headers[lang]||headers.fr;
      if(type) msg+='\n'+l[0]+': '+type;
      if(details) msg+='\n'+l[1]+': '+details;
      if(budget) msg+='\n'+l[2]+': '+budget;
      if(timing) msg+='\n'+l[3]+': '+timing;
      window.open('https://wa.me/212639879506?text='+encodeURIComponent(msg),'_blank','noopener');
    });
  }
})();
