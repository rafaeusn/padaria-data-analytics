"""Testes automatizados do RA3.

Executam o notebook do zero em uma pasta temporária (sem alterar o repositório)
e conferem a base, as saídas e os resultados do modelo.

Como rodar, na raiz do repositório:
    python -m pytest -v
"""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pandas as pd
import pytest

RAIZ = Path(__file__).resolve().parents[1]
NOTEBOOK = RAIZ / 'RA3_Analise_e_Machine_Learning.ipynb'
PREPARADO = RAIZ / 'data' / 'processed' / 'bakery_sales_preparado.csv'
GRAFICOS = [
    '01_distribuicao_variaveis.png', '02_unidades_por_hora.png', '03_media_por_dia_semana.png',
    '04_media_por_clima.png', '05_festival_boxplot.png', '06_promocoes_margem_unidades.png',
    '07_sobra_perecibilidade.png', '08_ml_observado_previsto.png',
]


@pytest.fixture(scope='session')
def execucao(tmp_path_factory):
    """Copia dados e notebook para uma pasta temporária e executa todas as células."""
    pasta = tmp_path_factory.mktemp('ra3')
    shutil.copytree(RAIZ / 'data', pasta / 'data')
    shutil.copy(NOTEBOOK, pasta / NOTEBOOK.name)
    # Kernel temporário que aponta para o mesmo Python do pytest: evita que o Jupyter
    # use outro "python3" instalado na máquina, sem as bibliotecas do requirements.txt.
    kernel = pasta / 'jupyter' / 'kernels' / 'ra3-pytest'
    kernel.mkdir(parents=True)
    (kernel / 'kernel.json').write_text(json.dumps({
        'argv': [sys.executable, '-m', 'ipykernel_launcher', '-f', '{connection_file}'],
        'display_name': 'RA3 (pytest)', 'language': 'python'}), encoding='utf-8')
    ambiente = {**os.environ, 'JUPYTER_PATH': str(pasta / 'jupyter')}
    comando = [sys.executable, '-m', 'jupyter', 'nbconvert', '--to', 'notebook', '--execute',
               '--ExecutePreprocessor.kernel_name=ra3-pytest', '--ExecutePreprocessor.timeout=600',
               '--output', 'executado.ipynb', NOTEBOOK.name]
    resultado = subprocess.run(comando, cwd=pasta, capture_output=True, text=True, env=ambiente)
    assert resultado.returncode == 0, 'O notebook falhou ao executar:\n' + resultado.stderr[-4000:]
    return pasta


def textos_de_saida(pasta):
    nb = json.loads((pasta / 'executado.ipynb').read_text(encoding='utf-8'))
    saidas = [o for c in nb['cells'] if c['cell_type'] == 'code' for o in c.get('outputs', [])]
    return nb, saidas


def numero(texto):
    return float(texto.replace('.', '').replace(',', '.'))


def test_base_preparada_do_ra1():
    df = pd.read_csv(PREPARADO, encoding='utf-8-sig')
    assert df.shape == (19321, 42)
    assert not df.duplicated(['Order_ID', 'Product']).any()
    assert df.isna().sum().sum() == 0
    assert df['Store_ID'].nunique() == 3 and df['Category'].nunique() == 7


def test_notebook_executa_sem_erros(execucao):
    _, saidas = textos_de_saida(execucao)
    erros = [o for o in saidas if o.get('output_type') == 'error']
    assert not erros, f"Células com erro: {[e['ename'] + ': ' + e['evalue'] for e in erros]}"


def test_testes_internos_do_notebook_passaram(execucao):
    _, saidas = textos_de_saida(execucao)
    texto = ''.join(''.join(o.get('text', '')) for o in saidas if o.get('output_type') == 'stream')
    assert 'Todos os 11 testes passaram.' in texto


def test_oito_graficos_gerados(execucao):
    pasta = execucao / 'outputs' / 'graficos'
    for nome in GRAFICOS:
        arquivo = pasta / nome
        assert arquivo.is_file(), f'Gráfico ausente: {nome}'
        assert arquivo.stat().st_size > 10_000, f'Gráfico vazio ou corrompido: {nome}'


def test_relatorio_markdown_completo(execucao):
    md = (execucao / 'outputs' / 'ra3_resultados.md').read_text(encoding='utf-8')
    for secao in ['## Origem e representatividade', '## Estatística descritiva',
                  '## Visualizações e interpretações', '## Machine Learning supervisionado',
                  '## Limitações e conclusão']:
        assert secao in md, f'Seção ausente no relatório: {secao}'
    for nome in GRAFICOS:
        assert nome in md


def test_modelo_supera_referencia(execucao):
    md = (execucao / 'outputs' / 'ra3_resultados.md').read_text(encoding='utf-8')
    mae_modelo, mae_ref = map(numero, re.search(r'\| MAE \(unidades\) \| ([\d.,]+) \| ([\d.,]+) \|', md).groups())
    r2_modelo, _ = map(numero, re.search(r'\| R² \| (-?[\d.,]+) \| (-?[\d.,]+) \|', md).groups())
    assert mae_modelo < mae_ref, 'O Random Forest deveria ter MAE menor que a referência.'
    assert r2_modelo > 0
    # Valores documentados no relatório (random_state=42); tolerância para versões diferentes do scikit-learn.
    assert mae_modelo == pytest.approx(2.526, abs=0.1)
    assert mae_ref == pytest.approx(2.801, abs=0.001)
