import Link from "next/link";
import DarkModeSwitcher from "./DarkModeSwitcher";
import DropdownMessage from "./DropdownMessage";
import DropdownNotification from "./DropdownNotification";
import DropdownUser from "./DropdownUser";
import Image from "next/image";

const Header = (props: {
    sidebarOpen: string | boolean | undefined;
    setSidebarOpen: (arg0: boolean) => void;
}) => {
    return (
        <header className="sticky top-0 z-999 flex w-full bg-white drop-shadow-1 dark:bg-boxdark dark:drop-shadow-none">
            <div className="flex flex-grow items-center justify-between px-4 py-4 shadow-2 lg:px-6 2xl:px-11">
                <Link className="flex items-center gap-2 flex-shrink-0 " href="/">
                    <Image
                        width={32}
                        height={32}
                        src={"/images/logo/logo-icon.svg"}
                        alt="Logo"
                    />
                    <span className="font-bold"> TraffiTrack </span>
                </Link>

                <div className="flex items-center gap-3 2xsm:gap-7">
                    <ul className="flex items-center gap-2 2xsm:gap-4">
                        {/* <!-- Dark Mode Toggler --> */}
                        <DarkModeSwitcher/>
                        {/* <!-- Dark Mode Toggler --> */}


                    </ul>

                    {/* <!-- User Area --> */}
                    {/*
                    <DropdownUser/>
                    */}
                    {/* <!-- User Area --> */}
                </div>
            </div>
        </header>
    );
};

export default Header;
