"""
=======================================================================
API PAGINATION HELPER - Backend support for DataTable
=======================================================================
Provides pagination, filtering, and sorting for Flask routes
"""

from flask import request, jsonify
from sqlalchemy import or_, and_, desc, asc


class DataTablePaginator:
    """
    Helper class to handle DataTable pagination, filtering, and sorting
    on the backend for Flask routes.

    Usage:
        @app.route('/api/users')
        def get_users_api():
            paginator = DataTablePaginator(
                model=User,
                base_query=User.query,
                searchable_fields=['username', 'email', 'nome_completo'],
                default_sort='id',
                default_order='desc'
            )
            return paginator.get_response()
    """

    def __init__(self, model, base_query, searchable_fields=None,
                 default_sort=None, default_order='asc', per_page_options=None):
        """
        Initialize the paginator

        Args:
            model: SQLAlchemy model class
            base_query: Base SQLAlchemy query (e.g., User.query)
            searchable_fields: List of field names to search in
            default_sort: Default column to sort by
            default_order: Default sort order ('asc' or 'desc')
            per_page_options: List of allowed per_page values
        """
        self.model = model
        self.base_query = base_query
        self.searchable_fields = searchable_fields or []
        self.default_sort = default_sort
        self.default_order = default_order
        self.per_page_options = per_page_options or [10, 20, 50, 100]

        # Parse request parameters
        self.page = request.args.get('page', 1, type=int)
        self.per_page = request.args.get('per_page', 20, type=int)
        self.search = request.args.get('search', '', type=str)
        self.sort_column = request.args.get('sort', default_sort, type=str)
        self.sort_order = request.args.get('order', default_order, type=str)

        # Validate per_page
        if self.per_page not in self.per_page_options:
            self.per_page = 20

        # Validate sort_order
        if self.sort_order not in ['asc', 'desc']:
            self.sort_order = 'asc'

    def apply_search(self, query):
        """Apply search filter to query"""
        if not self.search or not self.searchable_fields:
            return query

        search_term = f"%{self.search}%"
        conditions = []

        for field_name in self.searchable_fields:
            field = getattr(self.model, field_name, None)
            if field is not None:
                conditions.append(field.ilike(search_term))

        if conditions:
            query = query.filter(or_(*conditions))

        return query

    def apply_sort(self, query):
        """Apply sorting to query"""
        if not self.sort_column:
            return query

        column = getattr(self.model, self.sort_column, None)
        if column is None:
            return query

        if self.sort_order == 'desc':
            query = query.order_by(desc(column))
        else:
            query = query.order_by(asc(column))

        return query

    def get_paginated_data(self):
        """Get paginated, filtered, and sorted data"""
        query = self.base_query

        # Apply search
        query = self.apply_search(query)

        # Apply sorting
        query = self.apply_sort(query)

        # Paginate
        pagination = query.paginate(
            page=self.page,
            per_page=self.per_page,
            error_out=False
        )

        return pagination

    def get_response(self, serializer=None):
        """
        Get JSON response for API

        Args:
            serializer: Optional function to serialize model objects to dict
                       If None, uses to_dict() method on model

        Returns:
            Flask JSON response
        """
        pagination = self.get_paginated_data()

        # Serialize items
        if serializer:
            items = [serializer(item) for item in pagination.items]
        else:
            items = [item.to_dict() if hasattr(item, 'to_dict') else item.__dict__
                    for item in pagination.items]

        return jsonify({
            'items': items,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': self.page,
            'per_page': self.per_page,
            'has_prev': pagination.has_prev,
            'has_next': pagination.has_next,
            'prev_num': pagination.prev_num,
            'next_num': pagination.next_num
        })


def simple_pagination(query, page=None, per_page=None):
    """
    Simple pagination helper for quick use

    Usage:
        @app.route('/api/items')
        def get_items():
            items, meta = simple_pagination(Item.query)
            return jsonify({'items': items, 'meta': meta})
    """
    page = page or request.args.get('page', 1, type=int)
    per_page = per_page or request.args.get('per_page', 20, type=int)

    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    items = [item.to_dict() if hasattr(item, 'to_dict') else item.__dict__
            for item in pagination.items]

    meta = {
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'per_page': per_page,
        'has_prev': pagination.has_prev,
        'has_next': pagination.has_next
    }

    return items, meta


# Example usage in routes:
"""
from api_pagination import DataTablePaginator, simple_pagination

# Example 1: Full-featured DataTable endpoint
@app.route('/api/users')
def get_users_api():
    paginator = DataTablePaginator(
        model=User,
        base_query=User.query,
        searchable_fields=['username', 'email', 'nome_completo'],
        default_sort='id',
        default_order='desc'
    )
    return paginator.get_response()

# Example 2: Simple pagination
@app.route('/api/relatorios')
def get_relatorios_api():
    query = Relatorio.query

    # Apply custom filters
    status = request.args.get('status')
    if status:
        query = query.filter_by(status_atual=status)

    items, meta = simple_pagination(query)
    return jsonify({'items': items, 'meta': meta})

# Example 3: Custom serializer
@app.route('/api/audit')
def get_audit_api():
    def serialize_log(log):
        return {
            'id': log.id,
            'timestamp': log.created_at.isoformat(),
            'user': log.usuario_nome,
            'action': log.acao,
            'description': log.descricao
        }

    paginator = DataTablePaginator(
        model=AuditLog,
        base_query=AuditLog.query,
        searchable_fields=['descricao', 'usuario_nome'],
        default_sort='created_at',
        default_order='desc'
    )
    return paginator.get_response(serializer=serialize_log)
"""
