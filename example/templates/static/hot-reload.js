
window.addEventListener('load', () => {
    setInterval(() => {
        fetch("/last-update-date.json").then(response => {
            return response.json()
        }).then(data => {
            if (data.timestamp > + new Date() - 1501) {
                window.location = window.location.href
            }
        })
    }, 1500);
})
