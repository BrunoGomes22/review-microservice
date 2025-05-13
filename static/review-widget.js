async function loadReviews(productId, containerId) {
  const REVIEWS_API_URL = `http://127.0.0.1:8000/v1/entities/${productId}/reviews`;
  const AVERAGE_RATING_API_URL = `http://127.0.0.1:8000/v1/entities/${productId}/average-rating`;

  try {
    // Fetch the average rating
    const averageRatingResponse = await fetch(AVERAGE_RATING_API_URL);
    const averageRatingData = await averageRatingResponse.json();
    const average_rating = averageRatingData.average_rating || 0; // Default to 0 if not found

    // Fetch the reviews
    const reviewsResponse = await fetch(REVIEWS_API_URL);
    const reviews = await reviewsResponse.json();

    // Get the container by ID
    let container = document.getElementById(containerId);
    if (!container) {
      console.error(`Container with ID "${containerId}" not found.`);
      return;
    }

    // Determine the color for the average rating
    const numericAverageRating = parseFloat(average_rating);

    let averageRatingColor;
    if (numericAverageRating <= 2) {
      averageRatingColor = "#FF4D4D"; // Red for negative average
    } else if (numericAverageRating > 2 && numericAverageRating < 4) {
      averageRatingColor = "#FFD700"; // Yellow for neutral average
    } else {
      averageRatingColor = "#4CAF50"; // Green for positive average
    }

    console.log("Average Rating Color:", averageRatingColor);
    console.log("Numeric Average Rating:", numericAverageRating);

    // Update the widget content
    container.innerHTML = `
    <div style="border: 1px solid #ccc; border-radius: 8px; padding: 15px; width: 320px; background-color: #f9f9f9; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
      <h2 style="margin-top: 0; font-size: 18px; color: #333; text-align: center;">Reviews</h2>
      <p style="text-align: center; font-size: 16px; color: #555;">
        Average Rating: <strong style="color: ${averageRatingColor};">${average_rating.toFixed(1)}/5</strong>
      </p>
      <ul style="list-style: none; padding: 0; margin: 0; max-height: 200px; overflow-y: auto; border: 1px solid #ddd; border-radius: 4px; background-color: #fff;">
        ${reviews.length > 0
          ? reviews
              .map((rev) => {
                // Determine the color based on the rating
                let ratingColor;
                if (rev.rating <= 2) {
                  ratingColor = "#FF4D4D"; // Red for negative reviews
                } else if (rev.rating === 3) {
                  ratingColor = "#FFD700"; // Yellow for neutral reviews
                } else {
                  ratingColor = "#4CAF50"; // Green for positive reviews
                }
  
                return `
                  <li style="margin-bottom: 10px; padding: 10px; border-bottom: 1px solid #eee; word-wrap: break-word; overflow-wrap: break-word;">
                    <strong style="color: ${ratingColor};">${rev.rating}/5</strong> - <span style="color: #555;">${rev.comment}</span>
                  </li>`;
              })
              .join("")
          : "<p style='text-align: center; color: #888;'>No reviews yet.</p>"}
      </ul>
      <form id="review-form" style="margin-top: 15px;">
        <div style="margin-bottom: 15px;">
          <label for="review-rating" style="display: block; font-weight: bold; color: #333; margin-bottom: 5px;">Rating:</label>
          <div id="star-rating" style="display: flex; gap: 5px; cursor: pointer;">
            ${[1, 2, 3, 4, 5]
              .map(
                (star) =>
                  `<span data-value="${star}" style="font-size: 24px; color: #ccc;">&#9733;</span>`
              )
              .join("")}
          </div>
          <input type="hidden" id="review-rating" required>
        </div>
        <div style="margin-bottom: 15px;">
          <label for="review-comment" style="display: block; font-weight: bold; color: #333; margin-bottom: 5px;">Comment:</label>
          <textarea 
            id="review-comment" 
            required 
            style="width: 100%; height: 80px; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; resize: vertical; overflow-y: auto;"></textarea>
        </div>
        <button type="submit" style="width: 100%; padding: 10px; background-color: #168654; color: #fff; border: none; border-radius: 4px; font-size: 14px; cursor: pointer;">Submit</button>
      </form>
    </div>
  `;

    // Add event listeners to the stars
    const stars = container.querySelectorAll("#star-rating span");
    const ratingInput = container.querySelector("#review-rating");

    stars.forEach((star) => {
      star.addEventListener("click", () => {
        const rating = star.getAttribute("data-value");
        ratingInput.value = rating; // Set the hidden input value

        // Highlight the selected stars
        stars.forEach((s) => {
          s.style.color = s.getAttribute("data-value") <= rating ? "#FFD700" : "#ccc";
        });
      });
    });

    // Handle form submission
    document.getElementById("review-form").addEventListener("submit", async (e) => {
      e.preventDefault();
      const rating = document.getElementById("review-rating").value;
      const comment = document.getElementById("review-comment").value;

      const res = await fetch("http://127.0.0.1:8000/v1/reviews", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ entity_id: productId, rating, comment }),
      });

      if (res.ok) {
        loadReviews(productId, containerId); // Reload reviews
      }
    });
  } catch (error) {
    console.error("Error loading reviews or average rating:", error);
  }
}