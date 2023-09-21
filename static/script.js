document.addEventListener("DOMContentLoaded", () => {
    const getLocationButton = document.getElementById("getLocationButton");
    const outputBox = document.getElementById("outputBox");
    const priceRangeSelect = document.getElementById("priceRange");

    // Fetch the Google Places API key from the server
    fetch('/get-api-key')
        .then((response) => response.json())
        .then((data) => {
            const apiKey = data.apiKey;

             getLocationButton.addEventListener("click", async () => {
                if ("geolocation" in navigator) {
                    navigator.geolocation.getCurrentPosition(async (position) => {
                        const latitude = position.coords.latitude;
                        const longitude = position.coords.longitude;
                        const selectedPriceRange = priceRangeSelect.value; // Get the selected price range

                        let price_level = 0; // Default to 0 (all prices) if no price range is selected
                        if (selectedPriceRange !== "") {
                            price_level = parseInt(selectedPriceRange);
                        }

                        const response = await fetch(`/find-restaurant?lat=${latitude}&lng=${longitude}&priceRange=${price_level}`);
                        const data = await response.json();

                        if (data.error) {
                            outputBox.textContent = data.error;
                        } else if (data.restaurant) {
                            const restaurant = data.restaurant;
                            const photoReference = restaurant.photoReference;
                            const photoUrl = `https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference=${photoReference}&key=${apiKey}`;

                            outputBox.innerHTML = `
                                <h2>${restaurant.name}</h2>
                                <p>${restaurant.address}</p>
                                <img src="${photoUrl}" alt="Restaurant Photo" class="restaurant-image">
                            `;
                        } else {
                            outputBox.textContent = "No restaurants found nearby.";
                        }
                    }, (error) => {
                        console.error(`Error getting location: ${error.message}`);
                    });
                } else {
                    outputBox.textContent = "Geolocation is not available in your browser.";
                }
            });
        })
        .catch((error) => {
            console.error(`Error fetching API key: ${error.message}`);
        });
});