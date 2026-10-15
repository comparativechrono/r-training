/* =====================================================================
   Certificates, and the student's name.

   A course's certificate is unlocked when every step and question of the
   course is done (those marked "if you have time" don't count). It shows
   the name the student gives with the button at the top of the page, which
   is kept in this browser for the whole site (MG.user.fullName). The
   certificate is a PDF made here, in the browser, by pdf-lib with its fonts
   embedded (EB Garamond, and Great Vibes for the signature), and the page
   shows it with PDF.js. Nothing is sent anywhere.

   Used by the course pages (the last chapter, and a message when the
   course is finished) and by the landing page (index.html).
     MG.cert.status(id)          → { done, total, pct, complete, completedAt, started }
     MG.cert.nameDialog()        → a promise of the name ('' if none was given)
     MG.cert.pdf(id, name, date) → the certificate's bytes
     MG.cert.download(id)        the PDF, as a file
     MG.cert.preview(host, id)   draws the certificate into host
   ===================================================================== */
(function () {
  'use strict';
  const MG = window.MG;
  const { h, esc, toast, bus, siteStore } = MG;
  const CFG = MG.config;
  const CERT = Object.assign({ awardedBy: '', institution: '', signatory: '', signatoryRole: '' }, CFG.certificate || {});
  const COURSES = window.RT_COURSES || [];
  const abs = (p) => new URL(p, location.href).href;

  const course = (id) => COURSES.find((c) => c.id === id) || null;

  /* ------------------------------------------------------------------
     how far a student has got with a course
     ------------------------------------------------------------------ */
  /** what the course's page saved: its ticks and answers (the live state when it is this page) */
  function saved(c) {
    if (MG.tutorial && MG.tutorial.state && document.body.dataset.course === c.id) return MG.tutorial.state;
    return siteStore.get(c.dataPage + ':progress', null) || { tasks: {}, answers: {} };
  }
  function status(id) {
    const c = course(id);
    if (!c) return null;
    const st = saved(c);
    const tasks = st.tasks || {}, answers = st.answers || {};
    let done = 0;
    c.tasks.forEach((t) => tasks[t] && done++);
    c.questions.forEach((q) => answers[q] && answers[q].done && done++);
    const total = c.tasks.length + c.questions.length;
    const anyTouched = Object.keys(tasks).length > 0 || Object.keys(answers).length > 0;
    return {
      done,
      total,
      pct: total ? Math.round((done / total) * 100) : 0,
      // (once finished, a course stays finished: unticking a step, or a step added to the course later, doesn't
      // lock the certificate again; only "Start again" does)
      complete: !!st.completedAt || (total > 0 && done === total),
      completedAt: st.completedAt || null,
      started: anyTouched
    };
  }

  /* ------------------------------------------------------------------
     the student's name
     ------------------------------------------------------------------ */
  /** asks for the student's name → a promise of the name kept ('' if there is none) */
  function nameDialog(opts = {}) {
    return new Promise((resolve) => {
      const cur = MG.user.fullName();
      let settled = false;
      const m = MG.modal(opts.title || 'Your name', '', {
        onClose: () => {
          if (!settled) {
            settled = true;
            resolve(MG.user.fullName());
          }
        }
      });
      const input = h('input.prompt-input#studentNameIn', { type: 'text', value: cur, placeholder: 'For example, Ada Lovelace', maxlength: String(MG.user.MAX + 10), spellcheck: 'false', autocomplete: 'name', 'aria-describedby': 'studentNameNote' });
      const preview = h('span.name-prev-name');
      const note = h('p.user-note#studentNameNote', { 'aria-live': 'polite' });
      const save = h('button.btn.primary', { type: 'submit' }, 'Save');
      const cancel = h('button.btn', { type: 'button' }, 'Cancel');
      const form = h(
        'form.user-form',
        h('p', opts.why || 'Type your name as you would like it to appear on your certificates.'),
        h('label.user-label', { for: 'studentNameIn' }, 'Your name'),
        input,
        h('p.name-prev', h('span.muted', 'Your certificate will say: '), h('i', 'This is to certify that '), preview),
        note,
        h('p.hint', 'Your name is kept in this web browser only. It isn’t sent anywhere: if you ask the AI assistant a question, your name is replaced by “user” in what is sent.'),
        h('div.prompt-actions', h('span.grow'), cancel, save)
      );
      m.box.querySelector('.modal-b').appendChild(form);
      let chosen = cur;
      const update = () => {
        const n = MG.user.cleanName(input.value);
        note.classList.toggle('bad', n == null);
        if (n == null) note.textContent = `That is too long: a name can have at most ${MG.user.MAX} characters.`;
        else note.textContent = '';
        chosen = n;
        preview.textContent = n || '…';
        preview.classList.toggle('muted', !n);
        save.disabled = n == null;
      };
      input.addEventListener('input', update);
      update();
      form.addEventListener('submit', (e) => {
        e.preventDefault();
        if (chosen == null) return;
        const kept = MG.user.setFullName(chosen);
        if (kept == null) return;
        settled = true;
        m.close();
        if (kept) toast(`Saved. Your certificates will show the name <b>${esc(kept)}</b>.`, 'ok', 3500);
        resolve(kept);
      });
      cancel.addEventListener('click', () => m.close());
      setTimeout(() => {
        input.focus();
        input.select();
      }, 30);
    });
  }

  /* ------------------------------------------------------------------
     the certificate, as a PDF
     ------------------------------------------------------------------ */
  const FONTS = {
    serif: 'assets/fonts/EBGaramond-Regular.ttf',
    bold: 'assets/fonts/EBGaramond-SemiBold.ttf',
    italic: 'assets/fonts/EBGaramond-Italic.ttf',
    script: 'assets/fonts/GreatVibes-Regular.ttf'
  };
  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const s = document.createElement('script');
      s.src = abs(src);
      s.onload = () => resolve();
      s.onerror = () => reject(new Error('Could not load ' + src + '. Check your internet connection and try again.'));
      document.head.appendChild(s);
    });
  }
  let libs = null;
  /** pdf-lib, fontkit and the fonts, loaded the first time a certificate is made */
  function loadLibs() {
    if (!libs) {
      libs = (async () => {
        if (!window.PDFLib) await loadScript('assets/vendor/pdf-lib/pdf-lib.min.js');
        if (!window.fontkit) await loadScript('assets/vendor/pdf-lib/fontkit.umd.min.js');
        const fonts = {};
        await Promise.all(
          Object.entries(FONTS).map(async ([k, url]) => {
            const r = await fetch(abs(url));
            if (!r.ok) throw new Error('Could not load the certificate’s fonts. Check your internet connection and try again.');
            fonts[k] = new Uint8Array(await r.arrayBuffer());
          })
        );
        return fonts;
      })();
      libs.catch(() => (libs = null));
    }
    return libs;
  }

  const longDate = (d) => new Date(d).toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });

  /** the name, drawn by the browser with its own fonts – for a name in a script that EB Garamond doesn't have */
  function nameImage(text, px) {
    const scale = 4;
    const font = `600 ${px * scale}px "Noto Serif", "Times New Roman", serif`;
    const c = document.createElement('canvas');
    const g = c.getContext('2d');
    g.font = font;
    const w = Math.ceil(g.measureText(text).width) + 8 * scale;
    c.width = Math.max(1, w);
    c.height = Math.ceil(px * scale * 1.5);
    g.font = font;
    g.fillStyle = '#1b2340';
    g.textBaseline = 'alphabetic';
    g.fillText(text, 4 * scale, Math.round(px * scale * 1.1));
    return { url: c.toDataURL('image/png'), width: c.width / scale, height: c.height / scale, baseline: px * 1.1 };
  }

  /** the certificate of course id for name, finished on date → the PDF's bytes */
  async function pdf(id, name, date) {
    const c = course(id);
    if (!c) throw new Error('There is no course called ' + id + '.');
    const fonts = await loadLibs();
    const { PDFDocument, rgb } = window.PDFLib;
    const doc = await PDFDocument.create();
    doc.registerFontkit(window.fontkit);
    const F = {};
    // (whole fonts: they are already cut down to the alphabets they need, and pdf-lib's own subsetting loses many
    // of EB Garamond's letters)
    for (const k of Object.keys(fonts)) F[k] = await doc.embedFont(fonts[k], { subset: false });
    const W = 841.89, H = 595.28; // A4, landscape
    const page = doc.addPage([W, H]);
    const NAVY = rgb(27 / 255, 35 / 255, 64 / 255), ACCENT = rgb(11 / 255, 107 / 255, 138 / 255), MUTED = rgb(74 / 255, 85 / 255, 104 / 255), RULE = rgb(176 / 255, 186 / 255, 200 / 255);
    const top = (y) => H - y; // (the layout below measures from the top of the page)
    const centre = (text, y, font, size, color) => {
      const w = font.widthOfTextAtSize(text, size);
      page.drawText(text, { x: (W - w) / 2, y: top(y), size, font, color });
      return w;
    };
    const centreAt = (cx, text, y, font, size, color) => {
      const w = font.widthOfTextAtSize(text, size);
      page.drawText(text, { x: cx - w / 2, y: top(y), size, font, color });
    };
    const rule = (x1, x2, y, color, thickness) => page.drawLine({ start: { x: x1, y: top(y) }, end: { x: x2, y: top(y) }, thickness, color });
    const wrap = (text, font, size, max) => {
      const lines = [];
      let line = '';
      text.split(/\s+/).forEach((w) => {
        const t = line ? line + ' ' + w : w;
        if (font.widthOfTextAtSize(t, size) <= max || !line) line = t;
        else {
          lines.push(line);
          line = w;
        }
      });
      if (line) lines.push(line);
      return lines;
    };
    /** the same number of lines as wrap() gives, but as nearly equal in length as they can be (no word left alone) */
    const balanced = (text, font, size, max) => {
      const n = wrap(text, font, size, max).length;
      if (n < 2) return wrap(text, font, size, max);
      let lo = font.widthOfTextAtSize(text, size) / n, hi = max;
      for (let i = 0; i < 24; i++) {
        const mid = (lo + hi) / 2;
        if (wrap(text, font, size, mid).length > n) lo = mid;
        else hi = mid;
      }
      return wrap(text, font, size, hi);
    };

    // the frame
    page.drawRectangle({ x: 22, y: 22, width: W - 44, height: H - 44, borderColor: NAVY, borderWidth: 2.2 });
    page.drawRectangle({ x: 30, y: 30, width: W - 60, height: H - 60, borderColor: ACCENT, borderWidth: 0.8 });

    // who awards it
    if (CERT.awardedBy) centre(CERT.awardedBy, 88, F.bold, 17, NAVY);
    if (CERT.institution) centre(CERT.institution, 110, F.serif, 13.5, MUTED);
    rule(W / 2 - 32, W / 2 + 32, 128, ACCENT, 0.8);

    centre('Certificate of Completion', 188, F.italic, 46, NAVY);
    centre('This is to certify that', 232, F.serif, 15, MUTED);

    // the name: as large as fits; in the browser's own fonts if EB Garamond hasn't got its letters
    const fk = F.bold.embedder && F.bold.embedder.font;
    const covered = !fk || Array.from(name).every((ch) => /\s/.test(ch) || fk.hasGlyphForCodePoint(ch.codePointAt(0)));
    let size = 38;
    if (covered) {
      while (size > 18 && F.bold.widthOfTextAtSize(name, size) > 620) size -= 1;
      centre(name, 286, F.bold, size, NAVY);
    } else {
      let img = nameImage(name, size);
      while (size > 18 && img.width > 620) img = nameImage(name, --size);
      const png = await doc.embedPng(img.url);
      page.drawImage(png, { x: (W - img.width) / 2, y: top(286) - (img.height - img.baseline), width: img.width, height: img.height });
    }
    rule(W / 2 - 240, W / 2 + 240, 300, RULE, 0.6);

    centre('has successfully completed the course', 330, F.serif, 15, MUTED);
    centre(c.title, 368, F.bold, 28, NAVY);
    centre(c.programme, 392, F.italic, 14, MUTED);
    balanced(c.certSummary, F.serif, 12.5, 560).slice(0, 2).forEach((l, i) => centre(l, 420 + i * 16, F.serif, 12.5, MUTED));

    // the date, on the left
    const L = 236, R = W - 236, base = 506;
    centreAt(L, longDate(date), base - 8, F.serif, 15, NAVY);
    rule(L - 92, L + 92, base, NAVY, 0.6);
    centreAt(L, 'Date of completion', base + 16, F.serif, 10.5, MUTED);

    // the signature, on the right
    if (CERT.signatory) {
      centreAt(R, CERT.signatory, base - 9, F.script, 34, NAVY);
      rule(R - 92, R + 92, base, NAVY, 0.6);
      centreAt(R, CERT.signatory, base + 16, F.serif, 11.5, NAVY);
      const role = CERT.signatoryRole || CERT.awardedBy;
      if (role) centreAt(R, role, base + 30, F.italic, 10, MUTED);
    }

    // the seal, between them
    const sx = W / 2, sy = top(492);
    page.drawCircle({ x: sx, y: sy, size: 36, borderColor: ACCENT, borderWidth: 1.4 });
    page.drawCircle({ x: sx, y: sy, size: 31, borderColor: ACCENT, borderWidth: 0.5 });
    const rw = F.bold.widthOfTextAtSize('R', 30);
    page.drawText('R', { x: sx - rw / 2, y: sy - 4, size: 30, font: F.bold, color: NAVY });
    const pw = F.italic.widthOfTextAtSize(c.seal, 8.5);
    page.drawText(c.seal, { x: sx - pw / 2, y: sy - 16, size: 8.5, font: F.italic, color: MUTED });

    doc.setTitle(`Certificate of Completion – ${c.title} – ${name}`);
    doc.setSubject(`${c.title}: ${c.programme}`);
    doc.setAuthor([CERT.awardedBy, CERT.institution].filter(Boolean).join(', '));
    doc.setCreator(CFG.courseTitle || 'R training');
    doc.setLanguage('en-GB');
    doc.setCreationDate(new Date());
    return doc.save();
  }

  /** the certificate's file name: certificate-r-basics-Ada-Lovelace.pdf */
  function fileName(id, name) {
    const slug = String(name).normalize('NFKD').replace(/[̀-ͯ]/g, '').replace(/[^A-Za-z0-9]+/g, '-').replace(/^-+|-+$/g, '').toLowerCase();
    return `certificate-${id}${slug ? '-' + slug : ''}.pdf`;
  }

  /** a name to put on a certificate: the one kept, or asked for */
  async function nameForCertificate() {
    let name = MG.user.fullName();
    if (!name) name = await nameDialog({ title: 'Your name on the certificate', why: 'Your certificate needs your name. Type it as you would like it to appear.' });
    return name;
  }

  /** the PDF, as a file in the Downloads folder */
  async function download(id) {
    const st = status(id);
    if (!st || !st.complete) {
      toast('Finish every step and question of the course first, and your certificate will be ready.', 'warn', 5000);
      return false;
    }
    const name = await nameForCertificate();
    if (!name) return false;
    try {
      const bytes = await pdf(id, name, st.completedAt || new Date().toISOString());
      MG.downloadBlob(new Blob([bytes], { type: 'application/pdf' }), fileName(id, name));
      bus.emit('cert:download', { id });
      toast('Your certificate has been saved as a PDF in your downloads.', 'ok', 4000);
      return true;
    } catch (e) {
      console.error(e);
      toast(esc(e.message || String(e)), 'error');
      return false;
    }
  }

  let pdfjs = null;
  function loadPdfjs() {
    if (MG.pdfView && MG.pdfView.load) return MG.pdfView.load();
    if (!pdfjs) {
      pdfjs = import(abs('assets/vendor/pdfjs/pdf.min.mjs')).then((m) => {
        m.GlobalWorkerOptions.workerSrc = abs('assets/vendor/pdfjs/pdf.worker.min.mjs');
        return m;
      });
      pdfjs.catch(() => (pdfjs = null));
    }
    return pdfjs;
  }
  /** draws the certificate (as the PDF will be) into host */
  async function preview(host, id) {
    const st = status(id);
    const name = MG.user.fullName();
    host.innerHTML = '';
    host.classList.add('cert-preview');
    const wait = h('div.cert-wait', h('span.spinner'), h('span', 'Drawing your certificate…'));
    host.appendChild(wait);
    try {
      const bytes = await pdf(id, name || 'Your name', (st && st.completedAt) || new Date().toISOString());
      const lib = await loadPdfjs();
      const task = lib.getDocument({ data: bytes.slice(), isEvalSupported: false, enableXfa: false });
      const d = await task.promise;
      const pg = await d.getPage(1);
      const w = Math.max(280, host.clientWidth || 560);
      const vp1 = pg.getViewport({ scale: 1 });
      // (drawn at twice the size it is shown at, or more, so that the small print stays sharp)
      const ratio = Math.max(2, Math.min(window.devicePixelRatio || 1, 3));
      const vp = pg.getViewport({ scale: (w / vp1.width) * ratio });
      const canvas = h('canvas.cert-canvas', { role: 'img', 'aria-label': `Your certificate for ${course(id).title}, with the name ${name || '(no name yet)'}` });
      canvas.width = Math.round(vp.width);
      canvas.height = Math.round(vp.height);
      canvas.style.width = '100%';
      await pg.render({ canvasContext: canvas.getContext('2d'), viewport: vp }).promise;
      task.destroy().catch(() => {});
      host.innerHTML = '';
      host.appendChild(canvas);
      bus.emit('cert:preview', { id });
    } catch (e) {
      console.error(e);
      host.innerHTML = '';
      host.appendChild(h('p.cert-err', 'The certificate could not be drawn: ' + (e.message || String(e))));
    }
  }

  /* ------------------------------------------------------------------
     on a course's page: the certificate chapter, and the message when the course is finished
     ------------------------------------------------------------------ */
  /** what is still to do, chapter by chapter: [{ id, num, title, tasks, questions }] */
  function leftToDo() {
    const st = (MG.tutorial && MG.tutorial.state) || { tasks: {}, answers: {} };
    const out = [];
    document.querySelectorAll('.chapter').forEach((ch) => {
      const req = (el) => !el.closest('.optional');
      const tasks = Array.from(ch.querySelectorAll('[data-task]')).filter(req).filter((li) => !st.tasks[li.dataset.task]).length;
      const questions = Array.from(ch.querySelectorAll('.q[data-q]')).filter(req).filter((q) => !(st.answers[q.dataset.q] || {}).done).length;
      if (tasks || questions) out.push({ id: ch.id, num: ch.dataset.num || '', title: ch.dataset.title || ch.id, tasks, questions });
    });
    return out;
  }
  const plural = (n, one, many) => `${n} ${n === 1 ? one : many}`;

  /** the certificate chapter's panel */
  function panel(host) {
    const id = document.body.dataset.course;
    const c = course(id);
    if (!host || !c) return;
    const st = status(id);
    const name = MG.user.fullName();
    host.innerHTML = '';
    host.appendChild(
      h('div.cert-name', h('span.muted', 'The name on your certificate: '), name ? h('b', name) : h('i.muted', 'none yet'), h('button.btn.small', { type: 'button', onclick: () => nameDialog() }, name ? 'Change it' : 'Add your name'))
    );
    if (!st.complete) {
      const left = leftToDo();
      host.appendChild(
        h(
          'div.cert-locked',
          h('div.cert-lock-h', { html: MG.icon('lock') + `<span>Your certificate is unlocked when you have finished the course. You have done <b>${st.done}</b> of its <b>${st.total}</b> steps and questions.</span>` }),
          h('div.cert-bar', h('i', { style: { width: st.pct + '%' } })),
          left.length
            ? h(
                'ul.cert-left',
                left.map((x) =>
                  h(
                    'li',
                    h('button.linkbtn', { type: 'button', onclick: () => MG.app.showChapter(x.id, true) }, `${x.num ? x.num + '. ' : ''}${x.title}`),
                    h('span.muted', ' – ' + [x.tasks ? plural(x.tasks, 'step', 'steps') : '', x.questions ? plural(x.questions, 'question', 'questions') : ''].filter(Boolean).join(' and ') + ' to do')
                  )
                )
              )
            : null,
          h('p.hint', 'Steps and questions marked “If you have time” don’t count towards the certificate. A question with a Check button, or a choice of answers, counts once you have answered it correctly; any other question counts once you have written an answer.')
        )
      );
      return;
    }
    const prev = h('div.cert-prev-box');
    host.appendChild(h('p.cert-done', { html: `Well done: you finished <b>${esc(c.title)}</b> on ${esc(longDate(st.completedAt || Date.now()))}.` }));
    if (!name) host.appendChild(h('p.cert-noname', 'Add your name (with the button above) and your certificate will show it.'));
    host.appendChild(prev);
    host.appendChild(h('div.cert-actions', h('button.btn.primary', { type: 'button', html: MG.icon('download') + '<span>Download your certificate (PDF)</span>', onclick: () => download(id) })));
    preview(prev, id);
  }

  /** when the course is finished for the first time: a message, with the certificate */
  function celebrate() {
    const id = document.body.dataset.course;
    const c = course(id);
    if (!c) return;
    const m = MG.modal(
      'Course complete',
      `<div class="cert-cele"><p>Congratulations! You have finished every step and question of <b>${esc(c.title)}</b>, so your certificate is ready.</p>
       <p>It shows ${MG.user.fullName() ? 'your name, <b>' + esc(MG.user.fullName()) + '</b>,' : 'your name (you can add it now)'} and the date you finished the course.</p>
       <div class="prompt-actions"><button class="btn" type="button" data-x="see">See your certificate</button><button class="btn primary" type="button" data-x="dl">${MG.icon('download')}<span>Download it (PDF)</span></button></div></div>`
    );
    m.box.querySelector('[data-x="see"]').addEventListener('click', () => {
      m.close();
      const ch = document.querySelector('.chapter[data-cert]');
      if (ch) MG.app.showChapter(ch.id, true);
    });
    m.box.querySelector('[data-x="dl"]').addEventListener('click', async () => {
      m.close();
      await download(id);
    });
  }

  /** the course page: keep the certificate chapter up to date */
  function initCoursePage() {
    const host = document.querySelector('[data-cert-panel]');
    if (!host) return;
    const again = MG.debounce(() => {
      const ch = host.closest('.chapter');
      if (!ch || !ch.hidden) panel(host);
    }, 250);
    bus.on('app:chapter', ({ id }) => {
      const ch = host.closest('.chapter');
      if (ch && ch.id === id) panel(host);
    });
    bus.on('user:name', again);
    bus.on('progress:changed', again);
    bus.on('course:complete', () => {
      again();
      celebrate();
    });
    if (!host.closest('.chapter').hidden) panel(host);
  }

  MG.cert = { course, courses: () => COURSES.slice(), status, nameDialog, pdf, download, preview, fileName, longDate, panel, celebrate, initCoursePage, leftToDo };
})();
