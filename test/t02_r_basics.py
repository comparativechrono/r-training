"""A student works through R basics from start to finish, as the instructions ask: every step ticks itself, the
questions accept the right answers, the certificate is locked until the end and then unlocked, and the PDF has the
student's name, the course, the department, the university, the signature and the date. Then the landing page shows
the course as finished, with the certificate.
Run:  python3 test/t02_r_basics.py"""
import datetime
import os
import sys
import time
from student import Student, check, pdf_text, squash
import course_r_basics as C

s = Student('r-basics.html')
p = s.p

# ---- 0. Start here ----
s.chapter('start')
check(p.js('() => document.querySelector("#userBtn").classList.contains("unnamed")'), 'the name button stands out while there is no name')
check(s.name('Ada Lovelace') == 'Ada Lovelace', 'the name dialog saves the name')
check(p.js('() => document.querySelector("#userBtn").textContent.includes("Ada Lovelace")'), 'the name is shown at the top of the page')
s.step('s-name')
s.step('s-first', '1 + 1')

# ---- 1. R as a calculator ----
s.chapter('calc')
s.step('c-mult', '31 * 78')
s.step('c-div', '697 / 41')
s.run('2 + 3 * 4')
s.step('c-brackets', '(2 + 3) * 4')
s.run('5 *', wait=False)
time.sleep(1.5)
s.step('c-plus', '2')
s.short('c-q-mult', '2400', expect=False)
check(p.js('() => !document.querySelector(\'.q[data-q="c-q-mult"] .q-show\').hidden'), 'Show answer appears once a question has been tried')
s.short('c-q-mult', '2418')
s.short('c-q-div', '17')
s.choose('c-q-order', right=False)
s.choose('c-q-order')
s.new_script(['# my first script', '2 ^ 8'])
s.step('c-new')
p.js('() => { MG.app.rstudio.cm.setCursor({ line: 1, ch: 0 }); MG.app.rstudio.cm.focus(); }')
p.p.keyboard.press('Control+Enter')
time.sleep(0.5)
s.idle()
s.step('c-run')
p.js('() => MG.app.rstudio.cm.focus()')
p.p.keyboard.press('Control+s')
p.p.wait_for_selector('.rs-filedlg input[aria-label="File name"]')
p.p.fill('.rs-filedlg input[aria-label="File name"]', 'basics.R')
p.p.click('.rs-filedlg .btn.primary')
s.step('c-save')
check(p.js('() => MG.app.fs.exists("/home/user/basics.R")'), 'the script is saved as ~/basics.R')

# ---- 2. Objects ----
s.chapter('objects')
s.step('o-x', 'x <- 39')
s.step('o-y', '22 -> y')
s.not_yet('o-z', 'z is not made yet')
s.step('o-z', 'z <- x / y')
s.step('o-show', 'z')
s.short('o-q-z', '1.77')
s.choose('o-q-name')
s.choose('o-q-update')
# (Alt+- types the arrow in RStudio's Console)
p.p.click('.rs-conhost textarea.rc-input')
p.p.keyboard.type('w')
p.p.keyboard.press('Alt+Minus')
check(p.js('() => document.querySelector(".rs-conhost textarea.rc-input").value') == 'w <- ', 'Alt+- types the assignment arrow in the Console')
p.js('() => { document.querySelector(".rs-conhost textarea.rc-input").value = ""; }')

# ---- 3. Functions, text and help ----
s.chapter('functions')
s.run('root <- sqrt(2345)')
s.step('f-sqrt', 'log2(root)')
s.step('f-name', 'my.name <- "Ada"')
s.step('f-nchar', 'nchar(my.name)')
s.not_yet('f-substr', 'nchar is not substr')
s.step('f-substr', 'substr(my.name, 1, 1)')
s.step('f-help', '?sqrt')
s.step('f-search', '??substring', timeout=30)
s.short('f-q-log', '5.597686')
s.choose('f-q-quotes')
s.choose('f-q-default')

# ---- 4. Vectors ----
s.chapter('vectors')
s.step('v-c', 'some.numbers <- c(2, 5, 8, 12, 16)')
s.step('v-colon', 'number.range <- 5:9')
s.step('v-seq', 'number.series <- seq(from = 2, by = 3, length.out = 100)')
s.run('number.series')
s.run('head(number.series)')
s.step('v-tail', 'tail(number.series)')
s.step('v-rep', 'genotypes <- rep(c("WT", "KO1", "KO2", "KO3"), each = 25)')
s.short('v-q-last', '299')
s.choose('v-q-mix')
s.choose('v-q-seq')

# ---- 5. Vectorised operations ----
s.chapter('vectorised')
s.step('vo-sub', 'some.numbers - number.range')
s.step('vo-1000', 'number.series <- number.series * 1000')
out = s.run('3:10 + 11:13')
check('longer object length is not a multiple of shorter object length' in out, 'R gives the warning the text shows')
s.step('vo-warn')
s.step('vo-median', 'median(number.series)')
s.short('vo-q-sub', '-3 -1 1 4 7')
s.short('vo-q-last', '299000')
s.choose('vo-q-recycle')
s.step('vo-centre', 'centred <- number.series - median(number.series)')  # (optional)

# ---- 6. Comparing and selecting ----
s.chapter('select')
s.step('sv-test', 'number.series > 150000')
s.step('sv-count', 'sum(number.series > 150000)')
s.step('sv-first', 'number.series[1:10]')
s.step('sv-wt', 'sum(genotypes != "WT")')
s.short('sv-q-count', '50')
s.choose('sv-q-pick')

