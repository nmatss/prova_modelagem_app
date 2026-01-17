#!/usr/bin/env python3
"""
MINIFICAÇÃO DE CSS E JS PARA PRODUÇÃO
Reduz tamanho dos arquivos removendo espaços, comentários e otimizando código
"""

import os
import re
from pathlib import Path

# Diretórios
BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / 'static'
CSS_DIR = STATIC_DIR / 'css'
JS_DIR = STATIC_DIR / 'js'

def minify_css(content):
    """Minifica CSS removendo comentários e espaços desnecessários"""
    # Remover comentários /* ... */
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    # Remover múltiplos espaços
    content = re.sub(r'\s+', ' ', content)

    # Remover espaços ao redor de caracteres especiais
    content = re.sub(r'\s*([{}:;,>+~])\s*', r'\1', content)

    # Remover ponto e vírgula antes de }
    content = re.sub(r';\}', '}', content)

    # Remover espaços no início e fim
    content = content.strip()

    return content

def minify_js(content):
    """Minifica JS de forma básica (para produção use ferramentas como terser)"""
    # Remover comentários de linha única //
    content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)

    # Remover comentários de bloco /* ... */
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)

    # Remover múltiplos espaços
    content = re.sub(r'\s+', ' ', content)

    # Remover espaços ao redor de operadores
    content = re.sub(r'\s*([=+\-*/<>!&|,;{}()[\]])\s*', r'\1', content)

    # Remover espaços no início e fim
    content = content.strip()

    return content

def process_file(file_path, minify_func, suffix='.min'):
    """Processa um arquivo e cria versão minificada"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Pular arquivos já minificados
        if '.min.' in file_path.name:
            print(f"⏭️  Pulando {file_path.name} (já minificado)")
            return

        # Minificar
        minified = minify_func(content)

        # Calcular redução
        original_size = len(content)
        minified_size = len(minified)
        reduction = ((original_size - minified_size) / original_size * 100) if original_size > 0 else 0

        # Criar arquivo .min
        min_path = file_path.parent / f"{file_path.stem}{suffix}{file_path.suffix}"
        with open(min_path, 'w', encoding='utf-8') as f:
            f.write(minified)

        print(f"✅ {file_path.name} → {min_path.name}")
        print(f"   {original_size:,} bytes → {minified_size:,} bytes ({reduction:.1f}% redução)")

        return {
            'file': file_path.name,
            'original_size': original_size,
            'minified_size': minified_size,
            'reduction': reduction
        }

    except Exception as e:
        print(f"❌ Erro ao processar {file_path.name}: {e}")
        return None

def main():
    """Processa todos os arquivos CSS e JS"""
    print("🚀 Iniciando minificação de assets...\n")

    stats = {
        'css': [],
        'js': []
    }

    # Processar CSS
    print("📄 Minificando CSS...")
    for css_file in CSS_DIR.glob('*.css'):
        if '.min.' not in css_file.name:
            result = process_file(css_file, minify_css)
            if result:
                stats['css'].append(result)

    print()

    # Processar JS
    print("📜 Minificando JavaScript...")
    for js_file in JS_DIR.glob('*.js'):
        if '.min.' not in js_file.name:
            result = process_file(js_file, minify_js)
            if result:
                stats['js'].append(result)

    # Estatísticas finais
    print("\n" + "="*60)
    print("📊 ESTATÍSTICAS FINAIS")
    print("="*60)

    for file_type, results in stats.items():
        if results:
            total_original = sum(r['original_size'] for r in results)
            total_minified = sum(r['minified_size'] for r in results)
            total_reduction = ((total_original - total_minified) / total_original * 100) if total_original > 0 else 0

            print(f"\n{file_type.upper()}:")
            print(f"  Arquivos processados: {len(results)}")
            print(f"  Tamanho original: {total_original:,} bytes ({total_original/1024:.1f} KB)")
            print(f"  Tamanho minificado: {total_minified:,} bytes ({total_minified/1024:.1f} KB)")
            print(f"  Redução total: {total_reduction:.1f}% ({(total_original-total_minified)/1024:.1f} KB economizados)")

    print("\n✅ Minificação concluída!")
    print("\n💡 Dica: Use versões .min em produção atualizando base.html")
    print("   Exemplo: 'custom.css' → 'custom.min.css'")

if __name__ == '__main__':
    main()
