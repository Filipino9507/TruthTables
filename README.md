# TruthTables
Small utility tool used to generate truth tables based on logical expressions entered by the user.

Run from root directory using:\
`$ python3 main.py`

## Expression syntax
The expressions can contain **alphanumeric variable names**, **operators**, **parentheses** and **boolean literals**.

### Operators
- **logical and** - **&**
- **logical or** - **|**
- **logical not** - **!**
- **logical implication** - **=>**
- **logical equivalence** / XNOR - **<=>**

### Parentheses
- **normal parentheses** - **(...)** - control evaluation priority
- **capturing parentheses** - **[...]** - control evaluation priority and also capture the intermediate value, which is later displayed in the table as well

### Boolean literals
- **tautology** - **1** - always evaluates to true
- **contradiction** - **0** - always evaluates to false


## Result
The resulting table shows all the combinations of values (2^n for number of variables being n) and the resulting value of the entered expression
for each of them. The number of the possible variables is limited, so that the table can fit on the screen whole. To display resulting values for parts
of the expression, use **capturing parentheses**.
