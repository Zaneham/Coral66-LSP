"""
CORAL 66 Semantic Parser
Based on the Official Definition of CORAL 66 (HMSO 1970/1974)

CORAL 66 is the UK Ministry of Defence standard real-time programming language,
based on ALGOL 60, used in defence systems and industrial control applications.

Reference: XGC CORAL 66 Language Reference Manual (Crown Copyright 1970)
"""

import re
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass, field
from enum import Enum


class SymbolKind(Enum):
    """Symbol kinds for CORAL 66"""
    VARIABLE = "variable"
    ARRAY = "array"
    TABLE = "table"
    PROCEDURE = "procedure"
    FUNCTION = "function"
    SWITCH = "switch"
    LABEL = "label"
    PARAMETER = "parameter"
    ELEMENT = "element"
    OVERLAY = "overlay"


@dataclass
class Symbol:
    """A symbol in the CORAL 66 program"""
    name: str
    kind: SymbolKind
    data_type: str
    line: int
    column: int
    end_line: int = 0
    end_column: int = 0
    scope: str = "global"
    documentation: str = ""
    parameters: List[str] = field(default_factory=list)
    dimensions: List[str] = field(default_factory=list)
    elements: List[str] = field(default_factory=list)


@dataclass
class Reference:
    """A reference to a symbol"""
    name: str
    line: int
    column: int
    end_column: int = 0
    context: str = ""


@dataclass
class Diagnostic:
    """A diagnostic message"""
    line: int
    column: int
    end_column: int
    message: str
    severity: str = "error"


