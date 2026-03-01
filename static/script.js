// Global state
let allSongs = [];
let selectedSongs = new Set();
let currentAudio = null;
let playerModal = null;
let loadingModal = null;

// Pagination state
let currentPage = 1;
let songsPerPage = 15;
let filteredSongs = [];

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Initialize modals
    playerModal = new bootstrap.Modal(document.getElementById('playerModal'), { keyboard: false });
    loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'), { keyboard: false });

    // Event listeners
    document.getElementById('fetchBtn').addEventListener('click', fetchSongs);
    document.getElementById('loadBtn').addEventListener('click', loadExistingSongs);
    document.getElementById('downloadSelectedBtn').addEventListener('click', downloadSelected);
    document.getElementById('selectAllBtn').addEventListener('click', selectAll);
    document.getElementById('deselectAllBtn').addEventListener('click', deselectAll);
    document.getElementById('refreshBtn').addEventListener('click', refreshSongs);
    document.getElementById('exportBtn').addEventListener('click', exportSongs);
    document.getElementById('searchInput').addEventListener('input', filterSongs);
    document.getElementById('selectAllCheckbox').addEventListener('change', toggleSelectAll);

    // Load existing songs on startup
    loadExistingSongs();
});

// Show alert message
function showAlert(message, type = 'info') {
    const alertDiv = document.getElementById('statusAlert');
    const messageSpan = document.getElementById('statusMessage');
    
    messageSpan.textContent = message;
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.classList.remove('d-none');
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.classList.add('d-none');
    }, 5000);
}

// Show loading spinner
function showLoading(text = 'Processing...') {
    document.getElementById('loadingText').textContent = text;
    loadingModal.show();
}

// Hide loading spinner
function hideLoading() {
    loadingModal.hide();
}

// Fetch songs from curl command
async function fetchSongs() {
    const curlCommand = document.getElementById('curlInput').value.trim();
    
    if (!curlCommand) {
        showAlert('Please paste a curl command', 'warning');
        return;
    }

    showLoading('Fetching songs from curl...');

    try {
        const response = await fetch('/api/songs/fetch', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ curl_command: curlCommand })
        });

        const data = await response.json();
        hideLoading();

        if (data.success) {
            allSongs = data.songs;
            selectedSongs.clear();
            renderSongs();
            showAlert(`✓ ${data.message}`, 'success');
            document.getElementById('curlInput').value = '';
        } else {
            showAlert(`✗ ${data.message}`, 'danger');
        }
    } catch (error) {
        hideLoading();
        showAlert(`Error: ${error.message}`, 'danger');
    }
}

// Load existing songs from songs.json
async function loadExistingSongs() {
    showLoading('Loading songs...');

    try {
        const response = await fetch('/api/songs/load', {
            method: 'POST'
        });

        const data = await response.json();
        hideLoading();

        if (data.success) {
            allSongs = data.songs;
            selectedSongs.clear();
            renderSongs();
            
            if (allSongs.length > 0) {
                showAlert(`✓ Loaded ${allSongs.length} songs`, 'success');
            } else {
                showAlert('No songs found', 'info');
            }
        } else {
            showAlert(`✗ ${data.message}`, 'danger');
        }
    } catch (error) {
        hideLoading();
        showAlert(`Error: ${error.message}`, 'danger');
    }
}

