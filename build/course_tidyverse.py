"""Tidyverse: the second course of Introduction to R.

Working with data in the tidyverse, in RStudio: packages, reading files with readr, tidy data, choosing columns and rows
with dplyr, pipes, and plots with ggplot2. Adapted from the exercises of Introduction to R (with Tidyverse) by Simon
Andrews and Laura Biggins (Babraham Bioinformatics), as adapted by Tim Hearn, with the ideas from the course's slides
worked into the text (CC BY-NC-SA 2.0 UK)."""
from lib import *

# ---- checks made by R (see lib.rtask) ----
SMALL_COLS = ['Sample', 'Length', 'Category']
CHILD_COLS = ['CHR', 'POS', 'dbSNP', 'REF', 'ALT', 'QUAL', 'GENE', 'MutantReadPercent']
BRAIN_COLS = ['Species', 'Category', 'body', 'brain', 'log.brain', 'log.body']
LOADED = '"package:tidyverse" %in% search()'
IN_DATA = 'basename(getwd()) == "data"'
NO_SAMPLE = 'is.data.frame(v) && nrow(v) == 40 && identical(sort(names(v)), c("Category", "Length"))'
NO_ENST = 'is.data.frame(v) && nrow(v) == 25822 && ncol(v) == 9 && !any(c("ENST", "dbSNP") %in% names(v))'
QUALITY = 'all(v$QUAL == 200) && all(v$COVERAGE > 50) && all(v$MutantReadPercent > 70)'
CHR_POS = 'is.data.frame(v) && nrow(v) == 23690 && identical(names(v), c("CHR", "POS"))'
BINWIDTH = 'any(vapply(v$layers, function(l) !is.null(l$stat_params$binwidth), logical(1)))'
NO_EXTINCT = 'nrow(v$data) == 24 && !("Extinct" %in% v$data$Category)'

# what the short questions accept (regular expressions, tried on the answer in lower case with its spaces tidied)
ACC_MEDIAN = r'^6\.2[23]\d*$'
ACC_MEAN = r'^59\.88?\d*$||^59\.9$'
ACC_SD = r'^24\.1[12]?\d*$'
ACC_REF = r'^g$||^g \(?6,?982\)?$'
ACC_P = r'^2\.44 ?(e-0?6|x ?10\^?-6|× ?10\^?-6)$||^0\.00000244\d*$'

NAME_BTN = '<button class="do" type="button" data-student-name="1">Add your name</button>'

WIDE = '''wide <- tibble(
  Gene = c("ABC1", "DEF1"),
  WT_1 = c(8.86, 29.60), WT_2 = c(4.18, 41.22), WT_3 = c(8.90, 36.15),
  KO_1 = c(4.00, 11.18), KO_2 = c(14.52, 16.68), KO_3 = c(13.39, 1.64)
)'''
LONG_OUT = '''# A tibble: 12 × 4
   Gene  Genotype Replicate Value
   <chr> <chr>    <chr>     <dbl>
 1 ABC1  WT       1          8.86
 2 ABC1  WT       2          4.18
 3 ABC1  WT       3          8.9
 4 ABC1  KO       1          4
 5 ABC1  KO       2         14.5
 6 ABC1  KO       3         13.4
 7 DEF1  WT       1         29.6
 8 DEF1  WT       2         41.2
 9 DEF1  WT       3         36.2
10 DEF1  KO       1         11.2
11 DEF1  KO       2         16.7
12 DEF1  KO       3          1.64'''
LONG = 'pivot_longer(wide, -Gene, names_to = c("Genotype", "Replicate"), names_sep = "_", values_to = "Value")'

TRUMPTON_READ = '''Rows: 7 Columns: 5
── Column specification ────────────────────────────────────────────────────────
Delimiter: "\\t"
chr (2): LastName, FirstName
dbl (3): Age, Weight, Height

ℹ Use `spec()` to retrieve the full column specification for this data.
ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.'''

TRUMPTON = '''# A tibble: 7 × 5
  LastName FirstName   Age Weight Height
  <chr>    <chr>     <dbl>  <dbl>  <dbl>
1 Hugh     Chris        26     90    175
2 Pew      Adam         32    102    183
3 Barney   Daniel       18     88    168
4 McGrew   Chris        48     97    155
5 Cuthbert Carl         28     91    188
6 Dibble   Liam         35     94    145
7 Grub     Doug         31     89    164'''

SELECT_NAMES = '''# A tibble: 7 × 3
  FirstName LastName Weight
  <chr>     <chr>     <dbl>
1 Chris     Hugh         90
2 Adam      Pew         102
3 Daniel    Barney       88
4 Chris     McGrew       97
5 Carl      Cuthbert     91
6 Liam      Dibble       94
7 Doug      Grub         89'''

SELECT_POS = '''# A tibble: 7 × 2
  FirstName Weight
  <chr>      <dbl>
1 Chris         90
2 Adam         102
3 Daniel        88
4 Chris         97
5 Carl          91
6 Liam          94
7 Doug          89'''

SELECT_NEG = '''# A tibble: 7 × 4
  FirstName   Age Weight Height
  <chr>     <dbl>  <dbl>  <dbl>
1 Chris        26     90    175
2 Adam         32    102    183
3 Daniel       18     88    168
4 Chris        48     97    155
5 Carl         28     91    188
6 Liam         35     94    145
7 Doug         31     89    164'''

FILTER_170 = '''# A tibble: 3 × 5
  LastName FirstName   Age Weight Height
  <chr>    <chr>     <dbl>  <dbl>  <dbl>
1 Hugh     Chris        26     90    175
2 Pew      Adam         32    102    183
3 Cuthbert Carl         28     91    188'''

FILTER_CHRIS = '''# A tibble: 2 × 5
  LastName FirstName   Age Weight Height
  <chr>    <chr>     <dbl>  <dbl>  <dbl>
1 Hugh     Chris        26     90    175
2 McGrew   Chris        48     97    155'''

TRANSFORM = '''# A tibble: 10 × 3
       WT      KO difference
    <dbl>   <dbl>      <dbl>
 1 -5.11   -3.29       1.81
 2  1.12   -1.85      -2.97
 3 -3.99   -3.77       0.222
 4 -4.18   -2.46       1.72
 5 -1.93  -10.0       -8.10
 6 -8.69   -2.38       6.31
 7 -0.670   2.73       3.40
 8 -1.15   -2.59      -1.43
 9 -1.98    1.83       3.80
10 -1.06    0.372      1.43'''

TRANSFORM_ABS = '''# A tibble: 2 × 3
     WT     KO difference
  <dbl>  <dbl>      <dbl>
1 -1.93 -10.0       -8.10
2 -8.69  -2.38       6.31'''

