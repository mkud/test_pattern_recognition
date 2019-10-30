Let we have 3 kinds of characters:
* letters;
* digits;
* others.

You can add more types. For example, divide the letters into uppercase and lowercase. To do this, you will need to change `regex_int_mask_relations` in file `recognition.py`

You can specify the initial data for analysis as list `input_array` in file `recognition.py`

The analysis process is divided into stages:

## Stage 1:
Map all symbols in input data to internal mask presentation (letters/digits/others)
*Example:*
`"A--1012332/1" -> "loodddddddod"`

## Stage 2:
Group internal mask presentation by removing duplicate symbols.
This masks we will use for searching errors in the input data.
*Example:*
`"loodddddddod" -> "lodod"`
Plus counting duplicate symbols: `"loodddddddod" -> "lo{2}d{7}od"`

## Stage 3
Calc the popularity of all short masks to find the most popular. Other masks are considered erroneous.
*Example:*
`'lodod'` - most popular. Suitable for 80% of input data

## Stage 4:
We get all the groups of all input array, remove duplicates by set(). Consider only objects with the most popular mask.
*Example:*
list of groups:
`[{'S', 'A'}, {'--'}, {'1012332', '1231142'}, {'/'}, {'1', '2', '11'}]`
Length of this list = length of the most popular mask

## Stage 5:
Analyze each group to find a mutual beginning or end. If found - move it to a separate group. This will make it possible to specify the format more accurately.
*Example:*
Set `{'1012332', '1231142'}` has mutual parts - "1" at the begining and "2" at the end. So it will be divided into 3 groups `{'1'}`, `{'01233', '23114'}` and `{'2'}`.
Result list of groups:
`[{'S', 'A'}, {'--'}, {'1'}, {'01233', '23114'}, {'2'}, {'/'}, {'1', '2', '11'}]`
		 
## Stage 6:
Сollect from the resulting groups an array for the formation of regex
Available cases: 
* specific value (`{'--'}`);
* any char from set (`{'S', 'A'}`);
* string of one type (from `regex_int_mask_relations`) with len range (`{'1', '2', '11'}`).

*Example:*
result: `^[SA]--1\d{5}2/\d{1,2}$`
		
