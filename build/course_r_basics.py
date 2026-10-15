"""R basics: the first course of Introduction to R.

The R language itself, in RStudio, for people who have never used R (or programmed) before: R as a calculator, objects,
functions, text and help, vectors, vectorised operations, comparisons and selecting values, random numbers and a
t-test, and lists and data frames. Adapted from the exercises of Introduction to R (with Tidyverse) by Simon Andrews
and Laura Biggins (Babraham Bioinformatics), as adapted by Tim Hearn, with the ideas from the course's slides worked
into the text (CC BY-NC-SA 2.0 UK)."""
from lib import *

# ---- checks made by R (see lib.rtask): R expressions that are TRUE when a step is done ----
SERIES = 'seq(2, by = 3, length.out = 100)'
SERIES_MADE = (f'length(number.series) == 100 && (isTRUE(all.equal(as.numeric(number.series), {SERIES})) || '
               f'isTRUE(all.equal(as.numeric(number.series), {SERIES} * 1000)))')
SERIES_1000 = f'isTRUE(all.equal(as.numeric(number.series), {SERIES} * 1000))'
GENOTYPES = ('length(genotypes) == 100 && setequal(as.character(genotypes), c("WT", "KO1", "KO2", "KO3")) && '
             'all(table(as.character(genotypes)) == 25)')
MY_NAME = 'is.character(my.name) && length(my.name) == 1 && nchar(my.name) > 0'
CENTRED = ('any(vapply(ls(globalenv()), function(nm) { o <- get(nm, envir = globalenv()); is.numeric(o) && length(o) == 100 && '
           'isTRUE(all.equal(as.numeric(o), as.numeric(number.series - median(number.series)))) }, logical(1)))')
RESULTS = 'is.list(results) && !is.data.frame(results) && all(c("ratios", "counts") %in% names(results))'
ALL_RESULTS = 'is.data.frame(all.results) && nrow(all.results) == 5 && all(c("mon", "tue", "wed", "pass") %in% names(all.results))'

# what the short questions accept (regular expressions, tried on the answer in lower case with its spaces tidied)
ACC_17 = r'^17(\.0+)?$'
ACC_Z = r'^1\.77(3|27\d*)?$'
ACC_LOG = r'^5\.59[78]\d*$||^5\.6$'
ACC_SUB = r'^(\[1\] )?-3,? -1,? 1,? 4,? 7$'
ACC_1000 = r'^299,?000$||^2\.99e\+?0?5$'
ACC_MON = r'^0?\.60*$'

WHICH_BIG = ('identical(v, number.series > 150000) || identical(v, number.series[number.series > 150000]) || '
             'identical(v, which(number.series > 150000))')

NAME_BTN = '<button class="do" type="button" data-student-name="1">Add your name</button>'

RESULTS_CODE = '''results <- list(
  ratios = c(0.8, 1.2, 3.3, 1.8, 2.7),
  counts = c(100, 300, 200)
)'''

ALL_RESULTS_CODE = '''all.results <- data.frame(
  mon = c(0.8, 0.6, 0.2, 0.8, 0.6),
  tue = c(0.9, 0.7, 0.3, 0.8, 1.0),
  wed = c(0.8, 0.5, 0.3, 0.9, 0.9),
  pass = c(TRUE, FALSE, FALSE, TRUE, TRUE)
)'''

SUBSTR_THREE = '''substr(scientist, 5, 8)
substr(x = scientist, start = 5, stop = 8)
substr(
  start = 5,
  stop = 8,
  x = scientist
)'''

POWER = '''first <- rnorm(100, mean = 10, sd = 2)
second <- rnorm(100, mean = 10.1, sd = 2)
t.test(first, second)'''


def panes():
    """RStudio's four panes, laid out as they are in RStudio"""
    items = [
        ('Source', 'top left', 'An editor for scripts: files of R commands that you can run, save and come back to. It opens when you open or create a file.'),
        ('Environment', 'top right', 'The objects in R’s memory, with their values. The <b>History</b> tab next to it lists the commands you have run.'),
        ('Console', 'bottom left', 'Where R runs your commands. You type a command after the prompt, <code>&gt;</code>, press <kbd>Enter</kbd>, and R prints the answer underneath.'),
        ('Files, Plots, Packages, Help', 'bottom right', 'Your files, the graphs you draw, the packages you have installed, and R’s help pages.'),
    ]
    return ('<div class="ds-row panes" role="img" aria-label="RStudio’s four panes: Source at the top left, Environment at the top right, '
            'Console at the bottom left, and Files, Plots, Packages and Help at the bottom right.">' +
            ''.join(f'<div class="ds"><b>{t}</b><span class="ds-sub">{where}</span><span class="ds-text">{d}</span></div>' for t, where, d in items) + '</div>')


def structures():
    """R's data structures, as small diagrams"""
    def col(name, vals, kind):
        return f'<div class="ds-col {kind}"><span class="ds-name">{name}</span>' + ''.join(f'<span class="v">{v}</span>' for v in vals) + '</div>'
    vec = col('scores', ['0.8', '1.2', '3.3', '1.8', '2.7'], 'n')
    lst = col('ratios', ['0.8', '1.2', '3.3', '1.8', '2.7'], 'n') + col('counts', ['100', '300', '200'], 'n')
    df = (col('mon', ['0.8', '0.6', '0.2', '0.8', '0.6'], 'n') + col('tue', ['0.9', '0.7', '0.3', '0.8', '1.0'], 'n') +
          col('wed', ['0.8', '0.5', '0.3', '0.9', '0.9'], 'n') + col('pass', ['T', 'F', 'F', 'T', 'T'], 'l'))
    boxes = [
        ('Vector', 'one dimension, a single type', vec),
        ('List', 'named vectors of any types and lengths', lst),
        ('Data frame or tibble', 'named vectors of the same length, so the values form rows', df),
    ]
    return ('<div class="ds-row" role="img" aria-label="A vector is a single set of values of one type. A list holds several named vectors, '
            'which can have different lengths. A data frame holds several named vectors of the same length, which line up in rows.">' +
            ''.join(f'<div class="ds"><b>{t}</b><span class="ds-sub">{s}</span><div class="ds-cols">{d}</div></div>' for t, s, d in boxes) + '</div>')


