from pathlib import Path
import streamlit as st
import pandas as pd
import os

# paths 
HERE = Path(__file__).resolve().parent 
ROOT = HERE.parent
INPUT_DIR = ROOT / "input"
HELP_DIR = ROOT / "helps"

# input folder backup - not used
source_files = INPUT_DIR
files = sorted(f for f in os.listdir(source_files) if f.endswith((".txt", ".tsv")))

# separator resolver
def resolve_separator(choice: str):
    delim_map = {
        "Tab (\\t)": "\t",
        "Čárka (,)": ",",
        "Středník (;)": ";",
        "Whitespace": r"\s+",
    }
    return None if choice == "Auto" else delim_map[choice]

# data loader
def load_data(file_path: Path, sep: str | None = None) -> pd.DataFrame:
    if sep is None:
        return pd.read_csv(file_path, engine="python")
    else:
        return pd.read_csv(file_path, engine="python", sep=sep)

# tables
st.set_page_config(layout="wide")

st.title("Filtr vybraných genů")

st.sidebar.header("Seznam genů")

st.empty()

# sidebar - text area, button, warnings
with st.sidebar:
    list_genes = st.text_area("Pod sebe vypiš vybrané geny", key="genes_input", height=400)
    if st.button("Použít vybrané geny", type="primary"):
        st.session_state["genes_confirmed"] = st.session_state["genes_input"]
    warn_box = st.empty()

# input with confirmed genes, parse to set, dataframe
genes_text = st.session_state.get("genes_confirmed", "")
genes_to_keep = {g.strip() for g in genes_text.splitlines() if g.strip()}
#print(f"Parsed genes to keep: {genes_to_keep}")
df_genes_to_keep = pd.DataFrame(genes_to_keep, columns=["Gene"])

# check against reference list - unique hg19 and hg38 genes, warnings
df_unique_genes = pd.read_csv(ROOT / "unique_hg19_hg38.txt", sep="\t", header=None)
#print(df_unique_genes.head())
col1 = df_unique_genes[0].astype(str).str.strip()
col2 = df_genes_to_keep["Gene"].astype(str).str.strip()
notInHG = set(col2) - set(col1)
if list_genes.strip():
    if notInHG:
        warn_box.warning(f"Tyto geny nejsou v referenčním seznamu hg37 a hg38: \n\n{', '.join(sorted(notInHG))}")
    else:
        warn_box.success("Všechny zadané geny jsou v referenčním seznamu hg37 a hg38.")

# upload - txt or tsv files, multiple
uploaded_files = st.file_uploader(
    "Nahraj txt soubor se svými daty", accept_multiple_files=True, type=["txt", "tsv"], width="stretch"
)

# main - process each uploaded file
for uploaded_file in uploaded_files:

    # read data
    df_data = pd.read_csv(uploaded_file, engine="python", sep="\t")

    # original index
    df_data["_orig"] = range(len(df_data))

    st.subheader(f"Data: {uploaded_file.name}")
    
    # columns and index
    cols = df_data.columns.tolist()
    #print(cols)
    cols_index = {col: idx for idx, col in enumerate(cols)}

    # genes column processing, replace ; with ;, parse input genes
    genes_to_keep = {g.strip() for g in list_genes.splitlines() if g.strip()}
    col = df_data["Gene.refGeneWithVer"].astype(str)
    gene_col = df_data["Gene.refGeneWithVer"].str.replace(r"\x3b", ";", regex=False)
    #print(gene_col.unique())
    df_data["Gene.refGeneWithVer"] = gene_col
    #print(df_data["Gene.refGeneWithVer"].unique())
    st.dataframe(df_data)
    
    # explode genes - split ;, explode, strip
    exploded = (
        df_data.assign(_gene=gene_col.str.split(";"))
        .explode("_gene")
    )
    exploded["_gene"] = exploded["_gene"].str.strip()

    # filter - keep only selected genes, get original rows
    filtered_df = exploded[exploded["_gene"].isin(genes_to_keep)]
    out_original = df_data.loc[filtered_df.index.unique()]

    # final sort and drop helper column
    filtered_df = out_original.sort_values("_orig").drop(columns="_orig")

    st.subheader(f"Filtrovaná data: {uploaded_file.name}")
    st.dataframe(filtered_df)
    
    # prepare for download
    txt_bytes = filtered_df.to_csv(sep="\t", index=False, header=True).encode("utf-8")
    
    # download
    st.download_button(
        label="Stáhnout",
        data=txt_bytes,
        file_name=f"filtered_{uploaded_file.name}",
        mime="text/plain",
        icon=":material/download:",
        type="primary"
    )

# snow effect
#st.snow()