# Lexical analyzer

The first stage of translation is called lexical analysis or scanning. The lexical analyzer (scanner) reads the stream of characters, the source program, groups these characters into valid sequences defined by lexemes.
A lexeme is a structural unit of the language, consisting of elementary symbols of the language and not containing other structural units of the language. Programming language tokens are identifiers, constants, language keywords, operation signs, etc. P.
At the input of the lexical analyzer, the text of the source program is absorbed, and the output information is transmitted for further processing to the parser. For each token, the scanner builds an output token of the form:

`<token name, attribute value>`

The first component of a token, token_name, is an abstract symbol used during parsing, and the second component, attribute value, points to the entry in the identifier table corresponding to the given token.
Suppose, for example, that the source program contains an assignment statement:

`A = B - C / D`

The characters in this assignment can be grouped into the following tokens and mapped to the following tokens:

1. `A` is a token that can map to the token `<id,1>`, where `id` is an abstract character denoting an identifier, and `1` specifies an entry in the identifier table for a that stores information such as the name and type of the identifier;
1. The assignment symbol `=` is a token that maps to the token `<=>`. Since this token does not require an attribute value, the second component of this token is omitted. Any abstract symbol, such as "assign" can be used as the name of the token, but for convenience of notation, the token itself can be used as the name of the abstract symbol;
1. `B` is a token that maps to the `<id,2>` token, where `2` points to the entry in the identifier table for `B`;
1. `-` is a token mapped to token `<->`;
1. `C` is a token mapped to the `<id,3>` token, where `3` indicates the entry in the identifier table for `C`;
1. `/` is a lexeme mapped to the `</>` token;
1. `D` is a token mapped to the `<id,4>` token, where `4` indicates the entry in the identifier table for `D`.

Spaces separating tokens are ignored by the lexical analyzer.
The representation of the assignment instruction after lexical analysis as a sequence of tokens will take the following form:

`<id,1><=><id,2><-><id,3></><id,4>`

From a theoretical point of view, a lexical analyzer is not an obligatory, necessary part of a translator. Its functions can be performed at the stage of parsing. However, there are several reasons why lexical analysis is included in almost all translators:
- work with the text of the source program at the stage of parsing is simplified and the volume of processed information is reduced, since the lexical analyzer structures the source code of the program entering the input and removes all insignificant information;
- to select and parse lexemes in the text, you can use a simple, effective and theoretically well-developed analysis technique, while quite complex parsing algorithms are used at the stage of parsing the source language constructions;
- the scanner separates a complex parser from working directly with the text of the source program, the structure of which may vary depending on the version of the input language;
- with such a translator design, when moving from one version of the language to another, it is enough to rebuild a relatively simple scanner.

The functions performed by the lexical analyzer and the composition of lexemes that it distinguishes in the source program text may differ depending on the compiler version. Basically, lexical analyzers exclude comments and insignificant spaces from the text of the source program, as well as extract lexemes of the following types: identifiers, string, character and numeric constants, key (service) words of the input language.

The lexical analyzer of any translator can be implemented as a deterministic finite automaton.

The following classes have been developed to read a stream of characters from string data.

- `IStrReader` – string buffer interface for reading character stream from string data;
- `StrReader` - a class that implements the string buffer interface for reading a stream of characters from string data;
- `FileStrReader` – a class that implements the string buffer interface for reading a stream of characters from a text file.

The main methods of the `IStrReader` interface implemented by its subclasses are:
- `reset()` - Reset the buffer state to the initial state. Move the read head to the beginning of the string data;
- `read(count: int): str` - Read a string of the specified size from the buffer.

This interface is used by the lexical analyzer to read a sequence of data characters, which it then parses into individual tokens.

A lexeme or token is implemented by the `Token` class, which consists of two fields `kind` (lexeme type) and `value` (lexeme value). The `kind` field can be used as a token class identifier or token class name, and the `value` field can be used as a token identifier among tokens of the same class, or as the actual value of a token extracted from a sequence of characters.

The lexical analyzer is described using the ILexer interface. Main methods and properties of this interface:

* `data_reader` - property is a link to an instance of a class that implements the IStrReader interface;
* `num_column` – property number of the current viewed column in the analyzed text;
* `num_line` – property number of the current viewed line in the analyzed text;
* `_tokens` is a method for performing lexical analysis and extracting tokens in the analyzed text. All tokens returned by this method have the form (class_name, token_value);
* `tokens` - a method for performing lexical analysis and selection of tokens in the analyzed text. All tokens returned by this method have the form (class_number, token_number_in_class). 
This method uses the _tokens method in its work, but it enters the tokens received from it into the token table and instead returns the position in the token table as a token;
* `new_id_token` is a method for adding a token to the token table and converting this token into a token that represents a position in the token table;
* `lexemes` is a property for accessing the token table. The token table is a two-dimensional array, where the row index is class_number and the element index in the row is token_number_in_class. There is no table of identifiers as an explicit structure, but in an implicit form its similarity is contained in the table of tokens, as a string of program identifiers;
* `kinds` – property for converting class_number to class_name;
* `kind_ids` is a property for converting class_name to class_number.

The `Lexer` class is an implementation of the `ILexer` lexer interface. This class implements all the main methods and properties of `ILexer`. `Lexer` in lexical analysis uses the functions and classes of the Python standard regular expression library to extract tokens.

The lexical rules for the correct allocation of tokens are specified in the Lexer using the `specification` property. This is a list of tuples where the first element is the name of the token and the second element is a regular expression to extract the value of the token from the text.

`Lexer` solves the basic task of lexical analysis - extracting tokens from text, but this is not enough. For a lexical analyzer of programming languages, an important feature is the ability to distinguish keywords from identifiers, the ability to recognize lexemes that need to be discarded, for example, comments, the ability to convert cases when the programming language is case insensitive, the ability to recognize multiline lexemes. All the features described above are implemented using the `ProgLangLexer` class, which is an inheritor of the `Lexer` class and extends its `_tokens` method by implementing additional checks and token parsing algorithms.

To implement the possibility of distinguishing keywords from identifiers, `ProgLangLexer` has the `keywords` property, which takes a list of programming language keywords as a value. This class also has an `id_kind` property for specifying the class name of identifiers and a `keword_kind` property for specifying the class name of keywords.

To highlight multiline constructions, the `multitokens` property is used. As a value, it takes a list of boundary characters with the help of which the lexical analyzer understands where the end and where the beginning of multiline constructions is.

The `skip_kind` property is for specifying tokens that should be discarded. All tokens that contain the name from the `skip_kind ` property in the `kind` field will be instantly discarded.

The boolean property `case_sensitive` is used to specify case sensitivity. If its value is `True`, then the programming language is considered to be case sensitive.