# ---------------------------------------------------------------------------------------------------------------------
def ch_start():
    body = f'''
<h2 id="s-r">R and RStudio</h2>
<p>R is free, it runs on Windows, macOS and Linux, and it copes with far more data than a spreadsheet can. It comes with a wide range of statistical tests, thousands of add-on packages extend it further, and it can draw graphs that look exactly the way you want them to. That is why it is used so widely for analysing data and for drawing figures for publication. The price of all this is that R expects you to type commands rather than click on menus, which can feel daunting at first, so this course takes you through the basics one small step at a time.</p>
<p><b>RStudio</b> is a program that makes R much easier to work with, and it is what most people use. On your own computer, you would install R first (from <a href="https://www.r-project.org/" target="_blank" rel="noopener">r-project.org</a>) and then RStudio. Here, the <b>RStudio</b> tab of the workbench on the right is an imitation of RStudio made for teaching, and R itself runs inside your web browser, so there is nothing to install.</p>

<h2 id="s-panes">Finding your way around RStudio</h2>
<p>RStudio’s window is divided into four panes, laid out like this. Until you open a file, the Source pane is folded away and the Console has the left-hand side to itself.</p>
{panes()}

<h2 id="s-how">How this course works</h2>
<ul>
<li>Each chapter explains an idea, shows you some R, and then gives you an activity to do in the workbench. The instructions are on the left and the workbench is on the right; you can drag the divider between them to change their widths.</li>
<li>The steps of an activity tick themselves when R sees that you have done them, and they are then marked <span class="auto-tag">✓ spotted</span>. If a step hasn’t ticked when you know you have done it, you can tick it yourself.</li>
<li>Buttons such as {rstype("1 + 1")} type code into RStudio’s Console for you, and you then press <kbd>Enter</kbd> to run it. You will learn more by typing the code yourself, though, so use the buttons when you are stuck rather than all the time.</li>
<li>Questions with a <b>Check</b> button are marked straight away. Once you have had a go at a question, a <b>Show answer</b> button appears, so that you can compare your answer with ours.</li>
<li>Parts marked <b>If you have time</b> are extras, and they don’t count towards your certificate.</li>
<li>Your ticks and answers are saved in this web browser, on this computer. <b>My answers</b>, at the top of the page, downloads a copy of your answers.</li>
<li>The first time you open the course, R itself has to be downloaded into your browser (about 30&nbsp;MB), so it may take a moment to start.</li>
</ul>

<h2 id="s-name">Your name, for your certificate</h2>
<p>When you have finished the course, you can download a certificate with your name on it. Add your name now, with the button below or with the <b>Your name</b> button at the top right of the page. Type it exactly as you would like it to appear on your certificate, for example <i>Ada Lovelace</i>. Your name is only kept in this browser, and you can change it at any time.</p>
{callout("warn", "AI tools and your data", "<p>The <b>AI</b> tab has an AI assistant that you can ask about R, if you have a key for an AI service. Anything you type into it is sent to an AI company, so never paste personal data or patient data into it, or into any other AI tool.</p>")}
{activity("Get started", [
    task("s-name", f'Add your name for your certificate: {NAME_BTN}', check="named"),
    task("s-first", f'Click in RStudio’s Console, at the bottom left of the workbench, type {c("1 + 1")} and press <kbd>Enter</kbd>. R prints the answer, <code>[1] 2</code>, underneath.', auto="r:input kind=rstudio line%1+1"),
])}
'''
    return chapter("start", "0", "Start here", "rstudio", "Welcome to R basics", 10,
                   "R is a language and an environment for working with data: for calculations, statistics and graphs. This course starts from the very beginning, so you don’t need to have done any programming before.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_calc():
    ops = [
        ('<code>+</code>', 'addition', '<code>3 + 2</code>', '5'),
        ('<code>-</code>', 'subtraction', '<code>10 - 4</code>', '6'),
        ('<code>*</code>', 'multiplication', '<code>6 * 7</code>', '42'),
        ('<code>/</code>', 'division', '<code>2 / 7</code>', '0.2857143'),
        ('<code>^</code>', 'raising to a power', '<code>5 ^ 10</code>', '9765625'),
    ]
    body = f'''
<p>R understands the usual arithmetic operators:</p>
{table(['Operator', 'What it does', 'Example', 'Answer'], ops)}
<p>Here is what the Console looks like after three of these sums:</p>
{console(("3 + 2", "[1] 5"), ("2 / 7", "[1] 0.2857143"), ("5 ^ 10", "[1] 9765625"))}
<p>The <code>[1]</code> in front of each answer is something you will see all the time. It means that the line starts with the first value of the answer, which will make more sense when you meet answers that contain many values, in the chapter on vectors. R shows answers to seven significant figures, but it keeps the full value in its memory, and uses that in any further calculations.</p>
<p>R works out powers first, then multiplication and division, and then addition and subtraction, just as you would on paper. Use round brackets to change the order: {c("2 + 3 * 4")} is 14, but {c("(2 + 3) * 4")} is 20.</p>
{callout("concept", "Spaces, unfinished commands and the ↑ key", "<p>R ignores the spaces between the parts of a command, so <code>3+2</code> and <code>3 + 2</code> do the same thing, but spaces make your code easier to read. If you press <kbd>Enter</kbd> before a command is finished, for example straight after <code>5 *</code>, R shows a <code>+</code> instead of its usual prompt, to tell you that it is waiting for the rest of the command. Either type the rest of it, or press <kbd>Esc</kbd> to abandon it. In the Console, the <kbd>↑</kbd> key brings back the commands you ran before, so that you can change one and run it again.</p>")}
{activity("Do some sums", [
    rtask("c-mult", f'Use R to calculate 31 × 78. (In R, the multiplication sign is {c("*")}.)', lastv("isTRUE(all.equal(v, 2418))")),
    rtask("c-div", 'Calculate 697 ÷ 41.', lastv("isTRUE(all.equal(v, 17))")),
    task("c-brackets", f'Work out {c("2 + 3 * 4")}, and then the same sum with brackets: {c("(2 + 3) * 4")}.', auto="r:input kind=rstudio line%(2+3)*4"),
    task("c-plus", f'Type {c("5 *")} and press <kbd>Enter</kbd>. When R shows its <code>+</code> prompt, type {c("2")} and press <kbd>Enter</kbd> again to finish the command.', auto="r:input kind=rstudio promptKind=continue"),
])}
{q("c-q-mult", "What is 31 × 78?", "2418", accept="^2,?418$", placeholder="A number")}
{q("c-q-div", "And what is 697 ÷ 41?", "17", accept=ACC_17, placeholder="A number")}
{mcq("c-q-order", "What answer does R give for <code>10 - 2 * 3</code>?", [
    ("4", True, "R multiplies before it subtracts, so this is 10 − 6."),
    ("24", False, "That would be (10 - 2) * 3. Without the brackets, R does the multiplication first."),
    ("An error, because of the spaces", False, "The spaces make no difference to R. They are only there to make the code easier to read."),
])}

<h2 id="c-script">Keeping your commands in a script</h2>
<p>Anything you type into the Console is run straight away, but it isn’t kept anywhere, apart from in the list of commands on the History tab. When you are doing real work you will want a record of your commands, so that you can run them again, correct them, or show someone else what you did. In RStudio you do this by writing your commands in a <b>script</b>: a plain text file of R commands, saved with the extension <code>.R</code>.</p>
{activity("Start a script", [
    task("c-new", 'Choose File ▸ New File ▸ <b>R Script</b>. (The first button on RStudio’s toolbar, with a green plus sign, has the same menu.) A new, empty script opens in the Source pane, above the Console.', auto="rstudio:new kind=r"),
    task("c-run", f'Type {c("# my first script")} on the first line of the script, and {c("2 ^ 8")} on the second. With the cursor on the second line, press {kbd("Ctrl", "Enter")} ({kbd("⌘", "Enter")} on a Mac). RStudio sends the line to the Console and runs it.', auto="r:input kind=rstudio line%2^8"),
    task("c-save", f'Save the script with {kbd("Ctrl", "S")} ({kbd("⌘", "S")} on a Mac), and call it {c("basics.R")}.', auto="rstudio:saved path~basics"),
])}
{callout("info", "Console or script?", "<p>A line that starts with <code>#</code> is a <b>comment</b>. R ignores it, so you can use comments to leave notes for yourself. In this course you can type commands into either the Console or your script. The <b>show me</b> buttons put code into the Console, because that is the quickest way to try something out, but whenever you write something you want to keep, put it in your script and save it.</p>")}
'''
    return chapter("calc", "1", "R as a calculator", "rstudio", "R as a calculator", 15,
                   "The simplest way to use R is as a calculator: you type a sum into the Console, press <kbd>Enter</kbd>, and R prints the answer straight away.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_objects():
    body = f'''
<p>To create an object, you use the <b>assignment arrow</b>, which is made of a less-than sign and a hyphen. The arrow points from the value to the name it will be stored under, and it can point either way:</p>
{block("10 -> x" + chr(10) + "y <- 20")}
<p>Nothing is printed when you create an object, but it appears in the Environment pane, along with its value. To see the value in the Console, type the name of the object on its own. After that, you can use the name wherever you would have used the value, and you can store the result of a calculation as a new object:</p>
{console(("10 -> x", ""), ("y <- 20", ""), ("x", "[1] 10"), ("x + y", "[1] 30"), ("x + y -> z", ""), ("z", "[1] 30"))}
<p>If you assign a new value to a name that already exists, the old value is replaced, without any warning. You will also see code that uses <code>=</code> for assignment, as in <code>x = 10</code>. That works too, but <code>&lt;-</code> is what most R users write, and it is what this course uses. In RStudio, {kbd("Alt", "-")} ({kbd("Option", "-")} on a Mac) types the arrow for you, with a space on either side.</p>

<h2 id="o-names">Choosing names</h2>
<p>R has a few rules about names:</p>
<ul>
<li>A name can contain letters, numbers, dots (<code>.</code>) and underscores (<code>_</code>), but no spaces or other symbols.</li>
<li>It can’t start with a number: <code>sample2</code> is fine, but <code>2sample</code> isn’t.</li>
<li>Upper and lower case letters are different, so <code>Weight</code> and <code>weight</code> are two different objects.</li>
</ul>
<p>Beyond the rules, a good name tells you what an object holds: <code>weight</code> is better than <code>x</code>, and <code>gene_name</code> is better than <code>gn</code>. Most people keep their names in lower case and separate the words with dots or underscores, as in <code>gene.name</code> or <code>gene_name</code>. Pick one style and stick to it.</p>
{callout("concept", "Error: object not found", "<p>If you ask for an object that doesn’t exist, R tells you: <code>Error: object &#39;Z&#39; not found</code>. The usual causes are a typing mistake, a capital letter where you meant a small one (or the other way round), and forgetting to run the line that creates the object. The Environment pane shows you exactly which objects exist.</p>")}
{activity("Create some objects", [
    rtask("o-x", f'Give {c("x")} the value 39.', "isTRUE(all.equal(x, 39))"),
    rtask("o-y", f'Give {c("y")} the value 22.', "isTRUE(all.equal(y, 22))"),
    rtask("o-z", f'Make {c("z")} the value of {c("x")} divided by {c("y")}, using the objects rather than the numbers.', "isTRUE(all.equal(z, 39 / 22))"),
    task("o-show", f'Display the value of {c("z")} in the Console, and find {c("x")}, {c("y")} and {c("z")} in the Environment pane.', auto="r:input kind=rstudio line=z||r:input kind=rstudio line%print(z)"),
])}
{q("o-q-z", "What is the value of <code>z</code>, to two decimal places?", "1.77 (R prints 1.772727)", accept=ACC_Z, hint="type z in the Console to see its value", placeholder="A number")}
{mcq("o-q-name", "Which of these names is <em>not</em> allowed in R?", [
    ("<code>2nd.sample</code>", True, "A name can’t start with a number. <code>sample.2nd</code> or <code>second.sample</code> would be fine."),
    ("<code>sample_2</code>", False, "Underscores and numbers are both allowed, as long as the name doesn’t start with a number."),
    ("<code>Sample.Two</code>", False, "Capital letters are allowed, although <code>Sample.Two</code> and <code>sample.two</code> would be two different objects."),
])}
{mcq("o-q-update", "You run <code>x &lt;- 5</code> and then <code>x &lt;- x + 1</code>. What is the value of <code>x</code> now?", [
    ("6", True, "R works out the right-hand side first, using the value x has at that moment (5), and then stores the answer in x, replacing the old value. You will use this to change a whole set of values later on."),
    ("5", False, "The second command stores a new value in x, replacing the old one."),
    ("An error, because x can’t appear on both sides", False, "That is allowed: R works out x + 1 first, and only then stores the answer in x."),
])}
'''
    return chapter("objects", "2", "Objects", "rstudio", "Keeping values in objects", 15,
                   "Rather than typing the same values again and again, you can store a value in an <b>object</b> with a name, and then use the name instead of the value. Objects are often called variables.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_functions():
    body = f'''
<h2 id="f-call">Calling a function</h2>
<p>To use a function, you type its name followed by round brackets, with its arguments inside the brackets. For example, the function <code>sqrt</code> calculates square roots:</p>
{console(("sqrt(10)", "[1] 3.162278"))}
<p>An argument can be a value, an object, or the result of another function. When one function is inside another, R works from the inside out: in {c("log2(sqrt(16))")}, it first works out <code>sqrt(16)</code>, which is 4, and then <code>log2(4)</code>, which is 2. You can get the same answer in two steps instead, by storing the square root in an object and then giving the object to <code>log2</code>.</p>

<h2 id="f-text">Text</h2>
<p>Text in R always goes in quotes. You can use double quotes or single quotes, as long as you use the same kind at both ends:</p>
{block('scientist <- "Ada Lovelace"' + chr(10) + "first.name <- 'Ada'")}
<p>The quotes tell R that you mean the text itself. Without them, R thinks that you mean an object with that name, so <code>first.name &lt;- Ada</code> gives the error <code>object &#39;Ada&#39; not found</code>. Be careful with code that has been copied from a word processor: R only understands straight quotes (<code>"</code> and <code>&#39;</code>), not the curly ones (“ and ”) that word processors put in.</p>
<p>Two useful functions for text are <code>nchar</code>, which counts the characters in a piece of text, and <code>substr</code>, which extracts part of it, from a start position to a stop position. Spaces count as characters too:</p>
{console(('scientist <- "Ada Lovelace"', ""), ("nchar(scientist)", "[1] 12"), ("substr(scientist, 5, 8)", '[1] "Love"'))}

<h2 id="f-args">Arguments by position and by name</h2>
<p>Every argument of a function has a name. The arguments of <code>substr</code> are called <code>x</code> (the text), <code>start</code> and <code>stop</code>. If you give the arguments in the order the function expects, you don’t need to name them; if you do name them, you can give them in any order you like. These three commands all do exactly the same thing:</p>
{block(SUBSTR_THREE, show=False)}
<p>The last one is spread over several lines. R allows that: it keeps reading until the brackets are closed. Naming your arguments makes your code easier to read, and it lets you give a function just the arguments you need, as you will see in the next chapter.</p>

<h2 id="f-help">Getting help</h2>
<p>Every function has a help page. Type <code>?</code> followed by the name of the function, as in {c("?sqrt")}, and the page opens in the Help pane, at the bottom right. Help pages all follow the same pattern: <b>Description</b> says what the function does, <b>Usage</b> shows how to call it, with its arguments in order, <b>Arguments</b> explains each argument, <b>Value</b> describes what the function gives back, and <b>Examples</b>, at the end, has code that you can copy and run. In the Usage section, an argument written as <code>name = value</code> has a <em>default</em>: if you leave that argument out, R uses the value shown.</p>
<p>If you don’t know the name of the function you need, <code>??</code> searches all the help pages for a word or phrase. {c("??substring")} lists every help page that mentions substrings, and you can click on any of them to open it. Searching the web works well too, although “R” on its own isn’t much use as a search term. Add the name of the function or package you are asking about, as in <i>R substr</i>.</p>
{activity("Use some functions", [
    rtask("f-sqrt", 'Calculate the square root of 2345, and then calculate the log2 of the result. You can do it in one command, with one function inside the other, or in two.', lastv("isTRUE(all.equal(v, log2(sqrt(2345))))")),
    rtask("f-name", f'Put your own name into an object called {c("my.name")}. Remember the quotes.', MY_NAME),
    rtask("f-nchar", f'Use {c("nchar")} to find out how many characters there are in your name.', lastv("identical(v, nchar(my.name))")),
    rtask("f-substr", f'Use {c("substr")} to extract the first character of your name.', lastv("identical(v, substr(my.name, 1, 1)) && !identical(v, my.name)")),
    task("f-help", f'Open the help page for {c("sqrt")}, and find the section called Examples.', auto="r:help kind=rstudio topic=sqrt"),
    task("f-search", f'Search the help pages with {c("??substring")}, and open one of the pages it finds.', auto="r:help kind=rstudio topic~??"),
])}
{q("f-q-log", "What is the log2 of the square root of 2345? Give at least three decimal places.", "5.597686 (from <code>log2(sqrt(2345))</code>)", accept=ACC_LOG, placeholder="A number")}
{mcq("f-q-quotes", "You type <code>my.name &lt;- Ada</code>, without quotes. What happens?", [
    ("R reports <code>Error: object &#39;Ada&#39; not found</code>", True, "Without quotes, R takes Ada to be the name of an object and goes looking for it. Text always needs quotes."),
    ("<code>my.name</code> now holds the text Ada", False, "Only if the text is in quotes, as <code>&quot;Ada&quot;</code>."),
    ("<code>my.name</code> is left empty", False, "R stops with an error instead, and <code>my.name</code> isn’t changed."),
])}
{mcq("f-q-default", "The help page for <code>round</code> shows <code>round(x, digits = 0)</code> under Usage. What does <code>digits = 0</code> tell you?", [
    ("If you leave out <code>digits</code>, R rounds to 0 decimal places, which means to a whole number", True, "0 is the default value of digits. <code>round(z, 2)</code> would round z to two decimal places instead."),
    ("You always have to give a value for <code>digits</code>", False, "An argument that has a default value can be left out."),
    ("<code>digits</code> can only ever be 0", False, "0 is just the value R uses when you don’t give one. <code>round(z, 2)</code>, for example, rounds to two decimal places."),
])}
'''
    return chapter("functions", "3", "Functions and help", "rstudio", "Functions, text and help", 25,
                   "Most of the work in R is done by functions. You give a function some values to work on, which are called its <b>arguments</b>, and it gives you back a result.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_vectors():
    types = [
        ('numeric', 'numbers, with or without decimal places', '<code>3</code>, <code>0.25</code>, <code>-1.5</code>'),
        ('character', 'text, in quotes', '<code>"WT"</code>, <code>"Ada"</code>'),
        ('logical', 'TRUE or FALSE', '<code>TRUE</code>, <code>FALSE</code>'),
    ]
    body = f'''
<h2 id="v-what">Everything is a vector</h2>
<p>When you typed <code>x &lt;- 39</code>, you made a vector of length 1, whose first (and only) value is 39. This is why R prints <code>[1]</code> before an answer: the number in square brackets is the position, within the vector, of the first value on that line.</p>
<p>All the values in a vector must be of the same type. The types you will use most are:</p>
{table(['Type', 'What it holds', 'Examples'], types)}
<p>There are others too, such as <b>factors</b>, for text values that come from a fixed set of categories (the genotypes in an experiment, say), and dates.</p>

<h2 id="v-c">Making vectors with c()</h2>
<p>The function <code>c()</code>, which stands for <em>combine</em>, puts values together into a vector:</p>
{block('simple.vector <- c(1, 2, 4, 6, 3)' + chr(10) + 'some.names <- c("Ada", "Grace", "Alan", "Mary", "Rosalind")')}
<p>Because a vector can only hold one type of value, R converts values when you mix types. Any number can be written as text, but most text can’t be turned into a number, so if you mix numbers with text, you get a vector of text:</p>
{console(('c(1, 2, 3, "fred")', '[1] "1"    "2"    "3"    "fred"'))}
<p>The quotes in the output show that the numbers have become text, and you can no longer do arithmetic with them. Watch out for this when you read in data from files: a single word in a column of numbers turns the whole column into text.</p>

<h2 id="v-make">Functions that make vectors</h2>
<p>For a run of whole numbers, use the colon operator: <code>4:20</code> gives you every whole number from 4 to 20.</p>
{console(("4:20", " [1]  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20"))}
<p><code>seq()</code> makes other sequences. Its arguments are <code>from</code>, <code>to</code>, <code>by</code> and <code>length.out</code>. None of them is required: you give it enough of them to describe the sequence you want.</p>
{console(("seq(from = 2, by = 3, to = 14)", "[1]  2  5  8 11 14"), ("seq(from = 3, by = 10, to = 40)", "[1]  3 13 23 33"), ("seq(from = 5, by = 3.6, length.out = 5)", "[1]  5.0  8.6 12.2 15.8 19.4"))}
<p><code>rep()</code> repeats values. With <code>times</code> it repeats the whole vector, and with <code>each</code> it repeats each value in turn:</p>
{console(('rep(c("dog", "cat"), times = 3)', '[1] "dog" "cat" "dog" "cat" "dog" "cat"'), ('rep(c("dog", "cat"), each = 3)', '[1] "dog" "dog" "dog" "cat" "cat" "cat"'))}

<h2 id="v-look">Looking at long vectors</h2>
<p>A long vector fills the Console, and the numbers in square brackets at the start of each line help you to find your way through it. To see just part of it, <code>head()</code> shows you the first six values and <code>tail()</code> the last six; both have an argument <code>n</code> for a different number, as in <code>tail(number.series, n = 10)</code>. <code>length()</code> tells you how many values there are.</p>
{activity("Make some vectors", [
    rtask("v-c", f'Create a vector called {c("some.numbers")} that contains the numbers 2, 5, 8, 12 and 16.', "identical(as.numeric(some.numbers), c(2, 5, 8, 12, 16))"),
    rtask("v-colon", f'Use the colon operator to make a vector called {c("number.range")} that contains the numbers 5 to 9.', "identical(as.numeric(number.range), c(5, 6, 7, 8, 9))"),
    rtask("v-seq", f'Use {c("seq()")} to make a vector of 100 values that starts at 2 and goes up by 3 each time, and store it in a new object called {c("number.series")}.', SERIES_MADE),
    task("v-tail", f'Print {c("number.series")} to see the whole of it, and then look at its first and last values with {c("head()")} and {c("tail()")}.', auto="r:input kind=rstudio line%tail(number.series"),
    rtask("v-rep", f'Use {c("rep()")} to make a vector of 100 values that contains 25 each of WT, KO1, KO2 and KO3, and store it in an object called {c("genotypes")}.', GENOTYPES),
])}
{q("v-q-last", "What is the last value in <code>number.series</code>?", "299. The series goes 2, 5, 8 and so on: 2 + 99 × 3 = 299.", accept="^299$", hint="tail() shows you the last values", placeholder="A number")}
{mcq("v-q-mix", "What does <code>c(1, 2, 3, &quot;fred&quot;)</code> give you?", [
    ("A vector of text: <code>&quot;1&quot; &quot;2&quot; &quot;3&quot; &quot;fred&quot;</code>", True, "A vector can only hold one type, and text can’t become a number, so R turns the numbers into text."),
    ("An error, because you can’t mix numbers and text", False, "R doesn’t give an error here. It converts the values so that they are all of the same type."),
    ("The numbers 1, 2 and 3, with <code>&quot;fred&quot;</code> left out", False, "R doesn’t drop values. It converts them so that they are all of the same type."),
])}
{mcq("v-q-seq", "Which of these commands gives you <code>1 3 5 7 9</code>?", [
    ("<code>seq(from = 1, to = 9, by = 2)</code>", True, "From 1 to 9, going up by 2 each time."),
    ("<code>seq(from = 1, by = 2, length.out = 4)</code>", False, "length.out = 4 asks for four values, so this gives 1 3 5 7."),
    ("<code>rep(1:9, each = 2)</code>", False, "rep() repeats values: this gives 1 1 2 2 3 3 and so on, up to 9 9."),
])}
'''
    return chapter("vectors", "4", "Vectors", "rstudio", "Vectors", 25,
                   "In R, everything is a vector: an ordered set of values that are all of the same type. Even a single number is a vector, with just one value in it.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_vectorised():
    warn = 'Warning message:\nIn 3:10 + 11:13 :\n  longer object length is not a multiple of shorter object length'
    body = f'''
<p>Compare these three commands:</p>
{console(("2 + 3", "[1] 5"), ("c(2, 4) + c(3, 5)", "[1] 5 9"), ("simple.vector * 100", "[1] 100 200 400 600 300"))}
<p>You don’t have to tell R to go through the values one at a time: it simply applies the operation to all of them. Three rules decide how the values of two vectors are matched up.</p>

<h2 id="vo-rules">The rules</h2>
<p><b>1. Values in the same position are matched.</b> The first value of one vector goes with the first value of the other, the second with the second, and so on.</p>
{vecop(list(range(3, 11)), list(range(11, 19)), caption="<code>3:10 + 11:18</code>: each value is added to the value in the same position of the other vector.")}
<p><b>2. A shorter vector is recycled.</b> If one of the vectors is shorter, R goes back to its start and uses its values again, as many times as it needs to.</p>
{vecop(list(range(3, 11)), list(range(11, 15)), caption="<code>3:10 + 11:14</code>: the four values of the second vector are used twice (the paler ones are the second time round).")}
<p>This is why <code>simple.vector * 100</code> works: 100 is a vector with one value, which is recycled for every value of <code>simple.vector</code>.</p>
<p><b>3. If it doesn’t fit exactly, you get a warning.</b> When the length of the longer vector isn’t a multiple of the length of the shorter one, R still recycles the shorter vector and gives you an answer, but it warns you, because this is usually a sign of a mistake.</p>
{vecop(list(range(3, 11)), list(range(11, 14)), warn=warn, caption="<code>3:10 + 11:13</code>: the second vector runs out part of the way through its third time round.")}
<p>A warning is not the same as an error. After an error, R stops and gives you nothing; after a warning, you do get an answer, but R is telling you that it may not be the one you wanted.</p>

<h2 id="vo-functions">Functions work on whole vectors too</h2>
<p>Many functions work in the same way. <code>sqrt()</code>, <code>log2()</code> and <code>round()</code> work on each value of a vector, and <code>nchar()</code> counts the characters in each piece of text:</p>
{console(("log2(c(2, 4, 8, 1024))", "[1]  1  2  3 10"), ("nchar(some.names)", "[1] 3 5 4 4 8"))}
<p>Other functions summarise a whole vector with a single value. Among the most useful are <code>length()</code>, <code>sum()</code>, <code>mean()</code>, <code>median()</code>, <code>sd()</code> (the standard deviation), <code>min()</code> and <code>max()</code>.</p>
{activity("Vectorised maths", [
    rtask("vo-sub", f'Subtract {c("number.range")} from {c("some.numbers")}, using the {c("-")} operator in the same way as you would for any other subtraction, and look at the result.', lastv("identical(as.numeric(v), c(-3, -1, 1, 4, 7))")),
    rtask("vo-1000", f'Multiply every value in {c("number.series")} by 1000, and store the result in {c("number.series")}, replacing the original values.', SERIES_1000),
    task("vo-warn", f'Run {c("3:10 + 11:13")} to see the warning for yourself.', auto="r:input kind=rstudio line%3:10+11:13"),
    rtask("vo-median", f'Work out the median of {c("number.series")}.', lastv("isTRUE(all.equal(v, median(number.series)))")),
])}
{q("vo-q-sub", "What do you get when you subtract <code>number.range</code> from <code>some.numbers</code>?", "<code>-3 -1  1  4  7</code>: 2 − 5, 5 − 6, 8 − 7, 12 − 8 and 16 − 9.", accept=ACC_SUB, placeholder="The values, separated by spaces")}
{q("vo-q-last", "What is the last value of <code>number.series</code> now?", "299000 (299 × 1000)", accept=ACC_1000, placeholder="A number")}
{mcq("vo-q-recycle", "What does <code>c(1, 2, 3, 4) * c(10, 100)</code> give you?", [
    ("<code>10 200 30 400</code>", True, "The two values of the shorter vector are recycled: 1 × 10, 2 × 100, 3 × 10 and 4 × 100."),
    ("<code>10 200 3 4</code>", False, "R doesn’t stop when the shorter vector runs out: it goes back to its start and uses it again."),
    ("An error, because the vectors are different lengths", False, "Vectors of different lengths are fine, because R recycles the shorter one. Here 4 is a multiple of 2, so you don’t even get a warning."),
])}
{optional("Centring on the median", f"""
<p>Before comparing samples, people often centre their values on the median: they subtract the median from every value, so that the middle of the data sits at 0. Work out the median of {c("number.series")}, subtract it from all of its values, and store the answer in a new object called {c("centred")}. Then work out the mean and the standard deviation (<code>sd()</code>) of {c("centred")}.</p>
{activity("Centre the values", [rtask("vo-centre", f'Make {c("centred")}, the values of {c("number.series")} centred on their median.', CENTRED)])}
{q("vo-q-centre", "What are the mean and the standard deviation of the centred values? Compare the standard deviation with that of <code>number.series</code> itself.", "The mean is 0 and the standard deviation is 87034.48, the same as the standard deviation of <code>number.series</code>. Moving every value by the same amount moves the middle of the data, but it doesn’t change how spread out the values are.")}
""")}
'''
    return chapter("vectorised", "5", "Vectorised operations", "rstudio", "Vectorised operations", 20,
                   "When you do arithmetic with a vector, R does it to every value at once. This is called a <b>vectorised operation</b>, and it is what makes R so quick to work with: one short command can change thousands of values.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_select():
    ops = [
        ('<code>==</code>', 'equal to (with two equals signs, because a single <code>=</code> is used for naming arguments)'),
        ('<code>!=</code>', 'not equal to'),
        ('<code>&lt;</code> and <code>&gt;</code>', 'less than, and greater than'),
        ('<code>&lt;=</code> and <code>&gt;=</code>', 'less than or equal to, and greater than or equal to'),
    ]
    picks = [
        ('<code>some.numbers[2]</code>', '<code>5</code>', 'the second value'),
        ('<code>some.numbers[2:4]</code>', '<code>5 8 12</code>', 'the second to the fourth values'),
        ('<code>some.numbers[c(1, 5)]</code>', '<code>2 16</code>', 'the first and the fifth values'),
        ('<code>some.numbers[-1]</code>', '<code>5 8 12 16</code>', 'every value except the first'),
        ('<code>some.numbers[some.numbers &gt; 6]</code>', '<code>8 12 16</code>', 'the values that are greater than 6'),
    ]
    body = f'''
<h2 id="sv-compare">Comparisons</h2>
<p>R has six comparison operators:</p>
{table(['Operator', 'Meaning'], ops)}
<p>Like arithmetic, comparisons are done for every value of a vector, and the answer has a <code>TRUE</code> or a <code>FALSE</code> for each value:</p>
{console(("some.numbers", "[1]  2  5  8 12 16"), ("some.numbers > 6", "[1] FALSE FALSE  TRUE  TRUE  TRUE"), ('some.names == "Mary"', "[1] FALSE FALSE FALSE  TRUE FALSE"))}
<p>An answer like this is a <b>logical vector</b>. When you do arithmetic with <code>TRUE</code> and <code>FALSE</code>, R counts <code>TRUE</code> as 1 and <code>FALSE</code> as 0, so <code>sum()</code> tells you how many of the values passed the test:</p>
{console(("sum(some.numbers > 6)", "[1] 3"))}

<h2 id="sv-select">Selecting values</h2>
<p>Square brackets after the name of a vector select values from it. Inside the brackets you can give the positions of the values you want, or a logical vector that says, for each value, whether you want it:</p>
{table(['Code', 'Gives you', 'Which is'], picks)}
<p>The last of these is worth reading slowly. <code>some.numbers &gt; 6</code> gives <code>FALSE FALSE TRUE TRUE TRUE</code>, and the square brackets keep the values for which the answer is <code>TRUE</code>. In the Tidyverse course you will use exactly the same tests to choose rows from a table of data.</p>
{activity("Count and select", [
    rtask("sv-test", f'Find out which of the values in {c("number.series")} are greater than 150000.', lastv(WHICH_BIG)),
    rtask("sv-count", f'Now use {c("sum()")} to count how many of them are greater than 150000.', lastv("isTRUE(all.equal(as.numeric(v), sum(number.series > 150000)))")),
    rtask("sv-first", f'Select the first ten values of {c("number.series")}, using square brackets.', lastv("identical(v, number.series[1:10])")),
    rtask("sv-wt", f'Count how many of the values in {c("genotypes")} are not WT.', lastv("isTRUE(all.equal(as.numeric(v), 75))")),
])}
{q("sv-q-count", "How many of the values in <code>number.series</code> are greater than 150000?", "50, from <code>sum(number.series &gt; 150000)</code>.", accept="^50$", placeholder="A number")}
{mcq("sv-q-pick", "What does <code>some.numbers[some.numbers &lt; 10]</code> give you?", [
    ("<code>2 5 8</code>", True, "The test gives TRUE for the first three values, so the square brackets keep those three."),
    ("<code>TRUE TRUE TRUE FALSE FALSE</code>", False, "That is what the test inside the brackets gives. The square brackets then use it to select values from some.numbers."),
    ("<code>3</code>", False, "That is how many values pass the test, which is what sum(some.numbers &lt; 10) would tell you."),
])}
'''
    return chapter("select", "6", "Comparing and selecting", "rstudio", "Comparing and selecting values", 15,
                   "Comparisons are vectorised too. Comparing a vector with a value gives you a TRUE or a FALSE for every value, which you can use to count values or to pick them out.", body)


# ---------------------------------------------------------------------------------------------------------------------
TTEST_OUT = '''
	Welch Two Sample t-test

data:  c(1, 5, 3) and c(10, 15, 30)
t = -2.5058, df = 2.1475, p-value = 0.1206
alternative hypothesis: true difference in means is not equal to 0
95 percent confidence interval:
 -40.00292   9.33625
sample estimates:
mean of x mean of y 
  3.00000  18.33333 
'''


def ch_random():
    body = f'''
<p><code>rnorm()</code> draws random numbers from a normal distribution. Its first argument, <code>n</code>, is how many numbers you want, and its other two arguments, <code>mean</code> and <code>sd</code>, set the mean and the standard deviation of the distribution. If you leave those two out, R uses a mean of 0 and a standard deviation of 1. There are similar functions for other distributions, such as <code>runif()</code> (uniform), <code>rpois()</code> (Poisson) and <code>rbinom()</code> (binomial).</p>
<p><code>t.test()</code> carries out a t-test. Given one vector, it tests whether the mean of its values could be 0; given two, it tests whether their means could be the same. Here it is comparing two small sets of numbers:</p>
{console(("t.test(c(1, 5, 3), c(10, 15, 30))", TTEST_OUT))}
<p>The line to look at first is the one with the <b>p-value</b>. This is the probability of getting a difference at least as big as the one in your data if there were really no difference at all. By convention, a p-value below 0.05 is called significant. Here it is 0.12, so although the means of the two sets look very different (3 and 18.3), there are too few values, and they are too variable, for the difference to be significant. R has functions for many other tests too, such as <code>cor.test()</code> for correlations and <code>aov()</code> for analysis of variance.</p>
{callout("concept", "Random numbers are different every time", "<p>Each time you run <code>rnorm()</code> you get a different set of numbers, so your results won’t match anyone else’s, or even your own the next time you run the same command. When you need random numbers that you can reproduce, run <code>set.seed()</code> first, with any whole number you like: after <code>set.seed(42)</code>, <code>rnorm(3)</code> always gives the same three numbers.</p>")}
{activity("Test some random numbers", [
    rtask("r-norm", f'Use {c("rnorm()")} to generate 20 numbers from a normal distribution with a mean of 0 and a standard deviation of 1 (the defaults), and store them in an object called {c("normal.numbers")}.', "is.numeric(normal.numbers) && length(normal.numbers) == 20"),
    rtask("r-test", f'Give {c("normal.numbers")} to {c("t.test()")} to test whether their mean is significantly different from 0, and find the p-value.', lastv('inherits(v, "htest")')),
    task("r-mean1", f'Replace {c("normal.numbers")} with a new set of 20 numbers from a distribution with a mean of 1, using the {c("mean")} argument of {c("rnorm()")}. Then test them with {c("t.test()")} again.', auto="r:input kind=rstudio line%rnorm( line%mean=1"),
])}
{q("r-q-p", "Write down the p-values of your two t-tests. Which of them was significant, and is that what you expected?", "Your numbers will be different from anyone else’s, but usually the first p-value (true mean 0) is well above 0.05, so the test finds no significant difference from 0, and the second (true mean 1) is far below 0.05, which is significant. Both results are what you would expect, because the first set of numbers really did come from a distribution with a mean of 0, and the second from one with a mean of 1.")}
{mcq("r-q-false", "You test 20 numbers made by <code>rnorm(20)</code> and get a p-value of 0.03. What does that mean?", [
    ("It is a false positive: even when there is no real difference, about one test in twenty gives a p-value below 0.05", True, "The numbers really did come from a distribution with a mean of 0. A cut-off of 0.05 means accepting that, by chance, one test in twenty will look significant when there is nothing there."),
    ("<code>rnorm()</code> isn’t working properly", False, "rnorm() is fine. Random samples sometimes look unusual, purely by chance."),
    ("The true mean of the distribution isn’t 0", False, "It is, because rnorm(20) uses a mean of 0. The test has been fooled by chance."),
])}
{optional("How many values do you need?", f"""
<p>Make two vectors of values, one drawn from a normal distribution with a mean of 10 and a standard deviation of 2, and the other from a distribution with a mean of 10.1 and a standard deviation of 2. Then test them against each other:</p>
{block(POWER)}
<p>How many values do you need in each vector before the t-test can reliably tell that the two means are different? Try 1,000 values and then 10,000, and run each test several times.</p>
{q("r-q-power", "How many values did you need?", "With 100 or even 1,000 values in each vector, the test usually misses the difference. A difference of 0.1 is only a twentieth of the standard deviation, and you need around 6,300 values in each vector to detect it 80% of the time, and over 10,000 to detect it 95% of the time. Small differences need large samples.")}
""")}
'''
    return chapter("random", "7", "Random numbers", "rstudio", "Random numbers and a t-test", 15,
                   "R can generate random numbers from many statistical distributions, and it has functions for all the common statistical tests. Testing numbers whose true mean you know is a good way to get a feel for how a test behaves.", body)


# ---------------------------------------------------------------------------------------------------------------------
def ch_structures():
    body = f'''
{structures()}
<h2 id="ds-vector">Vectors</h2>
<p>A vector is a single set of values, all of the same type. You have already worked with plenty of them, and you have used functions such as <code>mean()</code> and <code>sd()</code> that summarise all the values of a vector at once.</p>
{console(("scores <- c(0.8, 1.2, 3.3, 1.8, 2.7)", ""), ("mean(scores)", "[1] 1.96"), ("sd(scores)", "[1] 1.035857"))}

<h2 id="ds-list">Lists</h2>
<p>A list collects several vectors together into a single object. The vectors can be of different types and different lengths, and each has a name. You take a vector out of a list with <code>$</code> followed by its name:</p>
{block(RESULTS_CODE)}
{console(("results$counts", "[1] 100 300 200"))}

<h2 id="ds-df">Data frames</h2>
<p>A data frame is a list whose vectors all have the same length. Because the vectors line up, a data frame has rows as well as columns, like a table in a spreadsheet: each column is a vector, with values of a single type, and each row holds one set of observations. Most of the data you analyse in R will be in data frames.</p>
{block(ALL_RESULTS_CODE)}
{console(("all.results", """  mon tue wed  pass
1 0.8 0.9 0.8  TRUE
2 0.6 0.7 0.5 FALSE
3 0.2 0.3 0.3 FALSE
4 0.8 0.8 0.9  TRUE
5 0.6 1.0 0.9  TRUE"""))}
<p><code>$</code> works in the same way as it does for a list: <code>all.results$mon</code> is the <code>mon</code> column, as a vector, so <code>mean(all.results$mon)</code> is the mean of that column. <code>head()</code> shows the first rows, <code>nrow()</code> and <code>ncol()</code> count the rows and the columns, and <code>str()</code> summarises the structure of the data frame, with the type of each column and its first few values. The Environment pane lists data frames under <b>Data</b>, and clicking on one opens it in a viewer, as does <code>View()</code> (with a capital V).</p>

<h2 id="ds-tibble">Tibbles</h2>
<p>A <b>tibble</b> is the tidyverse’s version of a data frame. It holds the same kind of data, but it is nicer to work with: when you print a tibble, it shows the type of each column and only the first ten rows, and it only shows as many columns as fit across the Console. You will use tibbles all through the Tidyverse course.</p>
{activity("Lists and data frames", [
    rtask("ds-list", f'Create the list {c("results")}, as above.', RESULTS),
    rtask("ds-mean", f'Calculate the mean of the counts in {c("results")}.', lastv("isTRUE(all.equal(v, 200))")),
    rtask("ds-df", f'Create the data frame {c("all.results")}, as above.', ALL_RESULTS),
    task("ds-view", f'Open {c("all.results")} in the viewer, by clicking on it in the Environment pane or with {c("View(all.results)")}.', auto="r:view kind=rstudio"),
    task("ds-str", f'Use {c("str()")} to look at the structure of {c("all.results")}.', auto="r:input kind=rstudio line%str(all.results"),
    rtask("ds-mon", f'Calculate the mean of the {c("mon")} column of {c("all.results")}.', lastv("isTRUE(all.equal(v, 0.6))")),
])}
{q("ds-q-mon", "What is the mean of the <code>mon</code> column?", "0.6, from <code>mean(all.results$mon)</code>.", accept=ACC_MON, placeholder="A number")}
{q("ds-q-pass", "On how many of the rows is <code>pass</code> TRUE? Use <code>sum()</code> to find out.", "3, from <code>sum(all.results$pass)</code>.", accept="^3$", placeholder="A number")}
{mcq("ds-q-df", "What is the difference between a list and a data frame?", [
    ("In a data frame, all the vectors have the same length, so their values line up in rows", True, "That is what gives a data frame its rows, and it is why it looks like a table."),
    ("A data frame can only hold numbers", False, "Each column holds a single type, but different columns can hold different types: all.results has both numbers and TRUE/FALSE values."),
    ("A list can only hold one vector", False, "A list can hold any number of vectors, of any types and lengths."),
])}

<h2 id="ds-next">What next?</h2>
<p>You have now met the core of the R language. In the <b>Tidyverse</b> course you will read real data from files into tibbles, choose the rows and columns you need, and draw plots with ggplot2. Before you go, open the last chapter to get your certificate.</p>
'''
    return chapter("structures", "8", "Data structures", "rstudio", "Lists and data frames", 20,
                   "Vectors are the building blocks of all the data in R. To hold data that is more complicated than a single set of values, R puts vectors together into lists and data frames.", body)


def ALL():
    return [ch_start(), ch_calc(), ch_objects(), ch_functions(), ch_vectors(), ch_vectorised(), ch_select(), ch_random(), ch_structures(),
            certificate_chapter("certificate", "★", "R basics", "Your certificate for R basics, with your name on it.")]
