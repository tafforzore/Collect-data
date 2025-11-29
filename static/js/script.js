// Gestion de l'aperçu des images
document.addEventListener('DOMContentLoaded', function() {
    const photoInput = document.getElementById('photos');
    const imagePreview = document.getElementById('imagePreview');
    
    if (photoInput) {
        photoInput.addEventListener('change', function(e) {
            imagePreview.innerHTML = '';
            imagePreview.style.display = 'block';
            
            const files = e.target.files;
            
            for (let i = 0; i < files.length; i++) {
                const file = files[i];
                
                if (file.type.startsWith('image/')) {
                    const reader = new FileReader();
                    
                    reader.onload = function(e) {
                        const col = document.createElement('div');
                        col.className = 'col-md-3 col-6';
                        
                        col.innerHTML = `
                            <div class="image-preview-container">
                                <img src="${e.target.result}" class="image-preview" alt="Aperçu">
                                <button type="button" class="remove-image" onclick="removeImagePreview(this)">
                                    <i class="fas fa-times"></i>
                                </button>
                            </div>
                        `;
                        
                        imagePreview.appendChild(col);
                    };
                    
                    reader.readAsDataURL(file);
                }
            }
        });
    }
    
    // Animation des cartes au scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Appliquer l'animation aux cartes de plantes
    document.querySelectorAll('.plant-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
});

function removeImagePreview(button) {
    const container = button.closest('.col-md-3, .col-6');
    container.remove();
    
    // Masquer la section d'aperçu si plus d'images
    const imagePreview = document.getElementById('imagePreview');
    if (imagePreview.children.length === 1) { // Le titre reste
        imagePreview.style.display = 'none';
    }
}

// Confirmation avant soumission
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('plantForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            const submitButton = this.querySelector('button[type="submit"]');
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Enregistrement...';
            submitButton.disabled = true;
        });
    }
});

// Toast pour les messages
function showToast(message, type = 'success') {
    const toastContainer = document.createElement('div');
    toastContainer.className = `toast align-items-center text-bg-${type} border-0`;
    toastContainer.setAttribute('role', 'alert');
    
    toastContainer.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    
    document.body.appendChild(toastContainer);
    const toast = new bootstrap.Toast(toastContainer);
    toast.show();
    
    // Nettoyer après fermeture
    toastContainer.addEventListener('hidden.bs.toast', function() {
        document.body.removeChild(toastContainer);
    });
}