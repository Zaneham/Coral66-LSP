# CORAL 66 Language Support for Visual Studio Code

[![VS Code Marketplace](https://img.shields.io/visual-studio-marketplace/v/ZaneHambly.coral66-lsp?label=VS%20Code%20Marketplace)](https://marketplace.visualstudio.com/items?itemName=ZaneHambly.coral66-lsp)

Language Server Protocol (LSP) implementation for **CORAL 66** (Computer On-line Real-time Applications Language), the programming language that has been flying British aircraft and sailing Royal Navy vessels since 1966.

The Americans had JOVIAL. We had CORAL. They started in 1959. We started in 1964. They'd say they were first. We'd say we did it properly.

## What is CORAL 66?

CORAL 66 was developed at the Royal Radar Establishment in Malvern, Worcestershire. If you've ever wondered what British defence scientists did between tea breaks in the 1960s, the answer is: they invented a programming language for real-time systems and then wrote it up with Crown Copyright.

The language became the inter-service standard for British military programming. When the Ministry of Defence needed software for aircraft, ships, tanks, or missile systems, CORAL 66 was the answer. It was also adopted by the civilian control and automation industry, because if it's good enough for a Tornado, it's good enough for a power station.

### Systems Running CORAL 66

| Domain | Systems |
|--------|---------|
| **Aircraft** | Tornado GR1/GR4 flight systems, Nimrod, Harrier avionics |
| **Royal Navy** | Submarine control systems, surface vessel combat systems, sonar processing |
| **Army** | Battlefield communication systems, Rapier missile system |
| **Industrial** | Nuclear power station monitoring, process control, railway signalling |

The Tornado entered service in 1979 and is still flying today. The CORAL 66 code went through the Gulf War, Kosovo, Afghanistan, Iraq, Libya, and Syria. It works in the desert. It works in the cold. It presumably works in the drizzle, because it's British.

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
  - PROCEDURE and RECURSIVE declarations
  - SWITCH jump tables
  - OVERLAY storage mapping
  - ABSOLUTE memory addressing (for when you need to talk to hardware)

## Installation

1. Install the extension from the VS Code Marketplace
2. Ensure Python 3.8+ is installed and available in PATH
3. Open any `.cor`, `.crl`, or `.coral` file
4. Your Tornado flight system now has syntax highlighting

## File Extensions

| Extension | Description |
|-----------|-------------|
| `.cor`    | CORAL 66 source file |
| `.crl`    | CORAL 66 source file (alternate) |
| `.coral`  | CORAL 66 source file (for the unabbreviated) |

## Language Overview

CORAL 66 is based on ALGOL 60, with practical additions from JOVIAL and FORTRAN. The committee that designed it understood that real-time systems need to talk to hardware, handle interrupts, and manage memory directly. They also understood that the resulting code would need to be maintained for decades by engineers who hadn't been born when it was written.

```coral66
COMMENT This is a comment in CORAL 66;
COMMENT It ends with a semicolon like everything else;
COMMENT The MOD insisted on readable code;

BEGIN
    INTEGER count, total := 0;
    FLOATING temperature;
    FIXED(16, 8) velocity;  COMMENT 16 bits total, 8 fractional;

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

    COMMENT Recursion was considered modern in 1966;
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

The `ANSWER` keyword instead of `RETURN` is a CORAL quirk. The committee felt it was clearer. They may have been right.

### Key Syntax Elements

- **Comments:** `COMMENT text;` (verbose but unambiguous)
- **Assignment:** `:=` (ALGOL heritage)
- **Statement terminator:** `;` (semicolon, naturally)
- **Blocks:** `BEGIN ... END`
- **Type specifiers:**
  - `INTEGER` for whole numbers
  - `FLOATING` for floating-point (when you trust the hardware)
  - `FIXED(totalbits, fractionbits)` for fixed-point (when you don't)
  - `UNSIGNED(totalbits)` for unsigned values
- **Word-logic operators:** `AND`, `OR`, `DIFFER`, `UNION`, `MASK`
- **Parameter modes:** `VALUE` (copy), `LOCATION` (reference)
- **Communicators:** `COMMON`, `LIBRARY`, `EXTERNAL`, `ABSOLUTE`

The `ABSOLUTE` communicator lets you place variables at specific memory addresses. This is how you talk to hardware registers. It's also how you create bugs that take three weeks to find, but the MOD presumably had procedures for that.

## Documentation Sources

This extension was developed using official UK Government documentation:

1. **Official Definition of CORAL 66** (HMSO 1970, reprinted 1974)
   - Crown Copyright, ISBN 0 11 470221 7
   - Her Majesty's Stationery Office
   - The definitive reference, written with the precision you'd expect from people who also wrote specifications for battleships

2. **XGC CORAL 66 Language Reference Manual**
   - XGC Software, based on the HMSO definition
   - For those who wanted the specification without the Crown Copyright notice on every page

3. **British Standard BS 5905**
   - Specification for Computer Programming Language CORAL 66
   - Because of course there's a British Standard

## Configuration

| Setting | Description | Default |
|---------|-------------|---------|
| `coral66.pythonPath` | Path to Python interpreter | `python` |
| `coral66.serverPath` | Path to LSP server script | (bundled) |
| `coral66.trace.server` | Trace level for debugging | `off` |

## Requirements

- Visual Studio Code 1.75.0 or later
- Python 3.8 or later
- Optional: an appreciation for understated British engineering

## Known Limitations

- The parser handles core CORAL 66 constructs but may not cover all implementation-specific extensions
- CODE statements (embedded assembly) are recognised but not parsed
- Some advanced overlay patterns may not be fully supported
- Cannot actually fly a Tornado (this is a syntax highlighter, not a flight computer)

## Why This Matters

The Tornado is scheduled to retire from RAF service in 2025. But CORAL 66 code runs in other systems too: Royal Navy vessels, industrial control systems, railway signalling. The language isn't going anywhere.

The engineers who wrote this code are retiring. The documentation lives in filing cabinets in Malvern, in MoD archives, in boxes that haven't been opened since the Cold War ended. Someone still needs to maintain this code, and they shouldn't have to do it with ed.

## Licence

Copyright 2025 Zane Hambly

Licensed under the Apache Licence, Version 2.0. See [LICENSE](LICENSE) for details.

Crown Copyright on the original language specification remains with the Crown, naturally.

## Contributing

Contributions are welcome. Particularly:
- Syntax patterns from real CORAL 66 code
- Corrections from people who actually programmed Tornado avionics
- War stories from the Royal Radar Establishment

Pull requests should be properly formatted. The MOD had standards. We should too.

## Related Projects

If you've made it this far into a language specification published by Her Majesty's Stationery Office, you might appreciate:

- **[JOVIAL J73 LSP](https://github.com/Zaneham/jovial-lsp)** - The American equivalent. Louder, more confident, used in rather more aircraft. F-15s, B-52s, AWACS. They started in 1959; we started in 1964. They'd say they were first. We'd say we did it properly.

- **[CMS-2 LSP](https://github.com/Zaneham/cms2-lsp)** - The US Navy's tactical language. Terminates statements with dollar signs, which tells you everything you need to know, really. Powers Aegis cruisers. We had Sea Dart.

- **[HAL/S LSP](https://github.com/Zaneham/hals-lsp)** - NASA's Space Shuttle language. The Americans went to the Moon with this sort of thing. We went to the Falklands with CORAL. Different priorities.

- **[CHILL LSP](https://github.com/Zaneham/chill-lsp)** - The ITU's telecommunications language. For telephone switches rather than aircraft. International committee design. Very thorough. Very slow to standardise.

- **[Minuteman Guidance Computer Emulator](https://github.com/Zaneham/minuteman-emu)** - An emulator for the computers in American nuclear missiles. We had Polaris, then Trident. Same general idea, different accent.

## Contact

Queries? Corrections? Strongly-worded letters about the correct interpretation of the HMSO specification?

zanehambly@gmail.com

Correspondence answered promptly, weather permitting. Will discuss CORAL over tea. Can explain why your avionics code does that thing it does. Has opinions about GOTO but keeps them appropriately reserved.

## Acknowledgements

- Royal Radar Establishment (RRE), Malvern
- UK Ministry of Defence
- Her Majesty's Stationery Office (HMSO)
- XGC Software for maintaining online documentation
- The engineers who wrote code for Tornado, knowing it would fly in combat
- Everyone who maintained that code through five wars and forty years
