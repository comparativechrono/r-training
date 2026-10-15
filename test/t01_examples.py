"""What the instructions show R printing (the Console snippets made with lib.console()) is what R really prints, in
RStudio's Console, with the Console 80 characters wide. Downloads the tidyverse (about a minute).
Run:  python3 test/t01_examples.py [r-basics|tidyverse]"""
import sys
import time
from student import Student, check
import lib
import course_r_basics
import course_tidyverse

which = sys.argv[1:] or ['r-basics', 'tidyverse']

if 'r-basics' in which:
    lib.EXAMPLES.clear()
    course_r_basics.ALL()
    ex = list(lib.EXAMPLES)
    print(len(ex), 'examples in R basics')
    s = Student('r-basics.html')
    # (the objects that the text creates with code shown in boxes, before its examples use them)
    s.run('simple.vector <- c(1, 2, 4, 6, 3)\nsome.names <- c("Ada", "Grace", "Alan", "Mary", "Rosalind")\nsome.numbers <- c(2, 5, 8, 12, 16)')
    s.run(course_r_basics.RESULTS_CODE)
    s.run(course_r_basics.ALL_RESULTS_CODE)
    s.examples(ex)
    check(not s.p.errors, f'no errors in the page ({s.p.errors[:3]})')
    s.close()

if 'tidyverse' in which:
    lib.EXAMPLES.clear()
    course_tidyverse.ALL()
    ex = list(lib.EXAMPLES)
    print(len(ex), 'examples in Tidyverse')
    s = Student('tidyverse.html')
    t0 = time.time()
    s.run('install.packages("tidyverse")')
    s.run('library(tidyverse)')
    print(f'tidyverse installed and loaded in {time.time() - t0:.0f} s')
    s.run('setwd("~/data")')
    s.run(course_tidyverse.WIDE)
    s.run('expression <- read_tsv("expr_data.txt", show_col_types = FALSE)')
    s.examples(ex)
    check(not s.p.errors, f'no errors in the page ({s.p.errors[:3]})')
    s.close()

print('failed:', check.failed)
sys.exit(1 if check.failed else 0)
