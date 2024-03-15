export async function GET() {
    try {
        const apiUrl = 'http://127.0.0.1:5000/count';

        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: {
                // If the API requires specific headers, add them here
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache',
            },
        });

        // Check if the request was successful
        if (!response.ok) {
            throw new Error(`Error fetching data: ${response.statusText}`);
        }

        // Parse the JSON response
        const data = await response.json();
        console.log(data);

        // Destructure the response data into named variables
        const [totalPersons, totalBicycles, totalCars, totalMotorBikes, totalBus, totalTrucks] = Object.values(data);


        // Return the results in a modern object shorthand notation
        const result = {
            totalPersons,
            totalBicycles,
            totalCars,
            totalMotorBikes,
            totalBus,
            totalTrucks,
        };

        // Return the parsed data as the response
        return new Response(JSON.stringify(result), {
            status: 200,
            headers: {
                'Content-Type': 'application/json',
            },
        });
    } catch (error) {
        // Handle any errors that occur during the fetch
        console.error('Fetch error:', error);

        // Return an error response
        return new Response(JSON.stringify({error: 'Failed to fetch data'}), {
            status: 500, // Internal Server Error status
            headers: {
                'Content-Type': 'application/json',
            },
        });
    }
}