class CORAL66Parser:
    """
    Parser for CORAL 66 language

    Based on the Official Definition of CORAL 66 (HMSO 1970)
    """

    # CORAL 66 keywords - uppercase
    KEYWORDS = {
        # Block structure
        'BEGIN', 'END',
        # Control flow
        'IF', 'THEN', 'ELSE', 'FOR', 'DO', 'WHILE', 'STEP', 'UNTIL', 'GOTO',
        # Procedures
        'PROCEDURE', 'RECURSIVE', 'ANSWER',
        # Data types
        'FLOATING', 'FIXED', 'INTEGER', 'UNSIGNED',
        # Declarations
        'ARRAY', 'TABLE', 'SWITCH', 'OVERLAY', 'WITH', 'PRESET',
        # Parameter modes
        'VALUE', 'LOCATION',
        # Communicators
        'COMMON', 'LIBRARY', 'EXTERNAL', 'ABSOLUTE',
        # Bit operations
        'BITS', 'LABEL',
        # Word logic operators
        'AND', 'OR', 'DIFFER', 'UNION', 'MASK',
        # Literals
        'OCTAL', 'LITERAL',
        # Comments
        'COMMENT',
        # Macros
        'DEFINE', 'DELETE',
        # Code statement
        'CODE',
    }

    # Operators
    OPERATORS = {
        ':=': 'assignment',
        '+': 'add',
        '-': 'subtract',
        '*': 'multiply',
        '/': 'divide',
        '<': 'less than',
        '<=': 'less than or equal',
        '=': 'equals',
        '>=': 'greater than or equal',
        '>': 'greater than',
        '<>': 'not equal',
    }

    def __init__(self):
        self.symbols: Dict[str, Symbol] = {}
        self.references: List[Reference] = []
        self.diagnostics: List[Diagnostic] = []
        self.lines: List[str] = []
        self.current_scope: str = "global"
        self.scope_stack: List[str] = ["global"]

    def parse(self, text: str) -> None:
        """Parse CORAL 66 source code"""
        self.symbols = {}
        self.references = []
        self.diagnostics = []
        self.lines = text.split('\n')
        self.current_scope = "global"
        self.scope_stack = ["global"]

        # Remove comments first
        cleaned_text = self._remove_comments(text)

        # Parse declarations
        self._parse_number_declarations(cleaned_text)
        self._parse_array_declarations(cleaned_text)
        self._parse_table_declarations(cleaned_text)
        self._parse_procedure_declarations(cleaned_text)
        self._parse_switch_declarations(cleaned_text)
        self._parse_overlay_declarations(cleaned_text)
        self._parse_labels(cleaned_text)

        # Parse references
        self._parse_references(cleaned_text)

    def _remove_comments(self, text: str) -> str:
        """Remove CORAL 66 comments"""
        # COMMENT ... ; style comments
        text = re.sub(r'\bCOMMENT\b[^;]*;', '', text, flags=re.IGNORECASE)
        # Bracketed comments are kept as they're part of syntax
        return text

    def _find_position(self, text: str, match_start: int) -> Tuple[int, int]:
        """Convert character offset to line and column"""
        line = text[:match_start].count('\n')
        last_newline = text.rfind('\n', 0, match_start)
        column = match_start - last_newline - 1 if last_newline >= 0 else match_start
        return (line, column)

    def _parse_number_declarations(self, text: str) -> None:
        """
        Parse number declarations:
        INTEGER id1, id2 := value
        FLOATING id1, id2
        FIXED(totalbits, fractionbits) id1, id2 := value
        """
        # INTEGER declarations
        pattern = r'\b(INTEGER)\s+([a-zA-Z][a-zA-Z0-9]*(?:\s*,\s*[a-zA-Z][a-zA-Z0-9]*)*)(?:\s*:=\s*([^;]+))?'
        for match in re.finditer(pattern, text, re.IGNORECASE):
            type_name = match.group(1).upper()
            id_list = match.group(2)
            preset = match.group(3)

            ids = [id.strip() for id in id_list.split(',')]
            for id_name in ids:
                if id_name and not id_name.upper() in self.KEYWORDS:
                    line, col = self._find_position(text, match.start())
                    self.symbols[id_name.lower()] = Symbol(
                        name=id_name.lower(),
                        kind=SymbolKind.VARIABLE,
                        data_type=type_name,
                        line=line,
                        column=col,
                        documentation=f"{type_name} variable"
                    )

        # FLOATING declarations
        pattern = r'\b(FLOATING)\s+([a-zA-Z][a-zA-Z0-9]*(?:\s*,\s*[a-zA-Z][a-zA-Z0-9]*)*)(?:\s*:=\s*([^;]+))?'
        for match in re.finditer(pattern, text, re.IGNORECASE):
            type_name = match.group(1).upper()
            id_list = match.group(2)

            ids = [id.strip() for id in id_list.split(',')]
            for id_name in ids:
                if id_name and not id_name.upper() in self.KEYWORDS:
                    line, col = self._find_position(text, match.start())
                    self.symbols[id_name.lower()] = Symbol(
                        name=id_name.lower(),
                        kind=SymbolKind.VARIABLE,
                        data_type=type_name,
                        line=line,
                        column=col,
                        documentation=f"{type_name} variable"
                    )

        # FIXED(totalbits, fractionbits) declarations
        pattern = r'\b(FIXED)\s*\(\s*(\d+)\s*,\s*(-?\d+)\s*\)\s+([a-zA-Z][a-zA-Z0-9]*(?:\s*,\s*[a-zA-Z][a-zA-Z0-9]*)*)(?:\s*:=\s*([^;]+))?'
        for match in re.finditer(pattern, text, re.IGNORECASE):
            totalbits = match.group(2)
            fractionbits = match.group(3)
            id_list = match.group(4)
            type_name = f"FIXED({totalbits},{fractionbits})"

            ids = [id.strip() for id in id_list.split(',')]
            for id_name in ids:
                if id_name and not id_name.upper() in self.KEYWORDS:
                    line, col = self._find_position(text, match.start())
                    self.symbols[id_name.lower()] = Symbol(
                        name=id_name.lower(),
                        kind=SymbolKind.VARIABLE,
                        data_type=type_name,
                        line=line,
                        column=col,
                        documentation=f"Fixed-point variable: {totalbits} total bits, {fractionbits} fraction bits"
                    )

    def _parse_array_declarations(self, text: str) -> None:
        """
        Parse array declarations:
        FLOATING ARRAY name[lower:upper]
        INTEGER ARRAY name[l1:u1, l2:u2]
        FIXED(t,f) ARRAY name[lower:upper] := values
        """
        # Number type ARRAY pattern
        pattern = r'\b(INTEGER|FLOATING)\s+ARRAY\s+([a-zA-Z][a-zA-Z0-9]*)\s*\[([^\]]+)\]'
        for match in re.finditer(pattern, text, re.IGNORECASE):
            type_name = match.group(1).upper()
            array_name = match.group(2)
            dimensions = match.group(3)

            line, col = self._find_position(text, match.start())
            self.symbols[array_name.lower()] = Symbol(
                name=array_name.lower(),
                kind=SymbolKind.ARRAY,
                data_type=f"{type_name} ARRAY",
                line=line,
                column=col,
                dimensions=[d.strip() for d in dimensions.split(',')],
                documentation=f"{type_name} array with dimensions [{dimensions}]"
            )

        # FIXED ARRAY pattern
        pattern = r'\b(FIXED)\s*\(\s*(\d+)\s*,\s*(-?\d+)\s*\)\s+ARRAY\s+([a-zA-Z][a-zA-Z0-9]*)\s*\[([^\]]+)\]'
        for match in re.finditer(pattern, text, re.IGNORECASE):
            totalbits = match.group(2)
            fractionbits = match.group(3)
            array_name = match.group(4)
            dimensions = match.group(5)
            type_name = f"FIXED({totalbits},{fractionbits})"

            line, col = self._find_position(text, match.start())
            self.symbols[array_name.lower()] = Symbol(
                name=array_name.lower(),
                kind=SymbolKind.ARRAY,
                data_type=f"{type_name} ARRAY",
                line=line,
                column=col,
                dimensions=[d.strip() for d in dimensions.split(',')],
                documentation=f"Fixed-point array [{dimensions}]: {totalbits} bits, {fractionbits} fraction bits"
            )

    def _parse_table_declarations(self, text: str) -> None:
        """
        Parse table declarations:
        TABLE name[width, length][
            element type wordpos;
            element type wordpos, bitpos
        ]
        """
        pattern = r'\bTABLE\s+([a-zA-Z][a-zA-Z0-9]*)\s*\[\s*(\d+)\s*,\s*(\d+)\s*\]\s*\[([^\]]*)\]'
        for match in re.finditer(pattern, text, re.IGNORECASE | re.DOTALL):
            table_name = match.group(1)
            width = match.group(2)
            length = match.group(3)
            elements_text = match.group(4)

            line, col = self._find_position(text, match.start())

            # Parse elements
            elements = []
            for elem_match in re.finditer(
                r'([a-zA-Z][a-zA-Z0-9]*)\s+(INTEGER|FLOATING|FIXED\s*\([^)]+\)|UNSIGNED\s*\([^)]+\))\s+(-?\d+)(?:\s*,\s*(\d+))?',
                elements_text,
                re.IGNORECASE
            ):
                elem_name = elem_match.group(1)
                elem_type = elem_match.group(2)
                elements.append(elem_name.lower())

                # Add element as a symbol
                elem_line, elem_col = self._find_position(text, match.start() + elements_text.find(elem_match.group(0)))
                self.symbols[f"{table_name.lower()}.{elem_name.lower()}"] = Symbol(
                    name=elem_name.lower(),
                    kind=SymbolKind.ELEMENT,
                    data_type=elem_type.upper(),
                    line=elem_line,
                    column=elem_col,
                    scope=table_name.lower(),
                    documentation=f"Element of TABLE {table_name}"
                )

            self.symbols[table_name.lower()] = Symbol(
                name=table_name.lower(),
                kind=SymbolKind.TABLE,
                data_type=f"TABLE[{width},{length}]",
                line=line,
                column=col,
                elements=elements,
                documentation=f"Table with width {width}, length {length}"
            )

    def _parse_procedure_declarations(self, text: str) -> None:
        """
        Parse procedure declarations:
        INTEGER PROCEDURE name(params); body
        FLOATING PROCEDURE name; body
        PROCEDURE name(params); body (void return)
        RECURSIVE with any of the above
        """
        # Pattern for typed procedures with parameters
        pattern = r'\b(INTEGER|FLOATING|FIXED\s*\([^)]+\))?\s*(RECURSIVE\s+)?PROCEDURE\s+([a-zA-Z][a-zA-Z0-9]*)\s*(?:\(([^)]*)\))?\s*;'
        for match in re.finditer(pattern, text, re.IGNORECASE):
            return_type = match.group(1)
            is_recursive = match.group(2) is not None
            proc_name = match.group(3)
            params_text = match.group(4)

            if return_type:
                kind = SymbolKind.FUNCTION
                type_str = return_type.upper() + " PROCEDURE"
            else:
                kind = SymbolKind.PROCEDURE
                type_str = "PROCEDURE"

            if is_recursive:
                type_str = "RECURSIVE " + type_str

            line, col = self._find_position(text, match.start())

            # Parse parameters
            params = []
            if params_text:
                # Parameters can be: VALUE type: id, id; LOCATION type: id
                param_parts = params_text.split(';')
                for part in param_parts:
                    part = part.strip()
                    if part:
                        # Extract identifiers from parameter specification
                        id_match = re.search(r':\s*([a-zA-Z][a-zA-Z0-9]*(?:\s*,\s*[a-zA-Z][a-zA-Z0-9]*)*)', part)
                        if id_match:
                            ids = [i.strip() for i in id_match.group(1).split(',')]
                            params.extend(ids)

                            # Add parameters as symbols in procedure scope
                            for param_name in ids:
                                self.symbols[f"{proc_name.lower()}.{param_name.lower()}"] = Symbol(
                                    name=param_name.lower(),
                                    kind=SymbolKind.PARAMETER,
                                    data_type="parameter",
                                    line=line,
                                    column=col,
                                    scope=proc_name.lower(),
                                    documentation=f"Parameter of {proc_name}"
                                )

            self.symbols[proc_name.lower()] = Symbol(
                name=proc_name.lower(),
                kind=kind,
                data_type=type_str,
                line=line,
                column=col,
                parameters=params,
                documentation=f"{type_str} - {'returns ' + return_type.upper() if return_type else 'no return value'}"
            )

    def _parse_switch_declarations(self, text: str) -> None:
        """
        Parse switch declarations:
        SWITCH name := label1, label2, label3
        """
        pattern = r'\bSWITCH\s+([a-zA-Z][a-zA-Z0-9]*)\s*:=\s*([a-zA-Z][a-zA-Z0-9]*(?:\s*,\s*[a-zA-Z][a-zA-Z0-9]*)*)'
        for match in re.finditer(pattern, text, re.IGNORECASE):
            switch_name = match.group(1)
            labels_text = match.group(2)

            labels = [l.strip() for l in labels_text.split(',')]

            line, col = self._find_position(text, match.start())
            self.symbols[switch_name.lower()] = Symbol(
                name=switch_name.lower(),
                kind=SymbolKind.SWITCH,
                data_type="SWITCH",
                line=line,
                column=col,
                elements=labels,
                documentation=f"Switch with labels: {', '.join(labels)}"
            )

    def _parse_overlay_declarations(self, text: str) -> None:
        """
        Parse overlay declarations:
        OVERLAY base WITH datadec
        """
        pattern = r'\bOVERLAY\s+([a-zA-Z][a-zA-Z0-9]*(?:\s*\[[^\]]*\])?)\s+WITH\s+'
        for match in re.finditer(pattern, text, re.IGNORECASE):
            base = match.group(1)

            line, col = self._find_position(text, match.start())
            # Use a unique key for overlays
            overlay_key = f"overlay_{line}_{col}"
            self.symbols[overlay_key] = Symbol(
                name=base.lower(),
                kind=SymbolKind.OVERLAY,
                data_type="OVERLAY",
                line=line,
                column=col,
                documentation=f"Overlay on {base}"
            )

    def _parse_labels(self, text: str) -> None:
        """
        Parse labels - identifiers followed by colon before a statement
        label: statement
        """
        # Labels are identifiers followed by : but not :=
        pattern = r'\b([a-zA-Z][a-zA-Z0-9]*)\s*:(?!=)'
        for match in re.finditer(pattern, text):
            label_name = match.group(1)
            # Skip if it looks like a parameter specification
            if label_name.upper() in self.KEYWORDS:
                continue

            line, col = self._find_position(text, match.start())
            # Don't override existing symbols
            if label_name.lower() not in self.symbols:
                self.symbols[label_name.lower()] = Symbol(
                    name=label_name.lower(),
                    kind=SymbolKind.LABEL,
                    data_type="LABEL",
                    line=line,
                    column=col,
                    documentation="Label"
                )

    def _parse_references(self, text: str) -> None:
        """Parse all identifier references in the code"""
        # Find all identifiers (lowercase letters followed by alphanumerics)
        pattern = r'\b([a-zA-Z][a-zA-Z0-9]*)\b'
        for match in re.finditer(pattern, text):
            name = match.group(1)
            # Skip keywords
            if name.upper() in self.KEYWORDS:
                continue

            line, col = self._find_position(text, match.start())
            self.references.append(Reference(
                name=name.lower(),
                line=line,
                column=col,
                end_column=col + len(name)
            ))

    def get_symbols(self) -> Dict[str, Symbol]:
        """Get all parsed symbols"""
        return self.symbols

    def get_references(self) -> List[Reference]:
        """Get all references"""
        return self.references

    def get_diagnostics(self) -> List[Diagnostic]:
        """Get all diagnostics"""
        return self.diagnostics

    def get_completions(self, line: int, column: int) -> List[Dict]:
        """Get completion items at position"""
        completions = []

        # Add keywords
        for kw in sorted(self.KEYWORDS):
            completions.append({
                'label': kw,
                'kind': 'keyword',
                'detail': 'CORAL 66 keyword',
                'documentation': f"CORAL 66 keyword: {kw}"
            })

        # Add symbols
        for name, sym in self.symbols.items():
            if '.' in name:  # Skip scoped symbols like table.element
                continue
            completions.append({
                'label': sym.name,
                'kind': sym.kind.value,
                'detail': sym.data_type,
                'documentation': sym.documentation
            })

        return completions

    def get_hover(self, line: int, column: int) -> Optional[Dict]:
        """Get hover information at position"""
        if line >= len(self.lines):
            return None

        line_text = self.lines[line]

        # Find the word at this position
        word_match = None
        for match in re.finditer(r'\b([a-zA-Z][a-zA-Z0-9]*)\b', line_text):
            if match.start() <= column <= match.end():
                word_match = match
                break

        if not word_match:
            return None

        word = word_match.group(1)

        # Check if it's a keyword
        if word.upper() in self.KEYWORDS:
            return {
                'contents': f"**{word.upper()}**\n\nCORAL 66 keyword"
            }

        # Check if it's a symbol
        if word.lower() in self.symbols:
            sym = self.symbols[word.lower()]
            return {
                'contents': f"**{sym.name}**: {sym.data_type}\n\n{sym.documentation}"
            }

        return None

    def get_definition(self, line: int, column: int) -> Optional[Dict]:
        """Get definition location for symbol at position"""
        if line >= len(self.lines):
            return None

        line_text = self.lines[line]

        # Find the word at this position
        for match in re.finditer(r'\b([a-zA-Z][a-zA-Z0-9]*)\b', line_text):
            if match.start() <= column <= match.end():
                word = match.group(1).lower()
                if word in self.symbols:
                    sym = self.symbols[word]
                    return {
                        'line': sym.line,
                        'column': sym.column,
                        'name': sym.name
                    }
                break

        return None

    def get_references_at(self, line: int, column: int) -> List[Dict]:
        """Get all references to symbol at position"""
        if line >= len(self.lines):
            return []

        line_text = self.lines[line]

        # Find the word at this position
        target_word = None
        for match in re.finditer(r'\b([a-zA-Z][a-zA-Z0-9]*)\b', line_text):
            if match.start() <= column <= match.end():
                target_word = match.group(1).lower()
                break

        if not target_word:
            return []

        # Find all references to this word
        refs = []
        for ref in self.references:
            if ref.name == target_word:
                refs.append({
                    'line': ref.line,
                    'column': ref.column,
                    'end_column': ref.end_column
                })

        return refs

    def get_document_symbols(self) -> List[Dict]:
        """Get all document symbols for outline"""
        symbols = []
        for name, sym in self.symbols.items():
            if '.' in name:  # Skip nested symbols
                continue
            symbols.append({
                'name': sym.name,
                'kind': sym.kind.value,
                'detail': sym.data_type,
                'line': sym.line,
                'column': sym.column
            })
        return sorted(symbols, key=lambda x: x['line'])


