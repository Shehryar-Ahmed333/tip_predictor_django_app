(function () {
  "use strict";

  var form = document.getElementById("tip-form");
  var bill = document.getElementById("total_bill");
  var slider = document.getElementById("bill_range");
  var size = document.getElementById("size");
  var receipt = document.getElementById("receipt");
  var statusEl = document.getElementById("status");
  var submitBtn = form.querySelector(".go");
  var DAYS = { Thur: "Thursday", Fri: "Friday", Sat: "Saturday", Sun: "Sunday" };
  var SCALE_MAX = 10;
  var timer = null;
  var requestId = 0;
  var shown = 0;
  var printed = false;

  function money(n) { return "$" + Number(n).toFixed(2); }
  function $(id) { return document.getElementById(id); }
  function val(name) { return form.querySelector('input[name="' + name + '"]:checked').value; }

  function clearErrors() {
    form.querySelectorAll("[data-error]").forEach(function (el) { el.textContent = ""; });
    statusEl.textContent = "";
  }

  function updateSlip() {
    var b = parseFloat(bill.value);
    $("r-bill").textContent = isNaN(b) ? "–" : money(b);
    $("r-size").textContent = size.value || "–";
    $("r-meta").textContent = DAYS[val("day")] + " " + val("time").toLowerCase();
  }

  function countTo(el, target) {
    var from = shown, start = null, dur = 450;
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      el.textContent = money(target); shown = target; return;
    }
    function frame(t) {
      if (start === null) start = t;
      var p = Math.min((t - start) / dur, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = money(from + (target - from) * eased);
      if (p < 1) requestAnimationFrame(frame); else shown = target;
    }
    requestAnimationFrame(frame);
  }

  function render(d) {
    countTo($("r-tip"), d.tip);
    $("r-pct").textContent = d.tip_percent + "%";
    $("r-pp").textContent = money(d.per_person);
    $("r-total").textContent = money(d.total);
    var lo = Math.min(d.low / SCALE_MAX, 1) * 100;
    var hi = Math.min(d.high / SCALE_MAX, 1) * 100;
    $("r-band").style.left = lo + "%";
    $("r-band").style.width = Math.max(hi - lo, 2) + "%";
    $("r-dot").style.left = Math.min(d.tip / SCALE_MAX, 1) * 100 + "%";
    $("r-range").textContent = "Likely between " + money(d.low) + " and " + money(d.high) + ".";
    if (!printed) {
      printed = true;
      receipt.classList.add("print");
    }
  }

  function predict() {
    clearErrors();
    updateSlip();
    var id = ++requestId;
    submitBtn.disabled = true;
    fetch(form.action, {
      method: "POST",
      body: new FormData(form),
      headers: { "X-Requested-With": "XMLHttpRequest" },
      credentials: "same-origin"
    })
      .then(function (res) { return res.json().then(function (data) { return { status: res.status, data: data }; }); })
      .then(function (r) {
        if (id !== requestId) return;
        if (r.data.ok) { render(r.data); return; }
        var errs = r.data.errors || {};
        Object.keys(errs).forEach(function (k) {
          var el = form.querySelector('[data-error="' + k + '"]');
          if (el) el.textContent = errs[k]; else statusEl.textContent = errs[k];
        });
      })
      .catch(function () {
        if (id === requestId) statusEl.textContent = "Could not reach the server. Check that it is running, then try again.";
      })
      .finally(function () { if (id === requestId) submitBtn.disabled = false; });
  }

  function schedule() {
    updateSlip();
    clearTimeout(timer);
    timer = setTimeout(predict, 250);
  }

  // Keep the number box and slider in sync.
  bill.addEventListener("input", function () {
    var b = parseFloat(bill.value);
    if (!isNaN(b)) slider.value = Math.min(Math.max(b, slider.min), slider.max);
    schedule();
  });
  slider.addEventListener("input", function () {
    bill.value = parseFloat(slider.value).toFixed(2);
    schedule();
  });

  size.addEventListener("input", schedule);
  form.querySelectorAll('input[type="radio"]').forEach(function (r) { r.addEventListener("change", schedule); });
  form.querySelectorAll("[data-step]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var n = parseInt(size.value, 10) || 1;
      size.value = Math.min(12, Math.max(1, n + parseInt(btn.dataset.step, 10)));
      schedule();
    });
  });

  form.addEventListener("submit", function (e) { e.preventDefault(); clearTimeout(timer); predict(); });

  predict();
})();
