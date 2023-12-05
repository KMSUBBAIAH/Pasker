document.addEventListener('DOMContentLoaded', function() {
    // Check if night mode is enabled in local storage
    const nightModeEnabled = localStorage.getItem('nightMode') === 'enabled';
  
    // Apply night mode if enabled
    if (nightModeEnabled) {
      document.body.classList.add('night-mode');
    }
  
    // Toggle night mode on button click
    const toggleNightModeBtn = document.getElementById('toggleNightMode');
    if (toggleNightModeBtn) {
      toggleNightModeBtn.addEventListener('click', function() {
        // Toggle night mode class on body
        document.body.classList.toggle('night-mode');
  
        // Update night mode status in local storage
        const isNightModeEnabled = document.body.classList.contains('night-mode');
        localStorage.setItem('nightMode', isNightModeEnabled ? 'enabled' : 'disabled');
      });
    }
  });
  