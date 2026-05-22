"""Cliente read-only para db_puket (SQL Server em db01.grupounico.com).

Encapsula consultas mestre (FORNECEDORES, PRODUTOS, COLECOES, etc.) com
cache TTL e timeout agressivo. Se a config Linx estiver desabilitada ou
a conexão falhar, as funções retornam lista vazia — o app continua
funcionando sem o autocomplete do ERP.

Referência: docs/linx_db_puket_analysis.md
"""
import logging
import re
import threading
import time
from typing import Any, Optional

try:
    import pyodbc  # type: ignore
    _PYODBC_AVAILABLE = True
except ImportError:
    pyodbc = None  # type: ignore
    _PYODBC_AVAILABLE = False

from config import Config

logger = logging.getLogger(__name__)

# Mensagens de erro do driver podem ecoar a connection string completa
# (com PWD=...). Sanitizamos antes de logar. Cobre formatos comuns:
#   PWD=valor;   PWD={valor};   PWD="valor";   PWD='valor';
_PWD_RE = re.compile(
    r'(PWD|PASSWORD|UID|USER)\s*=\s*'
    r'(?:\{[^}]*\}|"[^"]*"|\'[^\']*\'|[^;\s]+)',
    re.IGNORECASE,
)


def _sanitize(text: object) -> str:
    return _PWD_RE.sub(r'\1=***', str(text))


def _escape_like(value: str) -> str:
    """Escapa wildcards SQL Server (`%`, `_`, `[`) para uso em LIKE com `q`.

    Sem isto, busca por "100%" vira "%100%%" e poda resultados incorretos.
    """
    return (
        value.replace('[', '[[]')
             .replace('%', '[%]')
             .replace('_', '[_]')
    )

_cache: dict[str, tuple[float, Any]] = {}
_cache_lock = threading.Lock()


def _cache_get(key: str) -> Optional[Any]:
    with _cache_lock:
        entry = _cache.get(key)
        if not entry:
            return None
        ts, value = entry
        if time.time() - ts > Config.LINX_CACHE_TTL:
            _cache.pop(key, None)
            return None
        return value


def _cache_set(key: str, value: Any) -> None:
    with _cache_lock:
        _cache[key] = (time.time(), value)


def cache_clear() -> None:
    """Limpa o cache em memória (uso administrativo)."""
    with _cache_lock:
        _cache.clear()


def is_enabled() -> bool:
    """True se a integração estiver ligada e o driver disponível."""
    return (
        Config.LINX_DB_ENABLED
        and _PYODBC_AVAILABLE
        and bool(Config.LINX_DB_USER)
        and bool(Config.LINX_DB_PASSWORD)
    )


def _conn_str() -> str:
    return (
        f"DRIVER={{{Config.LINX_DB_DRIVER}}};"
        f"SERVER={Config.LINX_DB_HOST},{Config.LINX_DB_PORT};"
        f"DATABASE={Config.LINX_DB_NAME};"
        f"UID={Config.LINX_DB_USER};"
        f"PWD={Config.LINX_DB_PASSWORD};"
        f"TrustServerCertificate=yes;"
        f"Connection Timeout={Config.LINX_DB_TIMEOUT};"
    )


def _get_connection():
    if not is_enabled():
        raise RuntimeError('Integração Linx desabilitada ou pyodbc não instalado.')
    return pyodbc.connect(_conn_str(), timeout=Config.LINX_DB_TIMEOUT)


def ping() -> dict:
    """Healthcheck rápido — retorna {ok, latency_ms, error?}.

    Mensagens de erro são sanitizadas: a senha nunca aparece na resposta.
    """
    if not is_enabled():
        return {'ok': False, 'error': 'Integração desabilitada (LINX_DB_ENABLED=false ou pyodbc ausente).'}
    t0 = time.time()
    try:
        with _get_connection() as conn:
            cur = conn.cursor()
            cur.execute('SELECT 1')
            cur.fetchone()
        return {'ok': True, 'latency_ms': int((time.time() - t0) * 1000)}
    except Exception as exc:  # noqa: BLE001
        safe = _sanitize(exc)
        logger.warning('Linx ping falhou: %s', safe)
        return {'ok': False, 'error': safe, 'latency_ms': int((time.time() - t0) * 1000)}