AGE_WEIGHT = '''# A tibble: 1 × 2
    Age Weight
  <dbl>  <dbl>
1    26     90'''

PIPED = '''trumpton %>%
  filter(Height >= 170) %>%
  filter(FirstName == "Chris") %>%
  select(Age, Weight)'''

LONG_WAY = '''filter(trumpton, Height >= 170) -> answer1
filter(answer1, FirstName == "Chris") -> answer2
select(answer2, Age, Weight)'''

EXPRESSION = '''# A tibble: 12 × 4
   Gene       WT     KO pValue
   <chr>   <dbl>  <dbl>  <dbl>
 1 Mia1     5.83  3.24  0.1
 2 Snrpa    8.59  5.02  0.001
 3 Itpkc    8.49  6.16  0.04
 4 Adck4    7.69  6.41  0.2
 5 Numbl    8.37  6.81  0.1
 6 Ltbp4    6.96 10.4   0.001
 7 Shkbp1   7.57  5.83  0.1
 8 Spnb4   10.7   9.38  0.2
 9 Blvrb    7.32  5.29  0.05
10 Pgam1    0     0.285 0.5
11 Sertad3  8.13  3.02  0.0001
12 Sertad1  7.69  4.34  0.01  '''

FIRST_PLOT = 'ggplot(expression, aes(x = WT, y = KO)) + geom_point()'
RED_PLOT = '''expression %>%
  ggplot(aes(x = WT, y = KO)) +
  geom_point(colour = "red2", size = 5)'''
COL_PLOT = '''expression %>%
  ggplot(aes(x = Gene, y = WT)) +
  geom_col(fill = "red2")'''
HIST_PLOT = '''many.values %>%
  ggplot(aes(x = values)) +
  geom_histogram(binwidth = 0.1, fill = "yellow", colour = "black")'''
DENS_PLOT = '''many.values %>%
  ggplot(aes(x = values, fill = genotype)) +
  geom_density(colour = "black", alpha = 0.5)'''
LABEL_PLOT = '''expression %>%
  ggplot(aes(x = WT, y = KO, label = Gene)) +
  geom_point() +
  ggtitle("Expression level comparison") +
  xlab("WT expression level (log2 RPM)") +
  ylab("KO expression level (log2 RPM)") +
  geom_text(vjust = 1.2)'''
BROKEN_PLUS = '''ggplot(brain, aes(x = log.brain, y = log.body))
  + geom_point()'''


INSTALL = 'install.packages("tidyverse")'
TRUMPTON_CMD = 'trumpton <- read_tsv("~/data/trumpton.txt")'
EXPR_CMD = 'expression <- read_tsv("~/data/expr_data.txt")'
BLUE = 'colour = "blue2"'
Q_GENE = '17, from <code>filter(child, GENE == &quot;IGFN1&quot;)</code>.'
FIX_MODEL = ('The path in <code>setwd()</code> is for someone else’s computer (here it should be <code>setwd(&quot;~/data&quot;)</code>); '
             '<code>Child_Variants.csv</code> is a CSV file, so it needs <code>read_csv()</code>, not <code>read_tsv()</code>; '
             '<code>Category==A</code> needs quotes around A; <code>select(small, length&gt;80)</code> should be <code>filter()</code>, '
             'because it chooses rows, and the column is <code>Length</code>, with a capital L; <code>select()</code> needs the tibble '
             '<code>small</code>, not the name of the file, as its first argument; and the tibble is called <code>child</code>, not <code>Child</code>.')
PLUS_Q = ('Why does this code draw a plot with no points, and then give an error?<pre class="codeblock">' +
          BROKEN_PLUS.replace('<', '&lt;').replace('>', '&gt;') + '</pre>')
PLUS_OPTS = [
    ("The + is at the start of the second line, so R thinks the command ended with the first line", True, "R ran the first line as a complete command, which draws an empty plot, and then found a line starting with +. Move the + to the end of the first line."),
    ("geom_point() needs its own aes()", False, "geom_point() uses the aesthetics given to ggplot() unless you give it others."),
    ("The data should be piped into ggplot()", False, "Piping and giving the tibble as the first argument do the same thing."),
]


def packages():
    items = [
        ('tibble', 'Tibbles, the tidyverse’s tables of data'),
        ('readr', 'Reading data from text files into tibbles, and writing tibbles to files'),
        ('tidyr', 'Tidying data, so that it is laid out in the right shape'),
        ('dplyr', 'Choosing, filtering, changing and summarising data'),
        ('ggplot2', 'Drawing plots and graphs'),
    ]
    return table(['Package', 'What it is for'], [(f'<b>{a}</b>', b) for a, b in items])