// Render songs in table with pagination
function renderSongs(songs = allSongs) {
    const tbody = document.getElementById('songsTableBody');
    
    // Filter out songs with empty singer or song name
    filteredSongs = songs.filter(song => song.singer && song.singer.trim() && song.song && song.song.trim());
    currentPage = 1; // Reset to first page when rendering new results
    
    if (filteredSongs.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="5" class="text-center text-muted py-5">
                    <i class="fas fa-inbox"></i> No songs to display
                </td>
            </tr>
        `;
        updateSongCount();
        renderPagination();
        renderPlayerSection();
        return;
    }

    renderPage(1);
    updateSongCount();
}

// Render a specific page of songs
function renderPage(pageNum) {
    const tbody = document.getElementById('songsTableBody');
    
    if (filteredSongs.length === 0) {
        return;
    }
    
    currentPage = pageNum;
    const totalPages = Math.ceil(filteredSongs.length / songsPerPage);
    
    // Validate page number
    if (currentPage < 1) currentPage = 1;
    if (currentPage > totalPages) currentPage = totalPages;
    
    // Calculate start and end indices
    const startIdx = (currentPage - 1) * songsPerPage;
    const endIdx = startIdx + songsPerPage;
    const pageSongs = filteredSongs.slice(startIdx, endIdx);
    
    tbody.innerHTML = pageSongs.map((song, idx) => {
        const actualIndex = startIdx + idx;
        const isSelected = selectedSongs.has(actualIndex);
        const isDownloaded = song.downloaded;
        
        return `
            <tr class="fade-in">
                <td>
                    <input type="checkbox" class="form-check-input song-checkbox" 
                        data-index="${actualIndex}" ${isSelected ? 'checked' : ''}>
                </td>
                <td class="text-truncate" title="${song.song}">
                    <i class="fas fa-compact-disc text-success me-1"></i>${song.song}
                </td>
                <td class="text-truncate" title="${song.singer}">
                    <i class="fas fa-user text-info me-1"></i>${song.singer}
                </td>
                <td>
                    ${isDownloaded 
                        ? '<span class="badge bg-success"><i class="fas fa-check"></i> Downloaded</span>' 
                        : '<span class="badge bg-warning text-dark"><i class="fas fa-clock"></i> Pending</span>'}
                </td>
                <td>
                    <div class="song-actions">
                        ${isDownloaded 
                            ? `<button class="btn btn-sm btn-info" data-singer="${song.singer.replace(/"/g, '&quot;')}" data-song="${song.song.replace(/"/g, '&quot;')}" data-file="${song.file_path}" onclick="playSongBtn(this)" title="Play">
                                <i class="fas fa-play"></i>
                            </button>` 
                            : `<button class="btn btn-sm btn-warning" data-singer="${song.singer.replace(/"/g, '&quot;')}" data-song="${song.song.replace(/"/g, '&quot;')}" onclick="downloadSongBtn(this)" title="Download">
                                <i class="fas fa-download"></i>
                            </button>`}
                        <button class="btn btn-sm btn-danger" data-singer="${song.singer.replace(/"/g, '&quot;')}" data-song="${song.song.replace(/"/g, '&quot;')}" onclick="openYouTubeSearchBtn(this)" title="Search on YouTube">
                            <i class="fab fa-youtube"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `;
    }).join('');

    // Add event listeners to checkboxes
    document.querySelectorAll('.song-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const index = parseInt(this.dataset.index);
            if (this.checked) {
                selectedSongs.add(index);
            } else {
                selectedSongs.delete(index);
            }
            updateSelectAllCheckbox();
        });
    });

    updateSongCount();
    renderPagination();
}

// Update song count
function updateSongCount() {
    document.getElementById('songCount').textContent = filteredSongs.length;
}

// Render pagination controls
function renderPagination() {
    const totalPages = Math.ceil(filteredSongs.length / songsPerPage);
    const paginationContainer = document.getElementById('paginationContainer');
    
    if (!paginationContainer) {
        return;
    }
    
    if (totalPages <= 1) {
        paginationContainer.innerHTML = '';
        return;
    }
    
    let paginationHtml = `
        <nav aria-label="Page navigation" class="mt-3">
            <ul class="pagination justify-content-center mb-0">
                <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
                    <button class="page-link" onclick="goToPage(1)" title="First page">
                        <i class="fas fa-step-backward"></i>
                    </button>
                </li>
                <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
                    <button class="page-link" onclick="goToPage(${currentPage - 1})" title="Previous page">
                        <i class="fas fa-chevron-left"></i> Prev
                    </button>
                </li>
    `;
    
    // Generate page numbers
    const maxVisiblePages = 5;
    let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
    let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);
    
    if (endPage - startPage < maxVisiblePages - 1) {
        startPage = Math.max(1, endPage - maxVisiblePages + 1);
    }
    
    // Add "..." if there are pages before the visible range
    if (startPage > 1) {
        paginationHtml += `<li class="page-item"><span class="page-link">...</span></li>`;
    }
    
    // Add page numbers
    for (let i = startPage; i <= endPage; i++) {
        paginationHtml += `
            <li class="page-item ${i === currentPage ? 'active' : ''}">
                <button class="page-link" onclick="goToPage(${i})">${i}</button>
            </li>
        `;
    }
    
    // Add "..." if there are pages after the visible range
    if (endPage < totalPages) {
        paginationHtml += `<li class="page-item"><span class="page-link">...</span></li>`;
    }
    
    paginationHtml += `
                <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
                    <button class="page-link" onclick="goToPage(${currentPage + 1})" title="Next page">
                        Next <i class="fas fa-chevron-right"></i>
                    </button>
                </li>
                <li class="page-item ${currentPage === totalPages ? 'disabled' : ''}">
                    <button class="page-link" onclick="goToPage(${totalPages})" title="Last page">
                        <i class="fas fa-step-forward"></i>
                    </button>
                </li>
            </ul>
        </nav>
        <div class="text-center text-muted small mt-2">
            Page <strong>${currentPage}</strong> of <strong>${totalPages}</strong> 
            (${filteredSongs.length} total songs)
        </div>
    `;
    
    paginationContainer.innerHTML = paginationHtml;
}

// Navigate to a specific page
function goToPage(pageNum) {
    const totalPages = Math.ceil(filteredSongs.length / songsPerPage);
    if (pageNum >= 1 && pageNum <= totalPages) {
        renderPage(pageNum);
    }
}

// Update select all checkbox
function updateSelectAllCheckbox() {
    const checkbox = document.getElementById('selectAllCheckbox');
    const totalCheckboxes = document.querySelectorAll('.song-checkbox').length;
    const checkedCheckboxes = document.querySelectorAll('.song-checkbox:checked').length;
    
    checkbox.checked = checkedCheckboxes === totalCheckboxes && totalCheckboxes > 0;
    checkbox.indeterminate = checkedCheckboxes > 0 && checkedCheckboxes < totalCheckboxes;
}

// Toggle select all
function toggleSelectAll(e) {
    if (e.target.checked) {
        selectAll();
    } else {
        deselectAll();
    }
}

// Select all songs
function selectAll() {
    selectedSongs.clear();
    document.querySelectorAll('.song-checkbox').forEach((checkbox, index) => {
        checkbox.checked = true;
        selectedSongs.add(index);
    });
    updateSelectAllCheckbox();
}

// Deselect all songs
function deselectAll() {
    selectedSongs.clear();
    document.querySelectorAll('.song-checkbox').forEach(checkbox => {
        checkbox.checked = false;
    });
    updateSelectAllCheckbox();
}

// Download selected songs
async function downloadSelected() {
    if (selectedSongs.size === 0) {
        showAlert('❗ Please select at least one song', 'warning');
        return;
    }

    const songsToDownload = Array.from(selectedSongs).map(index => allSongs[index]);
    
    if (!confirm(`Download ${songsToDownload.length} song(s)?`)) {
        return;
    }

    showLoading(`Downloading ${songsToDownload.length} song(s)...`);

    try {
        const response = await fetch('/api/download/batch', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ songs: songsToDownload })
        });

        const data = await response.json();
        hideLoading();

        if (data.success) {
            showAlert(`✓ ${data.message}`, 'success');
            deselectAll();
            // Refresh songs to update status
            setTimeout(loadExistingSongs, 2000);
        } else {
            showAlert(`✗ ${data.message}`, 'danger');
        }
    } catch (error) {
        hideLoading();
        showAlert(`Error: ${error.message}`, 'danger');
    }
}

// Download single song
async function downloadSingleSong(singer, song) {
    if (!confirm(`Download "${song}" by ${singer}?`)) {
        return;
    }

    showLoading(`Downloading: ${song}...`);

    try {
        const response = await fetch('/api/download', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ singer, song })
        });

        const data = await response.json();
        hideLoading();

        if (data.success) {
            showAlert(`✓ ${data.message}`, 'success');
            setTimeout(loadExistingSongs, 1000);
        } else {
            showAlert(`✗ ${data.message}`, 'danger');
        }
    } catch (error) {
        hideLoading();
        showAlert(`Error: ${error.message}`, 'danger');
    }
}

// Filter songs
function filterSongs() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    
    const filtered = allSongs.filter(song => 
        song.song.toLowerCase().includes(searchTerm) || 
        song.singer.toLowerCase().includes(searchTerm)
    );
    
    renderSongs(filtered);
}

// Refresh songs
function refreshSongs() {
    loadExistingSongs();
}

// Export songs to text
async function exportSongs() {
    try {
        const response = await fetch('/api/songs/export');
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'songs.txt';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        showAlert('✓ Songs exported to songs.txt', 'success');
    } catch (error) {
        showAlert(`Error: ${error.message}`, 'danger');
    }
}

// Play song
function playSong(singer, song, filePath) {
    const playerTitle = document.getElementById('playerTitle');
    const playerInfo = document.getElementById('playerInfo');
    const audioPlayer = document.getElementById('audioPlayer');
    
    playerTitle.textContent = `${song}`;
    playerInfo.innerHTML = `<strong>${singer}</strong>`;
    
    // filePath is now just the filename, properly encode it
    const filename = encodeURIComponent(filePath);
    audioPlayer.src = `/api/play/${filename}`;
    
    playerModal.show();
}

// Button handlers to extract data attributes
function playSongBtn(btn) {
    const singer = btn.dataset.singer;
    const song = btn.dataset.song;
    const filePath = btn.dataset.file;
    playSong(singer, song, filePath);
}

function downloadSongBtn(btn) {
    const singer = btn.dataset.singer;
    const song = btn.dataset.song;
    downloadSingleSong(singer, song);
}

async function openYouTubeSearchBtn(btn) {
    const singer = btn.dataset.singer;
    const song = btn.dataset.song;
    
    try {
        const response = await fetch('/api/youtube/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ singer, song })
        });
        
        const data = await response.json();
        
        if (data.success) {
            window.open(data.youtube_url, '_blank');
            showAlert(`✓ Opening YouTube search for "${song}"`, 'success');
        } else {
            showAlert(`✗ ${data.message}`, 'danger');
        }
    } catch (error) {
        showAlert(`Error: ${error.message}`, 'danger');
    }
}

// Render player section with downloaded songs
function renderPlayerSection() {
    const downloadedSongs = allSongs.filter(song => song.downloaded && song.singer && song.singer.trim() && song.song && song.song.trim());
    const container = document.getElementById('playerContainer');
    
    if (downloadedSongs.length === 0) {
        container.innerHTML = `
            <i class="fas fa-music fa-3x mb-3 text-muted"></i>
            <p class="text-muted">No downloaded songs yet</p>
        `;
        return;
    }

    container.innerHTML = `
        <div class="row">
            <div class="col-md-6 mx-auto">
                <div class="list-group">
                    ${downloadedSongs.map((song, index) => `
                        <button type="button" class="list-group-item list-group-item-action bg-dark border-secondary text-light text-start"
                            data-singer="${song.singer.replace(/"/g, '&quot;')}" data-song="${song.song.replace(/"/g, '&quot;')}" data-file="${song.file_path}" onclick="playSongBtn(this)">
                            <div class="d-flex justify-content-between align-items-start">
                                <div class="flex-grow-1">
                                    <h6 class="mb-1">
                                        <i class="fas fa-music text-success me-2"></i>${song.song}
                                    </h6>
                                    <small class="text-muted">${song.singer}</small>
                                </div>
                                <span class="badge bg-success">
                                    <i class="fas fa-check"></i>
                                </span>
                            </div>
                        </button>
                    `).join('')}
                </div>
            </div>
        </div>
    `;
}

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Ctrl/Cmd + Enter to download selected
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
        event.preventDefault();
        downloadSelected();
    }
    
    // Ctrl/Cmd + A to select all
    if ((event.ctrlKey || event.metaKey) && event.key === 'a' && document.activeElement.tagName !== 'TEXTAREA') {
        event.preventDefault();
        selectAll();
    }
});
