export async function POST(req: Request) {
    const { startDate, endDate } = await req.json();

    try {
        // Format the dates
        const fromTime = formatDate(startDate);
        const toTime = formatDate(endDate);

        // Construct the API URL with query parameters
        const apiUrl = `http://127.0.0.1:5000/count?from_time=${fromTime}&to_time=${toTime}`;

        // Fetch data from the external API
        const response = await fetch(apiUrl, {
            method: 'GET', // GET request does not need a body
            headers: {
                'Content-Type': 'application/json',
            },
        });

        // Check if the request was successful
        if (!response.ok) {
            throw new Error(`Error fetching data: ${response.statusText}`);
        }

        const data = await response.json(); // Assuming you want to parse the JSON response

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
        console.error('Fetch error:', error);
        return new Response(JSON.stringify({ error: 'Failed to fetch data' }), {
            status: 500,
            headers: {
                'Content-Type': 'application/json',
            },
        });
    }
}

// Helper function to format dates
function formatDate(dateStr: { split: (arg0: string) => [any, any, any]; }) {
    const [day, month, yearTime] = dateStr.split('-');
    const [year, time] = yearTime.split(' ');
    return `${year}-${month}-${day}T${time}:00`;
}
