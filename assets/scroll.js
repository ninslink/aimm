
const els=document.querySelectorAll('.reveal');
const obs=new IntersectionObserver(entries=>{
entries.forEach(e=>{
if(e.isIntersecting){e.target.classList.add('visible')}
})
},{threshold:.2});
els.forEach(el=>obs.observe(el));
