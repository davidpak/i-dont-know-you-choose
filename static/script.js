document.addEventListener("DOMContentLoaded", () => {
    const getLocationButton = document.getElementById("getLocationButton");
    const locationText = document.getElementById("outputBox");

    getLocationButton.addEventListener("click", () => {
        if ("geolocation" in navigator) {
            navigator.geolocation.getCurrentPosition(async (position) => {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;

                const response = await fetch(`/find-restaurant?lat=${latitude}&lng=${longitude}`);
                const data = await response.json();

                if (data.restaurantName) {
                    locationText.textContent = `${data.restaurantName}`;
                } else {
                    locationText.textContent = "No restaurants found nearby.";
                }
            }, (error) => {
                console.error(`Error getting location: ${error.message}`);
            });
        } else {
            locationText.textContent = "Geolocation is not available in your browser.";
        }
    });
});
