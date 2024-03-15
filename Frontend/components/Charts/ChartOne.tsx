"use client";
import {ApexOptions} from "apexcharts";
import React, {useCallback, useEffect, useState} from "react";
import dynamic from "next/dynamic";

const ReactApexChart = dynamic(() => import("react-apexcharts"), {
    ssr: false,
});


const options: ApexOptions = {
    legend: {
        show: false,
        position: "top",
        horizontalAlign: "left",
    },
    colors: ["#3056D3", "#80CAEE", "#10B981", "#F0950C"],
    chart: {
        // events: {
        //   beforeMount: (chart) => {
        //     chart.windowResizeHandler();
        //   },
        // },
        fontFamily: "Satoshi, sans-serif",
        height: 335,
        type: "area",
        dropShadow: {
            enabled: true,
            color: "#623CEA14",
            top: 10,
            blur: 4,
            left: 0,
            opacity: 0.1,
        },

        toolbar: {
            show: false,
        },
    },
    responsive: [
        {
            breakpoint: 1024,
            options: {
                chart: {
                    height: 300,
                },
            },
        },
        {
            breakpoint: 1366,
            options: {
                chart: {
                    height: 350,
                },
            },
        },
    ],
    stroke: {
        width: [2, 2],
        curve: "straight",
    },
    // labels: {
    //   show: false,
    //   position: "top",
    // },
    grid: {
        xaxis: {
            lines: {
                show: true,
            },
        },
        yaxis: {
            lines: {
                show: true,
            },
        },
    },
    dataLabels: {
        enabled: false,
    },
    markers: {
        size: 4,
        colors: "#fff",
        strokeColors: ["#3056D3", "#80CAEE", "#10B981", "#F0950C"],
        strokeWidth: 3,
        strokeOpacity: 0.9,
        strokeDashArray: 0,
        fillOpacity: 1,
        discrete: [],
        hover: {
            size: undefined,
            sizeOffset: 5,
        },
    },
    xaxis: {
        type: "category",
        categories: [],
        axisBorder: {
            show: false,
        },
        axisTicks: {
            show: false,
        },
    },
    yaxis: {
        title: {
            style: {
                fontSize: "0px",
            },
        },
        min: 0,
        max: 5,
    },
};


interface TrafficData {
    data: number[];
}

/*interface TrafficDataStream {
    [vehicleType: string]: TrafficData;
}*/

interface ChartOneProps {
    trafficDataStream: TrafficDataStream | null;
}

interface TrafficDataPoint {
    count: number;
    timestamp: string; // Assuming timestamp is a string. Adjust if it's a Date object or another format.
}

interface TrafficDataStream {
    [vehicleType: string]: {
        data: TrafficDataPoint[];
    };
}


const ChartOne: React.FC<ChartOneProps> = ({trafficDataStream}) => {
    const [activeSeries, setActiveSeries] = useState<string>("person"); // Note the change to "person" to match your data keys
    //console.log(activeSeries);


    const getButtonClass = (seriesName: string) => {
        return `h-auto p-4 drop-shadow-lg rounded-lg ${activeSeries !== seriesName ? '' : 'bg-white text-black'}`;
    };

    // This function now dynamically creates series data from the trafficDataStream prop
    /*    const getFilteredSeries = useCallback(() => {
            if (!trafficDataStream) {
                return [];
            }
    
            const activeData = trafficDataStream[activeSeries]; // Access the active series data using the activeSeries state
            if (!activeData) {
                return [];
            }
    
            return [{
                name: activeSeries,
                data: activeData.data
            }];
        }, [trafficDataStream, activeSeries]);*/
    const getFilteredSeries = useCallback(() => {
        if (!trafficDataStream || !trafficDataStream[activeSeries]) {
            return [];
        }

        const seriesData = trafficDataStream[activeSeries].data.map(dataPoint => ({
            x: dataPoint.timestamp,
            y: dataPoint.count
        }));

        return [{
            name: activeSeries,
            data: seriesData
        }];
    }, [trafficDataStream, activeSeries]);
    const [chartOptions, setChartOptions] = useState<ApexOptions>(options); // Initialize chartOptions state with default options

    useEffect(() => {
        const maxCount = getFilteredSeries().reduce((max, series) => {
            const seriesMax = series.data.reduce((seriesMax, point) => Math.max(seriesMax, point.y), 0);
            return Math.max(max, seriesMax);
        }, 0);

        setChartOptions(prevOptions => ({
            ...prevOptions,
            xaxis: {
                ...prevOptions.xaxis,
                type: 'datetime', // Adjust if your timestamp format is different
            },
            yaxis: {
                ...prevOptions.yaxis,
                max: maxCount
            },
        }));
    }, [getFilteredSeries]);

    // NextJS Requirement
    const isWindowAvailable = () => typeof window !== "undefined";

    if (!isWindowAvailable()) return <></>;

    return (
        <div
            className="col-span-12 rounded-sm border border-stroke bg-white px-5 pt-7.5 pb-5 shadow-default dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:col-span-8">
            <div className="w-1/2 flex gap-3 px-8">
                <button className={getButtonClass("person")} onClick={() => setActiveSeries("person")}>Persons
                </button>
                <button className={getButtonClass("bicycle")} onClick={() => setActiveSeries("bicycle")}>Bicycles
                </button>
                <button className={getButtonClass("car")} onClick={() => setActiveSeries("car")}>Cars</button>
                <button className={getButtonClass("motorcycle")}
                        onClick={() => setActiveSeries("motorcycle")}>Motorbikes
                </button>
                <button className={getButtonClass("bus")} onClick={() => setActiveSeries("bus")}>Buses</button>
                <button className={getButtonClass("truck")} onClick={() => setActiveSeries("truck")}>Trucks</button>
            </div>

            <div id="chartOne" className="h-96">
                <ReactApexChart
                    options={chartOptions}
                    series={getFilteredSeries()}
                    type="area"
                    width="100%"
                    height="100%"
                />
            </div>
        </div>
    );
};

export default ChartOne;
