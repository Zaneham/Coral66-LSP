import * as path from 'path';
import * as vscode from 'vscode';
import {
    LanguageClient,
    LanguageClientOptions,
    ServerOptions,
    TransportKind
} from 'vscode-languageclient/node';

let client: LanguageClient;

export function activate(context: vscode.ExtensionContext) {
    const config = vscode.workspace.getConfiguration('coral66');
    const pythonPath = config.get<string>('pythonPath') || 'python';
    let serverPath = config.get<string>('serverPath') || '';

    // Use bundled server if no custom path specified
    if (!serverPath) {
        serverPath = context.asAbsolutePath('coral66_lsp_server.py');
    }

    const serverOptions: ServerOptions = {
        command: pythonPath,
        args: [serverPath],
        transport: TransportKind.stdio
    };

    const clientOptions: LanguageClientOptions = {
        documentSelector: [{ scheme: 'file', language: 'coral66' }],
        synchronize: {
            fileEvents: vscode.workspace.createFileSystemWatcher('**/*.{cor,crl,coral}')
        }
    };

    client = new LanguageClient(
        'coral66-lsp',
        'CORAL 66 Language Server',
        serverOptions,
        clientOptions
    );

    client.start();
}

export function deactivate(): Thenable<void> | undefined {
    if (!client) {
        return undefined;
    }
    return client.stop();
}