def main():
    """Test the parser"""
    test_code = '''
COMMENT This is a test CORAL 66 program;

BEGIN
    INTEGER count, total := 0;
    FLOATING temperature;
    FIXED(16, 8) velocity, acceleration;

    INTEGER ARRAY readings[0:99];
    FLOATING ARRAY matrix[1:10, 1:10];

    TABLE sensors[4, 100][
        id INTEGER 0;
        value FIXED(16, 8) 1;
        status UNSIGNED(8) 2, 0
    ];

    SWITCH action := start, process, finish;

    INTEGER PROCEDURE square(VALUE INTEGER: x);
    BEGIN
        ANSWER x * x
    END;

    RECURSIVE PROCEDURE factorial(VALUE INTEGER: n);
    BEGIN
        IF n <= 1 THEN ANSWER 1
        ELSE ANSWER n * factorial(n - 1)
    END;

    PROCEDURE initialize;
    BEGIN
        count := 0;
        total := 0
    END;

start:
    initialize;
    FOR count := 1 STEP 1 UNTIL 100 DO
    BEGIN
        readings[count] := square(count);
        total := total + readings[count]
    END;

process:
    temperature := FLOATING(total) / 100.0;

finish:
    COMMENT Done;
END
'''

    parser = CORAL66Parser()
    parser.parse(test_code)

    print("=" * 60)
    print("CORAL 66 SEMANTIC PARSER TEST")
    print("=" * 60)
    print()

    print("SYMBOLS FOUND:")
    print("-" * 40)
    for name, sym in sorted(parser.symbols.items()):
        print(f"  {sym.name:20} {sym.kind.value:12} {sym.data_type}")
    print()

    print("COMPLETIONS (first 10):")
    print("-" * 40)
    completions = parser.get_completions(0, 0)
    for c in completions[:10]:
        print(f"  {c['label']:20} {c['kind']:12} {c['detail']}")
    print()

    print("DOCUMENT SYMBOLS:")
    print("-" * 40)
    for sym in parser.get_document_symbols():
        print(f"  Line {sym['line']:3}: {sym['name']:20} ({sym['kind']})")


if __name__ == '__main__':
    main()
