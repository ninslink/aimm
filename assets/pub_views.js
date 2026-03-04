async function loadPublisherViews(){
  const els = document.querySelectorAll("[data-metrics-key]");
  if(!els.length) return;

  try{
    const r = await fetch("assets/frontiers_metrics.json", { cache: "no-store" });
    if(!r.ok) throw new Error("metrics json not found");
    const metrics = await r.json();

    for(const el of els){
      const key = el.getAttribute("data-metrics-key");
      const v = metrics && metrics[key] && typeof metrics[key].views === "number" ? metrics[key].views : null;
      el.textContent = (v === null) ? "Views: —" : `Views: ${v.toLocaleString()}`;
    }
  }catch(e){
    for(const el of els){
      el.textContent = "Views: —";
    }
  }
}

document.addEventListener("DOMContentLoaded", loadPublisherViews);
