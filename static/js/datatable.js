/**
 * =======================================================================
 * MODERN DATATABLE - Enhanced Table System with Sorting & Filtering
 * =======================================================================
 * Features:
 * - Multi-column sorting
 * - Real-time search/filter
 * - Type-aware sorting (string, number, date)
 * - Mobile-responsive
 * - Pagination support
 * - Performant (handles 1000+ rows)
 */

class DataTable {
  constructor(tableElement, options = {}) {
    this.table = tableElement;
    this.options = {
      sortable: true,
      searchable: true,
      perPage: 20,
      pagination: true,
      mobileBreakpoint: 768,
      ...options
    };

    // State
    this.rows = [];
    this.filteredRows = [];
    this.currentPage = 1;
    this.currentSort = {
      column: null,
      direction: null
    };
    this.searchTerm = '';

    // Elements
    this.thead = this.table.querySelector('thead');
    this.tbody = this.table.querySelector('tbody');
    this.headers = this.table.querySelectorAll('th[data-sortable="true"]');

    // Initialize
    this.init();
  }

  /**
   * Initialize the DataTable
   */
  init() {
    // Store original rows
    this.rows = Array.from(this.tbody.querySelectorAll('tr'));
    this.filteredRows = [...this.rows];

    // Setup sorting
    if (this.options.sortable) {
      this.setupSorting();
    }

    // Setup search
    if (this.options.searchable) {
      this.setupSearch();
    }

    // Setup pagination
    if (this.options.pagination) {
      this.setupPagination();
    }

    // Initial render
    this.render();

    console.log(`DataTable initialized with ${this.rows.length} rows`);
  }

  /**
   * Setup column sorting
   */
  setupSorting() {
    this.headers.forEach((header, index) => {
      header.addEventListener('click', () => this.sort(header, index));

      // Add sort icon if not exists
      if (!header.querySelector('.sort-icon')) {
        const icon = document.createElement('span');
        icon.className = 'sort-icon';
        icon.innerHTML = '<i class="bi bi-chevron-expand"></i>';
        header.appendChild(icon);
      }
    });
  }

  /**
   * Sort table by column
   */
  sort(header, columnIndex) {
    const type = header.dataset.type || 'string';

    // Determine sort direction
    let newDirection;
    if (!header.classList.contains('sorted-asc') && !header.classList.contains('sorted-desc')) {
      newDirection = 'asc';
    } else if (header.classList.contains('sorted-asc')) {
      newDirection = 'desc';
    } else {
      newDirection = 'asc';
    }

    // Clear all sorted classes
    this.headers.forEach(h => h.classList.remove('sorted-asc', 'sorted-desc'));

    // Add new sorted class
    header.classList.add(`sorted-${newDirection}`);

    // Store current sort
    this.currentSort = {
      column: columnIndex,
      direction: newDirection,
      type: type
    };

    // Sort filtered rows
    this.filteredRows.sort((a, b) => {
      const aCell = a.cells[columnIndex];
      const bCell = b.cells[columnIndex];

      if (!aCell || !bCell) return 0;

      let aVal = aCell.dataset.sortValue || aCell.textContent.trim();
      let bVal = bCell.dataset.sortValue || bCell.textContent.trim();

      // Convert based on type
      if (type === 'number') {
        aVal = parseFloat(aVal.replace(/[^\d.-]/g, '')) || 0;
        bVal = parseFloat(bVal.replace(/[^\d.-]/g, '')) || 0;
      } else if (type === 'date') {
        aVal = new Date(aVal);
        bVal = new Date(bVal);
      } else {
        // String comparison (case-insensitive)
        aVal = aVal.toLowerCase();
        bVal = bVal.toLowerCase();
      }

      // Compare
      let comparison = 0;
      if (aVal < bVal) comparison = -1;
      if (aVal > bVal) comparison = 1;

      return newDirection === 'asc' ? comparison : -comparison;
    });

    // Reset to first page after sort
    this.currentPage = 1;
    this.render();
  }

  /**
   * Setup search functionality
   */
  setupSearch() {
    const container = this.table.closest('.table-container');
    if (!container) return;

    const searchInput = container.querySelector('.table-search-input');
    if (!searchInput) return;

    let searchTimeout;
    searchInput.addEventListener('input', (e) => {
      clearTimeout(searchTimeout);
      searchTimeout = setTimeout(() => {
        this.filter(e.target.value);
      }, 300); // Debounce 300ms
    });
  }

  /**
   * Filter rows based on search term
   */
  filter(searchTerm) {
    this.searchTerm = searchTerm.toLowerCase().trim();

    if (!this.searchTerm) {
      this.filteredRows = [...this.rows];
    } else {
      this.filteredRows = this.rows.filter(row => {
        const text = row.textContent.toLowerCase();
        return text.includes(this.searchTerm);
      });
    }

    // Reset to first page after filter
    this.currentPage = 1;
    this.render();
  }

  /**
   * Setup pagination
   */
  setupPagination() {
    const container = this.table.closest('.table-container');
    if (!container) return;

    // Per-page selector
    const perPageSelect = container.querySelector('.per-page-select');
    if (perPageSelect) {
      perPageSelect.addEventListener('change', (e) => {
        this.options.perPage = parseInt(e.target.value);
        this.currentPage = 1;
        this.render();
      });
    }

    // Pagination buttons (setup in render)
  }

