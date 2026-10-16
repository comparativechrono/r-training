"""A student works through the Tidyverse course from start to finish: installing and loading the tidyverse, reading the
files, filtering, pipes and plots. Every step ticks itself, the steps of plots only tick for the plot they ask for,
and at the end the certificate is unlocked, with the right text. Downloads the tidyverse (about a minute).
Run:  python3 test/t03_tidyverse.py"""
import os
import sys
import time
from student import Student, check, pdf_text, squash

s = Student('tidyverse.html')
p = s.p

# ---- 0. Start here ----
s.chapter('start')
s.name('Grace Hopper')
s.step('t-name')
s.new_script(['library(tidyverse)', 'setwd("~/data")'], save_as='tidyverse.R')
s.step('t-script')
t0 = time.time()
s.run('install.packages("tidyverse")')
s.step('t-install', timeout=30)
s.step('t-library', 'library(tidyverse)', timeout=60)
print(f'the tidyverse was installed and loaded in {time.time() - t0:.0f} s')

# ---- 1. Reading files ----
s.chapter('reading')
s.not_yet('rd-wd', 'the working directory is still the home folder')
s.step('rd-wd', 'setwd("~/data")')
s.step('rd-small', 'small <- read_tsv("small_file.txt")')
s.step('rd-view', 'View(small)')
s.step('rd-median', 'median(log2(small$Length))')
s.step('rd-child', 'child <- read_csv("Child_Variants.csv")', timeout=30)
s.run('child')
s.step('rd-print', 'View(child)', timeout=30)
s.run('mean(child$MutantReadPercent)')
s.step('rd-mean', 'sd(child$MutantReadPercent)')
s.short('rd-q-median', '6.23')
s.short('rd-q-mean', '59.88')
s.short('rd-q-sd', '24.12')
s.choose('rd-q-type')

# ---- 2. Tidy data ----
s.chapter('tidy')
s.choose('td-q-batch')
s.choose('td-q-tidy')
import course_tidyverse as T  # noqa: E402
s.run(T.WIDE)
s.step('td-long', T.LONG)  # (optional)

# ---- 3. Choosing columns and rows ----
s.chapter('filter')
s.run('filter(small, Category == "B")')
s.not_yet('fl-a', 'that was category B')
s.step('fl-a', 'filter(small, Category == "A")')
s.step('fl-80', 'filter(small, Length > 80)')
s.step('fl-sample', 'select(small, -Sample)')
s.step('fl-mt', 'filter(child, CHR == "MT")')
s.step('fl-70', 'filter(child, MutantReadPercent >= 70)')
s.step('fl-qual', 'filter(child, QUAL == 200)')
s.step('fl-gene', 'filter(child, GENE == "IGFN1")')
s.step('fl-cols', 'select(child, -ENST, -dbSNP)')
s.short('fl-q-80', '16')
s.short('fl-q-gene', '17')
s.choose('fl-q-which')
s.choose('fl-q-quotes')

# ---- 4. Pipes ----
s.chapter('pipes')
s.step('pp-quality', 'child %>%\n  filter(QUAL == 200) %>%\n  filter(COVERAGE > 50) %>%\n  filter(MutantReadPercent > 70)')
s.step('pp-chr', 'child %>% filter(!CHR %in% c("X", "Y", "MT"))')
s.step('pp-dbsnp', 'child |> filter(dbSNP != ".") |> select(CHR, POS)')
s.short('pp-q-quality', '3961')
s.short('pp-q-dbsnp', '23,690')
s.choose('pp-q-pipe')
s.step('pp-del', 'child %>% filter(nchar(REF) > 1)')  # (optional)
s.step('pp-q', 'child %>% filter(substr(GENE, 1, 1) == "Q")')  # (optional)

# ---- 5. Your first plots ----
s.chapter('plots')
s.step('pl-read', 'brain <- read_tsv("brain_bodyweight.txt")')
s.run('ggplot(brain, aes(x = brian, y = body)) + geom_point()')
s.not_yet('pl-scatter', 'that plot has a mistake in it, and R could not draw it')
s.step('pl-scatter', 'ggplot(brain, aes(x = brain, y = body)) + geom_point()')
s.not_yet('pl-blue', 'the points are not blue yet')
s.step('pl-blue', 'ggplot(brain, aes(x = brain, y = body)) + geom_point(color = "blue2", size = 3)')
s.step('pl-log', 'ggplot(brain, aes(x = log.brain, y = log.body)) + geom_point(colour = "blue2", size = 3)')
s.not_yet('pl-category', 'the points are not coloured by Category yet')
s.step('pl-category', 'brain %>%\n  ggplot(aes(x = log.brain, y = log.body)) +\n  geom_point(aes(colour = Category), size = 3)')
check(p.js('() => MG.app.rstudio.plots.length') >= 4, 'the plots are drawn in the Plots pane')
s.choose('pl-q-extinct')
s.choose('pl-q-fixed')
s.step('pl-noext', 'brain %>% filter(Category != "Extinct") %>% ggplot(aes(x = log.brain, y = log.body, colour = Category)) + geom_point()')  # (optional)

