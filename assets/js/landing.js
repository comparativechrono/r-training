/* =====================================================================
   The landing page (index.html): the courses, how far the student has
   got with each (what each course's page saved in this browser), their
   name, and their certificates.
   ===================================================================== */
(function () {
  'use strict';
  const MG = window.MG;
  const { h, esc, bus } = MG;
  const CERT = (MG.config && MG.config.certificate) || {};
  const $ = (s, r) => (r || document).querySelector(s);

  function showName() {
    const n = MG.user.fullName();
    const t = $('[data-student-name-text]'), b = $('[data-name-btn]');
    if (t) {
      t.textContent = n || 'no name yet';
      t.classList.toggle('none', !n);
    }
    if (b) b.textContent = n ? 'Change' : 'Add your name';
  }

  function showCourse(card) {
    const id = card.dataset.course;
    const c = MG.cert.course(id);
    const st = MG.cert.status(id);
    if (!c || !st) return;
    card.classList.toggle('done', st.complete);
    card.classList.toggle('started', st.started && !st.complete);
    $('.cp-bar > i', card).style.width = st.pct + '%';
    $('.cp-text', card).textContent = st.complete
      ? `Finished on ${MG.cert.longDate(st.completedAt || Date.now())}`
      : st.started
        ? `${st.done} of ${st.total} steps and questions done (${st.pct}%)`
        : 'Not started yet';
    $('.course-go', card).textContent = st.complete ? 'Go back to the course' : st.started ? 'Carry on with the course' : 'Start the course';
    const box = $('.course-cert', card);
    box.innerHTML = '';
    if (st.complete) {
      box.append(
        h('button.btn', { type: 'button', html: MG.icon('download') + '<span>Download your certificate</span>', onclick: () => MG.cert.download(id) }),
        h('button.btn.small.linkish', { type: 'button', onclick: () => previewDialog(id) }, 'Preview')
      );
    } else {
      box.append(h('span.cert-lockline', { html: MG.icon('lock') + '<span>Your certificate is unlocked when you finish the course</span>' }));
    }
  }

  function previewDialog(id) {
    const c = MG.cert.course(id);
    const m = MG.modal(`Your certificate: ${c.title}`, '');
    m.box.classList.add('wide');
    const host = h('div.cert-prev-box');
    const acts = h('div.prompt-actions', h('button.btn', { type: 'button', onclick: () => MG.cert.nameDialog() }, 'Change the name'), h('span.grow'), h('button.btn.primary', { type: 'button', html: MG.icon('download') + '<span>Download (PDF)</span>', onclick: () => MG.cert.download(id) }));
    m.box.querySelector('.modal-b').append(host, acts);
    MG.cert.preview(host, id);
    const off = bus.on('user:name', () => MG.cert.preview(host, id));
    const x = m.box.querySelector('.modal-x');
    if (x) x.addEventListener('click', off);
  }

  function refresh() {
    showName();
    document.querySelectorAll('.course[data-course]').forEach(showCourse);
  }

  function init() {
    const dept = $('[data-awarded-by]');
    if (dept) dept.textContent = [CERT.awardedBy, CERT.institution].filter(Boolean).join(', ');
    const b = $('[data-name-btn]');
    if (b) b.addEventListener('click', () => MG.cert.nameDialog());
    bus.on('user:name', refresh);
    // (a course in another tab of this browser saved its progress, or a name)
    window.addEventListener('storage', refresh);
    window.addEventListener('pageshow', refresh);
    refresh();
    window.MG_READY = true;
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