  /**
   * Render the table with current state
   */
  render() {
    const start = (this.currentPage - 1) * this.options.perPage;
    const end = start + this.options.perPage;
    const pageRows = this.filteredRows.slice(start, end);

    // Clear tbody
    this.tbody.innerHTML = '';

    // Show appropriate rows
    if (pageRows.length === 0) {
      this.showEmptyState();
    } else {
      pageRows.forEach(row => this.tbody.appendChild(row));
    }

    // Update pagination UI
    this.updatePagination();

    // Update info
    this.updateInfo();
  }

  /**
   * Show empty state
   */
  showEmptyState() {
    const colspan = this.headers.length || this.table.querySelectorAll('th').length;
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td colspan="${colspan}" class="table-empty">
        <div class="table-empty-icon">
          <i class="bi bi-inbox"></i>
        </div>
        <h3>Nenhum resultado encontrado</h3>
        <p>${this.searchTerm ? 'Tente usar termos diferentes' : 'Não há dados para exibir'}</p>
      </td>
    `;
    this.tbody.appendChild(tr);
  }

  /**
   * Update pagination UI
   */
  updatePagination() {
    const container = this.table.closest('.table-container');
    if (!container) return;

    const paginationNav = container.querySelector('.pagination-nav');
    if (!paginationNav) return;

    const totalPages = Math.ceil(this.filteredRows.length / this.options.perPage);

    if (totalPages <= 1) {
      paginationNav.innerHTML = '';
      return;
    }

    const buttons = [];

    // Previous button
    buttons.push(`
      <button class="btn-page" ${this.currentPage === 1 ? 'disabled' : ''} data-page="${this.currentPage - 1}">
        <i class="bi bi-chevron-left"></i>
      </button>
    `);

    // Page numbers
    const pageNumbers = this.getPageNumbers(this.currentPage, totalPages);
    pageNumbers.forEach(page => {
      if (page === '...') {
        buttons.push(`<span class="pagination-ellipsis">...</span>`);
      } else {
        buttons.push(`
          <button class="btn-page ${page === this.currentPage ? 'active' : ''}" data-page="${page}">
            ${page}
          </button>
        `);
      }
    });

    // Next button
    buttons.push(`
      <button class="btn-page" ${this.currentPage === totalPages ? 'disabled' : ''} data-page="${this.currentPage + 1}">
        <i class="bi bi-chevron-right"></i>
      </button>
    `);

    paginationNav.innerHTML = buttons.join('');

    // Add event listeners
    paginationNav.querySelectorAll('.btn-page[data-page]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const page = parseInt(e.currentTarget.dataset.page);
        if (page >= 1 && page <= totalPages) {
          this.goToPage(page);
        }
      });
    });
  }

  /**
   * Get page numbers for pagination
   */
  getPageNumbers(current, total) {
    const pages = [];
    const delta = 1; // Number of pages to show on each side of current

    if (total <= 7) {
      // Show all pages if total is small
      for (let i = 1; i <= total; i++) {
        pages.push(i);
      }
    } else {
      // Show first, last, current, and nearby pages
      pages.push(1);

      if (current > 3) {
        pages.push('...');
      }

      for (let i = Math.max(2, current - delta); i <= Math.min(total - 1, current + delta); i++) {
        pages.push(i);
      }

      if (current < total - 2) {
        pages.push('...');
      }

      pages.push(total);
    }

    return pages;
  }

  /**
   * Go to specific page
   */
  goToPage(page) {
    this.currentPage = page;
    this.render();

    // Scroll to top of table
    this.table.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  /**
   * Update info display
   */
  updateInfo() {
    const container = this.table.closest('.table-container');
    if (!container) return;

    const infoEl = container.querySelector('.table-info');
    if (!infoEl) return;

    const start = (this.currentPage - 1) * this.options.perPage + 1;
    const end = Math.min(start + this.options.perPage - 1, this.filteredRows.length);
    const total = this.filteredRows.length;

    if (total === 0) {
      infoEl.innerHTML = 'Nenhum registro encontrado';
    } else {
      infoEl.innerHTML = `
        Mostrando <strong>${start}-${end}</strong> de <strong>${total}</strong> registro${total !== 1 ? 's' : ''}
      `;
    }
  }

  /**
   * Refresh the table data
   */
  refresh() {
    this.rows = Array.from(this.tbody.querySelectorAll('tr'));
    this.filter(this.searchTerm);
  }

  /**
   * Destroy the DataTable instance
   */
  destroy() {
    // Remove event listeners
    this.headers.forEach(header => {
      header.replaceWith(header.cloneNode(true));
    });

    // Clear state
    this.rows = [];
    this.filteredRows = [];
    this.currentSort = { column: null, direction: null };
    this.searchTerm = '';

    console.log('DataTable destroyed');
  }
}

/**
 * =======================================================================
 * AUTO-INITIALIZATION
 * =======================================================================
 */
document.addEventListener('DOMContentLoaded', function() {
  // Auto-initialize all tables with .table-modern class
  const tables = document.querySelectorAll('.table-modern');

  tables.forEach(table => {
    // Skip if already initialized
    if (table.dataset.datatableInit === 'true') return;

    // Check if table is inside a table-container
    const container = table.closest('.table-container');
    if (!container) {
      console.warn('Table not inside .table-container, skipping auto-init:', table);
      return;
    }

    // Initialize
    const dt = new DataTable(table);

    // Store reference
    table.datatableInstance = dt;
    table.dataset.datatableInit = 'true';
  });

  console.log(`Auto-initialized ${tables.length} DataTable(s)`);
});

/**
 * =======================================================================
 * EXPORT
 * =======================================================================
 */
// Make available globally
window.DataTable = DataTable;