def _safe_query(fn, default, *args, **kwargs):
    """Wrapper que captura falhas de conexão e retorna default.

    Mensagens de exceção são sanitizadas para nunca vazar a senha do ERP.
    """
    if not is_enabled():
        return default
    try:
        return fn(*args, **kwargs)
    except Exception as exc:  # noqa: BLE001
        logger.warning('Linx query falhou (%s): %s', fn.__name__, _sanitize(exc))
        return default


def _strip(value) -> str:
    if value is None:
        return ''
    return str(value).strip()


def buscar_fornecedores(q: str, limit: int = 10) -> list[dict]:
    """Busca fornecedores ativos por nome ou CNPJ.

    Retorna lista de dicts com chaves: codigo, nome, cnpj, tipo, beneficiador, licenciado.
    """
    q = (q or '').strip()
    if len(q) < 2:
        return []
    cache_key = f'fornecedores:{q.lower()}:{limit}'
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    def _do():
        like = f'%{_escape_like(q)}%'
        with _get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT TOP (?)
                    LTRIM(RTRIM(FORNECEDOR))      AS nome,
                    LTRIM(RTRIM(COD_FORNECEDOR))  AS codigo,
                    LTRIM(RTRIM(ISNULL(CGC_CPF, ''))) AS cnpj,
                    LTRIM(RTRIM(ISNULL(TIPO, '')))    AS tipo,
                    ISNULL(BENEFICIADOR, 0)       AS beneficiador,
                    ISNULL(LICENCIADO, 0)         AS licenciado
                FROM FORNECEDORES WITH (NOLOCK)
                WHERE ISNULL(INATIVO, 0) = 0
                  AND (FORNECEDOR LIKE ? OR CGC_CPF LIKE ?)
                ORDER BY FORNECEDOR
                """,
                limit, like, like,
            )
            rows = [
                {
                    'nome': _strip(r[0]),
                    'codigo': _strip(r[1]),
                    'cnpj': _strip(r[2]),
                    'tipo': _strip(r[3]),
                    'beneficiador': bool(r[4]),
                    'licenciado': bool(r[5]),
                }
                for r in cur
            ]
            return rows

    result = _safe_query(_do, [])
    _cache_set(cache_key, result)
    return result


def obter_fornecedor(codigo: str) -> Optional[dict]:
    """Detalhes completos de um fornecedor por COD_FORNECEDOR (para importar)."""
    codigo = (codigo or '').strip()
    if not codigo:
        return None
    cache_key = f'fornecedor:{codigo}'
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    def _do():
        with _get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT TOP 1
                    LTRIM(RTRIM(FORNECEDOR))      AS nome,
                    LTRIM(RTRIM(COD_FORNECEDOR))  AS codigo,
                    LTRIM(RTRIM(ISNULL(CGC_CPF, '')))    AS cnpj,
                    LTRIM(RTRIM(ISNULL(TIPO, '')))       AS tipo,
                    LTRIM(RTRIM(ISNULL(SUBTIPO_FORNECEDOR, ''))) AS subtipo,
                    ISNULL(BENEFICIADOR, 0)       AS beneficiador,
                    ISNULL(LICENCIADO, 0)         AS licenciado
                FROM FORNECEDORES WITH (NOLOCK)
                WHERE COD_FORNECEDOR = ?
                  AND ISNULL(INATIVO, 0) = 0
                """,
                codigo,
            )
            r = cur.fetchone()
            if not r:
                return None
            return {
                'nome': _strip(r[0]),
                'codigo': _strip(r[1]),
                'cnpj': _strip(r[2]),
                'tipo': _strip(r[3]),
                'subtipo': _strip(r[4]),
                'beneficiador': bool(r[5]),
                'licenciado': bool(r[6]),
            }

    result = _safe_query(_do, None)
    if result is not None:
        _cache_set(cache_key, result)
    return result


