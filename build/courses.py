"""The courses of the site, in order. make_pages.py makes a page for each (from template.html and the course's
module of chapters) and the landing page (index.html) that lists them.

To add a course: write its module of chapters (like course_r_basics.py, with ALL() listing the chapters), add an
entry here, and run  python3 build/make_pages.py."""

PROGRAMME = 'Introduction to R'

# the tabs of the workbench that a course page can have: (button title, label, the icon's SVG paths, the pane's root)
TABS = {
    'console': ('The standard R console', 'R console', '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 10l3 2-3 2M12 15h5"/>', 'rconRoot'),
    'rstudio': ('RStudio, an integrated development environment for R', 'RStudio', '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M12 4v16M3 12h18"/>', 'rsRoot'),
    'notebook': ('Jupyter-style notebooks in R', 'Notebook', '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 3v18M12 8h4M12 12h4"/>', 'nbRoot'),
    'terminal': ('A bash terminal, with Rscript and R', 'Terminal', '<path d="M4 17l6-5-6-5M12 19h8"/>', 'termRoot'),
    'editor': ('Your files and a text editor', 'Files', '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v1H7l-4 9z"/><path d="M3 19l3.5-8H22l-3.5 8z"/>', 'edRoot'),
    'assistant': ('AI assistant', 'AI', '<path d="M12 3l2 5.5L19.5 10 14 12l-2 5.5L10 12l-5.5-2L10 8.5z"/><path d="M19 17l.8 2 2 .8-2 .8-.8 2-.8-2-2-.8 2-.8z"/>', 'aiRoot'),
}

DATA_FILES = ('small_file.txt (tab-separated: 40 samples, with the columns Sample, Length and Category, which is A, B, C or D), '
              'Child_Variants.csv (25,822 variants found in a child’s exome, with the columns CHR, POS, dbSNP, REF, ALT, QUAL, GENE, ENST, '
              'MutantReads, COVERAGE and MutantReadPercent; dbSNP is "." where a variant has no ID), brain_bodyweight.txt (tab-separated: '
              '27 species, with the columns Species, Category (Domesticated, Wild or Extinct), body (kg), brain (g), log.brain and log.body), '
              'trumpton.txt (tab-separated: 7 people, with LastName, FirstName, Age, Weight and Height), expr_data.txt (Gene, WT, KO, pValue), '
              'transform_data.txt (WT, KO, difference), many_values.txt (100,000 values, each with a genotype, WT or KO), neutrophils.csv '
              '(the columns DMSO, TGX-221, PI103 and Akt1, with missing values), chr_data.txt, and broken_selects.R (a script with '
              'mistakes in it, which an exercise asks the student to fix)')