# ---------------------------------------------------------------------------------------------------------------------
def ch_start():
    body = f'''
<h2 id="t-what">What the tidyverse is</h2>
<p>R comes with everything you need to work with data, but over the years its functions have grown up in different styles, with different names and orders of arguments for similar jobs. The <b>tidyverse</b> is a collection of packages that share a single design. Data are kept in tibbles, laid out in a consistent (“tidy”) way, and almost every function takes a tibble as its first argument and gives you a tibble back, so that the functions fit together. The core packages are:</p>
{packages()}
<p>There are a few more, such as <b>stringr</b> for working with text, <b>forcats</b> for factors and <b>lubridate</b> for dates, which you won’t need in this course.</p>

<h2 id="t-packages">Installing and loading packages</h2>
<p>A <b>package</b> is a bundle of functions (and sometimes data) that adds to what R can do. There are two steps to using one:</p>
<ul>
<li><code>install.packages("tidyverse")</code> downloads the package and installs it. You only need to do this once: on your own computer it stays installed, and here it is kept in your browser for the next time you come back.</li>
<li><code>library(tidyverse)</code> loads the package into R’s memory, so that you can use its functions. You need to do this in every new R session: each time you start RStudio, restart R, or come back to this course.</li>
</ul>
<p>When it loads, the tidyverse tells you which packages it has attached, and their versions. It also lists some <b>conflicts</b>, such as <code>dplyr::filter() masks stats::filter()</code>. This means that two packages have a function with the same name, and that, from now on, <code>filter</code> means the one from dplyr. That is what you want, so you can ignore the message. If you ever need the other one, you can name its package, as in <code>stats::filter()</code>.</p>

<h2 id="t-how">How this course works</h2>
<p>This course works in the same way as R basics. The steps of each activity tick themselves when R sees that you have done them (or you can tick them yourself), questions with a <b>Check</b> button are marked straight away, and <b>Show answer</b> appears once you have had a go at a question. Parts marked <b>If you have time</b> don’t count towards your certificate. When you have done everything else, the last chapter has your certificate, with the name you give below.</p>
<p>Most of the steps in this course ask you to write some R yourself, and the text before each activity shows you examples of what you need.</p>
{callout("concept", "Keep your commands in a script", "<p>Whenever R starts again (when you come back to the course, or restart R), it starts afresh: the tidyverse isn’t loaded, the working directory is your home folder, and none of your data have been read in. If you keep your commands in a script as you go, starting with <code>library(tidyverse)</code>, you can get back to where you were by clicking <b>Source</b> at the top of the script, which runs the whole of it.</p>")}
{callout("warn", "AI tools and your data", "<p>The <b>AI</b> tab has an AI assistant that you can ask about R, if you have a key for an AI service. Anything you type into it is sent to an AI company. Never paste personal data or patient data into it, or into any other AI tool.</p>")}
{activity("Get ready", [
    task("t-name", f'Add your name for your certificate (if you did R basics in this browser, it is already there): {NAME_BTN}', check="named"),
    task("t-script", f'Start a new script (File ▸ New File ▸ <b>R Script</b>) and save it as {c("tidyverse.R")}. Write the commands from this course in it as you go.', auto="rstudio:saved path~tidyverse"),
    task("t-install", f'Install the tidyverse: {rscode(INSTALL)}. This takes about half a minute the first time.', check="installed:tidyverse", auto="rstudio:installed"),
    rtask("t-library", f'Load it with {rscode("library(tidyverse)")}, and read the messages it gives you. The first time, this takes about another half a minute.', LOADED),
])}
'''
    return chapter("start", "0", "Start here", "rstudio", "Welcome to the tidyverse", 15,
                   "The tidyverse is a collection of R packages for reading, tidying, transforming and plotting data, all designed to work together. This course builds on R basics, so if you haven’t done that course yet, do it first.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_reading():
    body = f'''
<h2 id="rd-readr">readr</h2>
<p>readr has a function for each of the common kinds of text file of data, and functions that write tibbles back out to files:</p>
{table(['Function', 'What it does'], [
    ('<code>read_csv("file.csv")</code>', 'reads a file of comma-separated values'),
    ('<code>read_tsv("file.txt")</code>', 'reads a file of tab-separated values (often ending in <code>.txt</code> or <code>.tsv</code>)'),
    ('<code>write_csv(data, "file.csv")</code>', 'writes a tibble to a file of comma-separated values'),
    ('<code>write_tsv(data, "file.txt")</code>', 'writes a tibble to a file of tab-separated values'),
])}
<p>Like any other function, <code>read_csv()</code> only gives you the data: it doesn’t keep them for you. To work with the data afterwards, store them in an object, as in <code>child &lt;- read_csv("Child_Variants.csv")</code>.</p>

<h2 id="rd-paths">File paths and the working directory</h2>
<p>A <b>file path</b> tells R where a file is. <code>~/data/small_file.txt</code> is the file <code>small_file.txt</code> in the <code>data</code> folder of your home folder, which is what <code>~</code> stands for. You can give R the full path of a file every time, but it soon becomes tedious. Instead, you can set R’s <b>working directory</b>: the folder in which R looks for files, unless you tell it otherwise. Once it is set, the name of a file in that folder is enough.</p>
<ul>
<li><code>getwd()</code> tells you what the working directory is, and <code>setwd("~/data")</code> changes it to your <code>data</code> folder.</li>
<li>In RStudio, you can also choose Session ▸ <b>Set Working Directory</b> ▸ <b>Choose Directory…</b>, or go to the folder in the Files pane and choose <b>More</b> ▸ <b>Set As Working Directory</b>. RStudio shows you the <code>setwd()</code> command it runs, which you can copy into your script.</li>
</ul>
<p>RStudio can also fill in file names for you. Type <code>read_tsv("")</code>, put the cursor between the quotes, and press <kbd>Tab</kbd>: RStudio lists the files in the working directory, and you can pick one rather than typing its name (and perhaps mistyping it).</p>

<h2 id="rd-spec">What readr tells you</h2>
<p>When it reads a file, readr guesses what type of data each column holds, and it tells you what it decided. Try it with a small file of seven people, giving its full path, because you haven’t set the working directory yet: {rscode(TRUMPTON_CMD)}</p>
{console((TRUMPTON_CMD, TRUMPTON_READ), ("trumpton", TRUMPTON))}
<p><code>chr</code> means character (text), and <code>dbl</code> means a number (it is short for <em>double</em>, which is how computers store numbers with decimal places). Always check readr’s guesses: a column of numbers that has been read as <code>chr</code> usually means that something in the column isn’t a number, such as a word, or a comma used as a decimal point. When you print a tibble, you see the type of each column under its name, and only the first ten rows; <code>View()</code>, or a click on the tibble in the Environment pane, shows you all of it.</p>
<p>As in R basics, <code>$</code> takes a single column out of a tibble, as a vector, so that you can give it to functions such as <code>mean()</code>:</p>
{console(("mean(trumpton$Height)", "[1] 168.2857"))}
{activity("Read some files", [
    rtask("rd-wd", 'Set the working directory to your <code>data</code> folder.', IN_DATA),
    rtask("rd-small", f'Read {c("small_file.txt")}, which is a tab-separated file, into a new tibble called {c("small")}. Use <kbd>Tab</kbd> to fill in the name of the file.', has_table(40, SMALL_COLS)),
    task("rd-view", f'View {c("small")}, and check that the types that readr guessed for its columns make sense.', auto="r:view kind=rstudio nrow=40"),
    rtask("rd-median", f'Find the median of the log2 of the lengths in {c("small")}. Use {c("$")} to take out the {c("Length")} column, {c("log2()")} to transform the values, and {c("median()")} to find the median of the result.', lastv("isTRUE(all.equal(v, 6.227664, tolerance = 1e-6))")),
    rtask("rd-child", f'Read {c("Child_Variants.csv")}, which is a file of comma-separated values, into a tibble called {c("child")}.', has_table(25822, CHILD_COLS)),
    task("rd-print", f'Print {c("child")} in the Console to see what it looks like, and then open it in the viewer by clicking on it in the Environment pane.', auto="r:view kind=rstudio nrow=25822"),
    rtask("rd-mean", f'Calculate the mean and the standard deviation of the {c("MutantReadPercent")} column of {c("child")}.', lastv("isTRUE(all.equal(v, 24.11675, tolerance = 1e-6))")),
])}
{q("rd-q-median", "What is the median of the log2 of the lengths?", "6.227664, from <code>median(log2(small$Length))</code>.", accept=ACC_MEDIAN, placeholder="A number")}
{q("rd-q-mean", "What is the mean of the MutantReadPercent column?", "59.88219, from <code>mean(child$MutantReadPercent)</code>.", accept=ACC_MEAN, placeholder="A number")}
{q("rd-q-sd", "And its standard deviation?", "24.11675, from <code>sd(child$MutantReadPercent)</code>.", accept=ACC_SD, placeholder="A number")}
{mcq("rd-q-type", "readr tells you <code>chr (6): CHR, dbSNP, REF, ALT, GENE, ENST</code>. Why has it read the column <code>CHR</code>, the chromosome, as text rather than as numbers?", [
    ("Because some chromosomes are called X, Y or MT, which aren’t numbers", True, "One value that isn’t a number is enough to make readr read the whole column as text. Here that is the right decision: a chromosome is a name, even when it looks like a number."),
    ("Because readr reads every column as text", False, "readr read POS, QUAL and the other numeric columns as numbers (dbl)."),
    ("Because CSV files can only hold text", False, "Everything in a CSV file is written as text, but readr turns columns that hold only numbers into numbers."),
])}
'''
    return chapter("reading", "1", "Reading files", "rstudio", "Reading data from files", 25,
                   "Most data reach R in a file. readr, one of the packages of the tidyverse, reads files of data into tibbles, and it tells you how it has interpreted each column.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_tidy():
    wide = table(['Gene', 'WT_1', 'WT_2', 'WT_3', 'KO_1', 'KO_2', 'KO_3'], [
        ('ABC1', '8.86', '4.18', '8.90', '4.00', '14.52', '13.39'),
        ('DEF1', '29.60', '41.22', '36.15', '11.18', '16.68', '1.64'),
    ])
    rows = [('ABC1', 'WT', '1', '8.86'), ('ABC1', 'WT', '2', '4.18'), ('ABC1', 'WT', '3', '8.90'), ('ABC1', 'KO', '1', '4.00'),
            ('ABC1', 'KO', '2', '14.52'), ('ABC1', 'KO', '3', '13.39'), ('DEF1', 'WT', '1', '29.60'), ('DEF1', 'WT', '2', '41.22'),
            ('DEF1', 'WT', '3', '36.15'), ('DEF1', 'KO', '1', '11.18'), ('DEF1', 'KO', '2', '16.68'), ('DEF1', 'KO', '3', '1.64')]
    long = table(['Gene', 'Genotype', 'Replicate', 'Value'], rows)
    body = f'''
<p>Think of a simple experiment, in which two genes (ABC1 and DEF1) are measured in two genotypes (WT and KO), with three replicates of each. Here are the results in <b>wide</b> format, with a row for each gene:</p>
{wide}
<p>This table is compact and easy to read, and you can see the measurements of each gene at a glance. But the genotype and the replicate of each value are hidden in the names of the columns, and the values are spread over six columns. If you wanted to record something else about each sample, such as the batch it was processed in, there would be nowhere obvious to put it.</p>
<p>Here are the same results in <b>long</b> format:</p>
{long}
<p>This is more verbose, because values such as the gene names are repeated. But the genotype and the replicate are now columns of their own, all the measurements are in a single column, and recording the batch of each sample would simply mean adding a <code>Batch</code> column.</p>

<h2 id="td-rules">What makes data tidy</h2>
<p>The long format is what the tidyverse calls <b>tidy</b> data:</p>
<ul>
<li>each variable has its own column,</li>
<li>each observation has its own row, and</li>
<li>each value has its own cell.</li>
</ul>
<p>The functions of the tidyverse expect data to be tidy. For a plot of the values coloured by genotype, for example, ggplot2 needs a column that says what the genotype of each value is, and the wide table doesn’t have one. Data often arrive in wide format, because that is how people lay out tables for reading, and the tidyr package has functions for converting between the two formats: <code>pivot_longer()</code> and <code>pivot_wider()</code>.</p>
{mcq("td-q-batch", "In the long format, how would you record the batch in which each sample was processed?", [
    ("Add a column called <code>Batch</code>", True, "In tidy data each variable has its own column, so a new variable means a new column."),
    ("Add a new row for each batch", False, "A row is a single observation (one measurement, here). The batch is a property of each observation, so it needs a column."),
    ("Put the batch into the names of the columns, as in WT_1_batch2", False, "That is how the wide format hides information in its column names, which is exactly what tidy data avoids."),
])}
{mcq("td-q-tidy", "A table has one row for each patient, with the columns <code>Patient</code>, <code>Monday</code>, <code>Tuesday</code> and <code>Wednesday</code>, which hold the patient’s blood pressure on each day. Is it tidy?", [
    ("No: the day is a variable, so a tidy version would have the columns Patient, Day and BloodPressure", True, "The days are hidden in the column names. A tidy table would have a row for each patient on each day."),
    ("Yes: each patient has a row of their own", False, "Each row holds three observations (three days), and the day itself isn’t in a column of its own."),
    ("Yes, as long as there are no missing values", False, "Tidiness is about how the table is laid out, not about whether it is complete."),
])}
{optional("Making wide data long", f"""
<p>Type in the wide table as a tibble, and then make it long with <code>pivot_longer()</code>. Its arguments say which columns to gather up (all except <code>Gene</code>), what to call the new columns that the old column names go into, how to split the old names (at the <code>_</code>), and what to call the column of values:</p>
{block(WIDE)}
{console((LONG, LONG_OUT))}
{activity("Tidy it", [rtask("td-long", "Make the wide table long, as above.", tib(12, ['Gene', 'Genotype', 'Replicate', 'Value']))])}
""")}
'''
    return chapter("tidy", "2", "Tidy data", "rstudio", "Tidy data", 10,
                   "A table of data can often be laid out in more than one way. The tidyverse has a clear opinion about which way is best, and its functions are designed around it.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_filter():
    tests = [
        ('<code>Height &gt; 170</code>', '<code>Height &lt; 170</code>', 'greater than, less than'),
        ('<code>Height &gt;= 170</code>', '<code>Height &lt;= 180</code>', 'greater than or equal to, less than or equal to'),
        ('<code>Age == 26</code>', '<code>FirstName == "Chris"</code>', 'equal to'),
        ('<code>Age != 26</code>', '<code>FirstName != "Chris"</code>', 'not equal to'),
    ]
    body = f'''
<p>All of dplyr’s functions take a tibble as their first argument, and they all give you back a new tibble. The tibble you started with isn’t changed, so if you want to keep a result, store it in an object. Inside the functions, you refer to the columns of the tibble just by their names, without quotes and without <code>$</code>.</p>
<p>These examples use <code>trumpton</code>, the small tibble from the last chapter. If it isn’t in your Environment pane, read it in again: {rscode(TRUMPTON_CMD)}</p>
{console(("trumpton", TRUMPTON))}

<h2 id="fl-select">Choosing columns with select()</h2>
<p>Give <code>select()</code> the names of the columns you want, in the order you want them. You can also give their positions, or put a minus sign in front of a column that you want to leave out:</p>
{console(("select(trumpton, FirstName, LastName, Weight)", SELECT_NAMES), ("select(trumpton, 2, 4)", SELECT_POS), ("select(trumpton, -LastName)", SELECT_NEG))}

<h2 id="fl-filter">Choosing rows with filter()</h2>
<p><code>filter()</code> keeps the rows for which a test is TRUE. The tests are the comparisons you used with vectors in R basics; text goes in quotes, as always.</p>
{table(['Test', 'Or', 'Meaning'], tests)}
{console(("filter(trumpton, Height >= 170)", FILTER_170), ('filter(trumpton, FirstName == "Chris")', FILTER_CHRIS))}
<p>A test can also use a function to transform a column first. In this table, <code>difference</code> can be large in either direction, and <code>abs()</code>, which gives the absolute value of a number (its size, ignoring its sign), finds the rows where the difference is more than 5 either way:</p>
{console(('transform.data <- read_tsv("transform_data.txt", show_col_types = FALSE)', ""), ("transform.data", TRANSFORM), ("filter(transform.data, abs(difference) > 5)", TRANSFORM_ABS))}
<p>(<code>show_col_types = FALSE</code> tells <code>read_tsv()</code> not to print the column types.) You don’t need to save the results of the steps below, but do look at each one, to check that it has worked.</p>
{activity("Filter the small file", [
    rtask("fl-a", f'From {c("small")}, extract all the rows where the {c("Category")} is A.', tib(10, ['Category'], 'all(v$Category == "A")')),
    rtask("fl-80", 'Extract the samples with a Length of more than 80.', tib(16, ['Length'], 'all(v$Length > 80)')),
    rtask("fl-sample", f'Remove the {c("Sample")} column, to leave just {c("Length")} and {c("Category")}.', lastv(NO_SAMPLE)),
])}
{activity("Filter the child’s variants", [
    rtask("fl-mt", f'From {c("child")}, extract the variants on the mitochondrial chromosome, which is called MT.', tib(6, ['CHR'], 'all(v$CHR == "MT")')),
    rtask("fl-70", f'Extract the variants with a {c("MutantReadPercent")} of 70 or more.', tib(9976, ['MutantReadPercent'], 'all(v$MutantReadPercent >= 70)')),
    rtask("fl-qual", 'Extract the variants with a quality of exactly 200. (Look at the data to find the name of the column.)', tib(22578, ['QUAL'], 'all(v$QUAL == 200)')),
    rtask("fl-gene", 'Extract all the variants in the gene IGFN1.', tib(17, ['GENE'], 'all(v$GENE == "IGFN1")')),
    rtask("fl-cols", f'Remove the {c("ENST")} and {c("dbSNP")} columns.', lastv(NO_ENST)),
])}
{q("fl-q-80", "How many samples in <code>small</code> have a Length of more than 80?", "16, from <code>filter(small, Length &gt; 80)</code>: the tibble it prints has 16 rows.", accept="^16$", placeholder="A number")}
{q("fl-q-gene", "How many of the child’s variants are in IGFN1?", Q_GENE, accept="^17$", placeholder="A number")}
{mcq("fl-q-which", "You want only the variants whose quality is 200. Which function do you need?", [
    ("<code>filter()</code>", True, "filter() chooses rows, and each variant is a row."),
    ("<code>select()</code>", False, "select() chooses columns. Here you want to keep some of the rows (the variants) and all of the columns."),
])}
{mcq("fl-q-quotes", "Why does <code>filter(small, Category == A)</code> give an error?", [
    ("A is text, so it needs quotes: without them, R looks for a column or an object called A", True, "R tells you that it can’t find an object called A. The right command is filter(small, Category == &quot;A&quot;)."),
    ("Because a test inside filter() needs = rather than ==", False, "A single = names an argument. A test for equality always needs ==."),
    ("Because the column is called category, with a small c", False, "The column is called Category, so that part is right. The problem is the missing quotes around A."),
])}
{optional("Fix a broken script", f"""
<p>The file <code>data/broken_selects.R</code> is a short script that tries to do some of the things you have just done, but almost every line has a mistake in it. Open it in RStudio {rsopen("data/broken_selects.R", "open broken_selects.R")}, and work through it a line at a time, fixing each line until it runs and gives the right result. Check the result of every line before you move on to the next.</p>
{activity("Fix it", [task("fl-fix", "Fix every line of <code>broken_selects.R</code>, and save the script.", auto="rstudio:saved path~broken_selects")])}
{q("fl-q-fix", "What was wrong with each line?", FIX_MODEL)}
""")}
'''
    return chapter("filter", "3", "Choosing columns and rows", "rstudio", "Choosing columns and rows", 30,
                   "dplyr, the tidyverse’s package for manipulating data, has a function for choosing columns, <code>select()</code>, and another for choosing rows, <code>filter()</code>.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_pipes():
    body = f'''
<p>Suppose you want to find the people in <code>trumpton</code> who are at least 170 cm tall and called Chris, and see just their age and weight. That takes three steps. One way to do it is to store the result of each step in an object, and use that object in the next step:</p>
{console(("filter(trumpton, Height >= 170) -> answer1", ""), ('filter(answer1, FirstName == "Chris") -> answer2', ""), ("select(answer2, Age, Weight)", AGE_WEIGHT))}
<p>This works, but it leaves objects you don’t need (<code>answer1</code> and <code>answer2</code>) lying around in R’s memory, and it is hard to see what is going on.</p>

<h2 id="pp-pipe">The pipe: %&gt;%</h2>
<p>Every dplyr function takes a tibble as its first argument and gives you a tibble back. That means you can pass the result of one function straight into the next, without storing it. The <b>pipe</b>, <code>%&gt;%</code>, does exactly that: it takes whatever is on its left and gives it to the function on its right as that function’s first argument. These two commands are the same:</p>
{block("select(trumpton, -LastName)" + chr(10) + "trumpton %>% select(-LastName)", show=False)}
<p>So the three steps above become a single command, which you can read from top to bottom, saying “and then” for each <code>%&gt;%</code>: take <code>trumpton</code>, and then keep the people who are at least 170 cm tall, and then keep those called Chris, and then select their age and weight.</p>
{console((PIPED, AGE_WEIGHT))}
<p>Writing each step on a line of its own makes a long command much easier to read. Put the <code>%&gt;%</code> at the end of each line rather than the start of the next, so that R knows the command carries on. In RStudio, {kbd("Ctrl", "Shift", "M")} ({kbd("⌘", "Shift", "M")} on a Mac) types a pipe for you. Depending on RStudio’s settings (Tools ▸ Global Options ▸ Code), it may type <code>|&gt;</code> instead: that is R’s own pipe, which works in the same way for everything in this course.</p>

<h2 id="pp-and">Several tests at once</h2>
<p>You can also give <code>filter()</code> several tests, separated by commas, and it keeps the rows for which all of them are TRUE. These two commands are the same as the two filters above:</p>
{block('trumpton %>% filter(Height >= 170, FirstName == "Chris")' + chr(10) + 'trumpton %>% filter(Height >= 170 & FirstName == "Chris")', show=False)}
<p><code>&amp;</code> means “and”, <code>|</code> means “or”, and <code>!</code> means “not”. <code>%in%</code> tests whether a value is one of a set of values, so <code>filter(trumpton, FirstName %in% c("Chris", "Liam"))</code> keeps the people called Chris or Liam, and <code>filter(trumpton, !FirstName %in% c("Chris", "Liam"))</code> keeps everyone else.</p>
{activity("Multi-stage filtering", [
    rtask("pp-quality", f'From {c("child")}, extract the variants with a quality of 200, a coverage of more than 50, and a {c("MutantReadPercent")} of more than 70.', tib(3961, ['QUAL', 'COVERAGE', 'MutantReadPercent'], QUALITY)),
    rtask("pp-chr", 'Remove all the variants on the X, Y and MT chromosomes.', tib(25345, ['CHR'], '!any(v$CHR %in% c("X", "Y", "MT"))')),
    rtask("pp-dbsnp", f'Show just the chromosome and position ({c("CHR")} and {c("POS")}) of the variants that have an ID in dbSNP. (Variants without an ID have a full stop, {c(".")}, in the {c("dbSNP")} column.)', lastv(CHR_POS)),
])}
{q("pp-q-quality", "How many variants pass all three quality tests?", "3961, from <code>child %&gt;% filter(QUAL == 200, COVERAGE &gt; 50, MutantReadPercent &gt; 70)</code>.", accept="^3,?961$", placeholder="A number")}
{q("pp-q-dbsnp", "How many of the variants have an ID in dbSNP?", "23690, from <code>child %&gt;% filter(dbSNP != &quot;.&quot;) %&gt;% select(CHR, POS)</code>.", accept="^23,?690$", placeholder="A number")}
{mcq("pp-q-pipe", "What does <code>small %&gt;% filter(Length &gt; 80)</code> mean?", [
    ("The same as <code>filter(small, Length &gt; 80)</code>", True, "The pipe makes what is on its left the first argument of the function on its right."),
    ("Keep the rows of <code>small</code> whose Length is more than 80 per cent of the largest", False, "%&gt;% isn’t a percentage: it is the pipe."),
    ("Store the filtered rows in <code>small</code>", False, "A pipe doesn’t store anything. To keep the result, you would need to assign it, as in small80 &lt;- small %&gt;% filter(Length &gt; 80)."),
])}
{optional("Transforming data in a filter", f"""
<p>In R basics you used <code>nchar()</code>, which counts the characters in each piece of text, and <code>substr()</code>, which extracts part of a piece of text. Both work inside a filter.</p>
{activity("Transform and filter", [
    rtask("pp-del", f'Use {c("nchar()")} on the {c("REF")} column to select the variants that are deletions: those where the reference sequence is more than one base long.', tib(602, ['REF'], 'all(nchar(v$REF) > 1)')),
    rtask("pp-q", f'Use {c("substr()")} to find all the variants in genes whose names start with Q.', tib(30, ['GENE'], 'all(substr(v$GENE, 1, 1) == "Q")')),
])}
{q("pp-q-del", "How many deletions are there, and how many variants in genes whose names start with Q?", "602 deletions, from <code>child %&gt;% filter(nchar(REF) &gt; 1)</code>, and 30 variants in genes starting with Q, from <code>child %&gt;% filter(substr(GENE, 1, 1) == &quot;Q&quot;)</code>.")}
""")}
'''
    return chapter("pipes", "4", "Pipes", "rstudio", "Combining steps with pipes", 25,
                   "Real questions usually take several steps: filter on one thing, then on another, then choose some columns. Pipes let you write those steps one after another, in the order in which they happen.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_plots():
    geoms = [
        ('<code>geom_point()</code>', 'points: scatter plots and strip charts'),
        ('<code>geom_line()</code>', 'line graphs'),
        ('<code>geom_boxplot()</code>', 'box plots'),
        ('<code>geom_col()</code> and <code>geom_bar()</code>', 'bar plots'),
        ('<code>geom_histogram()</code> and <code>geom_density()</code>', 'distributions'),
    ]
    body = f'''
<h2 id="pl-how">How a ggplot is put together</h2>
<p>Every plot in ggplot2 is built in the same way:</p>
<ol>
<li>Start with <code>ggplot()</code>, and give it the tibble that holds your data.</li>
<li>Say which columns of the data should control which parts of the plot, with <code>aes()</code>. These are the <b>aesthetics</b>: the position along the x axis, the position along the y axis, the colour, the size, and so on.</li>
<li>Add a <b>geometry</b> with <code>+</code>: the kind of plot you want, such as points, lines or bars.</li>
<li>Add anything else you need, such as titles or labels, with more <code>+</code>.</li>
</ol>
<p>The geometries all have names that start with <code>geom_</code>:</p>
{table(['Geometry', 'What it draws'], geoms)}
<p>These examples use a tibble of gene expression levels, from <code>expr_data.txt</code>. To try them yourself, read it in first: {rscode(EXPR_CMD)}</p>
{console(("expression", EXPRESSION))}
<p>To plot the expression in the KO samples against the expression in the WT samples, the tibble is <code>expression</code>, the aesthetics are <code>x = WT</code> and <code>y = KO</code>, and the geometry is points:</p>
{block(FIRST_PLOT)}
<p>Change <code>geom_point()</code> to <code>geom_line()</code>, and the same data are drawn as a line instead. Because the tibble is the first argument of <code>ggplot()</code>, you can also pipe the data into it.</p>

<h2 id="pl-aes">Fixed and mapped aesthetics</h2>
<p>An aesthetic can be set in two ways. A <b>fixed</b> value is the same for every point: all the points red, say, or all of them size 4. You give fixed values to the geometry, outside <code>aes()</code>:</p>
{block(RED_PLOT)}
<p>A <b>mapped</b> aesthetic comes from a column of your data: points coloured by genotype, or sized by the number of observations. Mappings go inside <code>aes()</code>, as in <code>aes(x = WT, y = KO, colour = genotype)</code>, and ggplot2 adds a legend to explain them. A mapping can be categorical (a column of text, which gives a separate colour for each value) or quantitative (a column of numbers, which gives a scale of colours from low to high).</p>
{callout("concept", "The + goes at the end of the line", "<p>Like the pipe, the <code>+</code> that adds a layer must go at the end of a line, not at the start of the next one. If a line ends without one, R thinks the command has finished there: it draws the plot without the layer, and then complains about the <code>+</code> on the next line.</p>")}
{activity("Your first ggplot", [
    rtask("pl-read", f'Read {c("brain_bodyweight.txt")}, a tab-separated file, into a tibble called {c("brain")}. It holds the weights of the brains and bodies of 27 species of animal.', has_table(27, BRAIN_COLS)),
    rtask("pl-scatter", f'Draw a scatter plot (with {c("geom_point()")}) of the weights of the brains and bodies, with {c("brain")} on the x axis and {c("body")} on the y axis.', gg("GeomPoint", maps={'x': 'brain', 'y': 'body'})),
    rtask("pl-blue", f'Make all the points blue2 ({c(BLUE)}) and size 3.', gg("GeomPoint", maps={'x': 'brain', 'y': 'body'}, fixed={'colour': 'identical(p, "blue2")', 'size': 'p == 3'})),
    rtask("pl-log", f'The points are all squashed into the bottom left-hand corner of the plot. Use the {c("log.brain")} and {c("log.body")} columns instead, and see whether the plot looks better.', gg("GeomPoint", maps={'x': 'log.brain', 'y': 'log.body'})),
    rtask("pl-category", f'Change the colour of the points from a fixed blue to a mapping, so that they are coloured by {c("Category")}.', gg("GeomPoint", maps={'x': 'log.brain', 'y': 'log.body', 'colour': 'Category'})),
])}
{mcq("pl-q-extinct", "What do you notice about the extinct species?", [
    ("Their bodies are far heavier, for the size of their brains, than those of the other animals, so they sit well above the rest", True, "The three extinct species are dinosaurs: Diplodocus, Triceratops and Brachiosaurus. Their brains were tiny for animals of their size."),
    ("They follow the same trend as the other animals", False, "Look at the three points in the Extinct colour: they are well away from the line that the other animals follow."),
    ("They had the largest brains of all", False, "Look along the x axis: the elephants and humans have far larger brains."),
])}
{mcq("pl-q-fixed", "What is the difference between <code>geom_point(colour = &quot;red&quot;)</code> and <code>ggplot(brain, aes(x = log.brain, y = log.body, colour = Category))</code>?", [
    ("The first makes every point red; the second colours each point according to the value in its Category column", True, "A fixed aesthetic goes outside aes(), and a mapped aesthetic, which comes from the data, goes inside it."),
    ("There is no difference: both set the colour of the points", False, "Only the second takes the colours from the data. The first gives every point the same colour."),
    ("The first is for points and the second is for lines", False, "Both of them can be used with any geometry. The difference is where the colour comes from."),
])}
{optional("Leave out the extinct species", f"""
<p>Draw your last plot again, but without the extinct species. Use what you learnt about <code>filter()</code> to remove them from the data, and pipe the filtered data straight into <code>ggplot()</code>.</p>
{activity("Filter, then plot", [rtask("pl-noext", "Plot the data without the extinct species.", gg("GeomPoint", maps={'x': 'log.brain', 'y': 'log.body'}, extra=NO_EXTINCT))])}
""")}
'''
    return chapter("plots", "5", "Your first plots", "rstudio", "Your first plots with ggplot2", 25,
                   "ggplot2 is the tidyverse’s package for plots. It is powerful and flexible, and it works in the same way as the rest of the tidyverse: the data come in a tibble, in tidy format, as the first argument.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_more():
    body = f'''
<h2 id="mo-bars">Bar plots: geom_col() and geom_bar()</h2>
<p>There are two geometries for bar plots, and which one you need depends on your data. Use <b><code>geom_col()</code></b> when your data already contain the heights of the bars. Then you need two aesthetics: <code>x</code> for the bars, and <code>y</code> for their heights. To plot the expression of each gene in the WT samples:</p>
{block(COL_PLOT)}
<p>Use <b><code>geom_bar()</code></b> when you want ggplot2 to count things for you: how many rows there are for each value of <code>x</code>. It only needs the <code>x</code> aesthetic. For example, <code>ggplot(small, aes(x = Category)) + geom_bar()</code> draws a bar for each category, as tall as the number of samples in it.</p>

<h2 id="mo-dist">Distributions: histograms and density plots</h2>
<p>A histogram divides the range of the values into bins, and draws a bar for each bin, as tall as the number of values in it. The argument <code>binwidth</code> sets how wide the bins are. These examples use <code>many_values.txt</code>, which has 100,000 values from two genotypes:</p>
{block('many.values <- read_tsv("many_values.txt", show_col_types = FALSE)' + chr(10) + HIST_PLOT)}
<p>A density plot (<code>geom_density()</code>) draws a smooth curve instead, which is often easier to read when you are comparing groups. Here the <code>fill</code> is mapped to the genotype, and <code>alpha</code>, the opacity, is set to 0.5, so that each curve shows through the other:</p>
{block(DENS_PLOT)}
{callout("concept", "fill and colour", "<p>For a shape with an inside, such as a bar or the area under a density curve, <code>fill</code> sets the colour of the inside and <code>colour</code> sets the colour of its outline. For points and lines, <code>colour</code> is the colour of the point or line itself. The help page of each geometry (for example <code>?geom_histogram</code>) lists all the aesthetics it understands.</p>")}
{activity("More plots", [
    rtask("mo-col", f'Draw a bar plot of the lengths of the samples in category A of {c("small")}. Filter the data to keep only the category A samples, pass the filtered tibble to {c("ggplot()")}, use {c("Sample")} for x and {c("Length")} for y, and use {c("geom_col()")}, because the data give the heights of the bars.', gg("GeomCol", maps={'x': 'Sample', 'y': 'Length'}, extra='all(v$data$Category == "A")')),
    rtask("mo-hist", f'Plot the distribution of the {c("MutantReadPercent")} values of {c("child")} as a histogram, and change its {c("fill")} and {c("colour")} to make it look better.', gg("GeomBar", stat="StatBin", maps={'x': 'MutantReadPercent'})),
    rtask("mo-bin", f'Try different values of {c("binwidth")} in {c("geom_histogram()")} to change how finely the distribution is divided up.', gg("GeomBar", stat="StatBin", maps={'x': 'MutantReadPercent'}, extra=BINWIDTH)),
    rtask("mo-dens", 'Plot the same distribution as a density plot.', gg("GeomDensity", maps={'x': 'MutantReadPercent'})),
    rtask("mo-bar", f'Draw a bar plot of how often each base is the reference base of a variant. Filter {c("child")} to keep only the variants whose {c("REF")} is a single letter (use {c("nchar()")}), pass them to {c("ggplot()")} with {c("REF")} as the x aesthetic, and use {c("geom_bar()")}: there is no y aesthetic, so ggplot2 counts the variants for each base.', gg("GeomBar", stat="StatCount", maps={'x': 'REF'}, extra='all(nchar(v$data$REF) == 1)')),
])}
{q("mo-q-ref", "Which base is most often the reference base of a single-base variant?", "G, with 6982 variants (C has 6813, T 5718 and A 5707). <code>child %&gt;% filter(nchar(REF) == 1) %&gt;% count(REF)</code> gives you the numbers.", accept=ACC_REF, placeholder="A base")}
{mcq("mo-q-colbar", "You have a tibble with one row for each sample, and you want a bar for each category, as tall as the number of samples in it. Which geometry do you need?", [
    ("<code>geom_bar()</code>, with Category as x", True, "geom_bar() counts the rows for each value of x, so it doesn’t need a y aesthetic."),
    ("<code>geom_col()</code>, with Category as x", False, "geom_col() needs a y aesthetic, the height of each bar, which your data would have to contain already."),
    ("<code>geom_histogram()</code>, with Category as x", False, "Histograms are for numbers, which they divide into bins. Category is text."),
])}
{mcq("mo-q-bin", "What happens to a histogram when you make <code>binwidth</code> smaller?", [
    ("There are more, narrower bars, which show more detail but are more ragged", True, "Each bin covers a smaller range of values, so there are more of them, each with fewer values in it."),
    ("There are fewer, wider bars", False, "That is what a larger binwidth does."),
    ("The bars get shorter, but there are just as many", False, "With narrower bins there are more bars as well as shorter ones."),
])}
'''
    return chapter("more", "6", "More kinds of plot", "rstudio", "Bar plots and distributions", 25,
                   "Points are only the start. ggplot2 has geometries for bar plots, histograms, density plots and many more, and they all work in the same way.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_labels():
    body = f'''
<p><code>ggtitle()</code> adds a title to a plot, and <code>xlab()</code> and <code>ylab()</code> change the labels of its axes. A plot can also have more than one geometry, each of them a <b>layer</b> drawn on top of the ones before. <code>geom_text()</code> writes text at each point, taken from the <code>label</code> aesthetic. Here the names of the genes are written just below the points, because <code>vjust = 1.2</code> moves each label down a little:</p>
{block(LABEL_PLOT)}
<p>The arguments <code>hjust</code> and <code>vjust</code> move the labels sideways and up or down. Try a few values to see what they do.</p>
{activity("Label your plot", [
    rtask("lb-title", f'Go back to your plot of {c("log.body")} against {c("log.brain")}, coloured by {c("Category")}, and give it a title and proper labels for its axes.', gg("GeomPoint", maps={'x': 'log.brain', 'y': 'log.body'}, labels=('title', 'x', 'y'))),
    rtask("lb-text", f'Add a {c("geom_text()")} layer that writes the name of each species next to its point. It needs a mapping of {c("label")} to {c("Species")}, which you can add to the {c("aes()")} in {c("ggplot()")} or give to {c("geom_text()")} in an {c("aes()")} of its own. Then use {c("hjust")} to move the names off the points.', gg("GeomText", maps={'label': 'Species'})),
])}
{mcq("lb-q-plus", PLUS_Q, PLUS_OPTS)}
{optional("A line of best fit", f"""
<p>The plot shows that animals with heavier brains tend to have heavier bodies. You can test whether this relationship is significant, and measure how strong it is, with two functions that ask similar questions of the same data, but which are used in quite different ways. That is a good reminder to read the help page of a function before you use it.</p>
<p><code>cor.test()</code> takes two vectors of the same length and tests the correlation between them. It gives you the correlation coefficient and a p-value. Use <code>$</code> to take the <code>log.brain</code> and <code>log.body</code> columns out of <code>brain</code>, and note the p-value, so that you can add it to the title of your plot.</p>
<p><code>lm()</code> fits a linear model. Its two main arguments are a <b>formula</b>, which describes the relationship you want to model, and the data. The formula <code>log.body ~ log.brain</code> means “log.body as predicted by log.brain”, so the command is <code>lm(log.body ~ log.brain, data = brain)</code>. It gives you the intercept and the slope of the line of best fit, which you can draw on your plot with <code>geom_abline(intercept = …, slope = …)</code>.</p>
{activity("Test, and draw the line", [
    rtask("lb-cor", f'Test the correlation between {c("log.brain")} and {c("log.body")} with {c("cor.test()")}.', lastv('inherits(v, "htest") && grepl("correlation", v$method)')),
    rtask("lb-lm", f'Fit a linear model of {c("log.body")} against {c("log.brain")} with {c("lm()")}.', lastv('inherits(v, "lm")')),
    rtask("lb-abline", f'Add the line of best fit to your plot with {c("geom_abline()")}, and put the p-value in the title.', gg("GeomAbline", extra='any(grepl("[0-9]", c(v$labels$title, v$labels$subtitle)))')),
])}
{q("lb-q-p", "What p-value does cor.test() give for the correlation?", "2.44e-06, which is 0.00000244: a highly significant correlation. The correlation coefficient is 0.77, and <code>lm()</code> gives an intercept of −2.283 and a slope of 1.215.", accept=ACC_P, placeholder="A number")}
""")}
'''
    return chapter("labels", "7", "Titles and labels", "rstudio", "Titles, labels and layers", 15,
                   "A plot that someone else will read needs a title and clear labels. ggplot2 builds a plot up in layers, so you add these, and other annotations, with <code>+</code>.", body)


def ALL():
    return [ch_start(), ch_reading(), ch_tidy(), ch_filter(), ch_pipes(), ch_plots(), ch_more(), ch_labels(),
            certificate_chapter("certificate", "★", "Tidyverse", "Your certificate for the Tidyverse course, with your name on it.")]