def buscar_produtos(q: str, limit: int = 20, colecao: Optional[str] = None) -> list[dict]:
    """Busca produtos (PRODUTOS + workflow IMB_WF) por código ou descrição.

    Retorna: codigo, descricao, colecao, linha, fornecedor (cod), refer_fabricante.
    """
    q = (q or '').strip()
    if len(q) < 2:
        return []
    cache_key = f'produtos:{q.lower()}:{limit}:{colecao or ""}'
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    def _do():
        like = f'%{_escape_like(q)}%'
        sql = """
            SELECT TOP (?)
                LTRIM(RTRIM(P.PRODUTO))           AS codigo,
                LTRIM(RTRIM(ISNULL(P.DESC_PRODUTO, ''))) AS descricao,
                LTRIM(RTRIM(ISNULL(P.COLECAO, ''))) AS colecao,
                LTRIM(RTRIM(ISNULL(P.LINHA, '')))   AS linha,
                LTRIM(RTRIM(ISNULL(P.FABRICANTE, ''))) AS fornecedor,
                LTRIM(RTRIM(ISNULL(P.REFER_FABRICANTE, ''))) AS refer_fabricante,
                CAST(ISNULL(P.PESO, 0) AS DECIMAL(10,3)) AS peso
            FROM PRODUTOS P WITH (NOLOCK)
            WHERE (P.PRODUTO LIKE ? OR P.DESC_PRODUTO LIKE ? OR P.REFER_FABRICANTE LIKE ?)
        """
        params: list = [limit, like, like, like]
        if colecao:
            sql += " AND P.COLECAO = ?"
            params.append(colecao)
        sql += " ORDER BY P.PRODUTO"

        with _get_connection() as conn:
            cur = conn.cursor()
            cur.execute(sql, *params)
            return [
                {
                    'codigo': _strip(r[0]),
                    'descricao': _strip(r[1]),
                    'colecao': _strip(r[2]),
                    'linha': _strip(r[3]),
                    'fornecedor_codigo': _strip(r[4]),
                    'refer_fabricante': _strip(r[5]),
                    'peso': float(r[6]) if r[6] is not None else 0.0,
                }
                for r in cur
            ]

    result = _safe_query(_do, [])
    _cache_set(cache_key, result)
    return result


