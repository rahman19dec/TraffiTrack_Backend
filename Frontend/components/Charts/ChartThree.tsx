"use client";
import React, {useEffect, useState} from "react";
import dynamic from "next/dynamic";
import {ApexOptions} from "apexcharts";

const ReactApexChart = dynamic(() => import("react-apexcharts"), {ssr: false});

interface ChartThreeState {
    series: number[];
}

const options: ApexOptions = {
    chart: {
        type: "donut",
    },
    colors: ["#845EC2", "#D65DB1", "#FF6F91", "#FF9671", "#FFC75F", "#FFBA00"],
    labels: ["Persons", "Bicycles", "Cars", "Motorbikes", "Buses", "Trucks"],
    legend: {
        show: true,
        position: "bottom",
    },
    plotOptions: {
        pie: {
            donut: {
                size: "65%",
                background: "transparent",
            },
        },
    },
    dataLabels: {
        enabled: false,
    },
    responsive: [
        {
            breakpoint: 2600,
            options: {
                chart: {
                    width: 380,
                },
            },
        },
        {
            breakpoint: 640,
            options: {
                chart: {
                    width: 200,
                },
            },
        },
    ],
};

interface ChartThreeProps {
    text: string;
    persons: number;
    bicycles: number;
    cars: number;
    motorbikes: number;
    buses: number;
    trucks: number;
}

const ChartThree: React.FC<ChartThreeProps> = ({text, persons, bicycles, cars, motorbikes, buses, trucks}) => {
    // Update the initial state to include all categories
    const [state, setState] = useState<ChartThreeState>({
        series: [persons, bicycles, cars, motorbikes, buses, trucks], //  numbers for Persons, Bicycles, Cars, Motorbikes, Buses, Trucks
    });

    useEffect(() => {
        // Update state whenever props change
        setState({series: [persons, bicycles, cars, motorbikes, buses, trucks]});
    }, [persons, bicycles, cars, motorbikes, buses, trucks]);

    return (
        <div
            className="col-span-12 rounded-sm border border-stroke bg-white px-5 pt-7.5 pb-5 shadow-default dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:col-span-5">
            <div className="mb-3 justify-between gap-4 sm:flex">
                <div>
                    <h5 className="text-xl font-semibold text-black dark:text-white">
                        {text}
                    </h5>
                </div>
                <p className="text-black dark:text-white">
                    Total instance count: {persons + bicycles + cars + motorbikes + buses + trucks}
                </p>
            </div>

            <div className="mb-2">
                <div id="chartThree" className="mx-auto flex justify-center w-[880px]">
                    <ReactApexChart
                        options={options}
                        series={state.series}
                        type="donut"
                    />
                </div>
            </div>
        </div>
    );
};

export default ChartThree;
