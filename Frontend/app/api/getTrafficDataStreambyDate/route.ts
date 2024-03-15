export async function POST(req: Request) {
    const {startDate, endDate} = await req.json();
    type ClassMapping = {
        [key: string]: string;
    };

    type ApiData = {
        [timestamp: string]: {
            [classId: string]: number;
        };
    };

    /*    type OutputData = {
            [className: string]: {
                data: number[];
            };
        };*/
    type OutputData = {
        [className: string]: {
            data: Array<{
                count: number;
                timestamp: string;
            }>;
        };
    };

    const mapCountsToObject = (data: ApiData): OutputData => {
        const classMapping: ClassMapping = {
            "0": "person",
            "1": "bicycle",
            "2": "car",
            "3": "motorcycle",
            "4": "bus",
            "5": "truck"
        };

        const outputData: OutputData = {
            "person": {data: []},
            "bicycle": {data: []},
            "car": {data: []},
            "motorcycle": {data: []},
            "bus": {data: []},
            "truck": {data: []}
        };

        Object.entries(data).forEach(([timestamp, counts]) => {
            Object.entries(counts).forEach(([key, value]) => {
                const className = classMapping[key];
                outputData[className].data.push({
                    count: value,
                    timestamp: timestamp
                });
            });
        });

        return outputData;
    };

    try {
        const fromTime = formatDate(startDate);
        const toTime = formatDate(endDate);

        const apiUrl = `http://127.0.0.1:5000/stat?from_time=${fromTime}&to_time=${toTime}`;

        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            throw new Error(`Error fetching data: ${response.statusText}`);
        }

        const data: ApiData = await response.json();

        const outputData = mapCountsToObject(data);

        //console.log(outputData.person);

        // Aggregate the counts by class into an array
//        const [totalPersons, totalBicycles, totalCars, totalMotorBikes, totalBus, totalTrucks] = aggregateCountsToArray(data);
        /*

                const result = {
                    totalPersons,
                    totalBicycles,
                    totalCars,
                    totalMotorBikes,
                    totalBus,
                    totalTrucks,
                };
        */


        // Return the parsed data as the response
        return new Response(JSON.stringify(outputData), {
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
