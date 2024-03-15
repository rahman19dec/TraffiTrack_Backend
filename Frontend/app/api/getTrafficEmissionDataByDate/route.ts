export async function POST(req: Request) {
    const {startDate, endDate} = await req.json();

    try {
        // Format the dates
        const fromTime = formatDate(startDate);
        const toTime = formatDate(endDate);

        // Construct the API URL with query parameters
        const apiUrl = `http://127.0.0.1:5000/carbon?from_time=${fromTime}&to_time=${toTime}`;

        // Fetch data from the external API
        const response = await fetch(apiUrl, {
            method: 'GET', // GET request does not need a body
            headers: {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache',
            },
        });

        // Check if the request was successful
        if (!response.ok) {
            throw new Error(`Error fetching data: ${response.statusText}`);
        }

        const data = await response.json(); // Assuming you want to parse the JSON response

        // Destructure the response data into named variables
        const [totalEmissionsPerVehicle, totalEmissions] = Object.values(data);
        // @ts-ignore
        const [totalPersonsEmissions, totalBicyclesEmissions, totalCarsEmissions, totalMotorBikesEmissions, totalBusEmissions, totalTrucksEmissions] = Object.values(totalEmissionsPerVehicle);


        // Return the results in a modern object shorthand notation
        const result = {
            totalPersonsEmissions,
            totalBicyclesEmissions,
            totalCarsEmissions,
            totalMotorBikesEmissions,
            totalBusEmissions,
            totalTrucksEmissions,
            totalEmissions
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
        return new Response(JSON.stringify({error: 'Failed to fetch data'}), {
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