# ---- 6. More kinds of plot ----
s.chapter('more')
s.step('mo-col', 'small %>% filter(Category == "A") %>% ggplot(aes(x = Sample, y = Length)) + geom_col()')
s.step('mo-hist', 'child %>% ggplot(aes(x = MutantReadPercent)) + geom_histogram(fill = "yellow", colour = "black")', timeout=30)
s.not_yet('mo-bin', 'the binwidth has not been changed')
s.step('mo-bin', 'child %>% ggplot(aes(x = MutantReadPercent)) + geom_histogram(binwidth = 2, fill = "yellow", colour = "black")', timeout=30)
s.step('mo-dens', 'ggplot(child, aes(MutantReadPercent)) + geom_density(fill = "yellow", alpha = 0.5)', timeout=30)
s.run('ggplot(child, aes(x = REF)) + geom_bar()')
s.not_yet('mo-bar', 'the variants with longer REFs are still there')
s.step('mo-bar', 'child %>% filter(nchar(REF) == 1) %>% ggplot(aes(x = REF)) + geom_bar()', timeout=30)
s.short('mo-q-ref', 'C', expect=False)
s.short('mo-q-ref', 'G')
s.choose('mo-q-colbar')
s.choose('mo-q-bin')

# ---- 7. Titles and labels (the last steps finish the course) ----
s.chapter('labels')
s.choose('lb-q-plus')
PLOT = 'ggplot(brain, aes(x = log.brain, y = log.body, colour = Category)) + geom_point()'
s.run(PLOT + ' + ggtitle("Brains and bodies")')
s.not_yet('lb-title', 'the axes have no labels yet')
s.step('lb-title', PLOT + ' + ggtitle("Brains and bodies") + xlab("Brain weight (log2 g)") + ylab("Body weight (log2 kg)")')
check(s.left() == ['lb-text'], f'only the last step is left to do ({s.left()})')
s.step('lb-text', PLOT + ' + geom_text(aes(label = Species), hjust = -0.1)')
time.sleep(1)
check(p.js('() => !!MG.tutorial.state.completedAt'), 'the course is finished')
check(p.js('() => /Course complete/.test(document.body.innerText)'), 'a message says the course is complete')
p.p.click('.modal [data-x="see"]')
# (the optional part still works)
s.chapter('labels')
s.step('lb-cor', 'cor.test(brain$log.brain, brain$log.body)')
s.step('lb-lm', 'lm(log.body ~ log.brain, data = brain)')
s.step('lb-abline', PLOT + ' + geom_abline(intercept = -2.283, slope = 1.215) + ggtitle("Brains and bodies (p = 2.44e-06)")')
s.short('lb-q-p', '2.44e-06')

# ---- the certificate ----
s.chapter('certificate')
p.wait('() => !!document.querySelector("[data-cert-panel] canvas.cert-canvas")', timeout=60000)
with p.p.expect_download(timeout=60000) as dl:
    p.p.click('[data-cert-panel] .cert-actions .btn.primary')
d = dl.value
pdf = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', d.suggested_filename)
os.makedirs(os.path.dirname(pdf), exist_ok=True)
d.save_as(pdf)
check(d.suggested_filename == 'certificate-tidyverse-grace-hopper.pdf', f'the file is called {d.suggested_filename}')
text = squash(pdf_text(pdf))
for want in ['Grace Hopper', 'Tidyverse', 'Part 2 of Introduction to R', 'Department of Genomic Medicine', 'University of Cambridge', 'Tim Hearn', 'readr', 'ggplot2']:
    check(want in text, f'the certificate says {want!r}')
p.shot('t03_certificate')

# ---- the landing page ----
p.open('index.html')
time.sleep(0.5)
check('Finished on' in p.js('() => document.querySelector(\'.course[data-course="tidyverse"]\').innerText'), 'the landing page shows the Tidyverse course as finished')
check('Not started yet' in p.js('() => document.querySelector(\'.course[data-course="r-basics"]\').innerText'), 'and R basics as not started')
check(not p.errors, f'no errors in the pages ({p.errors[:3]})')
s.close()
print('failed:', check.failed)
sys.exit(1 if check.failed else 0)
