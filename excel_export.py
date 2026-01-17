from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from flask import current_app
import os
from datetime import datetime

def export_relatorios_to_excel(relatorios_data):
    """
    Exporta relatórios para arquivo Excel
    
    Args:
        relatorios_data: Lista de dicionários com dados dos relatórios
    
    Returns:
        str: Caminho do arquivo Excel gerado
    """
    wb = Workbook()
    ws = wb.active
    ws.title = "Relatórios"
    
    # Estilos
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="e6007e", end_color="e6007e", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center")
    
    # Cabeçalhos expandidos
    headers = [
        "ID", "Código", "Coleção", "Descrição", "Temporada", "Ano",
        "Status Geral", "Referências", "Data Criação", "Última Atualização"
    ]
    for col_num, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = header
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment

    # Dados
    for row_num, relatorio in enumerate(relatorios_data, 2):
        ws.cell(row=row_num, column=1, value=relatorio.get('id', ''))
        ws.cell(row=row_num, column=2, value=relatorio.get('codigo', ''))
        ws.cell(row=row_num, column=3, value=relatorio.get('colecao', ''))
        ws.cell(row=row_num, column=4, value=relatorio.get('descricao_geral', ''))
        ws.cell(row=row_num, column=5, value=relatorio.get('temporada', ''))
        ws.cell(row=row_num, column=6, value=relatorio.get('ano', ''))
        ws.cell(row=row_num, column=7, value=relatorio.get('status_geral', ''))
        ws.cell(row=row_num, column=8, value=relatorio.get('num_referencias', 0))
        ws.cell(row=row_num, column=9, value=relatorio.get('data_criacao', ''))
        ws.cell(row=row_num, column=10, value=relatorio.get('data_atualizacao', ''))
    
    # Ajustar largura das colunas
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column_letter].width = adjusted_width
    
    # Salvar arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"relatorios_export_{timestamp}.xlsx"
    filepath = os.path.join(current_app.config['PDF_FOLDER'], filename)
    wb.save(filepath)
    
    return filename

def export_detalhes_to_excel(relatorio, referencias):
    """
    Exporta detalhes completos de um relatório para Excel
    
    Args:
        relatorio: Dados do relatório
        referencias: Lista de referências com provas
    
    Returns:
        str: Caminho do arquivo Excel gerado
    """
    wb = Workbook()
    
    # Aba 1: Informações Gerais
    ws_geral = wb.active
    ws_geral.title = "Informações Gerais"
    
    ws_geral['A1'] = "Campo"
    ws_geral['B1'] = "Valor"
    ws_geral['A1'].font = Font(bold=True)
    ws_geral['B1'].font = Font(bold=True)
    
    ws_geral['A2'] = "ID"
    ws_geral['B2'] = relatorio['id']
    ws_geral['A3'] = "Coleção"
    ws_geral['B3'] = relatorio.get('colecao', '')
    ws_geral['A4'] = "Descrição"
    ws_geral['B4'] = relatorio.get('descricao_geral', '')
    
    # Aba 2: Referências
    ws_refs = wb.create_sheet("Referências")
    headers_refs = [
        "Referência", "Tipo", "Origem", "Fornecedor", "Contato Fornecedor",
        "Matéria Prima", "Composição", "Gramatura", "Aviamentos", "Observações"
    ]
    for col_num, header in enumerate(headers_refs, 1):
        cell = ws_refs.cell(row=1, column=col_num)
        cell.value = header
        cell.font = Font(bold=True)

    row_num = 2
    for ref in referencias:
        ws_refs.cell(row=row_num, column=1, value=ref.get('numero_ref', ''))
        ws_refs.cell(row=row_num, column=2, value=ref.get('tipo', ''))
        ws_refs.cell(row=row_num, column=3, value=ref.get('origem', ''))
        ws_refs.cell(row=row_num, column=4, value=ref.get('fornecedor', ''))
        ws_refs.cell(row=row_num, column=5, value=ref.get('fornecedor_contato', ''))
        ws_refs.cell(row=row_num, column=6, value=ref.get('materia_prima', ''))
        ws_refs.cell(row=row_num, column=7, value=ref.get('composicao', ''))
        ws_refs.cell(row=row_num, column=8, value=ref.get('gramatura', ''))
        ws_refs.cell(row=row_num, column=9, value=ref.get('aviamentos', ''))
        ws_refs.cell(row=row_num, column=10, value=ref.get('observacoes', ''))
        row_num += 1

    # Aba 3: Provas
    ws_provas = wb.create_sheet("Provas")

    headers_provas = [
        "Referência", "Tipo", "Nº Prova", "Status", "Data Recebimento", "Data Prova",
        "Tamanhos", "Info Medidas", "Time Qualidade", "Time Estilo", "Time Modelagem",
        "Data Lacre", "Nº Lacre", "Informações Adicionais"
    ]
    for col_num, header in enumerate(headers_provas, 1):
        cell = ws_provas.cell(row=1, column=col_num)
        cell.value = header
        cell.font = Font(bold=True)

    row_num = 2
    for ref in referencias:
        for prova in ref.get('provas', []):
            ws_provas.cell(row=row_num, column=1, value=ref.get('numero_ref', ''))
            ws_provas.cell(row=row_num, column=2, value=ref.get('tipo', ''))
            ws_provas.cell(row=row_num, column=3, value=prova.get('numero_prova', ''))
            ws_provas.cell(row=row_num, column=4, value=prova.get('status', ''))
            ws_provas.cell(row=row_num, column=5, value=prova.get('data_recebimento', ''))
            ws_provas.cell(row=row_num, column=6, value=prova.get('data_prova', ''))
            ws_provas.cell(row=row_num, column=7, value=prova.get('tamanhos_recebidos', ''))
            ws_provas.cell(row=row_num, column=8, value=prova.get('info_medidas', ''))
            ws_provas.cell(row=row_num, column=9, value=prova.get('time_qualidade', ''))
            ws_provas.cell(row=row_num, column=10, value=prova.get('time_estilo', ''))
            ws_provas.cell(row=row_num, column=11, value=prova.get('time_modelagem', ''))
            ws_provas.cell(row=row_num, column=12, value=prova.get('data_lacre', ''))
            ws_provas.cell(row=row_num, column=13, value=prova.get('numero_lacre', ''))
            ws_provas.cell(row=row_num, column=14, value=prova.get('info_adicionais', ''))
            row_num += 1
    
    # Ajustar larguras
    for ws in [ws_geral, ws_refs, ws_provas]:
        for column in ws.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws.column_dimensions[column_letter].width = adjusted_width
    
    # Salvar
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"relatorio_{relatorio['id']}_detalhes_{timestamp}.xlsx"
    filepath = os.path.join(current_app.config['PDF_FOLDER'], filename)
    wb.save(filepath)
    
    return filename