def obter_produto(codigo: str) -> Optional[dict]:
    """Detalhes completos de um produto para pré-popular Referencia."""
    codigo = (codigo or '').strip()
    if not codigo:
        return None
    cache_key = f'produto:{codigo}'
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    def _do():
        with _get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT TOP 1
                    LTRIM(RTRIM(P.PRODUTO))           AS codigo,
                    LTRIM(RTRIM(ISNULL(P.DESC_PRODUTO, ''))) AS descricao,
                    LTRIM(RTRIM(ISNULL(P.COLECAO, ''))) AS colecao,
                    LTRIM(RTRIM(ISNULL(P.LINHA, '')))   AS linha,
                    LTRIM(RTRIM(ISNULL(P.FABRICANTE, ''))) AS fornecedor_codigo,
                    LTRIM(RTRIM(ISNULL(P.REFER_FABRICANTE, ''))) AS refer_fabricante,
                    CAST(ISNULL(P.PESO, 0) AS DECIMAL(10,3)) AS peso,
                    LTRIM(RTRIM(ISNULL(WF.SEXO, ''))) AS sexo,
                    ISNULL(WF.FACCAO, 0) AS faccao
                FROM PRODUTOS P WITH (NOLOCK)
                LEFT JOIN IMB_WF_PRODUTOS_DESENVOLVIMENTO WF WITH (NOLOCK)
                       ON WF.PRODUTO = P.PRODUTO
                WHERE P.PRODUTO = ?
                """,
                codigo,
            )
            r = cur.fetchone()
            if not r:
                return None
            sexo_raw = _strip(r[7])
            categoria = _mapear_categoria(_strip(r[1]), _strip(r[3]), sexo_raw)
            return {
                'codigo': _strip(r[0]),
                'descricao': _strip(r[1]),
                'colecao': _strip(r[2]),
                'linha': _strip(r[3]),
                'fornecedor_codigo': _strip(r[4]),
                'refer_fabricante': _strip(r[5]),
                'peso': float(r[6]) if r[6] is not None else 0.0,
                'sexo': sexo_raw,
                'faccao': bool(r[8]),
                'categoria_sugerida': categoria,
            }

    result = _safe_query(_do, None)
    if result is not None:
        _cache_set(cache_key, result)
    return result


def _mapear_categoria(descricao: str, linha: str, sexo: str) -> str:
    """Heurística: mapeia DESC_PRODUTO + LINHA + SEXO para baby/kids/teen/adulto.

    A descrição do produto é o sinal mais forte (ex: "MAIO BABY FOCA"). Linha
    no Puket descreve tipo (PRAIA, FITNESS), não idade. Ordem importa: baby
    antes de kids (alguns produtos têm "baby kids" — preferimos baby).

    A categorização é determinística (mesma entrada → mesma saída) para que
    o usuário possa sobrescrever depois sem ambiguidade.
    """
    # Padding com espaços para que tokens como " baby " peguem início/fim de string.
    haystack = f' {descricao or ""} {linha or ""} '.lower()
    if any(token in haystack for token in (' baby ', ' bebê ', ' bebe ', ' newborn ', ' recém ', ' recem ')):
        return 'baby'
    if any(token in haystack for token in (' kids ', ' infantil ', ' child ', ' inf ')):
        return 'kids'
    if any(token in haystack for token in (' teen ', ' juvenil ', ' adolesc')):
        return 'teen'
    return 'adulto'


def listar_colecoes(limit: int = 100) -> list[dict]:
    """Coleções ativas para popular dropdown."""
    cache_key = f'colecoes:{limit}'
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    def _do():
        with _get_connection() as conn:
            cur = conn.cursor()
            # Tabela tem registros em múltiplos idiomas (2=EN, 3=ES); colapsamos
            # por código pegando a primeira descrição não-vazia encontrada.
            cur.execute(
                """
                SELECT TOP (?)
                    LTRIM(RTRIM(COD_PRODUTO_COLECAO)) AS codigo,
                    LTRIM(RTRIM(MAX(ISNULL(DESC_COLECAO, '')))) AS descricao
                FROM PRT_EXP_PROD_COLECAO WITH (NOLOCK)
                GROUP BY COD_PRODUTO_COLECAO
                ORDER BY COD_PRODUTO_COLECAO DESC
                """,
                limit,
            )
            return [
                {'codigo': _strip(r[0]), 'descricao': _strip(r[1])}
                for r in cur
            ]

    result = _safe_query(_do, [])
    _cache_set(cache_key, result)
    return result


def listar_linhas() -> list[dict]:
    """Linhas (PRAIA, ACESSORIO, etc.) — tabela pequena (~20 linhas), cache longo."""
    cache_key = 'linhas'
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    def _do():
        with _get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                SELECT
                    LTRIM(RTRIM(COD_LINHA))         AS codigo,
                    LTRIM(RTRIM(ISNULL(LINHA, ''))) AS descricao
                FROM PRODUTOS_LINHAS WITH (NOLOCK)
                WHERE ISNULL(INATIVO, 0) = 0
                ORDER BY LINHA
                """
            )
            return [
                {'codigo': _strip(r[0]), 'descricao': _strip(r[1])}
                for r in cur
            ]

    result = _safe_query(_do, [])
    _cache_set(cache_key, result)
    return result
