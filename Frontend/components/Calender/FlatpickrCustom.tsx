import React, {useEffect, useRef} from 'react';
import flatpickr from "flatpickr";


const MyComponent: React.FC<{dateRangeRef: React.RefObject<HTMLInputElement>}> = ({dateRangeRef}) => {

    return (
        <>
            <div>
                <label className="mb-3 block text-black dark:text-white">
                    Date and Time Range
                </label>
                <div className="relative">
                    <input
                        ref={dateRangeRef}
                        type="text"
                        placeholder="Select date and time range"
                        className="custom-input-date custom-input-date-1 w-full rounded border-[1.5px] border-stroke bg-transparent py-3 px-5 font-medium outline-none transition focus:border-primary active:border-primary dark:border-form-strokedark dark:bg-form-input dark:focus:border-primary"
                    />
                </div>
            </div>
        </>
    );
};

export default MyComponent;