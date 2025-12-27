# CORAL 66 Language Support for Visual Studio Code

Language Server Protocol (LSP) implementation for **CORAL 66** (Computer On-line Real-time Applications Language), the UK Ministry of Defence standard real-time programming language.

## About CORAL 66

CORAL 66 was developed in 1964-1966 at the Royal Radar Establishment (RRE), Malvern, UK. The language became the inter-service standard for British military programming and was widely adopted in the control and automation industry.

CORAL 66 has been used in:

- **Tornado aircraft** flight control systems
- **Royal Navy** submarine and surface vessel systems
- **British Army** battlefield systems
- **Industrial control** and automation
- **Nuclear power station** monitoring

The language is based on ALGOL 60 with features from JOVIAL and FORTRAN, designed specifically for real-time computing and embedded systems.

## Features

- **Syntax highlighting** for CORAL 66 constructs
- **Code completion** for keywords, variables, procedures, arrays
- **Hover information** with type details
- **Go to definition** for symbols
- **Find references** across the document
- **Document outline** showing programme structure
- **Support for all CORAL 66 constructs:**
  - Number declarations (INTEGER, FLOATING, FIXED)
  - ARRAY declarations with dimensions
  - TABLE definitions with elements
  - PROCEDURE/RECURSIVE declarations
  - SWITCH jump tables
  - OVERLAY storage mapping

## Installation

1. Install the extension from the VS Code Marketplace
2. Ensure Python 3.8+ is installed and available in PATH
3. Open any `.cor`, `.crl`, or `.coral` file

## File Extensions

| Extension | Description |
|-----------|-------------|
| `.cor`    | CORAL 66 source file |
| `.crl`    | CORAL 66 source file (alternate) |
| `.coral`  | CORAL 66 source file (full) |

## Language Overview

CORAL 66 uses an ALGOL-like syntax with uppercase keywords:

```coral66
COMMENT This is a comment;

BEGIN
    INTEGER count, total := 0;
    FLOATING temperature;
    FIXED(16, 8) velocity;

    FLOATING ARRAY readings[0:99];

    TABLE sensors[4, 100][
        id INTEGER 0;
        value FIXED(16, 8) 1
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

start:
    count := 0;
    FOR count := 1 STEP 1 UNTIL 100 DO
        total := total + readings[count];

process:
    temperature := FLOATING(total) / 100.0;
    IF temperature > 50.0 THEN GOTO finish;
    GOTO start;

finish:
    COMMENT Done;
END
```

### Key Syntax Elements

- **Comments:** `COMMENT text;`
- **Assignment:** `:=`
- **Statement terminator:** `;` (semicolon)
- **Blocks:** `BEGIN ... END`
- **Type specifiers:**
  - `INTEGER` - Integer values
  - `FLOATING` - Floating-point values
  - `FIXED(totalbits, fractionbits)` - Fixed-point with scaling
  - `UNSIGNED(totalbits)` - Unsigned values
- **Word-logic operators:** `AND`, `OR`, `DIFFER`, `UNION`, `MASK`
- **Parameter modes:** `VALUE`, `LOCATION`
- **Communicators:** `COMMON`, `LIBRARY`, `EXTERNAL`, `ABSOLUTE`

## Documentation Sources

This extension was developed using official UK Government documentation:

1. **Official Definition of CORAL 66** (HMSO 1970, reprinted 1974)
   - Crown Copyright, ISBN 0 11 470221 7
   - Her Majesty's Stationery Office

2. **XGC CORAL 66 Language Reference Manual**
   - XGC Software, based on the HMSO definition

3. **British Standard BS 5905**
   - Specification for Computer Programming Language CORAL 66

## Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `coral66.pythonPath` | Path to Python interpreter | `python` |
| `coral66.serverPath` | Path to LSP server script | (bundled) |
| `coral66.trace.server` | Trace level for debugging | `off` |

## Requirements

- Visual Studio Code 1.75.0 or later
- Python 3.8 or later

## Known Limitations

- The parser handles core CORAL 66 constructs but may not cover all implementation-specific extensions
- CODE statements (embedded assembly) are recognised but not parsed
- Some advanced overlay patterns may not be fully supported

## Licence

Copyright 2025 Zane Hambly

Licensed under the Apache Licence, Version 2.0. See [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please open an issue or pull request on GitHub.

## Acknowledgements

- Royal Radar Establishment (RRE), Malvern
- UK Ministry of Defence
- Her Majesty's Stationery Office (HMSO)
- XGC Software for maintaining online documentation
- Edinburgh Computer History project
