document.addEventListener('DOMContentLoaded', function () {
    const downloadMenu = document.querySelector('.download-fikra-page');
    const installBtn = document.getElementById('pwa-download');
    const installLink = document.getElementById('install-link'); // الرابط
    let deferredPrompt;
    // منع إعادة تحميل الصفحة عند النقر على الرابط
    if (installLink) {
        installLink.addEventListener('click', (event) => {
            event.preventDefault();
        });
    }
    // التقاط حدث beforeinstallprompt عند توفره
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;        
        console.log("0")
        if (installBtn && downloadMenu) {
            console.log("1")
            installBtn.addEventListener('click', () => {
                if (deferredPrompt) {
                    console.log("2")
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
        }
    });
    function showDownloadMenu() {
        downloadMenu.style.display = 'block'; 
        setTimeout(() => {
            downloadMenu.style.visibility = 'visible';
            downloadMenu.style.opacity = '1';
            downloadMenu.style.transform = 'translate(-50%, -40%) scale(1)';
        }, 100);

        // إخفاء النافذة بعد 3 ثوانٍ
        setTimeout(hideDownloadMenu, 3000);
    }
    function hideDownloadMenu() {
        downloadMenu.style.opacity = '0';
        downloadMenu.style.transform = 'translate(-50%, -40%) scale(0.5)';
        setTimeout(() => {
            downloadMenu.style.visibility = 'hidden';
            downloadMenu.style.display = 'none';
        }, 300);
    }
    // إخفاء النافذة عند النقر خارجها
    document.addEventListener('click', function (e) {
        if (downloadMenu.style.visibility === 'visible' && !downloadMenu.contains(e.target) && e.target !== installBtn) {
            hideDownloadMenu();
        }
    });
});
