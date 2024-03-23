# fastcobol - Generate COBOL modules fast!
Working with Cobol usually includes a lot of overhead. For instance, the language itself only use global variables - and as such they must be declare at the head (working storage) in the same way assembler. Also, company-specific standards and code-policies for error handling and module calls take up a lot of text-space. Even the simplest cobol-modul will quickly be filled with extensive amounts of variables and sections. The fastcobol initiative aims for developers to work with logic in a more intuitive manner. The rendered cobol code can be inserted into company specific templates.

All initatives to help out are most welcome!

## roadmap
I am currently working on this project by myself at my spare time. The first goal is to get the basic concept working. There is still work to be done with the parser. After that the work of the renderer will begin. This will most likley be an iterative process where tokenizer and parser are revisited and enhanced.

When a simple alpha build is working I will put time into refactoring and re-evaluate design choices.

Then a list with features will be prioritezed. And the roadmap updated.

In the far future I hope to be able to add/import cobol copys, settings for different policies and maybe even try to implement OOP.


## Grammar for fastcobol
The grammar is written in [Backus-Naur Form](https://en.wikipedia.org/wiki/Backus?Naur_form). Developing fastcobol is an iterative process and the grammar will also be evaluated, modified and expanded during the process. It is a good reference to what is currently supported, or what will be supported in the coming release.

### alpha 0.2
```
<program> ::= PROGRAM <identifier> LBRACE <statement_list> <function_list> RBRACE 

<function_list> ::= { <function> } 
<function> ::= FUNC <identifier> 
               LPAREN <parameter_list> RPAREN 
               LBRACE <statement_list> <return_statement> RBRACE 

<parameter_list> ::= <identifier_list> | /* empty */ 

<identifier_list> ::= <identifier> | <identifier_list> COMMA <identifier> 

<return_statement> ::= RETURN <expression> SEMICOLON | /* empty */ 

<statement_list> ::= { <statement> } 
 
<statement> ::= <assignment_statement> SEMICOLON
              | <function_call> SEMICOLON
 
<assignment_statement> ::= <identifier> <operator> <expression> 

<function_call> ::= <identifier> 
                    LPAREN <argument_list> RPAREN  

<argument_list> ::= <expression> | <argument_list> COMMA <expression> 
 
<expression> ::= <term>
               | <expression> <operator> <term>
               | <function_call>
  
<term> ::= <integer>
         | <identifier>
         | <string_literal>
 
 <integer> ::= <digit> | <integer> <digit> 

 <identifier> ::= <letter> { <letter> | <digit> | '_' } 
 <letter> ::= 'a' | 'b' | ... | 'z' | 'A' | 'B' | ... | 'Z' 
 <digit> ::= '0' | '1' | ... | '9' 

 <operator> ::= '+' | '-' | '*' | '/' 

 <string_literal> ::= '"' { <character> } '"' 
 <character> ::= <letter> | <digit> | <special_character> 
 <special_character> ::= any character except double quote '"'
```
 
