# Implementace úlohy v2

Úkolem bylo vypracovat síťovou (webovou) mini aplikaci, která umožňuje získání informací o mapě na níž se vyskytují 2 entity. Jedna autonomní, druhá uživatelsky ovládáná. Tato implementace úlohy zahrnuje použítí technologie websocket.

## Instalace

Kód běží na nejnovější verzi `pythonu 3.11.4`, je tedy potřeba podle operačního systému nainstalovat příslušnou verzi.
Dále se používá knihovna [websockets](https://websockets.readthedocs.io/en/stable/) a je tedy potřeba ji také nainstalovat pomocí package manažeru:

```bash
pip install websockets
```

## Spuštění

Server je potřeba spustit. Běží na `localhost` a na portu `5002`. Spuštění provedeme v příslušné složce s projektem pomocí příkazu

```bash
python server.py
```

Nic není potřeba měnit či server pouštět s nějakou konfigurací. Server disponuje implicitní konfigurací v kódu.

## Testování

Ve složce s úlohou se nachází i soubor `client.py`, pomocí kterého lze provést základní testování funkčnosti serveru. Kód v klientu lze upravovat dle libosti. Testuje pouze základní funkcionalitu včetně nevalidních vstupů.
