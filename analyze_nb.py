
import json

def read_cells(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    for i in range(13, min(51, len(nb['cells']))):
        cell = nb['cells'][i]
        print(f"=== Cell {i} ({cell['cell_type']}) ===")
        print("".join(cell['source']).strip())
        print("=" * 30)

read_cells(r'C:\Users\adria\Downloads\TC2_Salinas_Apaza_Perez_Marcos_20231724_20230487_20212237_20221214.ipynb')
