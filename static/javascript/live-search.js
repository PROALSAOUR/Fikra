document.addEventListener('DOMContentLoaded', () => {
    const filterForm = document.getElementById('filter-form');
    const filterToggle = document.querySelector('.filter-toggle');
    const filterOptions = document.querySelector('.filter-options');
    const closeFilter = document.querySelector('.close-filter');
    const filterTabs = document.querySelectorAll('.filter-tab');
    const filterGroups = document.querySelectorAll('.filter-group');

    if (filterToggle && filterOptions && closeFilter) {
        filterToggle.addEventListener('click', () => {
            filterOptions.classList.toggle('visible');
        });

        closeFilter.addEventListener('click', () => {
            filterOptions.classList.remove('visible');
        });
    }

    if (filterForm) {
        filterForm.addEventListener('submit', (event) => {
            event.preventDefault();

            const inputs = filterForm.querySelectorAll('input, select');
            const queryParams = new URLSearchParams();

            inputs.forEach(input => {
                if (input.value.trim() !== '') {
                    queryParams.append(input.name, input.value);
                }
            });

            window.location.search = queryParams.toString();
        });
    }

    if (filterTabs.length) {
        filterTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const target = tab.getAttribute('data-target');
                
                filterGroups.forEach(group => {
                    if (group.id === target) {
                        group.classList.add('visible');
                    } else {
                        group.classList.remove('visible');
                    }
                });
            });
        });
    }
    
    let typingTimer;
    const doneTypingInterval = 500;
    const searchInput = document.getElementById('search-query');

    if (searchInput) {
        searchInput.addEventListener('input', (event) => {
            clearTimeout(typingTimer);
            typingTimer = setTimeout(() => {
                const query = event.target.value.trim();
                if (query.length > 0) {
                    filterForm.submit();
                }
            }, doneTypingInterval);
        });

        // لإعادة تعيين قيمة البحث بعد تحميل الصفحة
        const queryParams = new URLSearchParams(window.location.search);
        const searchQuery = queryParams.get('q');
        if (searchQuery) {
            searchInput.value = searchQuery;
        }
    }
});
