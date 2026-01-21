Aplikace vytvořená pro vyfiltrování řádků s požadovanými geny z uživatelova nahraného souboru

Jedná se o desktopovou Streamlit aplikaci, která umožňuje:
1) vložit seznam genů
2) nahrát jeden nebo více TSV/TXT souborů s variantami
3) vyfiltrovat řádky, kde se ve sloupci `Gene.refGeneWithVer` nachází alespoň jeden z vybraných genů
4) stáhnout zpět vyfiltrovaný soubor

Když jeden řádek obsahuje více genů (oddělených `;`), vyfiltruje celý původní řádek, pokud se v něm vyskytuje kterýkoli z cílových genů.

---

## Co aplikace dělá (logika)

### 1) Vstup: seznam genů
- V levém panelu zadá uživatel seznam hledaných genů (pod sebe).
- Klikne na **Použít vybrané geny**.
- Aplikace si seznam uloží do `st.session_state` (aby se neztratil při rerunu).

### 2) Kontrola proti referenčnímu seznamu
- Aplikace načte geny z referencí hg19 a hg38
- Porovná zadané geny s referenčním seznamem a zobrazí:
  - **warning**, pokud některé geny v referenci nejsou
  - **success**, pokud jsou všechny

### 3) Nahrání dat
- Je možné nahrát jeden nebo více souborů `.txt` / `.tsv`.
- Aplikace je načítá jako tabulku se separátorem tab (`\t`) pomocí `pandas.read_csv`.

### 4) Filtrace podle genů
- Pracuje se sloupcem `Gene.refGeneWithVer`.
- Opraví se případné kódování středníku `\x3b` -> `;`.
- Řádky se „rozbalí“ tak, že se hodnota ve sloupci rozdělí podle `;`:
  - vznikne pomocný sloupec `_gene`,
  - každý gen z původní buňky je samostatný řádek (explode).
- Vybere se podmnožina, kde `_gene` je v seznamu zadaných genů.
- Proběhne group do původního stavu.
- Výsledná tabulka má zachované původní pořadí řádků.

### 5) Výstup
- Zobrazí se:
  - původní data (tabulka)
  - filtrovaná data (tabulka)
- a nabídne se stažení TSV/TXT

---

## Požadavky

- Python 3.10+
- Balíčky:
  - `streamlit`
  - `pandas`

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Spuštění

- Exom_genes.bat - Windows
- Exom_genes_filter.desktop - Linux

<br>

🍬 2026 · [@AnnBeny](https://github.com/AnnBeny)

![app](https://img.shields.io/badge/app-Streamlit-blue?style=for-the-badge)
![domain](https://img.shields.io/badge/domain-bioinformatics-6A5ACD?style=for-the-badge)
![python](https://img.shields.io/badge/python-3.10+-blue?style=for-the-badge)
