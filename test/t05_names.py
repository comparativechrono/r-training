"""The student's name and the certificates, without working through a course: the name dialog (tidying a name, one
that is too long), the landing page and a course page sharing the name, a finished course with no name yet (the
download asks for one), a course that isn't finished (no certificate), names in other alphabets and scripts (a
picture of the name when the fonts don't have its letters), and what the PDF looks like.
Run:  python3 test/t05_names.py"""
import base64
import os
import sys
import time
from student import check, pdf_text, squash
from h import Page

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
os.makedirs(OUT, exist_ok=True)
p = Page(width=1300, height=900)
p.open('index.html')

# ---- the name dialog, from the landing page
check(p.js('() => document.querySelector("[data-student-name-text]").textContent') == 'no name yet', 'the landing page says there is no name yet')
p.p.click('[data-name-btn]')
p.p.wait_for_selector('#studentNameIn')
p.p.fill('#studentNameIn', 'x' * 71)
time.sleep(0.2)
check(p.js('() => document.querySelector("form.user-form button[type=submit]").disabled'), 'a name of 71 characters can’t be saved')
check('too long' in p.js('() => document.querySelector("#studentNameNote").textContent'), 'and the dialog says why')
p.p.fill('#studentNameIn', '  Mary ‮ Anning\u0007  ')
time.sleep(0.2)
check(p.js('() => document.querySelector(".name-prev-name").textContent') == 'Mary Anning', 'the preview shows the name tidied (spaces, control characters)')
p.p.click('form.user-form button[type="submit"]')
time.sleep(0.4)
check(p.js('() => MG.user.fullName()') == 'Mary Anning', 'the tidied name is saved')
check(p.js('() => document.querySelector("[data-student-name-text]").textContent') == 'Mary Anning', 'the landing page shows it')

# ---- the same name on a course page
p.open('r-basics.html')
check('Mary Anning' in p.js('() => document.querySelector("#userBtn").textContent'), 'the course page shows the same name')
check(p.js('() => MG.cert.download("r-basics")') is False, 'an unfinished course has no certificate to download')
time.sleep(0.3)
check('Finish every step' in p.js('() => document.body.innerText'), 'and the page says why')

# ---- a finished course, and no name: the download asks for one
p.open('index.html')
p.js('''() => {
  const c = window.RT_COURSES.find((x) => x.id === 'tidyverse');
  const st = { tasks: {}, answers: {}, completedAt: '2026-10-01T09:30:00Z' };
  c.tasks.forEach((t) => (st.tasks[t] = true));
  c.questions.forEach((q) => (st.answers[q] = { done: true }));
  MG.siteStore.set(c.dataPage + ':progress', st);
  MG.user.setFullName('');
}''')
p.open('index.html')
time.sleep(0.3)
card = p.js('() => document.querySelector(\'.course[data-course="tidyverse"]\').innerText')
check('Finished on 1 October 2026' in card, 'the landing page shows the course as finished on the day it was')
p.p.click('.course[data-course="tidyverse"] .course-cert .btn')
p.p.wait_for_selector('#studentNameIn')
check(True, 'Download asks for a name when there isn’t one')
p.p.fill('#studentNameIn', 'Rosalind Franklin')
with p.p.expect_download(timeout=60000) as dl:
    p.p.click('form.user-form button[type="submit"]')
path = os.path.join(OUT, dl.value.suggested_filename)
dl.value.save_as(path)
text = squash(pdf_text(path))
check('Rosalind Franklin' in text and '1 October 2026' in text and 'Tidyverse' in text, 'the certificate has the new name and the date the course was finished')
check(p.js('() => document.querySelector("[data-student-name-text]").textContent') == 'Rosalind Franklin', 'and the name is kept')

# ---- names in other alphabets and scripts
for i, name in enumerate(['Zoë Ó Briain-Łukasiewicz', 'Νίκη Παπαδοπούλου', 'Ольга Иванова', 'Nguyễn Thị Minh Khai', '李小龙', 'نور الهدى']):
    b64 = p.js('''async (n) => { const b = await MG.cert.pdf('tidyverse', n, '2026-10-01T09:30:00Z');
      let s = ''; for (let i = 0; i < b.length; i++) s += String.fromCharCode(b[i]); return btoa(s); }''', name)
    data = base64.b64decode(b64)
    f = os.path.join(OUT, f't05_name{i}.pdf')
    open(f, 'wb').write(data)
    t = squash(pdf_text(f))
    as_text = name.split()[0] in t
    as_picture = b'/Subtype /Image' in data
    if i < 4:
        check(as_text and not as_picture, f'{name!r} is written in the certificate’s font')
    else:
        check(as_picture, f'{name!r} (letters the fonts don’t have) is drawn as a picture')
check(len(open(os.path.join(OUT, 't05_name0.pdf'), 'rb').read()) < 600000, 'a certificate is less than 600 kB')
check(not p.errors, f'no errors in the pages ({p.errors[:3]})')
p.close()
print('failed:', check.failed)
sys.exit(1 if check.failed else 0)