COURSES = [
    {
        'id': 'r-basics',
        'page': 'r-basics.html',
        'data_page': 'rbasics',
        'module': 'course_r_basics',
        'title': 'R basics',
        'part': 1,
        'programme': 'Part 1 of ' + PROGRAMME,
        'subtitle': PROGRAMME + ', part 1: the R language, in RStudio',
        'description': 'R basics, the first part of an introduction to R for people who are new to it: calculations, objects, '
                       'functions and help, vectors and vectorised operations, and R’s data structures. R runs in your web browser, in an '
                       'RStudio-style workbench, so there is nothing to install.',
        'cert_summary': 'Using R in RStudio: calculations, objects, functions and help, vectors and vectorised operations, '
                        'and R’s data structures.',
        'seal': 'R basics',
        'card': 'Your first steps in R. Use it as a calculator, keep values in objects, call functions and read their help, and '
                'get to know vectors, the building blocks of all data in R.',
        'topics': ['Calculations, and objects to keep values in', 'Functions, their arguments, and R’s help', 'Vectors: c(), seq(), rep() and the colon',
                   'Vectorised operations and recycling', 'Random numbers and a first t-test', 'Lists, data frames and tibbles'],
        'time': 'About 2½ hours',
        'tabs': ['rstudio', 'editor', 'assistant'],
        'first': 'rstudio',
        'ai': {
            'course': 'R basics (the first part of Introduction to R), which teaches base R in RStudio',
            'aiData': 'The course’s data are in ~/data: ' + DATA_FILES + '. This first course mostly works with values the student types '
                      'in (numbers, text, and vectors made with c(), :, seq(), rep() and rnorm()), and ends with data frames.',
            'aiStyle': 'Show small, complete examples that run here. This course teaches base R, without packages: calculations, objects '
                       '(<- and ->), functions and their arguments (by position and by name), help (?name and ??words), vectors '
                       '(c(), the colon operator, seq(), rep()), vectorised operations and recycling, selecting values with [ ], '
                       'rnorm() and t.test(), and lists and data frames with $. Use base R in your examples, and leave the tidyverse '
                       'for the second course unless the student asks about it.',
            'aiChat': ['What is the difference between <- and = in R?',
                       'Why does c(1, 2, 3, "fred") turn the numbers into text?',
                       'What does recycling mean when I add two vectors of different lengths?',
                       'What does “Error: object not found” mean, and how do I fix it?'],
            'ex': {'obj': 'all.results', 'Obj': 'All.results', 'dataName': 'your data frame', 'file': '~/data/small_file.txt',
                   'read': 'small <- read.delim("~/data/small_file.txt")', 'mean': 'mean(all.results$mon)',
                   'cols': ['mon', 'tue', 'wed', 'pass', 'Sample', 'Length', 'Category'], 'factors': ['Category', 'Sample', 'pass']},
        },
    },
    {
        'id': 'tidyverse',
        'page': 'tidyverse.html',
        'data_page': 'tidyverse',
        'module': 'course_tidyverse',
        'title': 'Tidyverse',
        'part': 2,
        'programme': 'Part 2 of ' + PROGRAMME,
        'subtitle': PROGRAMME + ', part 2: reading, filtering and plotting data',
        'description': 'Tidyverse, the second part of an introduction to R for people who are new to it: reading data from files with '
                       'readr, choosing rows and columns with dplyr, combining steps with pipes, and drawing plots with ggplot2. R runs '
                       'in your web browser, in an RStudio-style workbench, so there is nothing to install.',
        'cert_summary': 'Working with data in the tidyverse: reading files with readr, choosing rows and columns with dplyr, '
                        'combining steps with pipes, and drawing plots with ggplot2.',
        'seal': 'Tidyverse',
        'card': 'Read data from files into tibbles, pick out the rows and columns you need, chain the steps together with pipes, '
                'and draw plots with ggplot2. Do R basics first.',
        'topics': ['Installing and loading the tidyverse', 'Reading files with readr, and tidy data', 'Choosing columns and rows: select() and filter()',
                   'Pipes: one step after another', 'Plots with ggplot2: points, bars, histograms', 'Titles, labels, and a line of best fit'],
        'time': 'About 3 hours',
        'tabs': ['rstudio', 'editor', 'assistant'],
        'first': 'rstudio',
        'ai': {
            'course': 'Tidyverse (the second part of Introduction to R), which teaches the tidyverse in RStudio',
            'aiData': 'The course’s data are in ~/data: ' + DATA_FILES + '.',
            'aiStyle': 'Show small, complete examples that run here, in the style of this course: the tidyverse, loaded with '
                       'library(tidyverse) (installed once with install.packages("tidyverse")) – readr (read_csv, read_tsv), dplyr '
                       '(select, filter, and the pipe %>%), and ggplot2 (ggplot, aes, geom_point, geom_col, geom_bar, geom_histogram, '
                       'geom_density, geom_text, ggtitle, xlab, ylab, geom_abline). Inside dplyr and ggplot2 functions, columns are '
                       'used by their names; $ takes a single column out as a vector.',
            'aiChat': ['Why does read_tsv() print a “column specification”?',
                       'What is the difference between select() and filter()?',
                       'What does the pipe %>% do?',
                       'When do I use geom_bar() and when geom_col()?'],
            'ex': {'obj': 'child', 'Obj': 'Child', 'dataName': 'the child variants data', 'file': '~/data/Child_Variants.csv',
                   'read': 'child <- read_csv("~/data/Child_Variants.csv")', 'mean': 'mean(child$MutantReadPercent)',
                   'cols': ['CHR', 'POS', 'dbSNP', 'REF', 'ALT', 'QUAL', 'GENE', 'ENST', 'MutantReads', 'COVERAGE', 'MutantReadPercent',
                            'Sample', 'Length', 'Category', 'Species', 'body', 'brain', 'log.brain', 'log.body',
                            'LastName', 'FirstName', 'Age', 'Weight', 'Height'],
                   'factors': ['CHR', 'REF', 'ALT', 'GENE', 'Category', 'Sample', 'Species', 'LastName', 'FirstName']},
        },
    },
]
