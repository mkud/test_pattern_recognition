# Pattern Recognition


<b>Dear prospective candidate,</b>

Our goal here is to assess your (a) general problem solving skills, (b) communication skills and (c) your coding aptitude in <em>Python 3</em>.
Therefore, we ask you to present your code together with your ideas, thoughts, and reasoning. It is no problem if you do not complete all of the tasks. If you get stuck in the middle of a problem you may give a partial answer. Please supplement your code with comments explaining the logic.

In any case, we encourage you to provide feedback about any obstacles that you encountered with this task.



##  Scenario Description

Imagine a system that processes various customer documents, like orders or invoices. The documents contain several pieces of information, e.g., order ID, address, company name, name of a person, zip code, bar code, date, IBAN, billing amounts.
Extracting the relevant information can be tough, because the data is unstructured. The system initially has no idea how an order ID may look like and where to find it on the document.
For example, the system reads the string `'1234567AB'` but has no idea if this might be an order ID, or a name.
But because there are other similar documents, it is possible in theory to derive the structure of an order ID.

## Task Description

Your job is to write a <em>Python 3</em> program that extracts relevant information from examples.
Assume that you get a list of strings containing digits, letters, and special characters.
The objective is to describe the pattern(s) of the input strings using regular expressions. 
For instance, consider the following list:

```
[ "123456",
  "654321",
  "101010",
  "999999",
  "939495" ]
```
A reasonable pattern for this list may be represented by the regular expression `r"^\d{6}$"`.

Your task is to "write a code that generates a regular expression, given the list of strings (use the `re` module that comes with Python).  

But there are some side conditions:
 
 - Since data is always dirty in the real world, we have to assume that the list contains errors, but at most 2% of the data is dirty. Dirty data may stem from wrong IDs (for instance an order ID with a different format coming from a different creditor) that have been put into your list accidentally, as well as from typing errors. As a result, a good pattern does not need to match every single input string in the list, but only the relevant ones.
 - Your heuristic should remember which input strings have not been considered during the pattern creation.
 - The resulting regular expression should match the input strings intelligently. Clearly, `r".*"` is valid pattern for any input, but it does not capture any useful information relating to the provided inputs.


## Hints 

 - This is a creative task which by its very nature is underspecified.
 - This task has multiple correct solutions which differ considerably. There are several ways to complete the challenge that we know of now, and we bet you will complete it in yet another different way that we are not expecting.
 - Most likely you will have to rely on further assumptions that are not stated in the task description. Please write them down, so we can follow your thoughts afterwards. 
 - The correctness of the output patterns for given input lists also depends on <em>your</em> reasoning.

## Examples

Some examples to describe the input list and one possible desired output.

### Example 1

<b>Input</b>

```
[ "2018-01-11",
  "2019-10-10",
  "1991-10-13",
  "2000-01-10",
  "2019-10-10"]
```
<b>Acceptable Output</b>
 
``` 
r"^\d{4}-\d{2}-\d{2}$" 
```

### Example 2

</b>Input</b>


```
[ "A-1012331/1",
  "A-1231141/2",
  "A-1231141/1",
  "A-1233441/2",
  "S-1231141/11" # <-- This ID might be considered erroneous.
 ]
```

<b>Acceptable Output 1</b>

```
  r"^A-\d{7}/\d{1}$" (with the assumption that "S-1231141/11" is erroneous)

```
<b>Acceptable Output 2</b>

```
  r"^[A-Z]-\d{7}/\d{1,2}$" (with the assumption that "S-1231141/11" is not erroneous)

```


Please feel free to add your own examples of list inputs at the beginning of your script (or your __main__() function) to help us know the extent of input patterns your script covers. You can revisit "Scenario Description" to know the type of information/input cases you might want to primarily cover.