# ---- 7. Random numbers ----
s.chapter('random')
s.step('r-norm', 'normal.numbers <- rnorm(20)')
s.step('r-test', 't.test(normal.numbers)')
s.not_yet('r-mean1', 'the numbers still have a mean of 0')
s.step('r-mean1', 'normal.numbers <- rnorm(20, mean = 1)')
s.run('t.test(normal.numbers)')
s.write('r-q-p', 'The first p-value was 0.6, not significant; the second was 0.0001, which is significant.')
s.choose('r-q-false')

# ---- 8. Data structures: the last step finishes the course ----
s.chapter('structures')
s.step('ds-list', 'results <- list(ratios = c(0.8, 1.2, 3.3, 1.8, 2.7), counts = c(100, 300, 200))')
s.step('ds-mean', 'mean(results$counts)')
s.step('ds-df', C.ALL_RESULTS_CODE)
s.step('ds-view', 'View(all.results)')
s.step('ds-str', 'str(all.results)')
s.short('ds-q-mon', '0.6')
s.short('ds-q-pass', '3')
s.choose('ds-q-df')
left = s.left()
check(left == ['ds-mon'], f'before the last step, only it is left to do ({left})')
check(p.js('() => !MG.tutorial.state.completedAt'), 'the course is not finished yet')
# the certificate is locked
s.chapter('certificate')
check(p.js('() => !!document.querySelector("[data-cert-panel] .cert-locked")'), 'the certificate is locked')
check('8. Data structures' in p.js('() => document.querySelector("[data-cert-panel]").innerText'), 'the locked certificate lists the chapter with something left to do')
p.p.click('[data-cert-panel] .cert-left button')
time.sleep(0.4)
check(p.js('() => !document.getElementById("structures").hidden'), 'its link opens that chapter')
s.step('ds-mon', 'mean(all.results$mon)')
time.sleep(1)
check(p.js('() => !!MG.tutorial.state.completedAt'), 'the course is finished')
check(p.js('() => document.querySelector(".progress-label").textContent') == '100% done', 'the progress bar says 100% done')
check(p.js('() => /Course complete/.test(document.querySelector(".modal") ? document.querySelector(".modal").innerText : "")'), 'a message says the course is complete')
check(p.js('() => /Ada Lovelace/.test(document.querySelector(".modal").innerText)'), 'the message names the student')
check(len(p.js('() => window.RT_COURSES.find((c) => c.id === "r-basics").tasks')) == 41, 'the optional steps do not count')

# ---- the certificate ----
p.p.click('.modal [data-x="see"]')
time.sleep(0.5)
check(p.js('() => !document.getElementById("certificate").hidden'), '“See your certificate” opens the certificate chapter')
p.wait('() => !!document.querySelector("[data-cert-panel] canvas.cert-canvas")', timeout=60000)
check(True, 'the certificate is drawn on the page')
with p.p.expect_download(timeout=60000) as dl:
    p.p.click('[data-cert-panel] .cert-actions .btn.primary')
d = dl.value
pdf = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', d.suggested_filename)
os.makedirs(os.path.dirname(pdf), exist_ok=True)
d.save_as(pdf)
check(d.suggested_filename == 'certificate-r-basics-ada-lovelace.pdf', f'the file is called {d.suggested_filename}')
text = squash(pdf_text(pdf))
today = datetime.date.today()
when = f'{today.day} {today.strftime("%B %Y")}'
for want in ['Ada Lovelace', 'R basics', 'Department of Genomic Medicine', 'University of Cambridge', 'Tim Hearn', 'Certificate of Completion', when,
             'has successfully completed the course']:
    check(want in text, f'the certificate says {want!r}')
print(text[:600])
p.shot('t02_certificate')

# ---- after a reload: still finished, and the course still knows the name ----
p.p.reload()
p.wait('window.MG_READY === true')
time.sleep(1)
check(p.js('() => !!MG.tutorial.state.completedAt && MG.cert.status("r-basics").complete'), 'after a reload the course is still finished')
check(not p.js('() => /Course complete/.test(document.body.innerText)'), 'the message is not shown again')

# ---- the landing page ----
p.open('index.html')
time.sleep(0.5)
card = p.js('() => document.querySelector(\'.course[data-course="r-basics"]\').innerText')
check('Finished on' in card and 'Download your certificate' in card, 'the landing page shows R basics as finished, with its certificate')
card2 = p.js('() => document.querySelector(\'.course[data-course="tidyverse"]\').innerText')
check('Not started yet' in card2 and 'unlocked when you finish' in card2, 'the Tidyverse course is not started, and its certificate is locked')
check(p.js('() => document.querySelector("[data-student-name-text]").textContent') == 'Ada Lovelace', 'the landing page shows the name')
p.p.click('.course[data-course="r-basics"] .course-cert .linkish')
p.wait('() => !!document.querySelector(".modal canvas.cert-canvas")', timeout=60000)
check(True, 'Preview shows the certificate')
p.shot('t02_landing_preview')
with p.p.expect_download(timeout=60000) as dl:
    p.p.click('.modal .prompt-actions .btn.primary')
check(dl.value.suggested_filename == 'certificate-r-basics-ada-lovelace.pdf', 'the certificate can be downloaded from the landing page')
check(not p.errors, f'no errors in the pages ({p.errors[:3]})')
s.close()
print('failed:', check.failed)
sys.exit(1 if check.failed else 0)
