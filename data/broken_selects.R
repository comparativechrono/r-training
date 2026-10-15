# Fix all of the problems in this script
# so everything works

setwd("C:/Users/someone/Desktop/R_tidyverse_intro_data")
library(tidyverse)
read_tsv("small_file.txt") -> small
read_tsv("Child_Variants.csv") -> child

filter(small, Category==A)

select(small, length>80)

select('small_file.txt',-Sample)

filter(Child, CHR=="MT")


