# Grammar for fastcobol
The grammar is written in [Backus-Naur Form](https://en.wikipedia.org/wiki/Backus?Naur_form). Developing fastcobol is an iterative process and the grammar will also be evaluated, modified and expanded during the process. It is a good reference to what is currently supported, or what will be supported in the coming release.

## fcbl alpha 0.1
```<program> ::= PROGRAM <identifier> LBRACE <function_list> <statement_list> RBRACE```

```<function_list> ::= { <function> }```

```<function> ::= FUNC <identifier> LPAREN <parameter_list> RPAREN LBRACE <statement_list> <return_statement> RBRACE```

```<parameter_list> ::= <identifier_list> | /* empty */```

```<identifier_list> ::= <identifier> | <identifier_list> COMMA <identifier>```

```<return_statement> ::= RETURN <expression> SEMICOLON | /* empty */```

```<statement_list> ::= { <statement> }```

```<statement> ::= <assignment_statement> | <function_call>```

```<assignment_statement> ::= <identifier> <operator> <expression> SEMICOLON```

```<function_call> ::= <identifier> LPAREN <argument_list> RPAREN SEMICOLON```

```<argument_list> ::= <expression> | <argument_list> COMMA <expression>```

```<expression> ::= <term>
               | <expression> <operator> <term>
               | <function_call>```

```<term> ::= <integer>
         | <identifier>
         | <string_literal>```

```<integer> ::= <digit> | <integer> <digit>```

```<identifier> ::= <letter> { <letter> | <digit> | '_' }```
```<letter> ::= 'a' | 'b' | ... | 'z' | 'A' | 'B' | ... | 'Z'```
```<digit> ::= '0' | '1' | ... | '9'```

```<operator> ::= '+' | '-' | '*' | '/'```

```<string_literal> ::= '"' { <character> } '"'```
```<character> ::= <letter> | <digit> | <special_character>```
```<special_character> ::= any character except double quote '"'```
