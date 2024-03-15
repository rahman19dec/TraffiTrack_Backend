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
    colors: ["#FF9A2F", "#FF7A07", "#F95D00", "#C04000"],
    labels: ["Cars", "Motorbikes", "Buses", "Trucks"],
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

interface ChartThreeV2Props {
    text: string;
    cars: number;
    motorbikes: number;
    buses: number;
    trucks: number;
    totalCarbon: number;
}

const ChartThreeV2: React.FC<ChartThreeV2Props> = ({text, totalCarbon, cars, motorbikes, buses, trucks}) => {
    // Update the initial state to include all categories
    const [state, setState] = useState<ChartThreeState>({
        series: [cars, motorbikes, buses, trucks], //  numbers for Persons, Bicycles, Cars, Motorbikes, Buses, Trucks
    });

    useEffect(() => {
        // Update state whenever props change
        setState({series: [cars, motorbikes, buses, trucks]});
    }, [cars, motorbikes, buses, trucks]);

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
                    Total Carbon: {totalCarbon} Tonnes
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

export default ChartThreeV2;
