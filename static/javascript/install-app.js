// الكود الخاص بعرض النافذة الخاصة بتحميل التطبيق
document.addEventListener('DOMContentLoaded', function () {
    const downloadMenu = document.querySelector('.download-fikra-page');
    const installBtn = document.getElementById('pwa-download');

    let deferredPrompt;
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;        

        if (installBtn && downloadMenu) {
            installBtn.addEventListener('click', () => {
                
                if (deferredPrompt) {
                    deferredPrompt.prompt();
                    deferredPrompt.userChoice.then((choiceResult) => {
                        if (choiceResult.outcome === 'accepted') {
                            console.log('User accepted the A2HS prompt');
                            showDownloadMenu();
                        } 
                        deferredPrompt = null;
                    });
                } else {
                    alert("التطبيق مثبت بالفعل على جهازك!");
                }
            });

            function showDownloadMenu() {
                downloadMenu.style.display = 'block'; // عرض القائمة
                setTimeout(() => {
                    downloadMenu.style.visibility = 'visible';
                    downloadMenu.style.opacity = '1';
                    downloadMenu.style.transform = 'translate(-50%, -40%) scale(1)';
                }, 100);
                hideDownloadMenu();
            }
    
            function hideDownloadMenu() {
                downloadMenu.style.opacity = '0';
                downloadMenu.style.transform = 'translate(-50%, -40%) scale(0.5)';
                setTimeout(() => {
                    downloadMenu.style.visibility = 'hidden';
                    downloadMenu.style.display = 'none';
                }, 300);
            }
    
            document.addEventListener('click', function (e) {
                if (downloadMenu.style.visibility === 'visible' && !downloadMenu.contains(e.target)) {
                    hideDownloadMenu();
                }
            });
        }
    });
});


// ===================================================================================================

