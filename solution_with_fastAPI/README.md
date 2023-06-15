# Implementace úlohy v1

Úkolem bylo vypracovat síťovou (webovou) mini aplikaci, která umožňuje získání informací o mapě na níž se vyskytují 2 entity. Jedna autonomní, druhá uživatelsky ovládáná. Tato implementace úlohy zahrnuje použítí technologie FastAPI a řešení pomocí REST API přístupu.

## Instalace

Kód běží na nejnovější verzi `pythonu 3.11.4`, je tedy potřeba podle operačního systému nainstalovat příslušnou verzi.
Dále se používají knihovny [FastAPI](https://fastapi.tiangolo.com/) a [uvicorn](https://www.uvicorn.org/) je tedy potřeba je nainstalovat pomocí package manažeru:

```bash
pip install fastapi
pip install uvicorn
```

## Spuštění

Server je potřeba spustit. Běží na `http://127.0.0.1` a na portu `8000`. Spuštění provedeme v příslušné složce s projektem pomocí příkazu

```bash
uvicorn main:app --reload
```

Spuštění serveru zde zajišťuje `uvicorn` jenže se stará i ho jeho případný hot-reload. Není tedy potřeba žádné dodatečné nastavování či externí konfigurace.

## Testování a dokumentace

Po spuštění serveru lze na adrese `http://127.0.0.1:8000/docs` automaticky vygenerevanou dokumentaci pomocí nástroje `Swagger`, ta ukazuje všechny dostupné endpointy aplikace a umožňuje na ně odesílat testovací requesty.
