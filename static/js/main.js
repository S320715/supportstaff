// MediTask — Auto-refresh for real-time task updates
// Polls the server every 30 seconds

if (typeof refreshUrl !== 'undefined') {
    setInterval(function () {
        fetch(refreshUrl)
            .then(function (response) {
                return response.json();
            })
            .then(function (tasks) {
                console.log('Tasks refreshed: ' + tasks.length + ' tasks loaded');
            })
            .catch(function (error) {
                console.log('Refresh error: ' + error);
            });
    }, 30000);
}