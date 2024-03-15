"use client";
import React, {useEffect, useRef, useState} from "react";
import 'flatpickr/dist/flatpickr.min.css';
import ChartOne from "../Charts/ChartOne";
import ChartThree from "../Charts/ChartThree";
import CardDataStats from "../CardDataStats";
import FlatpickrCustom from "@/components/Calender/FlatpickrCustom";
import {FaCar} from "react-icons/fa";
import {RiMotorbikeFill} from "react-icons/ri";
import {MdDirectionsBike} from "react-icons/md";
import {FaBus} from "react-icons/fa6";
import {LiaTruckSolid} from "react-icons/lia";
import {IoMdPeople} from "react-icons/io";
import flatpickr from "flatpickr";
import {initialEnv} from "@next/env";
import ChartThreeV2 from "@/components/Charts/ChartThreeV2";


const ECommerce: React.FC = () => {
    const [trafficData, setTrafficData] = useState({
        totalPersons: 0,
        totalBicycles: 0,
        totalCars: 0,
        totalMotorBikes: 0,
        totalBus: 0,
        totalTrucks: 0,
    });
    const [trafficEmissionData, setTrafficEmissionData] = useState({
        totalPersonsEmissions: 0,
        totalBicyclesEmissions: 0,
        totalCarsEmissions: 0,
        totalMotorBikesEmissions: 0,
        totalBusEmissions: 0,
        totalTrucksEmissions: 0,
        totalEmissions: 0
    });
    const [trafficDataStream, setTrafficDataStream] = useState(null);

    useEffect(() => {
        fetch('/api/getTotalTrafficData/')
            .then(response => response.json())
            .then(data => {
                setTrafficData(data);
            })
            .catch(error => {
                console.error('Error fetching data: ', error);
            });
    }, []);
    const startDateRef = useRef(null);
    const endDateRef = useRef(null);

    useEffect(() => {
        const now = new Date();
        // @ts-ignore
        flatpickr(startDateRef.current, {
            enableTime: true,
            dateFormat: "d-m-Y H:i",
            maxDate: now,
        });
        // @ts-ignore
        flatpickr(endDateRef.current, {
            enableTime: true,
            dateFormat: "d-m-Y H:i",
            maxDate: now,
        });
    }, []);
    const handleSubmit = () => {
        // Assuming you have startDateRef and endDateRef defined somewhere
        // @ts-ignore
        const startDate = startDateRef.current.value;
        // @ts-ignore
        const endDate = endDateRef.current.value;

        // First API call to getTrafficDataByDate
        fetch('/api/getTrafficDataByDate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache',
            },
            body: JSON.stringify({startDate, endDate}),
            cache: 'no-cache',
        })
            .then(response => response.json())
            .then(data => {
                //console.log('Traffic Data:', data);
                setTrafficData(data);
            })
            .catch(error => {
                console.error('Error fetching traffic data: ', error);
            });

        fetch('/api/getTrafficEmissionDataByDate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache',
            },
            body: JSON.stringify({startDate, endDate}),
            cache: 'no-cache',
        })
            .then(response => response.json())
            .then(data => {
                setTrafficEmissionData(data);
            })
            .catch(error => {
                console.error('Error fetching traffic data: ', error);
            });


        // Second API call to getTrafficDataStreambyDate
        fetch('/api/getTrafficDataStreambyDate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache',
            },
            body: JSON.stringify({startDate, endDate}),
            cache: 'no-cache',
        })
            .then(response => response.json())
            .then(dataStream => {
                //console.log('Traffic Data Stream:', dataStream);
                setTrafficDataStream(dataStream);
            })
            .catch(error => {
                console.error('Error fetching traffic data stream: ', error);
            });
    };
    return (
        <>
            {/* <!-- Time and date --> */}
            <div
                className="mb-4 rounded-sm border border-stroke bg-white shadow-default dark:border-strokedark dark:bg-boxdark">
                <div className="border-b border-stroke py-4 px-6.5 dark:border-strokedark">
                    <h3 className="font-medium text-black dark:text-white">
                        Filter by time and date
                    </h3>
                </div>
                <div className="flex flex-col gap-5.5 p-6.5">

                    <div>
                        <label className="mb-3 block text-black dark:text-white">
                            Set start and end date
                        </label>
                        <div className="relative">
                            <input ref={startDateRef} placeholder="Start Date"
                                   className="custom-input-date custom-input-date-1 my-4 w-full rounded border-[1.5px] border-stroke bg-transparent py-3 px-5 font-medium outline-none transition focus:border-primary active:border-primary dark:border-form-strokedark dark:bg-form-input dark:focus:border-primary"/>
                            <input ref={endDateRef} placeholder="End Date"
                                   className="custom-input-date custom-input-date-1 my-4 w-full rounded border-[1.5px] border-stroke bg-transparent py-3 px-5 font-medium outline-none transition focus:border-primary active:border-primary dark:border-form-strokedark dark:bg-form-input dark:focus:border-primary"/>
                        </div>
                    </div>

                    <div className="flex justify-start gap-3">

                        <button
                            className="max-w-xs rounded bg-primary py-2 px-4 text-white hover:bg-primary-dark"
                            onClick={handleSubmit}
                        >
                            Submit
                        </button>
                    </div>

                </div>

            </div>
            {/* <!-- Chat card --> */}

            <div className="grid grid-cols-2 gap-4 md:grid-cols-3 md:gap-6 xl:grid-cols-3 2xl:gap-7.5">
                <CardDataStats title="Total People" total={trafficData.totalPersons.toString()} rate=''>
                    <IoMdPeople size={'2em'} color="#845EC2"/>
                </CardDataStats>
                <CardDataStats title="Total Bicycles" total={trafficData.totalBicycles.toString()} rate=''>
                    <MdDirectionsBike size={'2em'} color="#D65DB1"/>
                </CardDataStats>
                <CardDataStats title="Total Cars" total={trafficData.totalCars.toString()} rate=''>
                    <FaCar size={'2em'} color="#FF6F91"/>
                </CardDataStats>
                <CardDataStats title="Total Motorbikes" total={trafficData.totalMotorBikes.toString()} rate=''>
                    <RiMotorbikeFill size={'2em'} color="#FF9671"/>
                </CardDataStats>
                <CardDataStats title="Total Buses" total={trafficData.totalBus.toString()} rate=''>
                    <FaBus size={'2em'} color="#FFC75F"/>
                </CardDataStats>
                <CardDataStats title="Total Trucks" total={trafficData.totalTrucks.toString()} rate=''>
                    <LiaTruckSolid size={'2em'} color="#FF8066"/>
                </CardDataStats>
            </div>

            <div className="mt-4 w-full">
                {process.env.NEXT_PUBLIC_SHOW_LINE_CHART === 'true' &&
                    <ChartOne trafficDataStream={trafficDataStream}/>}

                <br/>
                <ChartThree
                    text={'Total Traffic Count'}
                    persons={trafficData.totalPersons}
                    bicycles={trafficData.totalBicycles}
                    cars={trafficData.totalCars}
                    motorbikes={trafficData.totalMotorBikes}
                    buses={trafficData.totalBus}
                    trucks={trafficData.totalTrucks}
                />
                <ChartThreeV2 text={'Total Traffic Emission'}
                              totalCarbon={trafficEmissionData.totalEmissions}
                              cars={trafficEmissionData.totalCarsEmissions}
                              motorbikes={trafficEmissionData.totalMotorBikesEmissions}
                              buses={trafficEmissionData.totalBusEmissions}
                              trucks={trafficEmissionData.totalTrucksEmissions}
                />
            </div>
        </>
    );
};

export default ECommerce;
