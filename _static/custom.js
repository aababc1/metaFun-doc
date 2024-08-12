document.addEventListener("DOMContentLoaded", function() {
    const toc = document.querySelector('.bd-toc');
    const toggleButton = document.createElement('button');
    toggleButton.innerHTML = 'Toggle TOC';
    toggleButton.style.position = 'fixed';
    toggleButton.style.right = '10px';
    toggleButton.style.top = '10px';
    toggleButton.style.zIndex = '1000';
    document.body.appendChild(toggleButton);

    toggleButton.addEventListener('click', function() {
        if (toc.style.display === 'none') {
            toc.style.display = 'block';
        } else {
            toc.style.display = 'none';
        }
    });
});

