// noinspection BadExpressionStatementJS

/* --------------------------------------------------------
 * Lexical grammar
 */

{
  macros: { },

  rules:[
    ["\\/\\/.*",                 `/* skip comments */`],
    ["\\/\\**(.|\\s+)*\\*\\/",   `/* Skip block comments */`],
    ["\\/\\*(.|\\s+)*\\*\\/",    `/* Skip block comments */`],
    ["\\s+",                     `/* skip whitespace */`],
    //["\\"[^\\"]*\\",              `return 'STRING'`],
    [`"[^"]*"`,                 `yytext = yytext.slice(1,-1); return 'STRING'`],
    // --------------------------------------------------------
    // KerML
    // Keywords: Base

    [`\\babout\\b`,                  `return 'ABOUT'`],
    [`\\babstract\\b`,               `return 'ABSTRACT'`],
    [`\\balias\\b`,                  `return 'ALIAS'`],
    [`\\ball\\b`,                    `return 'ALL'`],
    [`\\band\\b`,                    `return 'AND'`],
    [`\\bas\\b`,                     `return 'AS'`],
    [`\\bassign\\b`,                 `return 'ASSIGN'`],
    [`\\bassoc\\b`,                  `return 'ASSOC'`],
    [`\\bbehavior\\b`,               `return 'BEHAVIOR'`],
    [`\\bbinding\\b`,                `return 'BINDING'`],
    [`\\bbool\\b`,                   `return 'BOOL'`],
    [`\\bby\\b`,                     `return 'BY'`],
    [`\\bclass\\b`,                  `return 'CLASS'`],
    [`\\bclassifier\\b`,             `return 'CLASSIFIER'`],
    [`\\bcomment\\b`,                `return 'COMMENT'`],
    [`\\bcomposite\\b`,              `return 'COMPOSITE'`],
    [`\\bconjugate\\b`,              `return 'CONJUGATE'`],
    [`\\bconjugates\\b`,             `return 'CONJUGATES'`],
    [`\\bconjugation\\b`,            `return 'CONJUGATION'`],
    [`\\bconnector\\b`,              `return 'CONNECTOR'`],
    [`\\bdatatype\\b`,               `return 'DATATYPE'`],
    [`\\bdefault\\b`,                `return 'DEFAULT'`],
    [`\\bdisjoining\\b`,             `return 'DISJOINING'`],
    [`\\bdisjoint  \\b`,             `return 'DISJOINT'`],
    [`\\bdoc\\b`,                    `return 'DOC'`],
    [`\\belement\\b`,                `return 'ELEMENT'`],
    [`\\belse\\b`,                   `return 'ELSE'`],
    [`\\bend\\b`,                    `return 'END'`],
    [`\\bexpr\\b`,                   `return 'EXPR'`],
    [`\\bfalse\\b`,                  `return 'FALSE'`],
    [`\\bfeature\\b`,                `return 'FEATURE'`],
    [`\\bfeatured\\b`,               `return 'FEATURED'`],
    [`\\bfeaturing\\b`,              `return 'FEATURING'`],
    [`\\bfilter\\b`,                 `return 'FILTER'`],
    [`\\bfirst\\b`,                  `return 'FIRST'`],
    [`\\bflow\\b`,                   `return 'FLOW'`],
    [`\\bfor\\b`,                    `return 'FOR'`],
    [`\\bfrom\\b`,                   `return 'FROM'`],
    [`\\bfunction\\b`,               `return 'FUNCTION'`],
    [`\\bgeneralization\\b`,         `return 'GENERALIZATION'`],
    [`\\bhastype\\b`,                `return 'HASTYPE'`],
    [`\\bid\\b`,                     `return 'ID'`],
    [`\\bif\\b`,                     `return 'IF'`],
    [`\\bimplies\\b`,                `return 'IMPLIES'`],
    [`\\bimport\\b`,                 `return 'IMPORT'`],
    [`\\bin\\b`,                     `return 'IN'`],
    [`\\binout\\b`,                  `return 'INOUT'`],
    [`\\binteraction\\b`,            `return 'INTERACTION'`],
    [`\\binv\\b`,                    `return 'INV'`],
    [`\\bis\\b`,                     `return 'IS'`],
    [`\\bistype\\b`,                 `return 'ISTYPE'`],
    [`\\blanguage\\b`,               `return 'LANGUAGE'`],
    [`\\bmember\\b`,                 `return 'MEMBER'`],
    [`\\bmetadata\\b`,               `return 'METADATA'`],
    [`\\bmultiplicity\\b`,           `return 'MULTIPLICITY'`],
    [`\\bnamespace\\b`,              `return 'NAMESPACE'`],
    [`\\bnonunique\\b`,              `return 'NONUNIQUE'`],
    [`\\bnot\\b`,                    `return 'NOT'`],
    [`\\bnull\\b`,                   `return 'NULL'`],
    [`\\bof\\b`,                     `return 'OF'`],
    [`\\bor\\b`,                     `return 'OR'`],
    [`\\bordered\\b`,                `return 'ORDERED'`],
    [`\\bout\\b`,                    `return 'OUT'`],
    [`\\bpackage\\b`,                `return 'PACKAGE'`],
    [`\\bportion\\b`,                `return 'PORTION'`],
    [`\\bpredicate\\b`,              `return 'PREDICATE'`],
    [`\\bprivate\\b`,                `return 'PRIVATE'`],
    [`\\bprotected\\b`,              `return 'PROTECTED'`],
    [`\\bpublic\\b`,                 `return 'PUBLIC'`],
    [`\\bredefines\\b`,              `return 'REDEFINES'`],
    [`\\bredefinition\\b`,           `return 'REDEFINITION'`],
    [`\\brelationship\\b`,           `return 'RELATIONSHIP'`],
    [`\\brep\\b`,                    `return 'REP'`],
    [`\\breturn\\b`,                 `return 'RETURN'`],
    [`\\bspecialization\\b`,         `return 'SPECIALIZATION'`],
    [`\\bspecializes\\b`,            `return 'SPECIALIZES'`],
    [`\\bstep\\b`,                   `return 'STEP'`],
    [`\\bstream\\b`,                 `return 'STREAM'`],
    [`\\bstruct\\b`,                 `return 'STRUCT'`],
    [`\\bsubclassifier\\b`,          `return 'SUBCLASSIFIER'`],
    [`\\bsubset\\b`,                 `return 'SUBSET'`],
    [`\\bsubsets\\b`,                `return 'SUBSETS'`],
    [`\\bsubtype\\b`,                `return 'SUBTYPE'`],
    [`\\bsuccession\\b`,             `return 'SUCCESSION'`],
    [`\\bthen\\b`,                   `return 'THEN'`],
    [`\\bto\\b`,                     `return 'TO'`],
    [`\\btrue\\b`,                   `return 'TRUE'`],
    [`\\btype\\b`,                   `return 'TYPE'`],
    [`\\btyped\\b`,                  `return 'TYPED'`],
    [`\\btyping\\b`,                 `return 'TYPING'`],
    [`\\bxor\\b`,                    `return 'XOR'`],

    // --------------------------------------------------------
    // Numbers.

    [`\\d+`,                `return 'NUMBER'`],
    [`\\w+`,                `return 'IDENTIFIER'`],

    // --------------------------------------------------------
    // Relationshp operators: :>
    [`\\:\\>`,                 `return 'SPECIALIZATION'`]
  ]

}

