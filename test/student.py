"""Helpers for the tests: a student working through a course in the browser (see h.py for the page itself).

    from student import Student
    s = Student('r-basics.html')
    s.chapter('calc')
    s.step('c-mult', '31 * 78')      # runs the command in RStudio's Console and waits for the step to tick
    s.short('c-q-mult', '2418')       # answers a question and presses Check
"""
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(SITE, 'build'))
from h import Page, check  # noqa: E402


def norm(text):
    """text as the Console shows it, for comparing: no spaces at the ends of lines, no blank lines at either end"""
    lines = [x.rstrip() for x in text.replace('\r', '').split('\n')]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return '\n'.join(lines)


def transcript(code, output):
    """what the Console shows for a command and its output (as lib.console() draws it)"""
    cl = code.split('\n')
    lines = ['> ' + cl[0]] + ['+ ' + x for x in cl[1:]]
    if output:
        lines.append(output)
    return '\n'.join(lines)


class Student:
    def __init__(self, page='r-basics.html', p=None, width=1500, height=950):
        self.p = p or Page(width=width, height=height)
        self.page = page
        self.p.open(page)
        self.p.js('() => { MG.app.showWorkbench("rstudio"); }')
        self.p.wait('() => MG.app.rstudio && MG.app.rstudio.S && MG.app.rstudio.S.idle', timeout=240000)

    # ---- the instructions ----
    def chapter(self, cid):
        self.p.p.click(f'.ch-tab[data-ch="{cid}"]')
        time.sleep(0.4)

    def done(self, tid):
        return bool(self.p.js('(id) => !!MG.tutorial.state.tasks[id]', tid))

    def wait_task(self, tid, timeout=15):
        t0 = time.time()
        while time.time() - t0 < timeout:
            if self.done(tid):
                return True
            time.sleep(0.25)
        return False

    def step(self, tid, code=None, timeout=15):
        """run code (if any) and check that the step ticks"""
        if code is not None:
            self.run(code)
        return check(self.wait_task(tid, timeout), f'step {tid} ticks' + (f' after {code!r}' if code else ''))

    def not_yet(self, tid, why):
        return check(not self.done(tid), f'step {tid} has not ticked ({why})')

    def short(self, qid, answer, expect=True):
        sel = f'.q[data-q="{qid}"]'
        self.p.p.fill(f'{sel} input', answer)
        self.p.p.click(f'{sel} .q-actions button:not(.q-show)')
        time.sleep(0.2)
        ok = bool(self.p.js('(id) => !!(MG.tutorial.state.answers[id] || {}).done', qid))
        return check(ok == expect, f'question {qid}: {answer!r} is {"accepted" if expect else "not accepted"}')

    def choose(self, qid, right=True):
        sel = f'.q[data-q="{qid}"] .mcq label' + ('[data-correct]' if right else ':not([data-correct])')
        self.p.p.locator(sel).first.click()
        time.sleep(0.2)
        ok = bool(self.p.js('(id) => !!(MG.tutorial.state.answers[id] || {}).done', qid))
        return check(ok == right, f'question {qid}: the {"right" if right else "wrong"} choice is {"accepted" if right else "not accepted"}')

    def write(self, qid, text):
        self.p.p.fill(f'.q[data-q="{qid}"] textarea', text)
        time.sleep(0.6)
        ok = bool(self.p.js('(id) => !!(MG.tutorial.state.answers[id] || {}).done', qid))
        return check(ok, f'question {qid}: a written answer counts')

    def left(self):
        """the steps and questions that count towards the certificate and aren't done yet"""
        return self.p.js('''() => {
          const c = window.RT_COURSES.find((x) => x.id === document.body.dataset.course);
          const st = MG.tutorial.state;
          return c.tasks.filter((t) => !st.tasks[t]).concat(c.questions.filter((q) => !(st.answers[q] || {}).done));
        }''')

    # ---- RStudio ----
    def text(self):
        return self.p.js('() => MG.app.rstudio.cv.text()')

    def idle(self, timeout=300000):
        self.p.wait('() => MG.app.rstudio.S.idle && !MG.app.rstudio.capture', timeout=timeout)

    def run(self, code, wait=True, settle=0.6):
        """run code in RStudio's Console, as if it had been typed there and Enter pressed; what the Console shows for it"""
        n0 = len(self.text())
        self.p.js('(c) => { MG.app.rstudio.consoleRun(c); }', code)
        if wait:
            time.sleep(0.3)
            self.idle()
            time.sleep(settle)
        return self.text()[n0:]

    def name(self, name, via='[data-student-name]'):
        """give a name for the certificate, with the dialog"""
        self.p.p.locator(via).first.click()
        self.p.p.wait_for_selector('#studentNameIn')
        self.p.p.fill('#studentNameIn', name)
        self.p.p.click('form.user-form button[type="submit"]')
        time.sleep(0.4)
        return self.p.js('() => MG.user.fullName()')

    def new_script(self, lines, run_line=None, save_as=None):
        """a new R script in the Source pane, with these lines typed into it; run_line: put the cursor on that line (from 1)
        and press Ctrl+Enter; save_as: save it with Ctrl+S under this name"""
        self.p.js('() => { MG.app.rstudio.newDoc("r"); }')
        time.sleep(0.5)
        k = self.p.p.keyboard
        for i, line in enumerate(lines):
            if i:
                k.press('Enter')
            k.type(line)
        if run_line:
            self.p.js('(n) => { MG.app.rstudio.cm.setCursor({ line: n - 1, ch: 0 }); MG.app.rstudio.cm.focus(); }', run_line)
            k.press('Control+Enter')
            time.sleep(0.5)
            self.idle()
        if save_as:
            self.p.js('() => MG.app.rstudio.cm.focus()')
            k.press('Control+s')
            self.p.p.wait_for_selector('.rs-filedlg input[aria-label="File name"]')
            self.p.p.fill('.rs-filedlg input[aria-label="File name"]', save_as)
            self.p.p.click('.rs-filedlg .btn.primary')
            time.sleep(0.6)

    def examples(self, examples, width=80):
        """run the commands the instructions show (lib.console()) and compare what R prints with what they show"""
        bad = 0
        for ex in examples:
            self.p.js('(w) => MG.app.rstudio.S.evalVoid("options(width = " + w + ")")', width)
            got = norm(self.run(ex['code'], settle=0.3))
            want = norm(transcript(ex['code'], ex['output']))
            if got != want:
                bad += 1
                print('--- the instructions show:\n' + want + '\n--- R shows:\n' + got + '\n---')
            check(got == want, f'R prints what the instructions show for {ex["code"].splitlines()[0][:70]!r}')
        return bad

    def close(self):
        self.p.close()


def pdf_text(path):
    import subprocess
    return subprocess.run(['pdftotext', '-layout', path, '-'], capture_output=True, text=True).stdout


def squash(s):
    return re.sub(r'\s+', ' ', s).strip()
