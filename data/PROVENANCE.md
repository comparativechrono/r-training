# Where the data come from

The files in this folder are copied into each student's `~/data` folder the first time they open a course (this file is not). They are the data files of the course *Introduction to R (with Tidyverse)* by Simon Andrews and Laura Biggins of [Babraham Bioinformatics](https://www.bioinformatics.babraham.ac.uk/training.html), as adapted by Tim Hearn, and they are shared under the same licence as the course, the [Creative Commons Attribution-NonCommercial-ShareAlike 2.0 UK licence](https://creativecommons.org/licenses/by-nc-sa/2.0/uk/). They were taken from the course’s data archive, `R_tidyverse_intro_data`, as supplied for these courses in October 2026.

| File | What it holds | Used in |
| --- | --- | --- |
| `small_file.txt` | 40 samples, with the columns `Sample`, `Length` and `Category` (A, B, C or D). Tab-separated | Tidyverse: reading files, filtering, bar plots |
| `Child_Variants.csv` | 25,822 sequence variants found in a child’s exome, with the columns `CHR`, `POS`, `dbSNP` (“.” where a variant has no ID), `REF`, `ALT`, `QUAL`, `GENE`, `ENST`, `MutantReads`, `COVERAGE` and `MutantReadPercent`. Comma-separated | Tidyverse: reading files, filtering, pipes, histograms and density plots |
| `brain_bodyweight.txt` | The weights of the brains (g) and bodies (kg) of 27 species, with their logs (base 2) and a `Category` (Domesticated, Wild or Extinct). Tab-separated | Tidyverse: the first plots, labels, correlation and a line of best fit |
| `trumpton.txt` | Seven people, with their names, ages, weights and heights. Tab-separated | Tidyverse: the examples of reading, `select()`, `filter()` and pipes |
| `expr_data.txt` | The expression of 12 genes in WT and KO samples, with a p-value for each. Tab-separated | Tidyverse: the examples of plots |
| `transform_data.txt` | Ten pairs of values (WT and KO) and their differences. Tab-separated | Tidyverse: the example of transforming data in a filter |
| `many_values.txt` | 100,000 values, each with a genotype (WT or KO). Tab-separated | Tidyverse: the examples of histograms and density plots |
| `broken_selects.R` | A short script with mistakes in it, which students fix | Tidyverse: “If you have time” in the chapter on choosing columns and rows |
| `neutrophils.csv`, `chr_data.txt` | Two more small data sets from the original course, which these courses don’t use. They are there for students to explore | – |

**Changes.** Only `broken_selects.R` has been changed. Its first line set the working directory to a folder on the course author’s own computer, whose path included their user name; it now uses a made-up path (`C:/Users/someone/Desktop/R_tidyverse_intro_data`), which is still wrong on purpose, because correcting it is one of the exercises. Its line endings have also been changed from Windows (CRLF) to Unix (LF) ones. The other files are byte-for-byte as they were in the archive.

The archive also contains the course’s model answers (`answers.Rmd` and `answers.html`). They have been left out of this site, because it is public.

