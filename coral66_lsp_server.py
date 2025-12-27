"""
CORAL 66 Language Server Protocol Implementation

Provides LSP support for CORAL 66, the UK Ministry of Defence
standard real-time programming language (HMSO 1970).

Features:
- Syntax highlighting
- Code completion
- Hover information
- Go to definition
- Find references
- Document symbols
"""

import sys
import json
import re
from typing import Dict, List, Any, Optional
from coral66_semantic_parser import CORAL66Parser, SymbolKind


class CORAL66LanguageServer:
    """LSP server for CORAL 66"""

    def __init__(self):
        self.documents: Dict[str, str] = {}
        self.parsers: Dict[str, CORAL66Parser] = {}

    def handle_message(self, message: Dict) -> Optional[Dict]:
        """Handle an incoming JSON-RPC message"""
        method = message.get('method', '')
        params = message.get('params', {})
        msg_id = message.get('id')

        # Route to appropriate handler
        handlers = {
            'initialize': self._handle_initialize,
            'initialized': self._handle_initialized,
            'shutdown': self._handle_shutdown,
            'exit': self._handle_exit,
            'textDocument/didOpen': self._handle_did_open,
            'textDocument/didChange': self._handle_did_change,
            'textDocument/didClose': self._handle_did_close,
            'textDocument/completion': self._handle_completion,
            'textDocument/hover': self._handle_hover,
            'textDocument/definition': self._handle_definition,
            'textDocument/references': self._handle_references,
            'textDocument/documentSymbol': self._handle_document_symbol,
        }

        handler = handlers.get(method)
        if handler:
            result = handler(params)
            if msg_id is not None:
                return {'jsonrpc': '2.0', 'id': msg_id, 'result': result}
        elif msg_id is not None:
            return {
                'jsonrpc': '2.0',
                'id': msg_id,
                'error': {'code': -32601, 'message': f'Method not found: {method}'}
            }

        return None

    def _handle_initialize(self, params: Dict) -> Dict:
        """Handle initialize request"""
        return {
            'capabilities': {
                'textDocumentSync': {
                    'openClose': True,
                    'change': 1,  # Full sync
                    'save': {'includeText': True}
                },
                'completionProvider': {
                    'triggerCharacters': ['.', '[', '('],
                    'resolveProvider': False
                },
                'hoverProvider': True,
                'definitionProvider': True,
                'referencesProvider': True,
                'documentSymbolProvider': True,
            },
            'serverInfo': {
                'name': 'coral66-lsp',
                'version': '1.0.0'
            }
        }

    def _handle_initialized(self, params: Dict) -> None:
        """Handle initialized notification"""
        return None

    def _handle_shutdown(self, params: Dict) -> None:
        """Handle shutdown request"""
        return None

    def _handle_exit(self, params: Dict) -> None:
        """Handle exit notification"""
        sys.exit(0)

    def _handle_did_open(self, params: Dict) -> None:
        """Handle textDocument/didOpen"""
        uri = params['textDocument']['uri']
        text = params['textDocument']['text']
        self._update_document(uri, text)
        return None

    def _handle_did_change(self, params: Dict) -> None:
        """Handle textDocument/didChange"""
        uri = params['textDocument']['uri']
        changes = params.get('contentChanges', [])
        if changes:
            text = changes[0].get('text', '')
            self._update_document(uri, text)
        return None

    def _handle_did_close(self, params: Dict) -> None:
        """Handle textDocument/didClose"""
        uri = params['textDocument']['uri']
        if uri in self.documents:
            del self.documents[uri]
        if uri in self.parsers:
            del self.parsers[uri]
        return None

    def _update_document(self, uri: str, text: str) -> None:
        """Update document and reparse"""
        self.documents[uri] = text
        parser = CORAL66Parser()
        parser.parse(text)
        self.parsers[uri] = parser

    def _handle_completion(self, params: Dict) -> List[Dict]:
        """Handle textDocument/completion"""
        uri = params['textDocument']['uri']
        position = params['position']

        if uri not in self.parsers:
            return []

        parser = self.parsers[uri]
        completions = parser.get_completions(position['line'], position['character'])

        # Convert to LSP format
        lsp_completions = []
        for c in completions:
            kind_map = {
                'keyword': 14,  # Keyword
                'variable': 6,  # Variable
                'array': 6,     # Variable
                'table': 22,    # Struct
                'procedure': 3, # Function
                'function': 3,  # Function
                'switch': 13,   # Enum
                'label': 15,    # Reference
                'parameter': 6, # Variable
                'element': 5,   # Field
            }
            lsp_completions.append({
                'label': c['label'],
                'kind': kind_map.get(c['kind'], 1),
                'detail': c['detail'],
                'documentation': c.get('documentation', '')
            })

        return lsp_completions

    def _handle_hover(self, params: Dict) -> Optional[Dict]:
        """Handle textDocument/hover"""
        uri = params['textDocument']['uri']
        position = params['position']

        if uri not in self.parsers:
            return None

        parser = self.parsers[uri]
        hover = parser.get_hover(position['line'], position['character'])

        if hover:
            return {
                'contents': {
                    'kind': 'markdown',
                    'value': hover['contents']
                }
            }

        return None

    def _handle_definition(self, params: Dict) -> Optional[Dict]:
        """Handle textDocument/definition"""
        uri = params['textDocument']['uri']
        position = params['position']

        if uri not in self.parsers:
            return None

        parser = self.parsers[uri]
        definition = parser.get_definition(position['line'], position['character'])

        if definition:
            return {
                'uri': uri,
                'range': {
                    'start': {'line': definition['line'], 'character': definition['column']},
                    'end': {'line': definition['line'], 'character': definition['column'] + len(definition['name'])}
                }
            }

        return None

    def _handle_references(self, params: Dict) -> List[Dict]:
        """Handle textDocument/references"""
        uri = params['textDocument']['uri']
        position = params['position']

        if uri not in self.parsers:
            return []

        parser = self.parsers[uri]
        refs = parser.get_references_at(position['line'], position['character'])

        lsp_refs = []
        for ref in refs:
            lsp_refs.append({
                'uri': uri,
                'range': {
                    'start': {'line': ref['line'], 'character': ref['column']},
                    'end': {'line': ref['line'], 'character': ref['end_column']}
                }
            })

        return lsp_refs

    def _handle_document_symbol(self, params: Dict) -> List[Dict]:
        """Handle textDocument/documentSymbol"""
        uri = params['textDocument']['uri']

        if uri not in self.parsers:
            return []

        parser = self.parsers[uri]
        symbols = parser.get_document_symbols()

        # Map to LSP SymbolKind
        kind_map = {
            'variable': 13,   # Variable
            'array': 18,      # Array
            'table': 23,      # Struct
            'procedure': 12,  # Function
            'function': 12,   # Function
            'switch': 10,     # Enum
            'label': 15,      # Constant (for labels)
            'element': 8,     # Field
            'parameter': 13,  # Variable
            'overlay': 23,    # Struct
        }

        lsp_symbols = []
        for sym in symbols:
            lsp_symbols.append({
                'name': sym['name'],
                'kind': kind_map.get(sym['kind'], 13),
                'location': {
                    'uri': uri,
                    'range': {
                        'start': {'line': sym['line'], 'character': sym['column']},
                        'end': {'line': sym['line'], 'character': sym['column'] + len(sym['name'])}
                    }
                }
            })

        return lsp_symbols


def main():
    """Main entry point for the LSP server"""
    server = CORAL66LanguageServer()

    while True:
        try:
            # Read Content-Length header
            header = ''
            while True:
                line = sys.stdin.readline()
                if not line:
                    sys.exit(0)
                if line == '\r\n' or line == '\n':
                    break
                header += line

            # Parse content length
            content_length = 0
            for line in header.split('\n'):
                if line.lower().startswith('content-length:'):
                    content_length = int(line.split(':')[1].strip())

            if content_length == 0:
                continue

            # Read content
            content = sys.stdin.read(content_length)
            message = json.loads(content)

            # Handle message
            response = server.handle_message(message)

            # Send response
            if response:
                response_str = json.dumps(response)
                sys.stdout.write(f'Content-Length: {len(response_str)}\r\n\r\n{response_str}')
                sys.stdout.flush()

        except Exception as e:
            sys.stderr.write(f'Error: {e}\n')
            sys.stderr.flush()


if __name__ == '__main__':
    main()
