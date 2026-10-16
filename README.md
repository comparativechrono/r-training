# R training: Introduction to R

**Two short online courses for people who are new to R: *R basics*, and then *Tidyverse*. R runs in the student's web browser, in an RStudio-style workbench with the instructions alongside it, so there is nothing to install. Each course ends with a certificate that the student can download as a PDF.**

The courses are adapted from *Introduction to R (with Tidyverse)* by Simon Andrews and Laura Biggins of [Babraham Bioinformatics](https://www.bioinformatics.babraham.ac.uk/training.html), as adapted by Tim Hearn. The exercises follow the original course, and the ideas that were in its slides (vectorised operations, recycling, data structures, tidy data, how a ggplot is put together, and so on) are now explained in the text of the chapters, so that the courses can be done without a lecture. The certificates are awarded by the Department of Genomic Medicine at the University of Cambridge and signed by Tim Hearn.

The site is built on the [R workbench](https://github.com/comparativechrono/r-workbench). R is provided by webR (R 4.6 compiled to WebAssembly), so the R that students use is real R, and everything they do stays in their own browser. The site is static (HTML, CSS and JavaScript only), so it can be hosted on GitHub Pages or any ordinary web server.

---

## Contents

1. [The site](#the-site)
2. [The two courses](#the-two-courses)
3. [How a course works](#how-a-course-works)
4. [Certificates](#certificates)
5. [Before students use it](#before-students-use-it)
6. [Publishing it on GitHub Pages](#publishing-it-on-github-pages)
7. [Trying it on your own computer](#trying-it-on-your-own-computer)
8. [Settings in `config.js`](#settings-in-configjs)
9. [Changing a course, or adding one](#changing-a-course-or-adding-one)
10. [What students keep, and privacy](#what-students-keep-and-privacy)
11. [Limitations](#limitations)
12. [How it was tested](#how-it-was-tested)
13. [Files](#files)
14. [Credits and licences](#credits-and-licences)

---

## The site

| Page | What it is |
| --- | --- |
| `index.html` | The landing page. It lists the two courses, shows how far the student has got with each, and has the student's name (for their certificates) and, once a course is finished, its certificate to preview and download |
| `r-basics.html` | Part 1, *R basics* |
| `tidyverse.html` | Part 2, *Tidyverse* |

Each course page has the instructions on the left and the workbench on the right, with three tabs:

| Tab | What it contains |
| --- | --- |
| **RStudio** | An IDE modelled on RStudio and made for teaching: the Source pane (scripts, run line by line with <kbd>Ctrl</kbd>+<kbd>Enter</kbd>, or all at once with Source), the Console, the Environment and History panes, and the Files, Plots, Packages, Help and Viewer panes. Its menus and keyboard shortcuts follow RStudio's, including <kbd>Alt</kbd>+<kbd>-</kbd> for `<-` and <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>M</kbd> for a pipe. `?name` and `??words` show help pages and searches in the Help pane |
| **Files** | The student's home folder (`~`), with the course's data in `~/data`, a text editor and viewers for tables, pictures and PDFs |
| **AI** | An AI assistant set up as an R tutor for the course, which students can use with a key of their own for an AI service |

## The two courses

### Part 1: R basics (about 2½ hours; 41 steps and 22 questions)

| Chapter | What students learn and do |
| --- | --- |
| 0. Start here | What R and RStudio are, RStudio's four panes, how the course works, and their name for the certificate |
| 1. R as a calculator | Arithmetic, what the `[1]` means, the order of operations, unfinished commands and the `+` prompt, and a first script, saved as `basics.R` |
| 2. Objects | Assignment with `<-` and `->`, the rules and conventions for names, and “object not found” |
| 3. Functions and help | Calling functions, one inside another, text and quotes, `nchar()` and `substr()`, arguments by position and by name, default values, `?` and `??` |
| 4. Vectors | Everything is a vector, the types of vector, `c()` and what happens when types are mixed, the colon, `seq()`, `rep()`, `head()` and `tail()` |
| 5. Vectorised operations | How values are matched, how a shorter vector is recycled and when R warns (with diagrams), and vectorised and summary functions. *If you have time:* centring values on their median |
| 6. Comparing and selecting | The comparison operators, logical vectors, counting with `sum()`, and selecting values with `[ ]`, by position and by condition |
| 7. Random numbers | `rnorm()`, `t.test()` and reading its p-value, false positives, and `set.seed()`. *If you have time:* how many values a t-test needs to see a small difference |
| 8. Data structures | Vectors, lists, data frames and tibbles, `$`, `View()` and `str()` |
| ★ Certificate | The certificate, unlocked when everything else is done |

### Part 2: Tidyverse (about 3 hours; 34 steps and 19 questions)

| Chapter | What students learn and do |
| --- | --- |
| 0. Start here | What the tidyverse is, installing and loading packages, the conflicts that `library(tidyverse)` reports, and keeping commands in a script |
| 1. Reading files | readr, file paths, the working directory, <kbd>Tab</kbd> to fill in file names, readr's column specification, and `$`. Reads `small_file.txt` and `Child_Variants.csv` |
| 2. Tidy data | Wide and long data, and what makes data tidy. *If you have time:* `pivot_longer()` |
| 3. Choosing columns and rows | `select()` (by name, by position and with `-`), `filter()` and its tests, and transforming a column in a filter. *If you have time:* fixing `broken_selects.R` |
| 4. Pipes | Intermediate objects, `%>%` (and R's own `|>`), several tests in one filter, `&`, `|`, `!` and `%in%`. *If you have time:* filters with `nchar()` and `substr()` |
| 5. Your first plots | How a ggplot is put together, geometries, and fixed and mapped aesthetics, with the brain and body weight data. *If you have time:* piping filtered data into `ggplot()` |
| 6. More kinds of plot | `geom_col()` and `geom_bar()`, histograms and `binwidth`, density plots, and `fill` and `colour` |
| 7. Titles and labels | `ggtitle()`, `xlab()`, `ylab()` and `geom_text()`. *If you have time:* `cor.test()`, `lm()` and a line of best fit with `geom_abline()` |
| ★ Certificate | The certificate |

The original course's model answers (`answers.Rmd`) are not part of this repository, because the site is public.

## How a course works

- **Steps tick themselves.** Each chapter ends with an activity, a list of steps. A step ticks itself (and is marked *✓ spotted*) when the workbench sees that it has been done, and students can also tick steps themselves. There are three kinds of check:
  - an **event** on the page, such as a command run in RStudio's Console, a help page opened, `View()` used, a script saved or a package installed;
  - a **condition**, such as the student having given their name, or a package being installed;
  - an **R check**: an R expression that RStudio's R session evaluates quietly after each command, which ticks the step when it is TRUE. Most of these look at the value of the student's last command (which R keeps in `.Last.value`), or at an object they were asked to make. Because they look at the result rather than the code, any correct way of getting it counts: `filter(small, Category == "A")`, `small %>% filter(Category == "A")` and `small[small$Category == "A", ]` all tick the same step, and a plot only ticks a step if it has the layers and aesthetics asked for and R can draw it.
- **Questions.** Short answers and multiple-choice questions are marked straight away. Questions that ask for a sentence count once the student has written something. The model answer to a question is shown, with *Show answer*, once the student has had a go (see `showModelAnswers` below).
- **If you have time.** Parts marked *If you have time* are extras for faster students. Their steps and questions are checked in the same way, but they don't count towards the certificate.
- **Progress** is shown at the top of each course, on each chapter's tab, and on the landing page.

## Certificates

When every step and question of a course is done (apart from the *If you have time* ones), its certificate is unlocked: the student gets a message, the last chapter shows the certificate, and they can download it as a PDF, there or on the landing page. Until then, the last chapter shows what is left to do, chapter by chapter.

The certificate is an A4 landscape PDF. It says that the student, by the name they gave, has completed the course (with its title, “Part 1 of Introduction to R” or “Part 2”, and a summary of what it covered), on the date they finished it, and it is awarded by the Department of Genomic Medicine, University of Cambridge, and signed by Tim Hearn. These details come from `config.js` (see below) and `build/courses.py`. There is no crest or logo on it.

The PDF is made in the student's browser by [pdf-lib](https://pdf-lib.js.org), with the fonts embedded (EB Garamond for the text and Great Vibes for the signature, both from `assets/fonts/`), and previewed on the page with PDF.js. Nothing is sent to a server. The fonts cover the Latin, Greek and Cyrillic alphabets, including Vietnamese; a name in another script (Chinese or Arabic, say) is drawn by the browser with its own fonts and placed on the certificate as a picture, so every name can be shown.

The student's name is set with the **Your name** button at the top of each page (or on the landing page). It is kept in the browser, shared by both courses, and it can be changed at any time, including after a course is finished. Names are tidied before they are used (extra spaces and invisible control characters are removed), and they can be up to 70 characters long.

**What a certificate shows.** A certificate is a record that the steps and questions of a course were completed in a browser, under the name that was typed in. The site can't check who did the work, and someone who knows how could unlock a certificate in their own browser without doing the course, so a certificate should be treated as a record of completing a training course, not as an assessed qualification. *Start again* (under **My answers**) locks the certificate again until the course has been finished once more.

## Before students use it

1. **Computers and browsers.** Students need a laptop or desktop computer with a current version of Chrome, Edge, Firefox or Safari; 8 GB of memory is comfortable. The pages work on a phone, but the screen is cramped.
2. **Network.** As well as your site, students' browsers must be able to reach `webr.r-wasm.org` (R itself: about 30 MB on the first visit, after which the browser keeps a copy) and `repo.r-wasm.org` (R packages: the tidyverse, which the second course installs, takes about half a minute to download the first time). Students who use the AI assistant also need to reach their AI service (for Gemini, `generativelanguage.googleapis.com`).
3. **AI keys.** The assistant uses a key that each student enters themselves. The key is only kept in the browser tab, never in a file or in the browser's long-term storage. Free Gemini keys are available at [aistudio.google.com/apikey](https://aistudio.google.com/apikey) (students need a Google account and must be 18 or over); please read Google's [Gemini API Additional Terms](https://ai.google.dev/gemini-api/terms) first. The courses can be done without the assistant.
4. **Shared computers.** Students' work is stored in the browser profile, so computers that wipe profiles when students log out will lose it. Students should download their certificate when they finish a course, and their answers (with **My answers**) before they leave.
5. **Personal and patient data.** The courses use public training data. The instructions and the assistant's settings tell students never to put personal or patient data into an AI tool.

## Publishing it on GitHub Pages

1. On GitHub, open the repository's *Settings → Pages → Build and deployment* page. Under Source choose **Deploy from a branch**, then choose the branch **main** and the folder **/ (root)**, and click Save. (The repository needs to be public, unless your GitHub plan supports Pages for private repositories.)
2. After a minute or so, the site is at `https://comparativechrono.github.io/r-training/`. That is the address to give students: it opens the landing page.
3. The first time a browser opens a page of the site, the page reloads itself once. This installs a small service worker (`isolation-sw.js`), which makes the page *cross-origin isolated*: R needs this to be interrupted with <kbd>Esc</kbd> and to wait for typed input. Without it, R still works, but a long calculation can't be stopped except by restarting R.

The empty file `.nojekyll` stops GitHub from processing the site. The site doesn't need the `build/` and `test/` folders, but keep `assets/vendor/licenses/` and the licence files next to the fonts and libraries. To host the site on another web server, copy the folder; it needs no server-side code, but its address must use `https` (or be `localhost`).

**Students' work belongs to the site's address.** If the site moves to a different address, students start afresh there, and their certificates would have to be earned again. All the GitHub Pages sites of one account share one address (`https://comparativechrono.github.io`), so another site there must not use this site's `storePrefix` (see below).

## Trying it on your own computer

Opening the pages directly from your disk (`file://…`) doesn't work, because browsers block the Web Workers and data files that R needs. Serve the folder with a local web server instead:

```bash
cd r-training
python3 serve.py 8000        # then open http://localhost:8000
```

`serve.py` sends the cross-origin isolation headers itself. Any other local web server will do, as long as the address is `localhost` or uses `https`.

## Settings in `config.js`

`assets/js/config.js` holds the settings you are most likely to change. **Never put an API key in it**, because anyone can read the files of a public site.

| Setting | What it does |
| --- | --- |
| `courseTitle`, `courseSubtitle` | The name of the programme and the line under it |
| `certificate` | `awardedBy` (the department) and `institution`, printed at the top of the certificates and of the landing page; `signatory`, the name written as the signature and printed under it; and `signatoryRole`, an optional line under the signatory's name (when it is empty, the department is printed there instead) |
| `showModelAnswers` | `'after-try'` (the default) shows a *Show answer* button under a question once the student has answered it, right or wrong. `true` shows the button straight away, and `false` hides model answers altogether. The answers are still in the pages' source code, so adding `?answers` to the address shows them all, which is handy for tutors but also open to students |
| `storePrefix` | The prefix for everything the site saves in the browser (`rtr`). Both courses share it, so a student's files and name are the same in each |
| `webrBase`, `rRepos` | Where R (webR 0.6.0) and R packages are downloaded from |
| `liveProvider`, `geminiModel`, `geminiFallbackModels`, `anthropicModel`, `aiWaitSeconds` | The AI service offered first, and the models to use. Models are retired from time to time, so keep these up to date |
| `biowasmBase`, `hostname`, `storageWarnMB` | The programs used by the terminal inside RStudio, the computer name in its prompt, and how much a student can store before the page warns them |

The course titles, the summaries printed on the certificates and the text of the landing page are in `build/courses.py` and `build/landing.html`.

## Changing a course, or adding one

The pages are generated by Python, from the files in `build/`:

| File | What it holds |
| --- | --- |
| `courses.py` | The list of courses, in order: for each, its page, title, the summary printed on its certificate, the text of its card on the landing page, the tabs of its workbench, and what the AI assistant is told about it |
| `course_r_basics.py`, `course_tidyverse.py` | The chapters of each course. `ALL()` lists them in order |
| `lib.py` | The helpers that write the chapters' HTML (see below) |
| `template.html`, `landing.html` | The course page and the landing page, with `{{PLACEHOLDERS}}` for what changes |
| `make_pages.py` | Writes `r-basics.html`, `tidyverse.html` and `index.html` |

After a change, run `python3 build/make_pages.py`, try the pages with `python3 serve.py`, and commit the pages together with your changes. `make_pages.py` reports the number of steps and questions in each course, and stops with an error if two steps, questions or headings in a course have the same name.

The helpers in `lib.py` include those of the R workbench (`chapter`, `activity`, `task`, `q`, `mcq`, `callout` and the buttons) and these, written for the courses:

| Helper | What it produces |
| --- | --- |
| `rtask(id, html, rcheck)` | A step that ticks when the R expression `rcheck` is TRUE in RStudio's R session (it is evaluated quietly after each command, for the chapter on screen) |
| `lastv(cond)`, `tib(n, cols, test)`, `has_table(n, cols)`, `gg(geom, …)` | Ready-made R checks: a condition on the value of the last command (`v`); “the last command gave a table with `n` rows (and these columns)”; “there is a table like this in R's memory, whatever its name”; and “the last command drew a ggplot with this geometry, these aesthetics mapped to these columns, these fixed aesthetics, these titles, and R can draw it” |
| `console((code, output), …)` | A piece of RStudio's Console: commands and what R prints for them. The tests run every one of these and check that R really prints what the instructions show |
| `block(code)`, `rscode(code)`, `rstype(code)` | R code with a *show me* button that types it into RStudio's Console (the student presses <kbd>Enter</kbd>) |
| `optional(title, html)` | An *If you have time* part, whose steps and questions don't count towards the certificate |
| `vecop(a, b, op)` | A diagram of a vectorised operation between two vectors, with recycling (and R's warning, if you give it) |
| `table(head, rows)`, `kbd(...)` | A table, and keys to press |
| `certificate_chapter(...)` | The last chapter of a course, which shows the certificate |

Everything in `data/` (except `PROVENANCE.md`) is copied into each student's `~/data` folder on their first visit. If you add files after students have started, increase `STARTERS_VERSION` in `build/make_pages.py`. Changing the steps or questions of a course after students have finished it doesn't take away their certificates (the date they finished is kept), but students who haven't finished will need to do any new steps.

## What students keep, and privacy

Students' files, ticks, answers, name and settings are stored in the browser's storage for the site, on their own computer, and they are still there when the student comes back in the same browser. Nothing is stored on a server. A different browser, a different computer or a private window won't have them, and clearing the browser's data for the site deletes them. **My answers** downloads a student's answers as a web page, and **My files** downloads their files as a `.zip` file.

The site sets no cookies and has no tracking or analytics. The only things that leave a student's computer are: requests for the pages themselves; R and its packages (from `webr.r-wasm.org` and `repo.r-wasm.org`); anything the student's own R code downloads; and, only if the student connects an AI model, their questions and whatever context they choose to send with them, which go to the AI service they chose, using their own key. The student's name is never sent: in anything that goes to the AI service, it is replaced by `user`. Certificates are made in the browser.

## Limitations

- **R in the browser** is R 4.6.0 (webR 0.6.0). Each R session runs on one processor core, with WebAssembly's memory limit of a few gigabytes. Packages come from the webR repository, which has most of CRAN, including the whole of the tidyverse.
- **The RStudio tab is an imitation** made for teaching. It has the panes, menus, dialogs and messages of RStudio that the courses need, but it is not RStudio, and it isn't made or endorsed by Posit. What students learn in it carries over to the real program.
- **Cross-origin isolation** needs `https` (or `localhost`) and a browser that allows service workers. It was tested in Chromium; please try the browsers your students will use.

## How it was tested

The site was tested in Chromium (with Playwright) on 15 October 2026, with R and its packages downloaded from webR's servers, using the scripts in `test/`:

| Script | What it checks |
| --- | --- |
| `t00_answers.py` | That the short questions accept the right answers (in the forms students are likely to type them) and not the wrong ones. It doesn't need a browser |
| `t01_examples.py` | That every piece of Console shown in the instructions is what R really prints: it runs all of them (53 in the two courses) in RStudio's Console and compares the output |
| `t02_r_basics.py` | A student working through R basics from start to finish: their name, every step (including a script typed, run with <kbd>Ctrl</kbd>+<kbd>Enter</kbd> and saved), every question, steps that must *not* tick yet, the locked certificate and what it lists, the message when the course is finished, the certificate's preview and PDF (its text checked with `pdftotext`), and the landing page afterwards, with its preview and download |
| `t03_tidyverse.py` | The same for the Tidyverse course, including installing and loading the tidyverse, and plots that must not tick their steps (a plot R can't draw, the wrong colours, the wrong data) |

The R workbench's own tests were also run against the scripts that the courses share with it, to check that the changes made for the courses (the name, the R checks, the certificates and the Console's handling of progress messages) haven't broken anything there. To run the tests you need Python 3, Playwright with Chromium, and `pdftotext` (from poppler-utils):

```bash
python3 build/make_pages.py
python3 test/t00_answers.py
python3 test/t01_examples.py
python3 test/t02_r_basics.py
python3 test/t03_tidyverse.py
```

## Files

| Path | What it is |
| --- | --- |
| `index.html`, `r-basics.html`, `tidyverse.html` | The pages (generated: see `build/`) |
| `assets/js/` | The site's code. Most of it comes from the R workbench; `cert.js` (certificates and the name dialog) and `landing.js` (the landing page) were written for the courses, and `core.js`, `tutorial.js`, `page.js`, `workbench.js`, `rsession.js`, `rstudio.js`, `rui.js` and `assistant.js` were changed for them |
| `assets/css/` | The styles; `course.css` and `landing.css` were written for the courses |
| `assets/fonts/` | The certificate's fonts, with their licences |
| `assets/vendor/` | Third-party libraries, with their licences (see `THIRD_PARTY.md`) |
| `data/` | The courses' data, copied into each student's `~/data` (see `data/PROVENANCE.md`) |
| `build/`, `test/` | The generator of the pages, and the tests |
| `isolation-sw.js`, `serve.py` | The service worker for cross-origin isolation, and a local web server for trying the site |

## Credits and licences

- **The courses.** The exercises and data are from *Introduction to R (with Tidyverse)* by Simon Andrews and Laura Biggins, [Babraham Bioinformatics](https://www.bioinformatics.babraham.ac.uk/training.html), as adapted by Tim Hearn. The course is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 2.0 UK licence](https://creativecommons.org/licenses/by-nc-sa/2.0/uk/), and so are these adaptations of it (the text of the chapters, in `build/course_*.py` and the pages made from them, and the data in `data/`): you may copy, share and adapt them for non-commercial purposes, as long as you credit the authors and share your version under the same licence.
- **The workbench**, its code and the RStudio imitation come from the [R workbench](https://github.com/comparativechrono/r-workbench).
- **R** in the browser is [webR](https://docs.r-wasm.org/webr/). Certificates are made with [pdf-lib](https://pdf-lib.js.org) and its fork of fontkit (MIT), in [EB Garamond](https://github.com/octaviopardo/EBGaramond12) and [Great Vibes](https://github.com/googlefonts/great-vibes) (SIL Open Font Licence 1.1).
- The licences of everything included in the site, or downloaded by it, are listed in [THIRD_PARTY.md](THIRD_PARTY.md).
