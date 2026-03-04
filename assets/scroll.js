(function(){
  const els = document.querySelectorAll(".reveal, .reveal-zoom");
  if(!els.length) return;

  const reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if(reduce){
    els.forEach(el => el.classList.add("is-visible"));
    return;
  }

  const io = new IntersectionObserver((entries) => {
    for(const e of entries){
      if(e.isIntersecting){
        e.target.classList.add("is-visible");
        io.unobserve(e.target);
      }
    }
  }, { threshold: 0.18, rootMargin: "0px 0px -10% 0px" });

  els.forEach(el => io.observe(el));
})();
