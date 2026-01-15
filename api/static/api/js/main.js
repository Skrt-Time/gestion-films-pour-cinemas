document.addEventListener('DOMContentLoaded', () => {

    const moviesGrid = document.getElementById('moviesGrid');
    const btnSearch = document.getElementById('btnSearch');
    const cityInput = document.getElementById('citySearch');

    // Utility to prevent XSS
    const escapeHtml = (unsafe) => {
        if (!unsafe) return "";
        return unsafe
             .replace(/&/g, "&amp;")
             .replace(/</g, "&lt;")
             .replace(/>/g, "&gt;")
             .replace(/"/g, "&quot;")
             .replace(/'/g, "&#039;");
    }

    // Function to render movies
    function renderMovies(movies) {
        moviesGrid.innerHTML = '';
        
        if (movies.length === 0) {
            moviesGrid.innerHTML = '<p style="color: grey; text-align: center; grid-column: 1/-1;">Aucun film trouvé pour cette recherche.</p>';
            return;
        }

        movies.forEach(movie => {
            // Adaptation des données API vers le format d'affichage
            let cityDisplay = "Non programmé";
            if (movie.programmations && movie.programmations.length > 0) {
                const cities = [...new Set(movie.programmations.map(p => p.cinema.ville))];
                cityDisplay = cities.map(c => escapeHtml(c)).join(', ');
            }

            const card = document.createElement('div');
            card.className = 'movie-card';
            card.innerHTML = `
                <div class="poster-wrapper">
                    <img src="${escapeHtml(movie.image_url)}" alt="${escapeHtml(movie.titre)}" onerror="this.src='https://dummyimage.com/600x900/000/fff&text=Poster+Manquant'">
                </div>
                <div class="card-info">
                    <div class="meta-info">${escapeHtml(movie.age_min)}</div>
                    <h3>${escapeHtml(movie.titre)}</h3>
                    <p>${escapeHtml(movie.realisateur)} • ${escapeHtml(movie.duree)}</p>
                    <p><i class="fa-solid fa-location-dot"></i> ${cityDisplay}</p>
                    <a href="/film/${movie.id}/" class="btn-details">Voir les détails</a>
                </div>
            `;
            moviesGrid.appendChild(card);
        });
    }

    // Fetch from API
    async function loadMovies(city = '') {
        moviesGrid.innerHTML = '<div class="loading-state"><i class="fa-solid fa-spinner fa-spin"></i> Chargement...</div>';
        try {
            let url = '/api/public/films/';
            if (city) {
                url += `?search=${encodeURIComponent(city)}`;
            }
            const response = await fetch(url);
            const movies = await response.json();
            renderMovies(movies);
        } catch (error) {
            console.error('Erreur API:', error);
            moviesGrid.innerHTML = '<p style="color: red; text-align: center;">Erreur de chargement des films.</p>';
        }
    }

    // Initial render
    loadMovies();

    // Search Logic
    btnSearch.addEventListener('click', () => {
        const query = cityInput.value.trim();
        loadMovies(query);
    });

    // Enter key support
    cityInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            btnSearch.click();
        }
    });

});
