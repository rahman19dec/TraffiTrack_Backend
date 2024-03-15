export async function POST(req: Request) {
    const {startDate, endDate} = await req.json();
    type ClassMapping = {
        [key: string]: string;
    };

// Define a type for the aggregated data to ensure we have a fixed order
    type AggregatedDataArray = number[];

// Define a type for the API data structure
    type ApiData = {
        [timestamp: string]: {
            [classId: string]: number;
        };
    };

// Function to map and sum counts by class, and return an array in a fixed order
    const aggregateCountsToArray = (data: ApiData): AggregatedDataArray => {
        const classMapping: ClassMapping = {
            "0": "person",
            "1": "bicycle",
            "2": "car",
            "3": "motorcycle",
            "4": "bus",
            "5": "truck"
        };

        // Initialize an object to store aggregated counts
        const aggregated: { [key: string]: number } = {
            "person": 0,
            "bicycle": 0,
            "car": 0,
            "motorcycle": 0,
            "bus": 0,
            "truck": 0
        };

        Object.values(data).forEach((curr) => {
            Object.entries(curr).forEach(([key, value]) => {
                const className = classMapping[key];
                aggregated[className] += value;
            });
        });

        // Return an array of the aggregated counts in the specified order
        return [
            aggregated["person"],
            aggregated["bicycle"],
            aggregated["car"],
            aggregated["motorcycle"],
            aggregated["bus"],
            aggregated["truck"]
        ];
    };
    try {
        // Format the dates
        const fromTime = formatDate(startDate);
        const toTime = formatDate(endDate);

        // Construct the API URL with query parameters
        const apiUrl = `http://127.0.0.1:5000/stat?from_time=${fromTime}&to_time=${toTime}`;

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


        const data: ApiData = await response.json();

        // Aggregate the counts by class into an array
        const [totalPersons, totalBicycles, totalCars, totalMotorBikes, totalBus, totalTrucks] = aggregateCountsToArray(data);

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
