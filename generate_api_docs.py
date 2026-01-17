#!/usr/bin/env python3
"""
Script para gerar automaticamente a documentação da API
Baseado nas rotas reais do Flask app
"""

from app import app
from datetime import datetime
import inspect

def get_route_docstring(endpoint):
    """Extrai docstring da função da rota"""
    if endpoint in app.view_functions:
        func = app.view_functions[endpoint]
        return inspect.getdoc(func) or "Sem documentação disponível"
    return "Sem documentação disponível"

def generate_api_documentation():
    """Gera documentação completa da API em Markdown"""

    output = []

    # Header
    output.append("# 🔌 API Reference (Auto-Generated)")
    output.append("")
    output.append(f"**Versão:** 2.1")
    output.append(f"**Última Atualização:** {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    output.append(f"**Gerado Automaticamente:** Sim")
    output.append("")
    output.append("---")
    output.append("")

    # Índice
    output.append("## 📑 Índice")
    output.append("")
    output.append("- [Autenticação](#autenticação)")
    output.append("- [Dashboard e Relatórios](#dashboard-e-relatórios)")
    output.append("- [Referências e Provas](#referências-e-provas)")
    output.append("- [Analytics](#analytics)")
    output.append("- [Exportação](#exportação)")
    output.append("- [Administração](#administração)")
    output.append("- [Auditoria](#auditoria)")
    output.append("- [Arquivos Estáticos](#arquivos-estáticos)")
    output.append("")
    output.append("---")
    output.append("")

    # Organizar rotas por blueprint
    routes_by_blueprint = {}

    with app.test_request_context():
        for rule in sorted(app.url_map.iter_rules(), key=lambda r: str(r)):
            # Pular rotas internas
            if rule.endpoint in ['static', '_debug_toolbar.static']:
                continue

            methods = sorted([m for m in rule.methods if m not in ['HEAD', 'OPTIONS']])
            endpoint = rule.endpoint
            blueprint = endpoint.split('.')[0] if '.' in endpoint else 'app'

            if blueprint not in routes_by_blueprint:
                routes_by_blueprint[blueprint] = []

            routes_by_blueprint[blueprint].append({
                'url': str(rule),
                'methods': methods,
                'endpoint': endpoint,
                'function': app.view_functions.get(endpoint).__name__ if endpoint in app.view_functions else 'N/A',
                'doc': get_route_docstring(endpoint)
            })

    # Mapear blueprints para seções
    blueprint_sections = {
        'auth': ('Autenticação', '🔐'),
        'app': ('Dashboard e Relatórios', '📊'),
        'admin': ('Administração', '👨‍💼'),
        'audit': ('Auditoria', '📜')
    }

    # Gerar documentação por seção
    for blueprint, (section_name, emoji) in blueprint_sections.items():
        if blueprint not in routes_by_blueprint:
            continue

        output.append(f"## {emoji} {section_name}")
        output.append("")

        for route in routes_by_blueprint[blueprint]:
            methods_str = ', '.join(route['methods'])

            # Header da rota
            output.append(f"### {methods_str} {route['url']}")
            output.append("")

            # Documentação da função
            output.append(f"**Função:** `{route['function']}`")
            output.append("")

            if route['doc'] != "Sem documentação disponível":
                output.append(f"**Descrição:**")
                output.append(route['doc'])
                output.append("")

            # Parâmetros da URL
            if '<' in route['url']:
                output.append("**Parâmetros da URL:**")
                import re
                params = re.findall(r'<([^>]+)>', route['url'])
                for param in params:
                    parts = param.split(':')
                    if len(parts) == 2:
                        param_type, param_name = parts
                        output.append(f"- `{param_name}` ({param_type})")
                    else:
                        output.append(f"- `{param}` (string)")
                output.append("")

            # Exemplo de requisição
            method = route['methods'][0] if route['methods'] else 'GET'
            example_url = route['url'].replace('<int:', '{').replace('<string:', '{').replace('<path:', '{').replace('>', '}')
            output.append(f"**Exemplo de Requisição:**")
            output.append(f"```http")
            output.append(f"{method} {example_url} HTTP/1.1")
            output.append(f"Host: localhost:5000")

            if method in ['POST', 'PUT', 'PATCH']:
                output.append(f"Content-Type: application/x-www-form-urlencoded")
                output.append("")
                output.append("# Parâmetros do formulário aqui")

            output.append(f"```")
            output.append("")

            output.append("---")
            output.append("")

    # Notas importantes
    output.append("## 📝 Notas Importantes")
    output.append("")
    output.append("### Estrutura de Dados")
    output.append("")
    output.append("**Hierarquia das Entidades:**")
    output.append("```")
    output.append("Relatorio (relatórios)")
    output.append("  └── Referencia (referencias)")
    output.append("      └── ProvaModelagem (provas)")
    output.append("          └── FotoProva (fotos)")
    output.append("```")
    output.append("")
    output.append("### Feedbacks")
    output.append("")
    output.append("⚠️ **IMPORTANTE:** Feedbacks (Qualidade, Estilo, Modelagem) são **COLUNAS** na tabela `provas`, não entidades separadas.")
    output.append("")
    output.append("Para atualizar feedbacks, use:")
    output.append("- `POST /relatorio/<int:id>/editar` - Edita o relatório e suas provas")
    output.append("- `POST /prova/atualizar_status` - Atualiza status e feedbacks de uma prova específica")
    output.append("")
    output.append("Campos de feedback na tabela `provas`:")
    output.append("```python")
    output.append("# Qualidade")
    output.append("time_qualidade: str")
    output.append("checklist_qualidade: str  # CSV")
    output.append("comentarios_qualidade: str")
    output.append("obs_qualidade: str")
    output.append("")
    output.append("# Estilo")
    output.append("time_estilo: str")
    output.append("checklist_estilo: str  # CSV")
    output.append("comentarios_estilo: str")
    output.append("obs_estilo: str")
    output.append("")
    output.append("# Modelagem")
    output.append("time_modelagem: str")
    output.append("checklist_modelagem: str  # CSV")
    output.append("comentarios_modelagem: str")
    output.append("obs_modelagem: str")
    output.append("```")
    output.append("")

    # Auditoria
    output.append("### Sistema de Auditoria")
    output.append("")
    output.append("⚠️ **STATUS:** O blueprint de auditoria existe no código mas está **DESABILITADO** em `app.py`.")
    output.append("")
    output.append("Para habilitar:")
    output.append("```python")
    output.append("# app.py - descomentar:")
    output.append("from audit_bp import audit_bp")
    output.append("app.register_blueprint(audit_bp, url_prefix='/auditoria')")
    output.append("```")
    output.append("")
    output.append("Rotas disponíveis quando habilitado:")
    output.append("- `GET /auditoria/` - Lista de logs")
    output.append("- `GET /auditoria/detalhes/<int:log_id>` - Detalhes de um log")
    output.append("- `GET /auditoria/timeline/<string:entidade>/<int:entidade_id>` - Timeline de uma entidade")
    output.append("- `GET /auditoria/usuario/<int:usuario_id>` - Logs de um usuário")
    output.append("- `GET /auditoria/exportar/csv` - Exportar logs para CSV")
    output.append("- `GET /auditoria/estatisticas` - Estatísticas de auditoria")
    output.append("")

    # Footer
    output.append("---")
    output.append("")
    output.append("## 📞 Suporte")
    output.append("")
    output.append("**Desenvolvedor:** Nicolas Matsuda")
    output.append("**Email:** nicolas.matsuda@grupounico.com")
    output.append("**Projeto:** Sistema de Gestão de Provas de Modelagem - Puket")
    output.append("")
    output.append("---")
    output.append("")
    output.append("**[⬅ Voltar ao Índice](../INDEX.md)**")
    output.append("")

    return '\n'.join(output)

if __name__ == '__main__':
    print("Gerando documentação da API...")

    doc = generate_api_documentation()

    # Salvar em arquivo
    output_file = 'DOCS/api/API_REFERENCE_AUTO.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(doc)

    print(f"✅ Documentação gerada: {output_file}")
    print(f"📊 Total de linhas: {len(doc.splitlines())}")

    # Mostrar preview
    print("\n" + "="*80)
    print("PREVIEW (primeiras 50 linhas):")
    print("="*80)
    for i, line in enumerate(doc.splitlines()[:50], 1):
        print(f"{i:3}: {line}")
